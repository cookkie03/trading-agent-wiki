---
title: "Piano Operativo di Sviluppo — Trading Agent"
type: artifact
tags:
  - architecture
  - roadmap
  - execution
  - multi-agent
  - quant
  - software
created: 2026-09-02
updated: 2026-09-02
status: active
related:
  - "[[artifacts/project-board]]"
  - "[[system/foundation/architecture]]"
  - "[[system/foundation/codebase-architecture]]"
  - "[[system/foundation/stack]]"
  - "[[system/foundation/mvp]]"
  - "[[system/foundation/implementation-status]]"
  - "[[_meta/comment-resolution-2026-07-13]]"
confidence: high
priority: high
area: software
---
# Piano Operativo di Sviluppo — Trading Agent

> **Documento Guida Ufficiale per lo Sviluppo della Codebase e l'Orchestrazione Multi-Agent**  
> Basato sulla rilettura integrale dei requisiti, sulle indicazioni operative di Luca e sui punti di allineamento con Salvatore (mercati/strategia).

---

## 1. Visione & Principi Cardine di Ingegneria

1. **Partenza da Zero & Nessun Debito Ereditato**:
   * Il repository di codice esterno parte da foglio bianco. Nessuna implementazione legacy viene considerata "acquisita".
   * I vecchi riferimenti a moduli implementati nel vault fungono unicamente da *reference design concettuale*.
2. **Architettura a Imbuto (Funnel Architecture)**:
   * Flusso decisionale gerarchico, lineare e deterministico:
     $$\text{Universe Filtering (Screening)} \longrightarrow \text{Desk Analysis (Deep Dive)} \longrightarrow \text{PM Synthesis \& Scoring} \longrightarrow \text{Risk Gate} \longrightarrow \text{Execution}$$
   * Evitare complessità non tracciabili, loop ciclici non controllati o grafi con divergenze infinite.
3. **Test-Driven Development (TDD) Rigoroso**:
   * Prima si sviluppano l'harness di test e i mock dei provider esterni;
   * Poi si implementano i tool deterministici e i calcoli quantitativi;
   * Successivamente si costruiscono i grafi agentici in LangGraph;
   * Infine si collegano i trigger temporali e i job asincroni.
4. **Ambito MVP USD-Only**:
   * L'MVP opera esclusivamente su azioni del mercato USA denominate in USD. Tutte le complessità di cambio valuta, cross-currency e hedging Forex sono esplicitamente posticipate al Post-MVP.
5. **Decoupling Radicale (Deep Modules)**:
   * Separazione netta tra:
     * **Data Layer / Tool Harness** (OpenBB, API broker, database);
     * **Quantitative Engine** (formule e indicatori matematici puri, 100% deterministici, zero LLM per il calcolo dei numeri);
     * **Agent Layer** (LangGraph, prompt versionati, ruoli semantici e sintesi);
     * **Interface Layer** (UI/Dashboard completamente disaccoppiata tramite contratti dati).

---

## 2. Roadmap di Sviluppo Dettagliata per Fasi

```
+-------------------------------------------------------------------------+
| FASE 0: Scaffolding & Setup Repository                                 |
+------------------------------------+------------------------------------+
                                     |
                                     v
+------------------------------------+------------------------------------+
| FASE 1: Data Layer & Tool Harness (OpenBB-first, Broker, Mock Tests)    |
+------------------------------------+------------------------------------+
                                     |
                                     v
+------------------------------------+------------------------------------+
| FASE 2: Quantitative Engine & Indicatori (Trend, Reversion, Value)     |
+------------------------------------+------------------------------------+
                                     |
                                     v
+------------------------------------+------------------------------------+
| FASE 3: Orchestrazione LangGraph & Agenti (PM, Desks, Risk, Schemas)    |
+------------------------------------+------------------------------------+
                                     |
                                     v
+------------------------------------+------------------------------------+
| FASE 4: Risk Gate & Execution Layer (Paper Trading, Sizing, Safety)    |
+------------------------------------+------------------------------------+
                                     |
                                     v
+------------------------------------+------------------------------------+
| FASE 5: Observability, LangSmith & UI Disaccoppiata (Streamlit)        |
+------------------------------------+------------------------------------+
                                     |
                                     v
+------------------------------------+------------------------------------+
| FASE 6: Post-MVP (News Summary Tool, GraphRAG, Advanced Quant)         |
+------------------------------------+------------------------------------+
```

