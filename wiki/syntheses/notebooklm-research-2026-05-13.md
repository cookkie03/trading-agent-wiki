---
title: Ricerca NotebookLM — Approcci da Progetti Simili AI+Finance (con riferimenti)
type: synthesis
tags:
  - architecture
  - backtesting
  - strategy
  - infrastructure
  - research
sources:
  - TradingAgents (TauricResearch)
  - MarketSenseAI 2.0 (arXiv 2502.00415)
  - Alpha Arena
  - AlpacaTradingAgent
  - cvx-portfolio-optimizer
  - Creo il mio Trading AI Agent (Simone Rizzo, 4 video)
created: 2026-05-13
updated: 2026-05-13
status: active
confidence: high
priority: high
area: research
related:
  - "[[build/mvp-prototype-design]]"
  - "[[theory/modular-trading-agent-architecture]]"
  - "[[decisions/decision-log]]"
  - "[[paper-trading-agents]]"
  - "[[paper-alpha-arena]]"
---

# Ricerca NotebookLM — Approcci da Progetti Simili AI+Finance

Sessione di interrogazione del notebook NotebookLM "Trading AI Agent" (2026-05-13).
Domande mirate su architettura, backtesting, LLM performance e portfolio management.
Tutte le risposte sono citate da fonti reali nel notebook (paper, documentazione, video).

---

## 1. Architettura Multi-Agent

### TradingAgents (TauricResearch) — 7 ruoli strutturati

Il framework più completo analizzato. Struttura in divisioni:

- **Analyst Team** (4 agenti specializzati): Fundamental, Sentiment, News, Technical (MACD/RSI)
- **Researcher Team**: Ricercatori Bull vs Bear — dibattono per far emergere rischi e opportunità
- **Trader Agent**: sintetizza report e dibattiti per decidere timing e size
- **Risk Management Team**: 3 livelli (aggressivo, neutrale, conservativo) — valuta la proposta del Trader
- **Fund Manager**: approvazione finale

**Comunicazione strutturata** (non chat): gli agenti si scambiano report e JSON strutturati. Il linguaggio naturale è riservato *solo* ai dibattiti Bull/Bear. Questo evita l'effetto "telefono senza fili" (perdita di informazioni nei prompt lunghi).

**Quick Thinker + Deep Thinker**: modelli economici e veloci (es. gpt-4.1-nano) per raccolta dati e news, modelli potenti e costosi solo per la decisione finale. Pattern consolidato e validato.

### MarketSenseAI 2.0 — 5 agenti in pipeline lineare

- News Agent → Fundamentals Agent (con "Chain-of-Agents" a 3 livelli per 10-Q/10-K) → Dynamics Agent (prezzi + Sharpe) → Macroeconomic Agent (RAG + HyDE) → **Signal Agent** (CoT finale → buy/hold/sell)
- Flusso lineare e modulare; ogni agente è un nodo indipendente
- Usa VectorBT Pro per backtesting

### AlpacaTradingAgent — adattamento di TradingAgents per Alpaca

- 5 analisti (aggiunge Macro Agent con dati FRED: inflazione, PIL)
- Research Manager fa da arbitro tra Bull e Bear
- Risk Management Team 3 livelli → Portfolio Manager → Execution Engine
- Configurable Quick/Deep Thinker (gpt-4.1-nano + o3)

### Nota su Risk Management Upstream vs Downstream

In TradingAgents il Risk Management Team *valuta la proposta* del Trader (downstream). Nel nostro design il Risk Analyst è **upstream** (imposta i paletti prima della decisione). Entrambi gli approcci sono validi; l'approccio upstream è più adatto allo swing trading perché riduce il costo di cicli rifiutati.

---

## 2. Backtesting — Framework e Metodologie

### Decisione chiusa: VectorBT

**VectorBT Pro** è il framework usato da MarketSenseAI 2.0 (il paper più rigoroso del notebook). Gestisce costi di transazione in modo preciso. **Chiude la decisione: vectorbt.**

### Framework alternativi analizzati

- **skfolio + scikit-learn**: motore di cvx-portfolio-optimizer. Pipeline completa dai prezzi all'ottimizzazione. Walk-Forward Backtesting + CPCV (Combinatorial Purged Cross-Validation). Per portfolio optimization, non per strategy testing.
- **Motori custom / paper trading**: Alpha Arena usa `src/trading_bot.py` custom su dati storici a 3 minuti. TradingAgents avanza giorno per giorno sui dati storici. Simone Rizzo usa PostgreSQL + cron ogni 15 minuti.

### Insidie critiche nel backtesting

- **Look-Ahead Bias**: usare dati di bilancio *prima* della loro pubblicazione reale. La funzione `align_to_pit` di skfolio impone il ritardo corretto (45gg per 10-Q, 90gg per 10-K).
- **Survivorship Bias**: escludere aziende delisted. cvx-optimizer sostituisce l'ultimo prezzo valido con un "delisting return" realistico (es. -30%).
- **Costi di transazione obbligatori**: MarketSenseAI applica 10bps per trade. Senza, i risultati sono gonfiati. Strategie ad alta frequenza soffrono enormemente.
- **Purging ed Embargoing** (CPCV): eliminare i dati adiacenti al confine training/test per evitare distorsioni da autocorrelazione.

