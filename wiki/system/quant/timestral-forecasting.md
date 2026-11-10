---
title: Timestral — Zero-Shot Time-Series Foundation Model Forecasting
type: build
tags:
  - quant
  - forecasting
  - build
  - software
  - time-series
  - infrastructure
created: 2026-10-31
updated: 2026-10-31
status: active
priority: high
area: software
related:
  - '[[system/foundation/architecture]]'
  - '[[system/foundation/stack]]'
  - '[[system/quant/quant-backtesting]]'
  - '[[system/agents/agents]]'
  - '[[system/agents/agent-behaviors]]'
  - '[[system/investment/state-schemas]]'
  - '[[system/tools/tools-inventory]]'
confidence: high
---

# Timestral — Zero-Shot Time-Series Foundation Model Forecasting

> Modulo quantitativo e time-series forecasting del `trading-agent`. Integra la famiglia di Time-Series Foundation Model (TSFM) open-weight di Mistral AI (Ottobre 2026) per fornire previsioni probabilistiche multivariate zero-shot su OHLCV, volatilità e covariate macroeconomiche.

---

## 1. Panoramica del Modello (Mistral AI, Ottobre 2026)

**Timestral** è una famiglia di Foundation Model specificamente progettata per l'analisi e la previsione di serie temporali complesse, rilasciata da **Mistral AI** nell'ottobre 2026 con licenza aperta **Modified MIT** (commercialmente utilizzabile e self-hostabile).

Il modello trasferisce il paradigma dei moderni Large Language Model al dominio numerico-temporale, superando i limiti del forecasting supervisionato classico (LSTM, GBDT) grazie a:

- **Architettura Patch-based Transformer**: la serie temporale viene segmentata in patch temporali contigue (token temporali densi) proiettate nello spazio latente dell'attenzione. Questo approccio riduce drasticamente la complessità computazionale rispetto all'attenzione punto-a-punto, preservando sia le micro-strutture intra-patch sia le dipendenze macroscopiche di lungo periodo.
- **Finestra di Contesto di 32k step (32.768 timestep)**: una delle estensioni di contesto più ampie nel panorama dei modelli time-series. Consente di ingerire contemporaneamente dati storici multi-scala (es. barre intraday o a 4 ore su più mesi unificate con serie giornaliere pluriennali e regimi macroeconomici passati).
- **Previsione Probabilistica su 21 Quantili**: anziché restituire una stima puntuale singola (spesso ingannevole sui mercati ad elevata varianza), Timestral genera direttamente l'intera distribuzione predittiva attraverso 21 quantili discreti:
  $$q \in \{0.01, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 0.99\}$$
  Questo approccio modella esplicitamente l'incertezza, l'asimmetria (skewness) e le code grasse (fat tails/kurtosis) dei ritorni finanziari.
- **Famiglia a 4 Scale di Parametri**:
  - **Timestral-5M**: variante ultra-compatta per edge computing o filtraggio millisecond-level.
  - **Timestral-28M**: variante ad altissima efficienza CPU (~17-25ms per inferenza), modello di default per microservizi di screening e decision gating.
  - **Timestral-123M**: variante bilanciata ad alta precisione multivariata per analisi di desk e swing trading.
  - **Timestral-209M**: modello flagship per correlazioni cross-asset complesse, orizzonti estesi e combinazione densa di covariate macroeconomiche.

---

## 2. Ruolo Architetturale nel Trading Agent

All'interno dell'architettura del `trading-agent` ([[system/foundation/architecture]]), Timestral opera come **motore di inferenza quantitativa deterministica**, posizionato nel Layer 3 (Origination / Analisi) e a supporto del Layer 4 (Rischio e Gate).

Rispetta rigorosamente il principio cardine del sistema:
> *L'LLM fa solo il ragionamento e la sintesi strategica; i calcoli, i segnali quantitativi e le distribuzioni predittive sono generati deterministicamente da modelli dedicati in ambiente Python.*

```
DB Centrale (Layer 1)
   │ (OHLCV + Volatilità + Macro Dati)
   ▼
[Timestral Inference Engine (Python/ONNX)] ◄── Esecuzione locale deterministica
   │
   ├─► 21 Quantili Previsionali (q01...q99)
   │
   ├──────────────────────────────┬──────────────────────────────┐
   ▼                              ▼                              ▼
Desk Analyst Technical      System One Gating           Portfolio Manager & Risk
(Livelli dinamici & SL/TP)  (Jev/CLM fast triage)       (Downside bands & Statuto)
```

