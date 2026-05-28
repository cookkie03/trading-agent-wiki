# Hot Cache — Trading Agent

> Contesto di sessione recente. Aggiornare a fine sessione. Tenere entro 300 righe.

## Sessione Corrente
- **Data**: 2026-05-27
- **Agent**: Antigravity
- **Operazione principale**: Ingestione conversazione 27/05 (chat e 18 note vocali) + aggiornamento specifiche: suddivisione Ricercatori/Esecutori, Statuto deterministico (10% riserva liquidità), esposizione a leva con opzioni Call/Put, LLM Token Cost Estimator e modello business "Piero".

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
│   └── metrics/    ← da popolare
├── references/     ← fonti ingestite
│   └── external/   ← paper e librerie terze
├── syntheses/      ← analisi trasversali
└── artifacts/      ← canvas + board
```

## Decisioni chiuse importanti (recenti)
- **Suddivisione Ricercatori vs Esecutori** (2026-05-27)
- **Statuto del Fondo & Riserva 10% cash** (2026-05-27)
- **Leva controllata via Opzioni Call/Put** (2026-05-27)
- **API LLM token cost equiparato a commissioni** (2026-05-27)
- **Business Model: Open Source + Friends Performance Fee (Piero site)** (2026-05-27)

## Decisioni ancora aperte (priorità)
- **Strategia del fondo**: da formalizzare con Salvatore (orientamento: multi-factor)
- **Frequenza ciclo**: 4h vs 24h (dipende da backtest)
- **Regole specifiche dello Statuto**: esposizione massima, regole vendita, drawdown limite (in corso)
- **Algoritmo di disinvestimento ottimale**: per recuperare liquidità senza violare il 10% cash (in corso)
- **LLM Token Cost Estimator**: implementazione algoritmo e auto-ricarica (in corso)
- **Dynamic Temporal Checkpoints**: feedback loop temporale gestito dall'AI (in corso)
- **Exchange per paper trading equity**: Alpaca? Interactive Brokers? Da scegliere

## Pending ingest
- `raw/audio/2026-05-13 13-14-17.m4a` — già in lista, richiede `/wiki-preprocess` (trascrizione mancante)
- `raw/articles/TradingAgents Code Wiki.md` — source page creata; lasciato in raw per consultazione
- `raw/articles/TradingAgents.md` / `.pdf` — già ingestato come `references/external/paper-trading-agents`

## Pagine create questa sessione
- [[references/conversazione-luca-salvatore-2026-05-27]] — Ingestione brainstorming del 27/05 (chat e 18 note vocali trascritte)

## Pagine aggiornate questa sessione
- [[build/modules/llm-agent-system]] — Ricercatori/Esecutori, opzioni leva, LangSmith
- [[build/modules/risk-management]] — Statuto deterministico, riserva 10%, token cost estimator
- [[build/decision-log]] — Nuove decisioni chiuse e aperte del 2026-05-27
- [[_meta/index]] — Collegamento nuova source page
- [[_meta/hot-cache]] — Aggiornamento contesto sessione

## Pagine chiave da aggiornare prossima sessione
- [[artifacts/luca-board]] — aggiornare task: Modulo A → Exchange + DB, togliere "LangGraph da imparare" (in corso), aggiungere "Studia il codice TradingAgents"
- [[artifacts/salvatore-board]] — aggiornare con domande emerse: indicatori tecnici e performance (tutte), calendario economico, workflow analista istituzionale
- [[build/system-map]] — aggiornare per riflettere scope stock-only e nuovi nomi componenti
- [[strategy/methods/mean-reversion-stat-arb]] — da completare quando Salvatore finisce di leggere l'articolo
- Decidere exchange per paper trading equity → aggiornare [[build/modules/exchange-db]] e [[build/stack]]
