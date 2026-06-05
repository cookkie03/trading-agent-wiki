# Hot Cache — Trading Agent

> Contesto di sessione recente. Aggiornare a fine sessione. Tenere entro 300 righe.

## Sessione Corrente
- **Data**: 2026-06-06
- **Agent**: Claude Code (Opus 4.8)
- **Operazione principale**: **passaggio al CODICE.** Design chiuso; primo codice "nostro" sul fork = **strato dati** ([[system/modules/data-layer]] · pacchetto `tradingagents/storage/`). Catena di design alle spalle: tool → comportamento → system prompt → topologia → gap analysis.

### CODICE 2026-06-06 — sessione autonoma a branch (storage + dominio + trade)
- **Mandato**: autonomia piena — branch + test + commit io, PR le valuta Luca.
- **3 branch nel fork** (`/Users/luca/Desktop/trading-agent`, base `my-main`):
  1. `feat/storage-layer` — `tradingagents/storage/` (4 aree + scheda ticker + research_states JSON; SQLite→Timescale; +`sqlalchemy` pyproject, `TRADINGAGENTS_DATABASE_URL` env). 7 test.
  2. `feat/domain-model` — `tradingagents/domain/`: enums (Direction 5-livelli), state Pydantic (gate completezza + `seal()` Opzione C), risk engine (ATR levels, R:R, sizing risk-based + heat/cap, guardrail Statuto). 15 test.
  3. `feat/trade-execution` (merge 1+2) — `tradingagents/execution/trade.py`: Trade deterministico, `client_order_id` idempotente, `inject_portfolio_state`, `propose_and_record`. 5 test.
- **Test**: `uv run pytest` → **27/27 verdi** sul branch d'integrazione. (pytest sta in `uv run`, non nel `.venv`.)
- **Committato** (sì, stavolta) sui 3 branch; `my-main` intatto. PR le decide Luca.
- **Divisione lavoro**: Luca = grafo (M1); Claude = dati/dominio/esecuzione deterministica (M2-M3).
- **Metodo**: contratti congelati (storage/domain) + test-oracolo + slice verticali; il parallelo-agenti va dietro contratti congelati.
- **4° branch** `feat/data-ingestion` (da `feat/storage-layer`, commit d2a6783) — `tradingagents/ingestion/`: `ingest_price_bars` DB-first (check-presenza + write-through, `YFinanceFetcher`) + `screen_ticker` deterministico → `ticker_card.screening_score`. 5 unit + 1 integration yfinance.
- **5° branch** `feat/indicators` (integra TUTTO, commit 9a0fda4) — `tradingagents/indicators/` (ATR/RSI/SMA/EMA/52w/drawdown + `atr_from_db`) + **test E2E** ingest→ATR→livelli→sizing→trade (no LLM).
- **6° branch** `feat/broker-adapter` (da `feat/trade-execution`, commit 14e2dc6) — `tradingagents/broker/` (`Broker` protocol + `PaperBroker` idempotente + `AlpacaBroker` paper REST) + `execution/submit.py` (`submit_trade`/`execute_thesis`/`reconcile_open_trades` = graceful recovery). 5 unit + 1 integration Alpaca.
- **Stato test totale**: storage 7 · domain 15 · trade 5 · ingestion 5 · indicators 7 · E2E 1 · broker 5 = **45 verdi** (+2 integration: yfinance, Alpaca-gated).
- **Catena deterministica completa**: yfinance → `price_bars` → indicatori/ATR → `atr_levels` → `position_size` → Trade → **broker (paper) → reconcile**. Manca solo il "cervello" LLM in mezzo (= grafo, lato Luca) che riempie view/direction dello state.
- **7° branch** `feat/alpha-core` (commit e4466a9) = **unione di TUTTO** (merge `feat/indicators` + `feat/broker-adapter`) + `tradingagents/orchestration/` (cycle runner). È la linea completa e runnabile.
  - `triggers.py` = Trigger Engine (`collect_triggers`: checkpoint + screening, dedup/priorità → coda unica).
  - `analyze.py` = `Analyzer` hook (**qui si innesta il grafo di Luca**) + `hold_analyzer` stub.
  - `cycle.py` = `run_cycle` (trigger→analyze→**cost gate**→execute, ritorna `CycleReport`).
  - cost: `broker/commission.py` + `execution/costs.py` (`assess_costs` net-EV) nel gate.
- **Stato test totale**: **283 verdi** (incl. ~239 del fork) su `feat/alpha-core`. (+2 integration: yfinance, Alpaca-gated.)
- **7 branch**, `my-main` intatto. `feat/alpha-core` = capolinea: catena completa **trigger → screening → [analyze=grafo] → cost gate → trade → broker → reconcile**. Manca solo il grafo reale al posto di `hold_analyzer`.
- **Prossimi pezzi**: il grafo LLM (lato Luca) che implementa `Analyzer`; mappare `agents/schemas.py` del fork → `ResearchState`; consuntivo costi post-fill + token metering; price-alert/calendario nel Trigger Engine; IBKR adapter; vendor news/fondamentali/macro→DB; queue persistente + scheduler.

