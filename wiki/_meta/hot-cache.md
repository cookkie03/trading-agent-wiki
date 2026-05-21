# Hot Cache — Trading Agent

> Contesto di sessione recente. Aggiornare a fine sessione. Tenere entro 300 righe.

## Sessione Corrente
- **Data**: 2026-05-21
- **Agent**: Claude Code
- **Operazione principale**: Ingest TradingAgents Code Wiki + note di lettura Luca (daily note 2026-05-19)

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
│   └── modules/    ← module-a, module-c, module-d, risk-analyst
├── strategy/       ← conoscenza di mercato (dominio Salvatore)
│   ├── index.md
│   ├── methods/    ← trend-following, factor-investing...
│   ├── indicators/ ← RSI, MACD, Pivot Points... (da popolare)
│   └── metrics/    ← Sharpe, Drawdown... (da popolare)
├── references/     ← fonti ingestite
│   └── external/   ← framework/librerie terze
├── syntheses/      ← analisi trasversali
└── artifacts/      ← canvas + board Luca + board Salvatore
```

## Decisioni ancora aperte (priorità)
- **Strategia del fondo**: da formalizzare con Salvatore (orientamento: multi-factor)
- **Frequenza ciclo**: 4h vs 24h (dipende da backtest)
- **Statuto del fondo**: regole hard limits (cash-out %, max esposizione, ecc.)

## Pending ingest
- `raw/notes/sessione-brainstorming-2026-05-13.md` — ingest formale ancora pendente
- `raw/articles/quant strategy/*.txt` — note audio di Salvatore su strategie quant, da ingestare
- `raw/audio/2026-05-13 13-14-17.m4a` — ingestato via trascrizione txt
- `raw/articles/TradingAgents Code Wiki.md` — source page creata; il file raw non è stato archiviato (contenuto molto lungo, lasciato in raw per consultazione)

## Pagine chiave da aggiornare prossima sessione
- [[artifacts/luca-board]] — aggiungere task esplicito "Implementa Modulo A" + "Studia LangGraph" + "Decidi fork vs from scratch"
- [[artifacts/salvatore-board]] — aggiungere domande per Salvatore (indicatori di performance, analisi tecnica, workflow investitore istituzionale)
- [[build/decision-log]] — formalizzare decisione fork vs from scratch con Salvatore

## Decisioni emerse questa sessione (da discutere)
- **Fork vs from scratch**: Luca dopo lettura Code Wiki propende per fork da TradingAgents. Da discutere con Salvatore e formalizzare
- **Self-scheduling vs cron**: decisione ancora aperta su come schedulare i cicli di analisi
- **Debate architecture**: mantenerla efficientata o ridisegnare? Da investigare prima di implementare Modulo D
