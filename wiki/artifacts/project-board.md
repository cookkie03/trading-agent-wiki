---
title: Project Board — Trading Agent
type: artifact
tags:
  - trading-agent
  - roadmap
  - execution
  - architecture
created: 2026-04-30T00:00:00.000Z
updated: 2026-10-31
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

## 🟠 Decisioni da prendere

- [ ] 🔀 **Definire il ruolo del Risk Analyst** — desk pari, gate finale o modello a due livelli; aggiornare routing e prompt dopo la decisione → [[system/agents/agent-behaviors]]
- [ ] 🔀 **Chiudere il confine Market / Sentiment** — Market: macro e catalizzatori; Sentiment: mood e posizionamento multi-fonte → [[system/agents/agent-behaviors]]
- [ ] 🔀 **Scegliere la strategia MVP** — una strategia, indicatori codificabili e protocollo di backtest prima di comporre i metodi → [[strategy/index]]
- [ ] 🔀 **Rivedere prompt e investment state insieme** — convalidare ruoli, fonti, stop e campi obbligatori → [[system/agents/system-prompts]]
- [ ] 🔀 **Rivedere il catalogo esteso dell'investment state** — Luca e Salvatore potano insieme campi core, opzionali e fuori scope → [[system/investment/investment-state-template]]
- [ ] 🛠 **Formalizzare la policy `next_check_date`** — fattori, intervallo massimo, eccezioni e spiegazione richiesta al PM → [[system/orchestration/trigger-engine]]
- [ ] 🛠 **Decidere la retention di documenti e dati** — raw/object storage, metadata, derivati e criteri di conservazione → [[system/data/data-vendors]]

## 🔴 Da fare

- [ ] 🛠 **Completare e verificare il runtime Docker** — Dockerfile, lock dipendenze, configurazione runtime, persistenza e gestione arresto con il primo flusso eseguibile → [[system/foundation/codebase-architecture#Alberatura approvata e requisito Docker — 2026-10-30]]

- [x] 🛠 **Analizzare Alpaca come vendor dati oltre il broker** — catalogo iniziale completato; equities, crypto, options, news, corporate actions, feed, limiti e licensing documentati. Fundamentals non confermati come prodotto API dedicato; adapter diretto avviato con OHLCV storico equities → [[system/data/data-vendors]]
- [ ] 🛠 **Costruire raccolta dati multi-vendor controllata** — capability catalog, schema normalizzato, provenance, rate limits, licensing e job opt-in per OpenBB, Alpaca e adapter diretti; niente scraping massivo implicito → [[system/data/data-vendors]]
- [ ] 🛠 **Completare smoke test runtime Yahoo/Alpaca** — Yahoo verificato con 66 barre persistite e deduplica; eseguire Alpaca con credenziali locali e registrare l’evidenza separata dai test offline → [[artifacts/mvp-database-2026-10-31]]

- [ ] 🛠 **Completare Fase 0 / Fase 1 della codebase** — configurazione e harness TDD; filoni attivi nel piano MVP, ruolo OpenBB in riesame → [[artifacts/piano-operativo-trading-agent]]
- [ ] 🛠 **Completare le schede di copertura data vendor** — capacità, freshness, limiti, costo, licenza, fallback, chiave dedup e fake test per ogni fonte → [[system/data/data-vendors]]
- [ ] 🛠 **Allineare le pagine legacy alla policy di stato** — rimuovere gli ultimi claim non verificabili e spostare gli snapshot nel reference design → [[system/foundation/implementation-status]]
- [ ] 📈 **Consolidare metriche e metodi** — creare “Metriche (definitivo)” e collegare indicatori, metodo e backtest senza duplicazioni → [[strategy/index]]
- [ ] 📈 **Definire fonti e indicatori di sentiment** — copertura, affidabilità, limiti e interpretazione di news/social/insider → [[strategy/questions-for-salvatore]]
- [ ] 🔀 **Studiare optimizer e OpenAlice come reference** — analisi architettura multi-asset e paper quantitativi → [[artifacts/piano-operativo-trading-agent]]

## 🟡 In corso

- [ ] 🛠 **MVP in quattro chat: vendor/schema, database, OpenBB e dashboard** — guida operativa, SQLite MVP e frontend React/TypeScript read-only; nuove implementazioni da verificare → [[artifacts/mvp-parallel-work-2026-10-31]]

- [ ] 🛠 **Catalogo tool/vendor per capacità, OpenBB in riesame** — mantenere l'inventario per capacità e completare la vista navigabile multi-provider → [[artifacts/tool-catalog.base]]
- [ ] 🛠 **Rendere leggibili le reference storiche** — distinguere pattern utili da snapshot non correnti, senza eliminare informazione → [[system/_reference/canvas-code-mapping]]

## 💡 Idee / Post-MVP

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