### Metriche di valutazione standard

**Strategie e portafogli**:
- Sharpe Ratio (più usato)
- Sortino Ratio (penalizza solo downside volatility)
- Maximum Drawdown + Calmar Ratio
- Information Ratio vs benchmark
- Win Rate + Profit Factor
- Cumulative e Annualized Return

**Predizione (ML)**:
- RMSE, MAE, MAPE

---

## 3. LLM — Performance nei Benchmark di Trading

### Alpha Arena — risultati

Competizione con 10.000$ reali in leva su contratti perpetui crypto (2 settimane):

| Modello | Rendimento | Note |
|---------|-----------|------|
| **Qwen 3 Max** | **+22.88%** | Picco ~+100%, alta volatilità |
| **DeepSeek Chat V3.1** | **+4.76%** | Picco ~+130% |
| Claude Sonnet 4.5 | -33% | |
| Grok 4 | ~-50% | Soggetto a overtrading |
| GPT-5 | >-50% | Tra i peggiori |
| Gemini 2.5 Pro | >-50% | Più iperattivo — più trade |

**Solo Qwen 3 Max e DeepSeek battono il buy-and-hold su BTC.**

### Causa principale delle perdite: overtrading + assenza SL/TP

- Grok ha aperto/chiuso 6 posizioni in 3 secondi, erodendo il capitale con spread e commissioni
- In "Monk Mode" (vincoli stringenti, leve più basse) le performance migliorano drasticamente — commissioni -70%, perdite si convertono in profitti

### Implicazioni per il nostro progetto

- **DeepSeek confermato**: ottimo rapporto costo/performance. 1/30 del costo di GPT-5.1.
- **Qwen 3 Max**: alternativa da testare in futuro (non disponibile facilmente come DeepSeek).
- **SL/TP obbligatori**: il progetto Simone Rizzo senza SL/TP ha subito drawdown devastanti nonostante win rate 66%. Il nostro design li ha già come vincolo hard — corretto.
- **Security Module è fondamentale**: senza vincoli deterministici l'LLM va in overtrading.

### Costruzione del Prompt Trader — pattern consolidato

Tutti i sistemi usano lo stesso pattern:

1. **Ruolo + stato portafoglio** (capitale totale, liquidità, posizioni aperte)
2. **Dati strutturati**: indicatori TA (MACD, RSI, Pivot Points), forecasting ML, news e sentiment (Fear & Greed)
3. **Input multi-agente** (se presente): report JSON degli analisti, sintesi dibattiti Bull/Bear
4. **Regole operative**: vincoli stringenti (es. "una sola posizione per coin", "operazioni ammesse: open/close/hold")
5. **Formato output obbligatorio**: risposta *esclusivamente* come oggetto JSON con campi: operazione, simbolo, direzione, leva, reasoning

---

## 4. Implementazione Pratica — Simone Rizzo

La serie video "Creo il mio Trading AI Agent" è il caso più vicino al nostro approccio.

**Architettura**:
- Exchange: Hyperliquid (DEX, leva fino a 40x), integrazione Python via **CCXT**
- DB: **PostgreSQL** — salva stato ogni 15 minuti (storico portafoglio, decisioni, indicatori, forecast vs reale)
- Deploy: **Railway** come Cron Job ogni 15 minuti
- Dashboard: generata con vibe-coding, mostra equity curve, posizioni, win rate, JSON reasoning dell'LLM