---

### Fase 0 — Scaffolding del Repository e Toolchain
*Obiettivo: predisporre la struttura del repository esterno `trading-agent` con toolchain moderna, linting, tipizzazione statica e suite di test.*

- [ ] **0.1 Setup Repository & Ambiente**:
  - Inizializzazione repository con `pyproject.toml` (Poetry o UV/Hatch).
  - Python 3.11+ con `mypy` (strict mode), `ruff` (linter + formatter) e `pytest`.
- [ ] **0.2 Gestione Configurazioni & Credenziali**:
  - Modulo `config` centralizzato basato su `pydantic-settings`.
  - Gestione sicura delle API Key (OpenBB, Alpaca, IBKR, LangSmith, OmniRoute LLM endpoints).
- [ ] **0.3 Alberatura Iniziale della Codebase**:
  ```
  trading-agent/
  ├── config/             # Pydantic settings & environment validation
  ├── data/               # Vendor adapters, OpenBB wrappers, caching
  ├── quant/              # Math pura: indicatori, scoring, sizing, backtest
  ├── agents/             # LangGraph workflows, state schemas, node definitions
  │   └── prompts/        # System prompts isolati e versionati (.txt / .md)
  ├── execution/          # Broker connectors, paper trading, order lifecycle
  ├── interface/          # Disconnected UI (Streamlit MVP)
  └── tests/              # Unit, integration & regression tests con fixtures
  ```

---

### Fase 1 — Data Layer & Tool Harness (OpenBB-first)
*Obiettivo: costruire un livello di accesso ai dati multi-vendor, resiliente e testabile offline tramite mock/vcr.*

- [ ] **1.1 OpenBB Platform Integration**:
  - Configurazione di OpenBB Platform SDK come punto di accesso primario ai dati di mercato.
  - Creazione di wrapper unificati per:
    * Prezzi storici OHLCV (intervalli giornalieri e orari);
    * Dati fondamentali di bilancio (Income statement, Balance sheet, Cash flow);
    * Dati macroeconomici (tassi FRED, inflazione CPI/PCE, PIL);
    * Calendario degli eventi societari (Earnings calendar, Dividendi, Split).
- [ ] **1.2 Multi-Vendor Fallback & Broker Adapter**:
  - Implementazione del fallback automatico: OpenBB $\rightarrow$ Yahoo Finance $\rightarrow$ Broker API.
  - Connector per dati in tempo reale via Alpaca / Interactive Brokers (IBKR).
- [ ] **1.3 Data Caching & Provenance**:
  - Caching locale (SQLite o Parquet/DuckDB) per minimizzare chiamate API e garantire riproducibilità.
  - Tracciamento della provenienza (`source_vendor`, `timestamp_utc`, `data_hash`) per ogni record estratto.
- [ ] **1.4 Test Suite del Data Layer**:
  - Fixtures e mock offline per ogni vendor in `tests/data/`.

---

### Fase 2 — Quantitative Engine & Indicatori (Matematica Pura)
*Obiettivo: creare la logica numerica deterministica per l'analisi tecnica, fondamentale e il calcolo del rating/score.*

- [ ] **2.1 Libreria Indicatori Tecnici**:
  - Calcolo deterministico di medie mobili (SMA/EMA 20, 50, 200), RSI (14), MACD (12, 26, 9), ATR (14), Bollinger Bands.
  - Moduli dedicati per:
    * **Trend Following**: Golden Cross, allineamento trend, breakout di massimi a 52 settimane.
    * **Mean Reversion**: Z-score di prezzo, deviazioni standard su bande, ipervenduto/ipercomprato.
- [ ] **2.2 Metriche Fondamentali & Value**:
  - Calcolo metriche di valutazione: P/E, P/B, EV/EBITDA, Free Cash Flow Yield, Debt/Equity, ROE/ROIC.
  - Integrazione logiche Factor Investing (Quality, Value, Momentum).
