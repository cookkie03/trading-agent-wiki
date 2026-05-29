# Hot Cache — Trading Agent

> Contesto di sessione recente. Aggiornare a fine sessione. Tenere entro 300 righe.

## Sessione Corrente
- **Data**: 2026-05-29
- **Agent**: Claude Code (Opus)
- **Operazione principale**: Ingestione delle due videochiamate Luca & Salvatore del 29/05 (mattina: LangChain/LangGraph + TradingAgents spiegato, decisione portfolio vs day-trading; pomeriggio: design architettura custom su `agents.canvas`). Definita la topologia agenti, il design del DB esteso, scelta OpenRouter+DeepSeek V4 Pro, Trader deterministico, Risk Analyst come gate bear, portafoglio iniziale investito, benchmark.

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
- `raw/audio/2026-05-13 13-14-17.m4a` — richiede `/wiki-preprocess` (trascrizione mancante)
- `raw/articles/TradingAgents Code Wiki.md` — source page creata; lasciato in raw per consultazione

## Pagine create questa sessione
- [[references/videochiamata-luca-salvatore-2026-05-29]] — source page delle due call del 29/05
- [[strategy/metrics/benchmark]] — benchmark della gestione attiva

## Pagine aggiornate questa sessione
- [[build/modules/llm-agent-system]] — topologia agenti 2026-05-29 (analisti, research_state, Risk Analyst gate, Trade deterministico, PM orchestratore, context rot, OpenRouter/DeepSeek)
- [[build/modules/exchange-db]] — design DB esteso (rendicontazione, dati live, costituzione, log, retention, extractors, market alert)
- [[build/modules/risk-management]] — Risk Analyst come gate bear + guardrail deterministici da Statuto-schema
- [[build/modules/quant-backtesting]] — posizione TA/fondamentali/sentiment di Salvatore
- [[build/decision-log]] — 10 decisioni chiuse del 29/05 + aggiornate le aperte
- [[build/stack]] — OpenRouter, DeepSeek V4 Pro + tabella costi, storage storico
- [[wiki/overview]], [[strategy/index]], [[artifacts/luca-board]], [[artifacts/salvatore-board]], [[_meta/index]]

## Pagine chiave da aggiornare prossima sessione
- [[build/system-map]] — **da aggiornare**: riflette ancora la vecchia struttura; allineare alla topologia 2026-05-29 (analisti → research_state → Risk Analyst → Trade deterministico, PM orchestratore, DB esteso, extractors)
- **Conflitto da risolvere** in [[build/modules/llm-agent-system]]: il vecchio "LLM Trader produce JSON" + "agente Esecutore gestisce la leva" vs nuovo "Trade = funzione deterministica". Da riconciliare dove vive la logica leva via opzioni (probabilmente nel research_state/Risk Analyst)
- Consolidare lo **schema DB definitivo** unendo le 5 tabelle core con le 4 aree logiche 2026-05-29
- Decidere exchange per paper trading equity → [[build/modules/exchange-db]] e [[build/stack]]