### Ambiti di Previsione Multivariata Zero-Shot
1. **Prezzi OHLCV**: traiettoria futura attesa (mediana $q_{0.50}$) e canali di espansione/compressione del prezzo per i timeframe target (4h / Daily, orizzonte swing trading).
2. **Volatilità Realizzata e Struttura a Termine**: stima forward-looking della volatilità (ampiezza delle bande $q_{0.90} - q_{0.10}$), superando l'indicatore retrospettivo dell'ATR (Average True Range).
3. **Covariate Esogene e Indicatori Macro**: integrazione nativa di serie ausiliarie come tassi di interesse (DGS10, Fed Funds), indice del dollaro (DXY), differenziali di rendimento, VIX e dati settoriali estratti dai vendor di Layer 2 ([[system/data/data-vendors]]).

Grazie alla capacità **zero-shot**, Timestral non richiede un addestramento specifico ticker-per-ticker, eliminando il rischio critico di overfitting e look-ahead bias tipico del backtesting ML convenzionale.

---

## 3. Integrazione con il Sistema Multi-Agente

L'integrazione di Timestral potenzia tre specifici componenti del sistema multi-agente:

### 3.1 Desk Analyst Technical (Technical + Volatilità)
Nel workflow del Desk Technical ([[system/agents/agent-behaviors]]):
- **Tool dedicato nell'inventario**: `get_timestral_forecast(ticker, horizon, covariates)` integrato nella Famiglia B ([[system/tools/tools-inventory]]).
- **Velocità su CPU**: con tempi di esecuzione compresi tra **17ms e 113ms su CPU**, l'Analyst Technical può invocare la previsione su domanda senza generare latenze perceptible o consumare chiamate LLM.
- **Costruzione dei livelli di trade**: anziché fissare stop loss e target price basandosi esclusivamente su moltiplicatori statici dell'ATR storico ($k_{\text{stop}} \cdot \text{ATR}$), l'agente Technical riceve la distribuzione dei quantili:
  - **Supporti/Resistenze dinamiche**: identificate dalla convergenza delle bande quantiliche inferiori ($q_{0.10}, q_{0.25}$) e superiori ($q_{0.75}, q_{0.90}$).
  - **Volatility-adjusted Sizing**: la dispersione della distribuzione futura modula la convinzione numerica del desk, segnalando regimi di espansione imminente della volatilità.

### 3.2 System One Decision Gating (Jev / CLM / Fast Filtering)
Nel meccanismo di pre-filtraggio e gating reattivo (System One decision engine):
- Prima di avviare il tavolo deliberativo completo (System Two, basato sui modelli di frontiera Claude/DeepSeek e costoso in termini di token e tempo), il sistema esegue un triage ad alta frequenza.
- Timestral fornisce i **prior numerici e probabilistici**: se la probabilità implicita di downside a breve termine supera la soglia di tolleranza (es. $P(\Delta \text{Price} < -k \cdot \text{ATR}) > 0.40$), il trade viene scartato o archiviato in fase di pre-screening.
- Latenza end-to-end inferiore a **50ms**, consentendo lo scanning rapido dell'intero universo di ticker ammissibili prima di attivare gli agenti cognitivi.

### 3.3 Portfolio Manager & Risk Analyst (Downside Bands & Statuto)
Nel Layer 4 e nella tesi di investimento (`research_state` → `investment_state`):
- **Bande di Downside Probabilistico**: i quantili estremi inferiori ($q_{0.01}$ e $q_{0.05}$) fungono da stima diretta di **Value at Risk (VaR)** e **Conditional VaR / Expected Shortfall** forward-looking.
- **Verifica con lo Statuto**: il Risk Analyst e i guardrail Python deterministici confrontano la massima perdita attesa sul quantile $q_{0.01}$ con il limite imposto dallo Statuto del fondo (es. VaR max 10% del portafoglio). Se il trade presenta asimmetria negativa estrema non compensata dal target price, il gate blocca la proposta con razionale quantitativo.

---

## 4. Benchmark e Confronto con Metodi Tradizionali

Timestral si posiziona al vertice dei benchmark aperti di time-series foundation models (rilevazioni ottobre 2026):

