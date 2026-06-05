# Hot Cache — Trading Agent

> Contesto di sessione recente. Aggiornare a fine sessione. Tenere entro 300 righe.

## Sessione Corrente
- **Data**: 2026-06-05
- **Agent**: Claude Code (Sonnet 4.6)
- **Operazione principale**: **Ingest conversazione Luca↔Salvatore 2026-06-04 sera** (15 audio WhatsApp + chat export + doc indicatori macro).

### Ingest 2026-06-05
- **Creata**: [[strategy/indicators/macro-indicators]] — 12 categorie indicatori macro (PIL completo, Consumi iniziato, Salvatore continua)
- **Chiarito**: backtesting = deterministico Python su DB storico, NON simulazione AI (equivoco risolto) → [[system/modules/quant-backtesting]]
- **Nuove decisioni**: no capitale prima della prova · feedback esterni solo a sistema finito
- **Nuove idee**: copy trading eToro Pro Investor (1.5% AUC/mese) + ZuluTrade · pipeline collaboratori (Diego Zappa primo, poi Trezzi + traders SIM)
- **Archiviati**: 15 .txt trascrizioni audio → `raw/archived/audio/`
- **NON mosso**: `Indicatori per Analisi Macroeconomica.md` (file di lavoro Salvatore al vault root)

### Sessione 2026-06-04
- **Operazione principale**: **Step 1 — design `entry_price`** + **commenti di Luca** + **cross-link glossario**. Sessione condotta da Claude (Luca preferiva reagire).
  - **`entry_price`**: ✅ **APPROVATO da Luca 2026-06-04** — backbone **ATR** (entry/stop/tp = `current_price ± k·ATR`, l'LLM dà i coefficienti `k_*`, Python traduce), `k_entry` **scalato per conviction**, **guardrail R:R** (default 1.5), limit non colpito → scade alla `next_check_date`. Numeri (ATR 14, k_stop=2, k_tp=3, soglia 1.5) da tarare in backtest. Decisione chiusa in [[system/decision-log]].
  - **Decisioni chiuse 2026-06-04**: autonomia totale (nessun input umano oltre l'accensione) · PM attivato anche dal `next_check_date` · backtesting = validatore continuo/asincrono delle soglie · **conviction = enum** (non 0-100).
  - **Nuovo**: [[system/investment-state-template]] (menu completo per Salvatore) · disinvestimento come batch di trade del PM · tool iniezione portafoglio · comportamento per-agente (aperto) · legenda colori canvas in [[_meta/taxonomy]].
  - **Glossario cross-linkato**: 145 link su 27 pagine (script `tmp/glosslink.py`, prima occorrenza, no tabelle). Aggiunti **ATR** e **Risk/Reward** al glossario. Spiegato leva-via-opzioni vs margine.
  - **Decisioni chiuse (seconda tornata 2026-06-04)**: `entry_price` **APPROVATO**; **aggregazione** `direction`/`conviction` = ogni desk propone, **PM aggrega e decide** (campo `agent_opinions`); **forma storage** = orientamento JSON/JSONB in colonna (no secondo DB).
  - **Pesi degli agenti** = output del **backtesting validatore** (hit-rate per-agente) ma **indicazione, non regola**: contesto/awareness in input al PM, non automatismo (scioglie tensione con "conviction dal PM") + funzione diagnostica "cosa migliorare di agenti e tool" → [[system/learning-feedback-loop]] §4.
  - **State annidati**: **orientamento C (ibrido)** scelto da Luca, *da validare al massimo* in fase di grafo (rework minimo via funzione di sealing) → [[system/state-schemas]]. Lo schema dello state è di fatto **chiuso a livello di design** (restano solo numeri da tarare in backtest e validazione di C).
  - **Istruzione PM "nel dubbio chiedi sempre"** (Luca): il PM decisore deve sempre interrogare di nuovo i desk a ogni incertezza, anche piccola, prima di decidere; no-trade preferibile a basi incerte. Tetti anti-loop = rete di sicurezza. → [[system/parallelism-design]] · [[system/modules/agents]] · card system-prompt in board.
  - **Validazione collettiva investment_state** (opzione, Luca): tutti gli agenti validano completezza·correttezza·esaustività fonti prima del sealing (`send_back` su lacuna) → [[system/state-schemas]] · [[system/modules/execution]].
  - **Graceful shutdown & recovery** (domanda Luca, che non conosce i DB → spiegazione dal basso): **DECISO** design in [[system/modules/data-layer]] — al boot routine di init = **riconciliazione col broker** (broker=verità) + controllo **intent log** (ordini `pending` verificati via **client order id** anti-doppione); policy: analisi a metà → scarta e ricomincia, ordine a metà → riconciliazione; **atomicità** copre crash a metà-scrittura; disallineamento DB↔broker → **allinea da solo + logga, no intervento umano** (autonomia totale). Checkpoint LangGraph = ottimizzazione futura. Aggiunte al glossario: Transazione/Atomicità, Riconciliazione, Idempotenza. Chiusa in [[system/decision-log]] + board ✅; resta da *implementare*.
  - **DB — accesso/performance** (domanda Luca): creata [[system/db-access-performance]] — quando/da chi è interrogato (read/write per attore), tecniche read/write (batch/COPY, pooling, BRIN, GIN su JSONB, materialized view), **minimizzazione query** (check-presenza, snapshot di ciclo in memoria, periodical synthesis, read-through cache), **DECISO** (Luca 2026-06-04): motore = **PostgreSQL + TimescaleDB** (hypertable + relazionale + JSONB); **cache = in-process** per l'MVP, **Redis idea futura** (solo se multi-processo). Chiuse in [[system/decision-log]] + board ✅.

### Sessione 2026-06-03
- **Operazione**: **Review pre-sviluppo + risposta alle lacune**. Luca ha risposto a un'analisi delle cose ancora da decidere/capire. Create **5 nuove pagine** (`system/state-schemas`, `system/position-sizing`, `system/rating-scoring`, `system/parallelism-design`, `strategy/questions-for-salvatore`); aggiornati decision-log, data-layer, execution, agents, quant-backtesting, stack, glossario, ideas-log, index. **Board ridisegnata come centrale operativa** (owner + riferimento pagina su ogni card). Nuova sezione in **CLAUDE.md** che formalizza la board come hub + convenzione owner/riferimenti.
- **Prossimi due passi concordati**: 1) strutturare lo schema dello state ([[system/state-schemas]]); 2) definire la formula di position sizing ([[system/position-sizing]]).
- **Luca ha rivisto e commentato l'intera analisi delle lacune** (tutti i punti B + C). Input aggiuntivi 2026-06-03: **subgraph come pattern granulare** per collegare parti diverse del sistema ([[system/parallelism-design]]); **disinvestimento a 2 livelli** (automatico via TP/trailing stop + valutato rating-based) ([[system/rating-scoring]], [[system/modules/execution]]).
- **Recuperate e unificate le idee iniziali sparse** ("agent di reportistica su cosa va male" + "ponderazione pesi degli agent del desk") → nuova pagina **[[system/learning-feedback-loop]]** (substrato logging · reportistica diagnostica · scoring agenti · ponderazione pesi · feedback post-trade). Decisione Luca: **reportistica = modulo deterministico + narrazione** (opzione, non agente dedicato). Aperto: punto di aggancio dei pesi (tensione con "conviction dal PM"); substrato di logging tesi-per-agente↔esito da predisporre **da subito**.