- [ ] **2.3 Motore di Scoring & Rating Deterministico**:
  - Funzione pura di aggregazione pesata che produce un `QuantScore` ($0 \dots 100$) per ticker.
- [ ] **2.4 Framework di Backtest Locale**:
  - Engine di backtest su serie storiche per validare la robustezza statistica delle strategie prima di associarvi agenti LLM.

---

### Fase 3 — Multi-Agent Orchestration & State Schemas (LangGraph)
*Obiettivo: implementare il grafo di decisione multi-agente con LangGraph, schema di stato immutabile e prompt versionati.*

- [ ] **3.1 Definizione Schemi di Stato (Pydantic / TypedDict)**:
  - `ResearchState`: stato interno del desk analisti per singolo ticker.
  - `InvestmentState`: scheda d'investimento centralizzata, annidata a campi fissi:
    * `ticker`, `timestamp`, `quant_score`, `macro_summary`, `fundamental_thesis`, `sentiment_signals`, `risk_assessment`, `pm_action_proposal`, `next_check_date`.
- [ ] **3.2 Desk Analisti Specializzati**:
  - **Market Analyst**: analisi dati macroeconomici, tassi, ciclo e catalizzatori di settore.
  - **Technical / Quant Analyst**: interpreta i segnali del Quantitative Engine (Fase 2).
  - **Fundamentals Analyst**: analizza trimestrali, guidance, salute del bilancio e moat.
  - **Sentiment Analyst**: sentiment da news, posizionamento istituzionale, insider transactions.
- [ ] **3.3 Portfolio Manager (PM) Agent**:
  - Node orchestratore in LangGraph che aggrega i report dei desk, valuta la coerenza e formula la proposta operativa:
    $$\text{Action} \in \{\text{BUY}, \text{HOLD}, \text{SELL}, \text{REBALANCE}, \text{NO\_ACTION}\}$$
  - Calcolo motivato e valorizzazione del campo obbligatorio `next_check_date`.
- [ ] **3.4 Trigger Engine & Event Schedulation**:
  - Gestione dei 3 canali di trigger:
    1. *Temporal / Calendar Trigger* (`next_check_date` scaduta);
    2. *Market Alert Trigger* (anomalie di prezzo, volatilità improvvisa, rottura livelli);
    3. *Macro Event Trigger* (rilascio dati inflazione, decisioni FOMC/FED).
- [ ] **3.5 System Prompts Isolation**:
  - Tutti i prompt memorizzati in `agents/prompts/` in formato markdown leggibile, senza codice hardcodato.

---

### Fase 4 — Risk Gate & Execution Management Layer
*Obiettivo: garantire la sicurezza del capitale con gate di blocco e gestione dell'ordine verso broker.*

- [ ] **4.1 Risk Analyst Gate (Ruolo & Vincoli)**:
  - Controllo deterministico di compliance pre-trade:
    * Esposizione massima per singolo ticker ($\le X\%$ del portafoglio);
    * Esposizione settoriale massima;
    * Drawdown massimo tollerato;
    * Validità del rapporto Risk/Reward ($\ge 2.0$).
  - Funzione di *Veto Power*: se il Risk Gate fallisce, l'ordine non può procedere a execution.
- [ ] **4.2 Position Sizing Deterministico**:
  - Modulo di dimensionamento della posizione (ATR-based, Fixed Fractional o Kelly Criterion frazionario).
- [ ] **4.3 Execution Adapter (Paper Trading First)**:
  - Connettore per invio ordini (Market, Limit, Stop Loss, Trailing Stop) tramite Alpaca Paper Trading API.
  - Gestione stato dell'ordine: `SUBMITTED` $\rightarrow$ `FILLED` / `REJECTED` / `CANCELLED`.
- [ ] **4.4 Audit Trail & Transaction Logging**:
  - Salvataggio immutabile su DB di: tesi dell'agent, stato del portafoglio al momento del trade, score, ordine ed esito.

---

### Fase 5 — Observability, Tracing & Interfaccia Disaccoppiata
*Obiettivo: garantire la totale visibilità decisionale e fornire una UI operativa per l'utente umano.*

- [ ] **5.1 LangSmith Tracing & Observability**:
  - Tracciamento end-to-end di ogni run di LangGraph (token spesi, latenza, prompt usati, decisioni PM).