### Design 2026-06-06 — Trigger Engine + Cost accounting (input Luca, aperti)
- **Trigger Engine centralizzato** → [[system/trigger-engine]]: un componente unico raccoglie alert·`next_check_date`·calendario·periodical synthesis·news, normalizza in `TriggerEvent`, immette nella **coda D del funnel**. "Perché si sveglia" (engine) vs "come decide" (funnel). Da implementare nel cycle runner.
- **Cost accounting a runtime** → [[system/cost-accounting]]: commissioni broker + token cost in 3 momenti — stima pre-trade (guardrail **net-EV / R:R-after-cost** → no-trade se i costi non sono coperti) · consuntivo post-fill (campi su `trade`) · net performance al learning loop. `CommissionModel` nell'adapter broker; token meter nel wrapper LLM. Aperto.

### Design 2026-06-06 — gap analysis fork TradingAgents ↔ design (ponte al codice)
- **Fork** in `/Users/luca/Desktop/trading-agent` (`cookkie03/trading-agent`, vivo, produce report). **Copre gran parte del design**: 4 analisti, PM, grafo LangGraph, tool (incl. reddit/stocktwits), structured output, multi-provider, quick/deep think, checkpoint, output_language=English, past_context.
- **Creata** [[system/fork-gap-analysis]]: TENGO/ELIMINO/AGGIUNGO + roadmap **M0→M6** (M0 wiring OpenRouter+DeepSeek+run as-is · M1 grafo nostro · M2 DB · M3 rischio+trade deterministico · M4 esecuzione broker · M5 funnel · M6 leva/learning).
- **ELIMINO**: bull/bear + research_manager, risk debate 3→1, LLM trader→Python, 4 analisti→2 desk. **AGGIUNGO**: DB centrale, esecuzione broker, sizing/ATR/Statuto, funnel multi-ticker, OpenRouter+DeepSeek. **Differenza chiave**: PM fork=giudice finale → nostro=orchestratore in cima (riscrivere `graph/setup.py`).
- **graphify**: `graphify-out/` già nel fork (2026-05-26), conferma la mappa; ri-girare dopo modifiche.
- **Punto aperto**: ordine **M1 vs M2** (grafo-prima vs DB-prima) — proposta M1 prima, da confermare.
- **Dir di lavoro codice**: `/Users/luca/Desktop/trading-agent` (aggiunta come working dir).

### Design 2026-06-06 — topologia parallelismo multi-ticker (architettura a imbuto)
- **Decisione**: alternative A–E **composte** in un **funnel** → **E** screening deterministico (modulo Python/quant, **non LLM**) → **D** coda di priorità → **A** deep-dive subgraph per-ticker (i 6 agenti) → **B/C** scheda ticker nel DB. Subgraph vs nodi già deciso (subgraph). → [[system/parallelism-design]].
- **Screening** (6 domande di Luca): non-agente · usa info passate (segnali quant + feedback) · aggiornato da extractor+mantainer · 2 popolazioni (portafoglio sempre + universo per origination) · cadenza periodical-synthesis + on-trigger · scrive `screening_score` nella **scheda ticker del DB**, NON sullo state classico.
- **MVP**: prima **D+A**, poi E e B/C senza rework. Restano da tarare numeri/soglie (soglia screening, K, cadenze, segnali dello score).
- **Bivio design/codice**: topologia = ultima vera decisione architetturale. Restano: **schema DB concreto** (= ponte al codice) + criteri info-sufficienti/anti-loop. Il resto = implementazione o Salvatore.

### Design 2026-06-06 — system prompt degli agenti
- **Creata** [[system/system-prompts]]: metodo prompt-eng (principio separazione comportamento/forma/tool + 7 principi) + **scheletro a 7 blocchi** + **tutti e 6 i system prompt scritti per intero** (Technical · Market · Sentiment · Fondamentali · **PM** orchestratore · **Risk** gate bear), in inglese. **IMPIANTO APPROVATO.**
- **Scelte di Luca**: prompt **in inglese** (doc resta IT).
- **Resta**: consolidamento nel **Prompt Builder** (assemblaggio prompt + contesto XML + schema strict) + rifinitura iterativa LangSmith.