| Benchmark | Ruolo / Dataset | Posizionamento Timestral | Note |
|-----------|-----------------|--------------------------|------|
| **GIFT-Eval** | General Time-Series Forecasting Evaluation | **#1 Assoluto** | Supera Chronos, TimesFM, Moirai e PatchTST in compiti multivariati |
| **TIME** | Time-series Industrial & Market Evaluation | **#1 Assoluto** | Massima robustezza su serie finanziarie ad alta componente stocastica |
| **fev-bench** | Feature & Exogenous Variables Benchmark | **Top-tier** | Benchmark di riferimento per previsioni con covariate esogene |

### Confronto Strutturale con Modelli Tradizionali

```
Tradizionale (LSTM / LightGBM)                Timestral TSFM
┌─────────────────────────────────┐           ┌─────────────────────────────────┐
│ Feature Engineering manuale     │           │ Rappresentazione latente patch  │
│ Stima puntuale (un solo numero) │    VS     │ 21 Quantili probabilistici      │
│ Overfitting / Training per-asset│           │ Zero-Shot cross-asset           │
│ Contesto corto (<200 barre)     │           │ Finestra 32k step               │
└─────────────────────────────────┘           └─────────────────────────────────┘
```

| Dimensione | LSTM / BiLSTM | LightGBM / GBDT | Timestral (TSFM) |
|------------|---------------|-----------------|------------------|
| **Architettura** | Recurrent Neural Network | Gradient Boosted Trees | Patch-based Transformer |
| **Finestra di Contesto** | Tipicamente 50-200 step (soffre di vanishing gradient) | Finestra fissa basata su lag espliciti | **Fino a 32.768 step** (multi-regime) |
| **Multivariato & Covariate** | Complesso da stabilizzare | Richiede feature engineering manuale massivo | **Nativo con cross-attention** |
| **Output Incertezza** | Stima puntuale; quantili richiedono Monte Carlo dropout | Richiede addestramento di N modelli separati (pinball loss) | **21 Quantili unificati in un unico pass** |
| **Capacità Zero-Shot** | Nessuna (richiede riaddestramento per ogni asset) | Nessuna (ipersensibile a drift di distribuzione) | **Nativa out-of-the-box** su asset non visti |
| **Latenza Inferenza CPU** | 20-50ms | 5-15ms | **17-113ms** (a seconda della taglia 5M-209M) |
| **Rischio Overfitting** | Molto elevato sui dati finanziari | Elevato se non regolarizzato rigidamente | **Minimo** (generalizzazione fondazionale) |

---

## 5. Specifiche di Deployment e Runtime

Il modulo è concepito per girare in modalità **self-hosted e locale**, senza dipendenze da API esterne, garantendo riservatezza totale sui dati e sulle posizioni del fondo.

### Profili e Latenze per Variante

| Modello | Parametri | RAM / Memoria | Latenza CPU (batch=1) | Scenario d'uso ideale |
|---------|-----------|---------------|-----------------------|-----------------------|
| **Timestral-5M** | 5M | ~25 MB | **~17 ms** | High-frequency screening, microservizi edge |
| **Timestral-28M** | 28M | ~110 MB | **~24 ms** | Default di sistema per screening continuo e System One gating |
| **Timestral-123M** | 123M | ~480 MB | **~68 ms** | Analisi approfondita Desk Technical per swing trading |
| **Timestral-209M** | 209M | ~820 MB | **~113 ms** | Flagship multi-asset con 10+ covariate macroeconomiche |

### Schema di Output del Tool (`module_outputs`)

Il tool restituisce al sistema uno schema JSON strutturato:

```json
{
  "ticker": "AAPL",
  "model": "timestral-28m",
  "timestamp": "2026-10-31T14:30:00Z",
  "context_length": 1024,
  "horizon_steps": 10,
  "quantiles": {
    "q0.01": [220.10, 218.40, 216.50],
    "q0.05": [223.50, 222.10, 220.80],
    "q0.10": [225.80, 224.90, 223.70],
    "q0.50": [232.40, 233.10, 234.00],
    "q0.90": [239.20, 241.50, 243.80],
    "q0.95": [241.80, 244.30, 247.10],
    "q0.99": [245.50, 249.00, 252.30]
  },
  "metrics": {
    "median_expected_return": 0.0069,
    "downside_var_95": -0.0483,
    "volatility_forecast_annualized": 0.214,
    "skewness": 0.12
  }
}
```

Questo payload viene depositato in `module_outputs` nel DB centrale e fornito come contesto al Desk Technical e al Risk Engine deterministico.

---

*Vedi anche: [[system/quant/quant-backtesting]] per le metriche di validazione, [[system/foundation/architecture]] per il workflow di Layer 3/4, e [[system/tools/tools-inventory]] per l'inventario dei tool.*