### Sessione precedente (2026-05-29)
- **Refactor strutturale completo del wiki**: `build/`→`system/`, `references/` eliminata, moduli ricreati su `architettura.canvas` (`data-layer`/`agents`/`execution`/`quant-backtesting`). Decisioni: dissolvi le call (date inline); naming inglese; PM = agente LLM orchestratore.

## Stato attuale del progetto
- Fase: **Design → sviluppo in preparazione**
- **Architettura**: monolite modulare, principio deterministico (Statuto rigido Python upstream)
- **Prototipo**: paper trading autonomo su exchange equity (da scegliere) + backtesting continuativo
- **Orizzonte trade**: swing trading (4h/daily / checkpoint AI flessibili)
- **Scope**: **Stock-only** (equity pura) — poi multi-asset: commodities, BTC only, derivati futures/opzioni
- **Framework**: LangChain + LangGraph (fork da TradingAgents TauricResearch)
- **Debug/Evaluation**: LangSmith + LangSmith CLI
- **LLM**: OpenRouter + DeepSeek V4 Pro, output JSON obbligatorio
- **Backtesting**: VectorBT (decisione chiusa)

## Struttura wiki (post-refactor 2026-05-29)
```
wiki/
├── _meta/          ← navigazione (index, log, hot-cache, taxonomy, glossario, onboarding)
├── overview.md     ← entry point
├── system/         ← spec software (dominio Luca)
│   ├── architecture.md · mvp.md · stack.md · data-providers.md
│   ├── decision-log.md · ideas-log.md
│   └── modules/    ← data-layer · agents · execution · quant-backtesting
├── strategy/       ← conoscenza di mercato (dominio Salvatore)
│   ├── index.md
│   ├── methods/    ← trend-following · factor-investing · mean-reversion-stat-arb · dual-portfolio
│   ├── indicators/ ← da popolare
│   └── metrics/    ← benchmark
├── prior-art/      ← esterni studiati/forkati
│   ├── tradingagents/ ← paper · code-wiki · graph-schema
│   ├── libraries/  ← cvx-portfolio-optimizer · rizzo-trading-agent · sfc-portfolio-tracker
│   └── papers/     ← alpha-arena · brenndoerfer-quant-trading · notion-trading-concepts
├── syntheses/      ← analisi trasversali
└── artifacts/      ← architettura.canvas (corrente) + architecture/ (canvas) + project-board
```