- [ ] **5.2 Dashboard Streamlit (MVP Read-Only)**:
  - Visualizzazione portafoglio attivo, P&L, allocazione e storico ordini.
  - Scheda Ticker interattiva: lettura dell'`InvestmentState` generato dagli agenti.
  - Visualizzazione della lista di attesa e scadenze `next_check_date`.
- [ ] **5.3 Architettura Disaccoppiata per Futuro Frontend**:
  - Interfaccia basata su API interne / contratti JSON stabili, consentendo in futuro la sostituzione trasparente con frontend React/TypeScript.

---

### Fase 6 — Post-MVP & Backlog di Ricerca Avanzata
*Obiettivo: espansioni future già identificate nelle daily notes ma escluse dallo scope MVP.*

- [ ] **6.1 News Historical Summary Tool**:
  - Tool dedicato che esegue query parametriche (`start_date`, `end_date`, `keywords`) su archivi news e genera recap strutturati tramite LLM.
- [ ] **6.2 Memoria Semantica & Knowledge Graph**:
  - Integrazione di LightRAG / GraphRAG locale (`ragcli`) per recuperare correlazioni storiche e tesi pregresse.
- [ ] **6.3 Studio Approfondito di Paper e Repository Esterni**:
  - **[OpenAlice](https://github.com/TraderAlice/OpenAlice)**: analisi architettura multi-asset e gestione cicli di vita posizione.
  - **[CVX Portfolio Optimizer](https://codewiki.google/github.com/silviobaratto/optimizer)**: studio di Black–Litterman e allocazione Idzorek.
  - **[Kronos Foundation Model](https://arxiv.org/abs/shiyu-coderKronos)**: foundation model per serie storiche e tokenizzazione finanziaria.
  - **FinRL / Alpha Arena**: benchmark di competition tra LLM trader.
- [ ] **6.4 Learning & Feedback Loop**:
  - Meta-scoring automatico delle tesi degli analisti confrontate con l'esito reale a 30/60/90 giorni.
  - Ponderazione dinamica (RL weighting) dei desk in base all'accuratezza storica.

---

## 3. Matrice dei Punti Aperti con Salvatore (Meeting Prep)

| # | Argomento | Domanda Chiave / Opzioni | Impatto su Codice |
|---|---|---|---|
| **1** | **Strategia MVP Base** | Partiamo con *Value + Trend Following* o *Mean Reversion* come prima strategia codificata? | Seleziona i primi indicatori da inserire nel Quantitative Engine. |
| **2** | **Ruolo Risk Analyst** | Il Risk Analyst deve operare come desk analitico preliminare o come gatekeeper deterministico di blocco finale prima dell'ordine? | Struttura del grafo LangGraph e routing dell'edge verso Execution. |
| **3** | **Confine Market vs Sentiment** | Il Market Analyst gestisce solo macro/tassi/settori e il Sentiment solo news/social/mood, o ci sono sovrapposizioni? | Definizione degli schemi di output dei singoli nodi analisti. |
| **4** | **Criteri `next_check_date`** | Quali parametri guidano il PM nel fissare la revisione (volatilità, giorni ad earnings, time-horizon della strategia)? | Algoritmo di calcolo della data di trigger nel PM node. |
| **5** | **Indicatori Tecnici Chiave** | Quali timeframes e parametri standard usiamo per SMA, RSI, ATR e Bande di Bollinger? | Parametrizzazione predefinita nel modulo `quant/indicators.py`. |

---

## 4. Skill Hermes Collegate alla Realizzazione del Piano

* **`software-development/test-driven-development`**: Esecuzione ciclo TDD per ogni modulo (dati, quant, execution).
* **`software-development/codebase-design`**: Strutturazione delle interfacce profonde dei moduli.
* **`software-development/to-spec` & `software-development/to-tickets`**: Suddivisione dei milestone in ticket atomici implementabili.
* **`research/competitor-news-monitor` & `research/arxiv`**: Monitoraggio continuo di aggiornamenti su OpenAlice, Kronos e paper finanziari.
* **`note-taking/obsidian` & `aside/obsidian-markdown`**: Manutenzione sincronizzata della wiki e della Project Board ad ogni avanzamento.
