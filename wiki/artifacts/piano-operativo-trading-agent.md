---
title: Piano Operativo di Sviluppo — Trading Agent
type: artifact
tags:
  - multi-agent
  - architecture
  - roadmap
created: 2026-09-02T00:00:00.000Z
updated: 2026-11-02T00:00:00.000Z
status: active
related:
  - "[[artifacts/project-board]]"
  - "[[system/foundation/architecture]]"
  - "[[system/foundation/codebase-architecture]]"
  - "[[system/foundation/stack]]"
  - "[[system/foundation/mvp]]"
  - "[[system/foundation/implementation-status]]"
  - "[[comment-resolution-2026-07-13]]"
confidence: high
priority: high
area: software
---
# Piano Operativo di Sviluppo — Trading Agent

> **Documento Guida Ufficiale per lo Sviluppo della Codebase e l'Orchestrazione Multi-Agent**  
> Basato sulla rilettura integrale dei requisiti, sulle indicazioni operative di Luca e sui punti di allineamento con Salvatore (mercati/strategia).

---

## Priorità correnti — 2026-11-04

La sequenza operativa e i prossimi passi vivono solo nella [[artifacts/project-board#Priorità operative correnti — 2026-11-04]]. La priorità harness-first e l'ordine delle fasi sottostanti sono superati, conservati come contesto storico e inventario da rivalutare, non come istruzioni operative. Il tree resta da definire insieme; [[artifacts/architettura.canvas]] è il riferimento di design prioritario nei dubbi e gli altri canvas sono idee o reference. Gli agenti si testano con fake prima dell'infrastruttura reale. Safety e risk restano deterministici; nessuna attivazione dell'esecuzione reale. Lavoro e filoni esistenti sono conservati, non cancellati.

## 1. Visione & Principi Cardine di Ingegneria

1. **Partenza da Zero & Nessun Debito Ereditato**:
   * Il repository di codice esterno parte da foglio bianco. Nessuna implementazione legacy viene considerata "acquisita".
   * I vecchi riferimenti a moduli implementati nel vault fungono unicamente da *reference design concettuale*.
2. **Architettura a Imbuto (Funnel Architecture)**:
   * Flusso decisionale gerarchico, lineare e deterministico:
     $$\text{Universe Filtering (Screening)} \longrightarrow \text{Desk Analysis (Deep Dive)} \longrightarrow \text{PM Synthesis \& Scoring} \longrightarrow \text{Risk Gate} \longrightarrow \text{Execution}$$
   * Evitare complessità non tracciabili, loop ciclici non controllati o grafi con divergenze infinite.
3. **Riuso selettivo di prior-art verificata**:
   * Quando una feature coincide con `TauricResearch/TradingAgents`, studiare prima l’implementazione upstream e riusare il codice il più possibile, rispettando licenza Apache-2.0, attribuzione e compatibilità con i contratti propri.
   * Il riuso non implica fork né copia indiscriminata: isolare gli adattamenti dietro interfacce profonde del progetto e mantenere test, provenance e vincoli deterministici locali.
4. **Test-Driven Development (TDD) Rigoroso**:
   * Il precedente ordine harness → tool → grafi → trigger è storico e superato come priorità; per la sequenza corrente vedere la [[artifacts/project-board#Priorità operative correnti — 2026-11-04]].
   * I workflow agentici si testano con fake; i collegamenti reali arrivano successivamente.
4. **Ambito MVP USD-Only**:
   * L'MVP opera esclusivamente su azioni del mercato USA denominate in USD. Tutte le complessità di cambio valuta, cross-currency e hedging Forex sono esplicitamente posticipate al Post-MVP.
5. **Decoupling Radicale (Deep Modules)**:
   * Separazione netta tra:
     * **Data Layer / Tool Harness** (OpenBB, API broker, database);
     * **Quantitative Engine** (formule e indicatori matematici puri, 100% deterministici, zero LLM per il calcolo dei numeri);
     * **Agent Layer** (LangGraph, prompt versionati, ruoli semantici e sintesi);
     * **Interface Layer** (UI/Dashboard completamente disaccoppiata tramite contratti dati).

6. **Il sistema agentico non è una strategia quantitativa automatica**:
   * Una sequenza fissa di indicatori e soglie (`EMA + breakout + ATR → buy/sell`) è una baseline quantitativa deterministica, non il cuore del Trading Agent.
   * Il Quantitative Engine calcola indicatori, metriche, screening e guardrail riproducibili; non sostituisce il ragionamento degli agenti e non decide da solo la tesi d'investimento.
   * Gli agenti LLM raccolgono e interpretano evidenze, formulano ipotesi, confrontano segnali concordanti e contraddittori, dichiarano incertezze e condizioni di invalidazione, discutono la tesi e propongono una decisione.
   * La decisione finale deve restare tracciabile nello state; i numeri usati dagli agenti devono provenire da tool deterministici con provenance, non essere inventati dal modello.

7. **Separazione tra strategia, evidenza, tesi e trade**:
   * La strategia definisce obiettivo, domande, tool prioritari, evidenze attese e vincoli di dominio; non si riduce a un singolo segnale di entry/exit.
   * `QuantitativeEvaluation` raccoglie evidenze numeriche calcolate dai tool.
   * `ResearchState` conserva la tesi in costruzione e i contributi dei desk.
   * `InvestmentState` conserva la tesi completa e validata dal Risk Analyst.
   * `TradeIntent` è la proposta esecutiva; solo una funzione Python deterministica la trasforma in un ordine conforme ai guardrail.

8. **Strategia MVP come contesto di ragionamento**:
   * L'MVP usa trend following su barre hourly, azioni USA, USD-only, long-only e swing trading.
   * Questa scelta definisce il contesto e le domande prioritarie del sistema; non impone una formula unica né trasforma l'MVP in un bot di indicatori.
   * Indicatori come EMA, RSI, MACD, ATR, volume e supporti/resistenze sono capacità interrogabili dagli agenti. Le soglie e le combinazioni restano versionate, motivate e validabili; una baseline deterministica serve come confronto, non come sostituto del sistema agentico.

---

## 1.1 Contratto concettuale dell'agent system

Il diagramma a quattro aree e le responsabilità seguenti sono **una proposta**, non una topologia consolidata: l'interpretazione a due desk in [[system/foundation/architecture]] e quella a quattro aree vanno chiarite rispetto a [[artifacts/architettura.canvas]]. Non è deciso il numero di agenti; numero, ruoli e routing restano aperti. La priorità operativa è tracciata nella [[artifacts/project-board#Priorità operative correnti — 2026-11-04]]. Nessuna esecuzione reale è autorizzata.

Flusso proposto:

```text
Trigger
  → Portfolio Manager
  → desk Market / Technical / Fundamentals / Sentiment
  → evidenze + ipotesi + conflitti
  → PM synthesis
  → Risk Analyst: antitesi + gate deterministico
  → InvestmentState
  → TradeIntent
  → execution paper
```

### Responsabilità dei ruoli

- **Portfolio Manager**: decide quali desk chiamare, quali dati mancano, quando il quadro è sufficientemente completo; non calcola indicatori a mano.
- **Technical Analyst**: interroga OHLCV e capability quantitative su più finestre/timeframe, interpreta trend, breakout, volatilità, volume, supporti/resistenze e condizioni di invalidazione.
- **Market Analyst**: valuta regime macro, settore, tassi, catalizzatori ed eventi imminenti.
- **Sentiment Analyst**: valuta news, mood, posizionamento e possibili divergenze tra sentiment e prezzo.
- **Fundamentals Analyst**: valuta earnings, guidance, bilancio, valutazione e rischi societari; il suo compito non è inventare il timing hourly.
- **Risk Analyst**: attacca la tesi, espone scenari contrari e applica i controlli numerici deterministici su sizing, concentrazione, liquidità, drawdown e rischio di portafoglio.
- **Execution**: non ragiona; converte solo una proposta approvata in un'azione conforme ai guardrail.

### Forma dello state

La forma comune deve essere estensibile ma leggibile:

```text
StrategyProfile
  → obiettivo, famiglia, domande, tool, evidenze attese e vincoli
QuantitativeEvaluation
  → valori, timestamp, fonte, parametri, formula_version, interpretazione disponibile
ResearchState
  → identity, trigger, contesto, contributi desk, evidenze, ipotesi,
    bull_case, bear_case, conflitti, incertezze, invalidation_conditions,
    proposta di direzione, conviction, entry/exit/risk thesis,
    next_check_date, completezza, status, provenance
InvestmentState
  → ResearchState completo, validato e approvato dal Risk Analyst
TradeIntent
  → direzione, strumento, quantità proposta, limiti prezzo, stop,
    motivazione, riferimenti allo state e decisione di approvazione
```

Lo schema resta annidato e a campi espliciti, come già deciso nella wiki; l'estensibilità viene ottenuta tramite profili di strategia, collezioni tipizzate di evidenze e contributi, non tramite un dizionario opaco che nasconde il contratto. La stessa forma deve poter ospitare trend following, mean reversion e factor investing senza aggiungere campi strutturali specifici come `SMA20` o `hedge_ratio` allo state comune.

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
*Obiettivo: creare capability numeriche deterministiche — analisi tecnica, fondamentale, metriche, screening e guardrail — che gli agenti possono interrogare e interpretare. Il Quantitative Engine non è il decisore autonomo e non sostituisce il sistema multi-agent.*

- [ ] **2.0 Studio preliminare dei tool quantitativi**:
  - Analizzare [`microsoft/qlib`](https://github.com/microsoft/qlib) per data handling, feature engineering, model/research workflow e criteri di point-in-time correctness.
  - Analizzare [`caalopezgo/quantlab`](https://github.com/caalopezgo/quantlab) per la separazione data → features → strategy → portfolio → risk → paper execution, backtest walk-forward e contratti del risk engine.
  - Produrre una nota tecnica con capacità verificate, licenze, dipendenze, codice riusabile e incompatibilità con il monolite modulare; nessuna dipendenza viene adottata prima della decisione esplicita.
- [ ] **2.1 Modulo Quantitative Research Tools**:
  - Definire un’interfaccia propria e stretta per strategie quantitative, feature/indicatori, portfolio construction e metriche, indipendente dai tool esterni.
  - Integrare adapter per Qlib e QuantLab solo dove forniscono leverage reale; il core mantiene contratti, provenance e determinismo propri.
  - Rendere ogni run riproducibile e registrabile nel DB centrale, con dataset/versione, parametri, formula/model version, costi e risultato.
- [ ] **2.2 Modulo VectorBT per Backtesting**:
  - Studiare preliminarmente [`polakowo/vectorbt`](https://github.com/polakowo/vectorbt): modello dati, portfolio simulation, costi/slippage, gestione dei segnali e limiti rispetto al replay event-driven del progetto.
  - Integrare un adapter `vectorbt` dietro un’interfaccia di backtesting propria, senza esporre direttamente API vectorbt agli agenti.
  - Rendere il backtesting accessibile sia a un umano (CLI/notebook o interfaccia esplicita) sia agli agenti tramite tool deterministico con input/output strutturati e limiti di risorse.
  - Separare sempre ricerca esplorativa e valutazione ufficiale: niente risultati vectorbt entra nel decision state senza dataset, periodo, costi, parametri e versione registrati.
- [ ] **2.3 Libreria Indicatori e Capability Tecniche**:
  - Calcolo deterministico di medie mobili (SMA/EMA 20, 50, 200), RSI (14), MACD (12, 26, 9), ATR (14), Bollinger Bands.
  - Moduli dedicati per:
    * **Trend Following**: allineamento del trend, breakout, forza del movimento e condizioni di invalidazione.
    * **Mean Reversion**: Z-score di prezzo, deviazioni standard su bande, ipervenduto/ipercomprato.
  - Gli indicatori sono capability interrogabili dagli agenti, non una pipeline fissa che decide automaticamente entry/exit.
- [ ] **2.2 Metriche Fondamentali & Value**:
  - Calcolo metriche di valutazione: P/E, P/B, EV/EBITDA, Free Cash Flow Yield, Debt/Equity, ROE/ROIC.
  - Integrazione logiche Factor Investing (Quality, Value, Momentum).
- [ ] **2.3 Quantitative Evaluation e Scoring**:
  - Definire output strutturati con valore, timestamp, fonte, parametri, `formula_version` e contesto di calcolo.
  - Eventuali score deterministici (`QuantScore`) sono evidenze per il PM e non sostituiscono la tesi multi-agent.
- [ ] **2.4 Framework di Backtest Locale**:
  - Engine di backtest su serie storiche per validare baseline quantitative, capability e robustezza statistica prima e durante l'associazione agli agenti LLM.
  - Separare sempre la baseline deterministica di confronto dalla strategia agentica: nessun risultato entra nello state decisionale senza dataset, periodo, costi, parametri e versione registrati.

---

### Fase 3 — Multi-Agent Orchestration & State Schemas (LangGraph)
*Obiettivo: implementare il grafo di decisione multi-agente con LangGraph, schema di stato immutabile e prompt versionati.*

- [ ] **3.0 Riuso compatibile da `TauricResearch/TradingAgents`**:
  - Per ogni feature coincidente, confrontare prima l’implementazione upstream, la licenza Apache-2.0, i test e le assunzioni sui dati.
  - Riutilizzare il codice il più possibile quando è compatibile con i contratti locali; preferire porting/adattamento minimo e attribuito rispetto a una riscrittura duplicata.
  - Non importare implicitamente topologia, provider, prompt, schema o side effect che violino DB centrale, determinismo, provenance o state schema locale.
  - Registrare per ogni riuso la versione/commit upstream, la parte incorporata, le modifiche locali e i test di equivalenza/regressione.

- [ ] **3.1 Definizione Schemi di Stato (Pydantic / TypedDict)**:
  - `StrategyProfile`: obiettivo, famiglia, domande guida, tool prioritari, evidenze attese e vincoli della strategia. Il profilo non è una sequenza rigida di entry/exit.
  - `QuantitativeEvaluation`: evidenze numeriche calcolate dai tool, con valore, timestamp, fonte, parametri, `formula_version` e contesto di calcolo.
  - `ResearchState`: tesi in costruzione per singolo ticker/run, con identità, trigger, contesto di mercato e portafoglio, contributi dei desk, evidenze, ipotesi, bull case, bear case, conflitti, incertezze, condizioni di invalidazione, proposta di direzione, conviction, tesi di entry/exit/risk, `next_check_date`, completezza, status e provenance.
  - `InvestmentState`: `ResearchState` completo, validato e approvato dal Risk Analyst; è l'unico state da cui può derivare una proposta esecutiva.
  - `TradeIntent`: proposta esecutiva strutturata con direzione, strumento, quantità proposta, limiti di prezzo, stop, motivazione, riferimenti allo state e approvazione del gate.
  - Gli schemi restano annidati e a campi espliciti. L'estensibilità passa da profili, collezioni tipizzate di evidenze e contributi, non da dizionari opachi. Lo stesso contratto deve ospitare trend following, mean reversion e factor investing senza introdurre campi strutturali specifici come `SMA20` o `hedge_ratio`.
- [ ] **3.2 Desk Analisti Specializzati**:
  - **Market Analyst**: valuta regime macro, tassi, ciclo, settore, catalizzatori ed eventi imminenti; indica ciò che sostiene o contraddice la direzione valutata.
  - **Technical Analyst**: interroga OHLCV e capability quantitative su più finestre/timeframe; interpreta trend, breakout, volume, volatilità, supporti/resistenze e condizioni di invalidazione. Non inventa indicatori né numeri.
  - **Fundamentals Analyst**: analizza trimestrali, guidance, salute del bilancio, valutazione, moat, earnings imminenti e rischio di gap; non decide da solo il timing hourly.
  - **Sentiment Analyst**: valuta news, mood, posizionamento e divergenze tra sentiment e prezzo.
  - Ogni desk produce evidenze citabili, ipotesi, livello di confidenza, conflitti rilevati e condizioni che falsificherebbero la propria lettura.
- [ ] **3.3 Portfolio Manager (PM) Agent**:
  - Node orchestratore in LangGraph che decide quali desk/tool chiamare, identifica i dati mancanti, confronta evidenze concordanti e contraddittorie, e stabilisce quando il quadro è sufficientemente completo.
  - Il PM costruisce la tesi, esplicita cosa la conferma e cosa la invalida, assegna la conviction e formula la proposta operativa:
    $$\text{Action} \in \{\text{BUY}, \text{HOLD}, \text{SELL}, \text{REBALANCE}, \text{NO\_ACTION}\}$$
  - Il PM non calcola indicatori a mano e non sostituisce i gate deterministici. `next_check_date` deve essere motivata sulla base di trigger e rischio di obsolescenza della tesi.
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
  - Il Risk Analyst svolge due funzioni separate:
    * **Antitesi qualitativa**: attacca la tesi, cerca scenari contrari, fragilità, rischi non considerati e condizioni di invalidazione.
    * **Gate quantitativo deterministico**: verifica compliance pre-trade senza affidarsi al giudizio LLM:
      * Esposizione massima per singolo ticker ($\le X\%$ del portafoglio);
      * Esposizione settoriale massima;
      * Drawdown massimo tollerato;
      * Validità del rapporto Risk/Reward ($\ge 2.0$);
      * sizing, liquidità, riserva cash e rischio complessivo di portafoglio.
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
- [ ] **5.2 Cockpit operativo React/TypeScript (MVP)**:
  - Visualizzazione portafoglio attivo, P&L, allocazione e storico ordini.
  - Scheda Ticker interattiva: lettura dell'`InvestmentState` generato dagli agenti.
  - Visualizzazione della lista di attesa e scadenze `next_check_date`.
- [ ] **5.3 Architettura Disaccoppiata per Futuro Frontend**:
  - Interfaccia basata su API interne e contratti JSON stabili per lettura e modifica delle risorse autorizzate, con frontend React/TypeScript. Il cockpit include configurazioni, strategie, state, provider, agenti, workflow e osservabilità.

---

### Fase 6 — Post-MVP & Backlog di Ricerca Avanzata
*Obiettivo: espansioni future già identificate nelle daily notes ma escluse dallo scope MVP.*

- [ ] **6.0 Studio preliminare e decisione di adozione — PostgreSQL, pgvector, FTS, RAG**:
  - Studiare [`Jiangge89/trading-agent`](https://github.com/Jiangge89/trading-agent) come reference per PostgreSQL, `pgvector`, full-text search (FTS), memoria degli agenti e RAG; verificare codice, schema, migrazioni, licenza e limiti prima di adottare pattern.
  - Valutare PostgreSQL come adapter di persistenza/search per ambienti multi-processo o deployati, mantenendo l’interfaccia del repository indipendente dal database.
  - Valutare `pgvector` per embeddings e similarity search, senza sostituire FTS: i due meccanismi hanno scopi distinti e possono essere combinati nel retrieval ibrido.
  - Implementare FTS per ricerca lessicale/auditabile su documenti, eventi, decisioni e memoria; definire stemming, lingua, ranking, filtri temporali e provenance.
  - Implementare RAG come feature futura prioritaria: ingestion documenti → chunk/metadata → embedding → retrieval ibrido FTS+vector → contesto citabile nello state; il RAG non può diventare fonte non tracciata per segnali o ordini.
  - Definire policy di retention, isolamento per ticker/run, versionamento degli embeddings, cancellazione/rebuild dell’indice e fallback deterministico quando retrieval è incompleto.
  - Nessuna migrazione da SQLite né dipendenza obbligatoria da PostgreSQL prima di benchmark, schema review e decisione esplicita; il primo adapter resta quello già verificato nel repository.
- [ ] **6.1 Quant avanzato e ricerca**:
  - Usare Qlib/QuantLab per esperimenti di strategie quantitative solo attraverso il modulo `Quantitative Research Tools` e con risultati registrati.
  - Usare vectorbt per sweep esplorativi e backtest accessibili a umano e agenti; validare i risultati con il framework ufficiale event-driven quando diventano decision-relevant.
- [ ] **6.2 Knowledge/RAG**:
  - Integrare progressivamente memoria episodica, documenti finanziari e decision log nel retrieval ibrido, mantenendo citazioni, timestamp e provenance.
- [ ] **6.3 News Historical Summary Tool**:
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
porta a termine la trasposizione in codice del piano /home/luca/trading-agent-wiki/wiki/artifacts/piano-operativo-trading-agent.md facendo riferimento alla metodologia di software development stabilita nei @docs/ + progetta e realizza un front end completo che includa ogni feature del codice e si concretizzi in un cockpit completo usando /impeccable, realizza i test secondo la metodologia studiata e consolidata nei docs (stile antirez) e /tdd e fa si che siano tutti verdi + studia deep le repository citate nel piano-operativo paragonando il codice di ogni repository trovata nel piano con il codice attuale, fai una stima delle ottimizzazioni applicabili potenzialmente al nostro codice in termini di righe di codice risparmiato e cerca di ottimizzare il piu possibile il codice per avvicinarti il piu possibile alla stima di risparmio iniziale (senza trucchetti o workaround o forme inline o compatte python solo per accorciare, intendo ottimizzazioni funzionali, logiche)
## 3. Matrice dei Punti Aperti con Salvatore (Meeting Prep)

| # | Argomento | Domanda Chiave / Opzioni | Impatto su Codice |
|---|---|---|---|
| **1** | **Strategia MVP Base** | Partiamo con *Value + Trend Following* o *Mean Reversion* come prima strategia codificata? | Seleziona i primi indicatori da inserire nel Quantitative Engine. |
| **2** | **Ruolo Risk Analyst** | Il Risk Analyst deve operare come desk analitico preliminare o come gatekeeper deterministico di blocco finale prima dell'ordine? | Struttura del grafo LangGraph e routing dell'edge verso Execution. |
| **3** | **Confine Market vs Sentiment** | Il Market Analyst gestisce solo macro/tassi/settori e il Sentiment solo news/social/mood, o ci sono sovrapposizioni? | Definizione degli schemi di output dei singoli nodi analisti. |
| **4** | **Criteri `next_check_date`** | Quali parametri guidano il PM nel fissare la revisione (volatilità, giorni ad earnings, time-horizon della strategia)? | Algoritmo di calcolo della data di trigger nel PM node. |
| **5** | **Indicatori Tecnici Chiave** | Quali timeframes e parametri standard usiamo per SMA, RSI, ATR e Bande di Bollinger? | Parametrizzazione predefinita nel modulo `quant/indicators.py`. |

---

## 4. Skill Collegate alla Realizzazione del Piano

* **`software-development/test-driven-development`**: Esecuzione ciclo TDD per ogni modulo (dati, quant, execution).
* **`software-development/codebase-design`**: Strutturazione delle interfacce profonde dei moduli.
* **`software-development/to-spec` & `software-development/to-tickets`**: Suddivisione dei milestone in ticket atomici implementabili.
* **`research/competitor-news-monitor` & `research/arxiv`**: Monitoraggio continuo di aggiornamenti su OpenAlice, Kronos e paper finanziari.
* **`note-taking/obsidian` & `aside/obsidian-markdown`**: Manutenzione sincronizzata della wiki e della Project Board ad ogni avanzamento.
* tutte le skill di mattpocock