---
title: Project Board — Trading Agent
type: artifact
tags:
  - trading-agent
  - roadmap
  - execution
  - architecture
created: 2026-04-30T00:00:00.000Z
updated: 2026-11-01
status: active
related:
  - "[[system/foundation/decision-log]]"
  - "[[system/foundation/implementation-status]]"
  - "[[comment-resolution-2026-07-13]]"
confidence: high
priority: high
area: ops
kanban-plugin: board
---

## Priorità operative correnti — 2026-11-04

> [!important] Promemoria UI da non dimenticare
> Prima di progettare o implementare la UI del Trading Agent su GitHub, **chiedere a Giuseppe (vedi lista contatti)** un confronto e un aiuto.

La board è l'unico indice canonico dei prossimi passi; le fasi precedenti nel [[artifacts/piano-operativo-trading-agent]] sono riferimento storico, non una roadmap concorrente. **Solo questa sezione è attiva**: tutte le card e i filoni nelle sezioni successive, inclusi quelli indicati come «In corso» (chat/vendor/UI e catalogo provider), sono sospesi, conservati e non cancellati, finché non rientrano nella sequenza seguente.

1. [ ] 🔀 **Verificare e definire i sei agenti** — Market, Sentiment, Technical, Fundamental, Risk e Portfolio Manager separati; valutare il codice residuo, ruoli, contratti e comportamenti prima di deciderne la destinazione → [[system/agents/agent-behaviors]]
2. [ ] 🛠 **Definire grafo e confini dopo la verifica** — grafo sotto `agents`; distinguere trigger, grafo e tool. Nomi e collocazione dei trigger/workflow esterni e cartelle `orchestration`/`steps` restano aperti; nessuna creazione ora. Testare il workflow con fake prima dell'infrastruttura reale → [[system/foundation/codebase-architecture#Decisione e confini — 2026-11-05]]
3. [ ] 🛠 **Definire e realizzare i tool** — dopo il workflow → [[system/tools/tools-inventory]]
4. [ ] 🛠 **Collegare adapter, provider e dati reali** — dopo i tool; mantenere risk e safety deterministici, senza attivare esecuzione reale → [[system/data/data-vendors]]
5. [ ] 🛠 **Progettare e costruire il cockpit UI end-to-end** — dopo i livelli precedenti; prima chiedere a **Giuseppe (vedi lista contatti)** un confronto sulla UI. Usare **[21st.dev](https://21st.dev/)** per ricerca/selezione e integrazione di componenti React/shadcn e la skill **[Impeccable](https://github.com/pbakaus/impeccable)** per shape, design direction, critique, audit e polish. Realizzare le schermate e gli stati previsti dalla spec, integrandoli con i contratti read-only reali e verificando responsive, accessibilità e interazioni → [[system/interface/frontend-module]] · [[system/interface/observability-dashboard]] · [[artifacts/mvp-dashboard-2026-10-31]]

## 🟠 Decisioni da prendere

- [ ] 🔀 **Definire il ruolo del Risk Analyst** — desk pari, gate finale o modello a due livelli; aggiornare routing e prompt dopo la decisione → [[system/agents/agent-behaviors]]
- [ ] 🔀 **Chiudere il confine Market / Sentiment** — Market: macro e catalizzatori; Sentiment: mood e posizionamento multi-fonte → [[system/agents/agent-behaviors]]
- [x] 🔀 **Scegliere la strategia MVP** — trend following hourly, long-only, azioni USA, USD-only, swing trading; indicatori e protocollo di backtest da chiudere → [[strategy/index]]
- [ ] 🔀 **Rivedere prompt e investment state insieme** — convalidare ruoli, fonti, stop e campi obbligatori → [[system/agents/system-prompts]]
- [ ] 🔀 **Rivedere il catalogo esteso dell'investment state** — Luca e Salvatore potano insieme campi core, opzionali e fuori scope → [[system/investment/investment-state-template]]
- [ ] 🛠 **Formalizzare la policy `next_check_date`** — fattori, intervallo massimo, eccezioni e spiegazione richiesta al PM → [[system/orchestration/trigger-engine]]
- [ ] 🛠 **Decidere la retention di documenti e dati** — raw/object storage, metadata, derivati e criteri di conservazione → [[system/data/data-vendors]]
- [ ] 🛠 **Studiare PostgreSQL, pgvector e FTS** — schema, migrazione eventuale da SQLite, ricerca ibrida e retention; nessuna migrazione prima di benchmark/review → [[artifacts/piano-operativo-trading-agent]]
- [ ] 🛠 **Progettare RAG come feature futura prioritaria** — ingestion, chunking, embeddings, retrieval ibrido, citazioni e provenance nello state → [[artifacts/piano-operativo-trading-agent]]

## 🔴 Da fare

- [x] 🛠 **Completare e verificare il runtime Docker MVP** — Dockerfile, lock dipendenze, volume SQLite, healthcheck e smoke read-only verificati; il dev launcher resta locale e senza Docker → [[system/foundation/codebase-architecture#Alberatura approvata e requisito Docker — 2026-10-30]]

- [x] 🛠 **Analizzare Alpaca come vendor dati oltre il broker** — catalogo iniziale completato; equities, crypto, options, news, corporate actions, feed, limiti e licensing documentati. Fundamentals non confermati come prodotto API dedicato; adapter diretto avviato con OHLCV storico equities → [[system/data/data-vendors]]
- [ ] 🛠 **Costruire raccolta dati multi-vendor controllata** — capability catalog, schema normalizzato, provenance, rate limits, licensing e job opt-in per OpenBB, Alpaca e adapter diretti; niente scraping massivo implicito → [[system/data/data-vendors]]
- [ ] 🛠 **Verificare il flusso end-to-end provider → SQLite → outbox/SMA → dashboard** — fixture deterministica, freshness/source visibili e caso vuoto/errore; coordinare vendor, storage e read model → [[artifacts/mvp-parallel-work-2026-10-31]]
- [ ] 🛠 **Decidere il destino del bridge Telegram locale** — validare confini di sicurezza, packaging e test; poi committare o rimuovere il lavoro non tracciato → [[system/interface/telegram-claude-bridge]]
- [x] 🛠 **Completare smoke test runtime Yahoo/Alpaca/OpenBB** — OpenBB reale e Alpaca paper read-only verificati con configurazione locale; evidenze separate dai test offline → [[artifacts/mvp-database-2026-10-31]]

- [ ] 🛠 **Completare Fase 0 / Fase 1 della codebase** — filone sospeso, non cancellato; configurazione e harness saranno rivalutati secondo la priorità corrente; OpenBB percorso principale per dati di mercato → [[artifacts/piano-operativo-trading-agent]]
- [ ] 🛠 **Completare le schede di copertura data vendor** — capacità, freshness, limiti, costo, licenza, fallback, chiave dedup e fake test per ogni fonte → [[system/data/data-vendors]]
- [ ] 🛠 **Allineare le pagine legacy alla policy di stato** — rimuovere gli ultimi claim non verificabili e spostare gli snapshot nel reference design → [[system/foundation/implementation-status]]
- [ ] 📈 **Consolidare metriche e metodi** — creare “Metriche (definitivo)” e collegare indicatori, metodo e backtest senza duplicazioni → [[strategy/index]]
- [ ] 📈 **Definire fonti e indicatori di sentiment** — copertura, affidabilità, limiti e interpretazione di news/social/insider → [[strategy/questions-for-salvatore]]
- [ ] 🔀 **Studiare optimizer e OpenAlice come reference** — analisi architettura multi-asset e paper quantitativi → [[artifacts/piano-operativo-trading-agent]]
- [ ] 🛠 **Studiare Qlib e QuantLab** — scheda comparativa, licenze, dipendenze, codice riusabile e compatibilità col modulo quantitative research → [[artifacts/piano-operativo-trading-agent]]
- [ ] 🛠 **Studiare e integrare vectorbt** — adapter di backtesting accessibile a umano e agenti, con risultati versionati e riproducibili → [[artifacts/piano-operativo-trading-agent]]
- [ ] 🛠 **Definire riuso da TradingAgents** — per feature coincidenti, verificare upstream/licenza/test e riusare il codice compatibile con contratti locali → [[artifacts/piano-operativo-trading-agent]]

## 🟡 In corso

- [ ] 🛠 **MVP in quattro chat: vendor/schema, database, OpenBB e dashboard** — guida operativa, SQLite MVP e frontend React/TypeScript read-only; nuove implementazioni da verificare → [[artifacts/mvp-parallel-work-2026-10-31]]
- [x] 🛠 **Implementare la materializzazione incrementale dei derivati — SMA v1** — migration `indicator_values`/outbox, ingestion atomica, worker idempotente, watermark, status, retry e rebuild verificati; estendere agli altri indicatori solo dopo chiusura delle formule/parametri MVP → [[system/db-access-performance]]
- [x] 🛠 **Formalizzare le formule tecniche pure iniziali** — EMA, RSI Wilder, MACD, ATR Wilder e Pivot Points classici disponibili e testati in `analysis.indicators`; la materializzazione resta SMA-only finché la strategia MVP non chiude i parametri → [[system/quant/quant-backtesting]]

- [ ] 🛠 **Catalogo tool/vendor per capacità, OpenBB-first** — mantenere l'inventario per capacità e completare la vista navigabile multi-provider; fallback da definire → [[artifacts/tool-catalog.base]]
- [ ] 🛠 **Rendere leggibili le reference storiche** — distinguere pattern utili da snapshot non correnti, senza eliminare informazione → [[system/_reference/canvas-code-mapping]]

## 💡 Idee / Post-MVP

- [ ] 🛠 **Ricercare la portabilità tra backend agentici** — valutare successivamente LangGraph, Hermes, Pi e Claude Code; nessuna compatibilità è acquisita → [[system/foundation/codebase-architecture#Decisione e confini — 2026-11-05]]

- [ ] 🔀 **Sintesi strutturata dello storico news** — tool parametrico per date/parole chiave e recap di competizione/mercato → [[system/data/data-vendors]]
- [ ] 🛠 **Memoria semantica RAG + grafi** — valutare librerie solo dopo stabilizzazione di dati, dedup e contratti → [[system/agents/agent-memory]]
- [ ] 🛠 **Benchmark dinamico e rating-drift trigger** — introdurre dopo MVP, senza guidare oggi le decisioni del PM → [[system/orchestration/universe-watchlist]]
- [ ] 🛠 **Backtest utente persistente nella UI** — evoluzione futura su contratti stabili; frontend React/TypeScript MVP già nel piano parallelo → [[system/interface/frontend-module]]
- [ ] 🔀 **Scouting periodico di prior-art** — OpenBB, FinRL, Kronos, SFC e altri riferimenti diventano decisioni solo dopo una scheda di studio → [[system/data/data-sources-tool-map]]

## ✅ Fatto

- [x] 🛠 **Adottate le convenzioni pragmatiche per i commenti Python** — metodo why-first ispirato ad antirez; docstring per interfacce, invarianti e vincoli; commenti algoritmici per le future ratio economiche e commenti storici solo per vincoli esterni verificabili → [[system/foundation/python-commenting-conventions]]
- [x] 🛠 **Primo Broker read-only con Alpaca e test offline** — conto, posizioni e finestra ordini; prova paper opt-in predisposta ma non eseguita sul conto di Luca → [[system/foundation/implementation-status#Broker read-only — verifica 2026-10-31]]

- [x] 🛠 **Approvata e avviata la struttura modulare** — package iniziali e packaging presenti; requisito Docker produzione registrato → [[system/foundation/codebase-architecture#Alberatura approvata e requisito Docker — 2026-10-30]]

- [x] 🛠 **Ripartenza da zero con skill di Matt Pocock conservate** — rimosso codice precedente nel commit locale `88ca413`; cronologia preservata, nessun push → [[system/foundation/implementation-status#Ripartenza confermata — 2026-10-30]]

- [x] 🛠 **Collegate le due cartelle locali ai repository GitHub** — clone completo di codice e wiki, tracking `origin/main` e regola di consultare la wiki prima di ogni attività negli `AGENTS.md` locali → [[system/foundation/implementation-status#Verifica workspace — 2026-10-30]]
- [x] 🛠 **Assorbiti i commenti Obsidian e le daily note rilevanti** — ogni annotazione ha una destinazione; le pagine operative non contengono più commenti nascosti → [[comment-resolution-2026-07-13]]
- [x] 🛠 **Riorganizzato `wiki/system/` per dominio** — spostati i file, aggiornati i wikilink e separato il reference design → [[system/foundation/wiki-reorganization]]
- [x] 🛠 **Stabilita la policy di stato del vault** — la wiki descrive requisiti; il repository esterno non viene attestato senza verifica → [[system/foundation/implementation-status]]
- [x] 🛠 **Scelta framework consolidata** — LangGraph + LangSmith; Datapizza AI resta prior-art storico → [[system/foundation/stack]]
- [x] 🛠 **State schema aggiornato** — struttura annidata a campi fissi, senza Opzione C/sealing → [[system/investment/state-schemas]]

%% kanban:settings
```
{"kanban-plugin":"board","list-collapse":[null,null,null,null,null]}
```
%%
