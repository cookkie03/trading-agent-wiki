# Hot Cache — Trading Agent

> Contesto di sessione recente. Aggiornare a fine sessione. Tenere entro 300 righe.

## Sessione Corrente
- **Data**: 2026-05-29
- **Agent**: Claude Code (Opus)
- **Operazione principale**: **Lint + ristrutturazione** della wiki per allinearla alle call del 29/05 (segue l'ingest delle due videochiamate fatto in precedenza nella stessa giornata). Riscritta `system-map` sulla topologia 29/05, riconciliato il conflitto Trader in `llm-agent-system`, consolidato lo schema DB in `exchange-db`, ingeriti i 3 file pending (daily-notes 28/29 + transcript 05-13). Cleanup: rimossi 54 frammenti spazzatura in `raw/audio/`, rimossa la stub `artifact-workbench`, fixati link rotti. Canvas riorganizzati da Luca in Obsidian (in parallelo) → tutti sotto `artifacts/`.

## Stato attuale del progetto
- Fase: **Design → sviluppo in preparazione**
- **Architettura**: monolite modulare, principio deterministico (Statuto rigido Python upstream)
- **Prototipo**: paper trading autonomo su exchange equity (da scegliere) + backtesting continuativo
- **Orizzonte trade**: swing trading (4h/daily / checkpoint AI flessibili)
- **Scope**: **Stock-only** (equity pura) — poi multi-asset: commodities, BTC only, derivati futures/opzioni
- **Framework**: LangChain + LangGraph (fork da TradingAgents TauricResearch)
- **Debug/Evaluation**: LangSmith + LangSmith CLI (portale UI per evaluation)
- **LLM**: DeepSeek, output JSON obbligatorio
- **Backtesting**: VectorBT (decisione chiusa)

## Struttura componenti (post-ristrutturazione 2026-05-23)
```
wiki/build/modules/
├── exchange-db.md          ← Exchange + DB (ex Modulo A)
├── quant-backtesting.md    ← Quant Agent + Backtesting (ex Modulo C)
├── llm-agent-system.md     ← LLM Agent System (ex Modulo D)
└── risk-management.md      ← Risk Management (ex Risk Analyst)
```

## Struttura wiki
```
wiki/
├── _meta/          ← navigazione (index, log, hot-cache, taxonomy, glossario)
├── overview.md     ← entry point
├── build/          ← spec software (dominio Luca)
│   ├── system-map.md
│   ├── mvp-prototype-design.md
│   ├── stack.md
│   ├── decision-log.md
│   ├── ideas-log.md  ← log append-only idee di progetto
│   └── modules/    ← exchange-db, quant-backtesting, llm-agent-system, risk-management
├── strategy/       ← conoscenza di mercato (dominio Salvatore)
│   ├── index.md
│   ├── methods/    ← trend-following, factor-investing, mean-reversion-stat-arb
│   ├── indicators/ ← da popolare
│   └── metrics/    ← benchmark (+ stub da creare: sharpe-ratio, max-drawdown, win-rate)
├── references/     ← fonti ingestite
│   └── external/   ← paper e librerie terze
├── syntheses/      ← analisi trasversali
└── artifacts/      ← board + canvas
    └── architecture/ ← canvas di design (agents.canvas = corrente, langchain, idea, trading-floor)
```
> Nota: `wiki/build/architecture/` è stato eliminato; i canvas vivono tutti sotto `artifacts/`.

## Decisioni chiuse importanti (recenti)
- **Portfolio / mid-term confermato, NO day trading** (2026-05-29)
- **OpenRouter + DeepSeek V4 Pro** come provider/modello principale (2026-05-29)
- **Trader = funzione Python deterministica (NON agent)** (2026-05-29)
- **Head of Analyst eliminato; Risk Analyst = gate bear unico** (2026-05-29)
- **Guardrail deterministici da Statuto-schema** (2026-05-29)
- **Avvio con portafoglio già investito** + universo investibile come lista (2026-05-29)
- **Benchmark: S&P 500 + 60/40 all-world**, idea selezione attiva S&P (2026-05-29)
- **Investment State come gate di completezza pre-trade** (2026-05-29)
- **Riscrivere il grafo tenendo base TradingAgents** (2026-05-29)
- **Suddivisione Ricercatori vs Esecutori**, **Statuto & 10% cash**, **Leva via Opzioni**, **Token cost = commissioni**, **Business Model Piero** (2026-05-27)

## Decisioni ancora aperte (priorità)
- **Analisti: 2 o 4 agenti?** (market/sentiment/fondamentale/technical separati o accorpati) — a sviluppo
- **Indicatori di sentiment**: da inventare (non esistono standard) — con Salvatore
- **Desk di monitoring/evaluation**: design dell'agente che sorveglia le posizioni esistenti
- **Strategia del fondo**: da formalizzare con Salvatore (orientamento: multi-factor)
- **Frequenza ciclo**: 4h vs 24h (dipende da backtest)
- **Regole specifiche dello Statuto**: esposizione massima, regole vendita, drawdown limite (in corso)
- **Algoritmo di disinvestimento ottimale**: per recuperare liquidità senza violare il 10% cash (in corso)
- **Dynamic Temporal Checkpoints**: feedback loop temporale gestito dall'AI (in corso)
- **Exchange per paper trading equity**: Alpaca? Interactive Brokers? Da scegliere

## Pending ingest
- **File market driver di Salvatore** (4 macro-categorie) — atteso in `raw/` come TXT, da arricchire e ingestare in `strategy/indicators/`
- **Documento indicatori di valuation** (Salvatore + associazione) — atteso, poi TXT + ingest
- `raw/articles/AlphaArena/` + `raw/articles/optimizer/` + `raw/articles/TradingAgents*` — lasciati in raw per consultazione (source page già esistenti)
- ~~daily-notes 28/29~~ ✅ ingerite; ~~transcript 05-13~~ ✅ archiviata (pagina già completa)
- `raw/daily-notes/model.md` = template vuoto (resta, non si ingerisce)

## Lint + ristrutturazione questa sessione (2026-05-29)
- ✅ [[build/system-map]] — riscritta sulla topologia 29/05 (PM orchestratore → analisti → research_state → Risk Analyst gate → Trade deterministico; Layer DB esteso, Extractors, gate; protocollo state+DB con context rot)
- ✅ [[build/modules/llm-agent-system]] — **conflitto Trader risolto**: Funzione e sezione Leva riallineate (convinzione `Strong` nel research_state, esecuzione deterministica); path canvas → `artifacts/architecture/`; ingerita daily-note 29 (tool indicatori); link rotto framework rimosso
- ✅ [[build/modules/exchange-db]] — **schema DB consolidato** (5 core ↔ 4 aree logiche in un mapping unico); domanda storage SQL/JSON (daily-note 28)
- ✅ [[build/decision-log]] — aggiunta domanda aperta "forma di storage per area"
- ✅ [[_meta/index]] — fixato link rotto `dev-roadmap.canvas`, riorganizzata sezione Canvas, aggiunta orfana `tradingagents-graph-schema`, aggiornate descrizioni moduli
- ✅ [[references/videochiamata-luca-salvatore-2026-05-13]] — link rotti `ops/` fixati, raw_source_path → transcript archiviato
- ✅ [[references/tradingagents-code-wiki]], [[references/tradingagents-graph-schema]] — link rotti canvas fixati
- 🗑️ rimossi: 54 frammenti spazzatura `raw/audio/.txt*.txt`, stub `artifacts/artifact-workbench.md`
- 📦 archiviati: daily-notes 28/29, transcript+mp3 05-13

## Cleanup pass 2 (stessa sessione)
- ✅ [[build/mvp-prototype-design]] — rimosso ciclo operativo vecchio + decisioni fondanti (duplicavano system-map/decision-log); allineato a stock-only + topologia 29/05; mantenuti metriche a due livelli e insight NotebookLM
- 🗑️ rimosso `artifacts/kanban-project-status.md` — fermo al 06/05, `type:ops` (ruolo eliminato), "Blocked: Crypto vs Equity" già deciso, soppiantato da luca-board + salvatore-board. Sistemati i link in index e videochiamata-04-30
- 🔧 risolti tutti i link rotti minori: `[[strategy/]]`→`[[strategy/index]]`, stub metriche in trend-following → testo, puntatore raw in ideas-log → path archiviato
- **Stato link**: 0 link rotti reali nella wiki

## Da fare prossima sessione
- Decidere **forma di storage per area** (SQL/JSON/time-series) + exchange paper trading equity
- Decidere **analisti 2 vs 4** e dove vive l'aggregazione del segnale `Strong`
- Creare pagine metriche (`sharpe-ratio`, `max-drawdown`, `win-rate`) in `strategy/metrics/` solo quando servono davvero