### Design 2026-06-06 — comportamento per-agente del desk
- **Creata** [[system/agent-behaviors]]: per i 4 agenti (Market · Sentiment · Technical · Fondamentali) **5 dimensioni** (input · tool · output nello state · ragionamento · stop). **IMPIANTO APPROVATO.**
- **Scelte di Luca**: (1) news/sentiment **per tipo di informazione** — Market=catalizzatori, Sentiment=mood da **più fonti** (social/Reddit/StockTwits/X + news-sentiment); (2) **tutti contribuiscono alla direzione** (contributo primario per specialità, ma libertà su tutto); (3) **stop = auto-stop + PM può richiamare**.
- **Sotto-lavoro aperto**: enumerare le **fonti/tool di sentiment** (famiglia D di [[system/tools-inventory]] già aggiornata con split `get_news`/`get_news_sentiment`/`get_social_sentiment`) — si interseca con "indicatori di sentiment" (Salvatore).
- **Prossimo passo**: scrivere i **system prompt** che realizzano questi comportamenti (Prompt Builder) → [[system/modules/agents]].

### Design 2026-06-06 — inventario tool degli agenti
- **Creata** [[system/tools-inventory]]: **9 famiglie** di tool (A prezzi · B indicatori · C fondamentali · D news/sentiment · E macro · F calendario · G portafoglio · H opzioni · I guardrail=non-tool), ognuna con 5 etichette (cosa · live/storico · write-through · agente · vendor). 2 regole trasversali: **parametrici mai hardcoded** + dato live torna all'agente *e* copia nel DB. **IMPIANTO APPROVATO da Luca.**
- **Scelte di Luca**: `inject_portfolio_state` = **auto a ogni ciclo + richiamabile**; indicatori = **un tool parametrico** `compute_indicator`; vendor live MVP = **decidiamo dopo** (candidato Finnhub).
- **Resta aperto**: solo i **vendor** (live MVP + opzioni), a implementazione del data-layer → [[system/tools-inventory]] · decision-log (open row "Tool agenti: vendor").
- **Prossimo passo naturale**: **comportamento per-agente** (quali tool usa ogni desk Market/Sentiment/Technical/Fondamentali, in che ordine, criterio di stop) → [[system/modules/agents]].

### Design 2026-06-05 — position sizing + autonomia informativa + tool
- **Position sizing** (passo n°2): modello **risk-based** in [[system/position-sizing]] — budget di rischio % scalato per conviction → quantità da `stop_distance = k_stop × ATR` + **portfolio heat**. Volatility-adjustment *gratis*. **IMPIANTO APPROVATO da Luca**; restano solo i numeri (1% risk, heat 5–6%, cap 10%) da tarare in backtest.
- **Opzione C (state annidati) CONFERMATA** da Luca dopo spiegazione a voce (piatto a runtime → annidato al sealing; sealing = una funzione). Da validare in fase di grafo. → [[system/state-schemas]].
- **Idea sul piatto**: **intervento agenti sul sizing** (da valutare rischi/benefici; via di mezzo = fattore ±X% clampato) → [[system/position-sizing]] · [[system/ideas-log]].
- **Autonomia informativa real-time first + write-through** (DECISO, input Luca): agenti chiamano info aggiornate in autonomia, anche più volte; **prima il tool real-time**, che consegna all'agente + **copia nel DB** (centro unico). DB-first = solo per storico/immutabile. → [[system/modules/agents]] · [[system/modules/data-layer]].
- **Selezione tool da costruire** (input Luca): aggiunto come cosa a cui pensare → TODO [[system/modules/agents]] + board.
- **Opzione C** rispiegata a voce a Luca (non la ricordava) — vedi chat; flag in "Da fare" risolto.

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
- ✅ **Opzione C rispiegata a voce** (2026-06-05) — Luca non la ricordava; spiegata in chat (brutta→raccoglitore, sealing = una funzione). Resta solo da *validare in fase di grafo*.
- 🔵 **Reazione di Luca al modello risk-based di position sizing** → [[system/position-sizing]] (proposto, in attesa).
- ✅ Schema dello state **completato a livello di design** (entry_price, conviction enum, aggregazione PM, storage JSON, state annidati→C da validare, validazione collettiva opzione).
- ✅ **Selezione dei tool da costruire per gli agenti** (2026-06-06) — impianto approvato, inventario in [[system/tools-inventory]]; restano solo i vendor.
- ✅ **Comportamento per-agente del desk** (2026-06-06) — impianto approvato → [[system/agent-behaviors]]. Resta: scrivere i system prompt + enumerare le fonti di sentiment.
- ✅ **Tutti e 6 i system prompt + metodo** (2026-06-06) — 4 desk + PM + Risk, in inglese → [[system/system-prompts]].
- 🔵 **Consolidare il Prompt Builder** (assemblaggio prompt + contesto XML + schema strict) + rifinitura iterativa LangSmith → [[system/system-prompts]] · [[system/modules/agents]].
- Verificare in Obsidian che la graph view non abbia orfani inattesi
- Creare pagine metriche (`sharpe-ratio`, `max-drawdown`, `win-rate`) in `strategy/metrics/` solo quando servono
