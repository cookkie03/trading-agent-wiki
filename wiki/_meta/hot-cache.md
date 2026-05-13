# Hot Cache — Trading Agent

> Contesto di sessione recente. Aggiornare a fine sessione. Tenere entro 300 righe.

## Sessione Corrente
- **Data**: 2026-05-13
- **Agent**: Claude Code
- **Operazioni**: Sessione di brainstorming + ricerca NotebookLM (43 fonti). Chiuse decisioni principali + framework backtesting + conferma LLM. Creata synthesis dalla ricerca.

## Pagine toccate (sessione corrente)
- [[references/videochiamata-luca-salvatore-2026-05-13]] — CREATA — call 2026-05-13 con strategia trend following, value investing, architettura
- [[ops/wiki-restructuring-plan]] — CREATA — piano ristrutturazione wiki (pianificato, non eseguito)
- [[decisions/decision-log]] — aggiunte: value investing non scalabile, struttura wiki quant aperta
- [[_meta/index]] — aggiornato con nuova reference e ops/wiki-restructuring-plan

## Pagine toccate (sessione precedente 2026-05-13)
- [[build/mvp-prototype-design]] — CREATA + aggiornata con decisione backtesting e insights NotebookLM
- [[syntheses/notebooklm-research-2026-05-13]] — CREATA — synthesis da ricerca su 43 fonti
- [[decisions/decision-log]] — aggiornate decisioni chiuse 2026-05-13 (6 nuove)
- [[_meta/index]] — aggiunta voce syntheses
- [[_meta/log]] — aggiunta entry sessione 2026-05-13

## Stato attuale del progetto
- Fase: **Design → prossimo passo: sviluppo Modulo A**
- **Architettura scelta**: monolite modulare (Opzione A), con path evolutivo verso microservizi
- **Tipo prototipo**: agente autonomo paper trading (Binance Testnet) + backtesting continuativo + metriche per-trade e portfolio
- **Orizzonte trade**: swing trading (4h/daily)
- **Sequenza sviluppo**:
  - Track 1 (Luca solo): **Modulo A** — Exchange Module + DB
  - Track 2 (Luca + Salvatore, in parallelo): **Modulo C** — Quant Agent + Backtesting
  - Track 3 (dopo A completato): **Modulo D** — Prompt Builder + LLM Trader
- **Ciclo aggiornato**: Risk Analyst Agent è UPSTREAM del Trader (fonte: trading-floor.canvas)
- **Portfolio**: architettura portfolio-first, MVP deployment su singolo asset

## Pending ingest
- `raw/notes/sessione-brainstorming-2026-05-13.md` — da completare ingest formale (interrotto)
- `raw/audio/2026-05-13 13-14-17.m4a` — INGESTATO tramite trascrizione txt
- `raw/articles/quant strategy/*.txt` — audio/note di Salvatore su strategie quant, da ingestare
- Le trascrizioni in `raw/audio/` possono essere archiviate in `raw/archived/`

## Decisioni ancora aperte
- ~~Framework backtesting~~ **CHIUSO: VectorBT** (2026-05-13)
- Strategia del fondo: formalizzare con Salvatore (orientamento: multi-factor fundamentals)
- Frequenza ciclo: 4h vs 24h (dipende da backtest iniziali)

## Note sessione critiche
- **Metriche per-trade e portfolio sono separate**: non sono sovrapponibili. Il sistema le raccoglie a due livelli indipendenti. I trade di ribilanciamento trattati come eventi discreti danno metriche per-trade leggibili dentro un framework portfolio.
- **Risk Analyst upstream**: imposta i paletti PRIMA del Trader, non valida dopo. Insight da trading-floor.canvas.
- Il **principio deterministico** rimane vincolo hard: LLM solo per ragionamento, tutto il resto Python.