## Moduli (allineati ad `architettura.canvas`)
- **data-layer** — DB centrale (4 aree: rendicontazione, dati live, costituzione, log) + Extraction (extractors set, adaptive extractor, market alert, calendar tool, **mantainer**)
- **agents** — PM orchestratore + Analyst Research (Market+Sentiment) + Analyst Technical (Technical+Fondamentali) + Risk Analyst (bear + Statuto + guardrail + token cost + leva opzioni)
- **execution** — Investment State (gate completezza) → Trade (Python deterministico) → Exchange (paper) → transactions
- **quant-backtesting** — strategia quant + VectorBT (offline, non nel canvas)

## Decisioni chiuse importanti (recenti)
- **Broker intercambiabili via adapter** — Alpaca MVP → IBKR prod (2026-06-02)
- **Storage principalmente time-series + oggetti** (2026-06-02)
- **Extractor DB-first con queue + check presenza** (2026-06-02)
- **Transaction cost auto-adattivo** (no hardcoded) (2026-06-02)
- **Conviction level assegnato dal PM** (2026-06-02)
- **`mantainer` = technical → rendicontazione** (confermato 2026-06-02)
- **Deploy su mini-server di casa 24/7 + .env locale** (2026-06-02)
- **Approccio incrementale (alpha-first)** (2026-06-02)
- **Portfolio / mid-term confermato, NO day trading** (2026-05-29)
- **OpenRouter + DeepSeek V4 Pro** come provider/modello principale (2026-05-29)
- **Trader = funzione Python deterministica (NON agent)** (2026-05-29)
- **PM = agente LLM orchestratore** (umano solo override iniziale) (2026-05-29)
- **2 desk analisti**: Analyst Research + Analyst Technical (chiude "2 vs 4") (2026-05-29, da canvas)
- **Head of Analyst eliminato; Risk Analyst = gate bear unico** (2026-05-29)
- **Guardrail deterministici da Statuto-schema** (2026-05-29)
- **Avvio con portafoglio già investito** + universo investibile come lista (2026-05-29)
- **Benchmark: S&P 500 + 60/40 all-world** (2026-05-29)
- **Investment State come gate di completezza pre-trade** (2026-05-29)
- **Riscrivere il grafo tenendo base TradingAgents** (2026-05-29)
- **Statuto & 10% cash · Leva via Opzioni · Token cost = commissioni · Business Model Piero** (2026-05-27)

## Decisioni ancora aperte (priorità)
> Lista completa e navigabile in [[artifacts/project-board]] (sezione 🟠) e [[system/decision-log]].
- **Schema state** + **formula position sizing** (i due prossimi passi)
- **`entry_price` limit order** · **parallelismo multi-ticker** · **criteri info-sufficienti**
- **VaR / overfitting / test benchmark / rating asset / opzioni** → [[strategy/questions-for-salvatore]]
- **Indicatori di sentiment**: da inventare — con Salvatore
- **Desk di monitoring/evaluation**: design dell'agente che sorveglia le posizioni
- **Strategia del fondo**: da formalizzare con Salvatore (multi-factor)
- **Frequenza ciclo**: 4h vs 24h (dipende da backtest)
- **Regole specifiche dello Statuto** + **algoritmo di disinvestimento ottimale** (in corso)
- **Dynamic Temporal Checkpoints**: feedback loop temporale gestito dall'AI

## Pending ingest
- **Indicatori per Analisi Macroeconomica.md** (vault root) — **parziale**: PIL completo, Consumi appena iniziato; Salvatore sta completando le sezioni 2-12. Quando finito → aggiornare [[strategy/indicators/macro-indicators]]
- **Documento indicatori di valuation** (Salvatore) — atteso, poi TXT + ingest (ognuno dell'associazione cura un indicatore stock)
- `raw/articles/AlphaArena/` + `optimizer/` + `TradingAgents*` — in raw per consultazione (pagine prior-art già esistenti)
- `raw/daily-notes/model.md` = template vuoto (resta)

## Da fare prossima sessione
- ⚠️ **Rispiegare a voce a Luca la "validazione dell'opzione C / sealing"** dello state — non gli era chiaro; in [[system/state-schemas]] c'è già un callout *"in parole semplici"* (analogia brutta→raccoglitore) da cui partire.
- ✅ Schema dello state **completato a livello di design** (entry_price, conviction enum, aggregazione PM, storage JSON, state annidati→C da validare, validazione collettiva opzione).
- Passo concordato n°2: **formula di position sizing** → [[system/position-sizing]]
- Verificare in Obsidian che la graph view non abbia orfani inattesi
- Creare pagine metriche (`sharpe-ratio`, `max-drawdown`, `win-rate`) in `strategy/metrics/` solo quando servono
