---
title: "Project Board — Trading Agent"
type: artifact
tags:
  - roadmap
  - execution
  - architecture
created: 2026-04-30
updated: 2026-07-13
status: active
related:
  - "[[system/foundation/decision-log]]"
  - "[[system/foundation/implementation-status]]"
  - "[[_meta/comment-resolution-2026-07-13]]"
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

- [ ] 🛠 **Completare le schede di copertura data vendor** — capacità, freshness, limiti, costo, licenza, fallback, chiave dedup e fake test per ogni fonte → [[system/data/data-vendors]]
- [ ] 🛠 **Allineare le pagine legacy alla policy di stato** — rimuovere gli ultimi claim non verificabili e spostare gli snapshot nel reference design → [[system/foundation/implementation-status]]
- [ ] 📈 **Consolidare metriche e metodi** — creare “Metriche (definitivo)” e collegare indicatori, metodo e backtest senza duplicazioni → [[strategy/index]]
- [ ] 📈 **Definire fonti e indicatori di sentiment** — copertura, affidabilità, limiti e interpretazione di news/social/insider → [[strategy/questions-for-salvatore]]
- [ ] 🔀 **Studiare optimizer come reference quant** — documentazione, Black–Litterman/Idzorek e criterio riuso vs replica → [[prior-art/libraries/cvx-portfolio-optimizer]]

## 🟡 In corso

- [ ] 🛠 **Catalogo tool/vendor OpenBB-first** — mantenere l'inventario per capacità e completare la vista navigabile multi-provider → [[artifacts/tool-catalog.base]]
- [ ] 🛠 **Rendere leggibili le reference storiche** — distinguere pattern utili da snapshot non correnti, senza eliminare informazione → [[system/_reference/canvas-code-mapping]]

## 💡 Idee / Post-MVP

- [ ] 🔀 **Sintesi strutturata dello storico news** — tool parametrico per date/parole chiave e recap di competizione/mercato → [[system/data/data-vendors]]
- [ ] 🛠 **Memoria semantica RAG + grafi** — valutare librerie solo dopo stabilizzazione di dati, dedup e contratti → [[system/agents/agent-memory]]
- [ ] 🛠 **Benchmark dinamico e rating-drift trigger** — introdurre dopo MVP, senza guidare oggi le decisioni del PM → [[system/orchestration/universe-watchlist]]
- [ ] 🛠 **Frontend TypeScript e backtest utente persistente** — evoluzione della UI read-only su contratti stabili → [[system/interface/frontend-module]]
- [ ] 🔀 **Scouting periodico di prior-art** — OpenBB, FinRL, Kronos, SFC e altri riferimenti diventano decisioni solo dopo una scheda di studio → [[system/data/data-sources-tool-map]]

## ✅ Fatto

- [x] 🛠 **Assorbiti i commenti Obsidian e le daily note rilevanti** — ogni annotazione ha una destinazione; le pagine operative non contengono più commenti nascosti → [[_meta/comment-resolution-2026-07-13]]
- [x] 🛠 **Riorganizzato `wiki/system/` per dominio** — spostati i file, aggiornati i wikilink e separato il reference design → [[system/foundation/wiki-reorganization]]
- [x] 🛠 **Stabilita la policy di stato del vault** — la wiki descrive requisiti; il repository esterno non viene attestato senza verifica → [[system/foundation/implementation-status]]
- [x] 🛠 **Scelta framework consolidata** — LangGraph + LangSmith; Datapizza AI resta prior-art storico → [[system/foundation/stack]]
- [x] 🛠 **State schema aggiornato** — struttura annidata a campi fissi, senza Opzione C/sealing → [[system/investment/state-schemas]]

%% kanban:settings
```
{"kanban-plugin":"board","list-collapse":[null,null,null,null,null]}
```
%%
