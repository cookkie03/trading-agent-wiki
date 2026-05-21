# Hot Cache — Trading Agent

> Contesto di sessione recente. Aggiornare a fine sessione. Tenere entro 300 righe.

## Sessione Corrente
- **Data**: 2026-05-22
- **Agent**: Claude Code
- **Operazione principale**: Ingest batch pending — Tool Set/Provider dati, note quant Salvatore (dual portfolio + mean reversion), articolo Brenndoerfer, update videochiamata-05-13 con contenuto extra audio

## Stato attuale del progetto
- Fase: **Design → sviluppo Modulo A inizia ora**
- **Architettura**: monolite modulare, principio deterministico
- **Prototipo**: paper trading autonomo su Binance Testnet + backtesting continuativo
- **Orizzonte trade**: swing trading (4h/daily)
- **Sequenza sviluppo**:
  - Track 1 (Luca solo): **Modulo A** — Exchange + DB → [[build/modules/module-a-exchange-db]]
  - Track 2 (Luca + Salvatore): **Modulo C** — Quant + Backtesting → [[build/modules/module-c-quant-backtest]]
  - Track 3 (dopo A): **Modulo D** — Prompt Builder + LLM Trader → [[build/modules/module-d-prompt-builder-trader]]
- **LLM**: DeepSeek, output JSON obbligatorio
- **Backtesting**: VectorBT (decisione chiusa)
- **Risk Analyst**: upstream del Trader (imposta paletti prima della decisione)

## Struttura wiki post-ristrutturazione
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
│   └── modules/    ← module-a, module-c, module-d, risk-analyst
├── strategy/       ← conoscenza di mercato (dominio Salvatore)
│   ├── index.md
│   ├── methods/    ← trend-following, factor-investing...
│   ├── indicators/ ← RSI, MACD, Pivot Points... (da popolare)
│   └── metrics/    ← Sharpe, Drawdown... (da popolare)
├── references/     ← fonti ingestite
│   └── external/   ← paper e librerie terze (paper-trading-agents, paper-alpha-arena, cvx-portfolio-optimizer)
├── syntheses/      ← analisi trasversali
└── artifacts/      ← canvas + board Luca + board Salvatore
```

## Decisioni ancora aperte (priorità)
- **Strategia del fondo**: da formalizzare con Salvatore (orientamento: multi-factor)
- **Frequenza ciclo**: 4h vs 24h (dipende da backtest)
- **Statuto del fondo**: regole hard limits (cash-out %, max esposizione, ecc.)

## Pending ingest
- `raw/audio/2026-05-13 13-14-17.m4a` — già ingestato via trascrizione txt, .m4a lasciato in raw
- `raw/articles/TradingAgents Code Wiki.md` — source page creata; lasciato in raw per consultazione (file molto lungo)
- `raw/articles/TradingAgents.md` / `.pdf` — già ingestato come `references/external/paper-trading-agents`; da archiviare se non serve più
- Tutto il resto: archiviato in `raw/archived/`

## Pagine create questa sessione
- [[references/tool-set-provider-dati-exchange]] — broker + provider dati per l'Italia
- [[references/note-audio-salvatore-quant-strategy]] — dual portfolio + mean reversion (note Salvatore)
- [[references/quantitative-trading-strategies-brenndoerfer]] — articolo tecnico quant trading completo
- [[strategy/methods/mean-reversion-stat-arb]] — strategia candidata per Modulo C

## Pagine aggiornate questa sessione
- [[references/videochiamata-luca-salvatore-2026-05-13]] — aggiunte sez. 8-11 (struttura agenti verbale, order book, fork vs from scratch)

## Pagine chiave da aggiornare prossima sessione
- [[artifacts/luca-board]] — aggiungere task esplicito "Implementa Modulo A" + "Studia LangGraph" + "Decidi fork vs from scratch"
- [[artifacts/salvatore-board]] — aggiungere domande per Salvatore (indicatori, analisi tecnica, workflow investitore)
- [[build/decision-log]] — formalizzare decisione fork vs from scratch con Salvatore
- [[strategy/methods/mean-reversion-stat-arb]] — da completare quando Salvatore finisce di leggere l'articolo trovato

## Decisioni ancora aperte (carry-over)
- **Fork vs from scratch**: Luca propende per fork da TradingAgents. Da discutere e formalizzare con Salvatore
- **Self-scheduling vs cron**: aperta
- **Debate architecture**: mantenerla o ridisegnare? Da investigare prima di Modulo D
- **Strategia Modulo C**: mean reversion è candidata principale (Salvatore) — da decidere con Luca
- **Dual portfolio value+quant**: idea embrionale di Salvatore, da discutere in sessione dedicata