**Moduli costruiti**:
- `indicators.py`: MACD, RSI, EMA, **Pivot Points** (fondamentali — danno all'LLM riferimenti spaziali)
- `plot_forecast.py`: **Facebook Prophet** per previsioni a 1min e 1ora
- `sentiment.py` / `news.py`: Fear & Greed (CoinMarketCap API), news da feed XML
- Whale Alerts: reverse engineering di pagine web (no API costose)

**Problema critico di Prophet**: non funziona su crolli improvvisi. Genera previsioni bullish mentre il mercato crolla. → **Non usare Prophet come modulo di forecasting principale.**

**Risultati settimana 1** (testnet):
- Partito da 996$, chiuso a 1.063$ (+6%)
- Win rate 66.7% (16 profit, 8 loss)
- Ha operato short in mercato bearish correttamente
- **Ma**: senza SL/TP l'equity curve ha subito oscillazioni violente durante i 15min di "sonno"

---

## 5. Portfolio Management — Black-Litterman e Rebalancing

### Integrazione LLM → ottimizzazione quantitativa

Il pattern standard per tradurre una decisione LLM in pesi concreti:

1. LLM produce "views" strutturate: `{"BTCUSDT": 0.05, "confidence": 0.7}` (rendimento atteso + confidenza)
2. Le views vengono iniettate in **Black-Litterman** o **Entropy Pooling**
3. Python calcola i pesi ottimali incrociando views + covarianza storica (zero token)
4. **Rebalancing Gate**: eseguire ordini *solo se* drift dai pesi target > soglia (es. 5%) — evita overtrading

### Tecniche di risk management disponibili

- **CVaR** (Conditional Value at Risk): più robusto del VaR per i code tail risk
- **CDaR** (Conditional Drawdown at Risk): ottimizza il drawdown atteso nei peggiori scenari
- **Max Drawdown constraint**: hard limit sul drawdown massimo tollerato
- **Robust Mean-Risk**: si protegge da stime errate usando "insiemi di incertezza ellissoidali"
- **Regime detection (HMM)**: adatta la metrica di rischio al regime di mercato — varianza in toro, CVaR in orso

### Entropy Pooling — più potente di Black-Litterman

Permette viste su qualsiasi momento statistico: varianza, correlazione, skewness, curtosi, CVaR — non solo rendimenti attesi. Supporta disuguaglianze (`BTCUSDT >= 0.03`). In un sistema multi-agent, **Opinion Pooling** aggrega forecast di più agenti con pesi di probabilità.

---

---

## Riferimenti precisi ai paper

> Standard da seguire: ogni claim estratto da un paper deve avere qui il riferimento alla sezione. Aggiornare man mano.

| Claim | Paper | Sezione / Nota |
|-------|-------|---------------|
| TradingAgents: 7 ruoli (Analyst, Researcher Bull/Bear, Trader, Risk Team, Fund Manager) | TradingAgents (TauricResearch) | §3 Framework Architecture; Fig. 1 |
| Comunicazione strutturata via report/JSON tra agenti (non chat) | TradingAgents | §3.2 Communication Protocol |
| Quick Thinker + Deep Thinker (modelli diversi per raccolta vs decisione) | TradingAgents | §3.3 Model Configuration |
| VectorBT Pro per backtesting con costi di transazione | MarketSenseAI 2.0 | §4.2 Experimental Setup; 10bps per trade |
| Look-Ahead Bias: align_to_pit (45gg per 10-Q, 90gg per 10-K) | cvx-portfolio-optimizer docs | §Point-in-Time Alignment |
| Walk-Forward + CPCV per validazione temporale | cvx-portfolio-optimizer / skfolio | §Backtesting Methods |
| Alpha Arena: Qwen 3 Max +22.88%, DeepSeek +4.76%, Claude -33%, GPT-5 >-50% | Alpha Arena (arXiv o paper interno) | §Results Table |
| Overtrading causa principale perdite: Grok 6 posizioni in 3 secondi | Alpha Arena | §Analysis of Trading Behavior |
| Monk Mode (vincoli stringenti) riduce commissioni -70% | Alpha Arena | §Risk-Constrained Experiment |
| Black-Litterman: LLM produce views (rendimento atteso + confidenza) | cvx-portfolio-optimizer docs | §Black-Litterman Integration |
| Entropy Pooling: viste su varianza/correlazione/CVaR, non solo rendimenti | cvx-portfolio-optimizer docs | §Entropy Pooling |
| Rebalancing Gate: esegui ordini solo se drift > soglia | cvx-portfolio-optimizer docs | §Hybrid Rebalancing |
| Simone Rizzo: +6%, win rate 66.7%, ma drawdown senza SL/TP | Video serie pt4 | risultati settimana 1 |
| Prophet non funziona su crolli improvvisi | Video serie pt3/pt4 | osservazioni backtesting |
| Pivot Points fondamentali come riferimenti spaziali per l'LLM | Video serie pt2 | feedback community |
| MarketSenseAI: 5 agenti in pipeline lineare (News → Fundamentals → Dynamics → Macro → Signal) | MarketSenseAI 2.0 (arXiv:2502.00415) | §3 Architecture |
| Chain-of-Agents a 3 livelli per analisi 10-Q/10-K | MarketSenseAI 2.0 | §3.2 Fundamentals Agent |
| RAG + HyDE per report macro istituzionali | MarketSenseAI 2.0 | §3.4 Macroeconomic Agent |

---

## Decisioni chiuse da questa sessione

| Tema | Decisione | Fonte |
|------|-----------|-------|
| Framework backtesting | **VectorBT** | MarketSenseAI usa VectorBT Pro |
| LLM principale | **DeepSeek** confermato | Alpha Arena: miglior rapporto costo/perf |
| SL/TP | Obbligatori, hard constraint | Simone Rizzo: senza → drawdown devastante |
| Prophet | **Non usare** come forecast principale | Non regge i crolli improvvisi |
| Comunicazione inter-agent | **JSON strutturato** (non chat) | Tutti i framework convergono su questo |

## Cose da approfondire (aperte)

- Qwen 3 Max: accessibilità e costo via API (alpha arena winner)
- Walk-Forward Backtesting specifico per swing trading su crypto
- HMM per regime detection: complessità di implementazione vs beneficio
- Pivot Points: da aggiungere come input al Prompt Builder (tutti li usano)
