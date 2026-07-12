---
title: "System Wiki Reorganization"
type: build
tags:
  - architecture
  - roadmap
  - software
created: 2026-06-23
updated: 2026-06-23
status: active
confidence: medium
area: ops
related:
  - "[[artifacts/project-board]]"
  - "[[system/codebase-architecture]]"
  - "[[system/decision-log]]"
  - "[[system/modules/data-layer]]"
  - "[[system/modules/agents]]"
  - "[[system/modules/execution]]"
  - "[[system/tools-inventory]]"
---
%%tutta questa pagina mi sembra già la conseguenza di alcuni commenti inseriti in giro per la wiki, buona base di partenza per eventuali ristrutturazioni, contiene informazioni molto utili sul come voglio che sia questa wiki%%
# System Wiki Reorganization

Pagina di lavoro per ripulire `wiki/system/` senza perdere informazione.

## Obiettivo

Rendere `wiki/system/` leggibile e ordinata per un umano che deve progettare o implementare il codice oggi, distinguendo bene:

- **design attuale**;
- **contesto storico**;
- **backlog operativo**;
- **idee future**.

## Problemi rilevati

- Molte pagine mischiano design, storia di branch e stato operativo corrente.
- In più punti compaiono claim `🟢 Implementato` o `✅` che non rappresentano il codice attuale.
- Alcuni task erano rimasti solo in commenti `%%...%%` o nelle daily notes.

## Policy editoriale adottata

- I claim di implementazione non vengono cancellati brutalmente: diventano **contesto storico** o **reference design**.
- Le pagine operative devono parlare al presente solo quando descrivono decisioni ancora valide.
- I task escono dai commenti e finiscono in board o in pagine dedicate.
- Le informazioni scartate non si eliminano: si archiviano, si assorbono in pagine migliori o si spostano nei log.

## Mapping operativo dei commenti

I commenti inline e le daily notes non vanno riscritti in prosa piu' pulita: vanno smistati nel punto che governa davvero il comportamento futuro.

| Tipo di input              | Destinazione primaria                                                                                          | Effetto richiesto                                                        |
| -------------------------- | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Task per coding agent      | [[artifacts/project-board]] + pagina tecnica collegata                                                         | Card azionabile con owner e link; dettaglio nella pagina target          |
| Task per Luca              | [[artifacts/project-board]] + pagina decisionale                                                               | Validazione o scelta esplicita, non task tecnico nascosto                |
| Task/domanda per Salvatore | [[strategy/questions-for-salvatore]] o pagina `strategy/` pertinente                                           | Domanda formulata come decisione di mercato o dato da fornire            |
| Idea architetturale        | [[system/codebase-architecture]], [[system/data-sources-tool-map]], [[system/frontend-module]] o pagina modulo | Vincolo o backlog tecnico, non nota sparsa                               |
| Correzione di stato        | Pagina che contiene il claim errato                                                                            | Nota di stato corrente + contesto storico, senza cancellare storia utile |
| Prior-art da studiare      | `wiki/prior-art/` o backlog `raw/articles/`                                                                    | Resta research finche' non produce una decisione o un task               |

## Priorita' di pulizia

1. **Pagine che influenzano la percezione dello stato software**: [[system/architecture]], [[system/stack]], [[system/canvas-code-mapping]], [[system/modules/data-layer]], [[system/modules/agents]], [[system/modules/execution]], [[system/tools-inventory]].
2. **Pagine che guidano il nuovo build**: [[system/codebase-architecture]], [[system/data-sources-tool-map]], [[system/frontend-module]], [[system/system-prompts]], [[system/state-schemas]].
3. **Pagine strategy/market**: [[strategy/index]], [[strategy/questions-for-salvatore]], metodi e metriche.
4. **Prior-art e log storici**: non vanno "normalizzati" aggressivamente; devono restare riconoscibili come storia o fonti.

## Claim di implementazione

Regola editoriale:

- se una sezione dice `Implementato`, `branch`, `test verdi`, `commit` o simili, va marcata come **contesto storico / reference design**;
- se la scelta resta valida, va spostata in una sezione di design corrente;
- se la scelta e' dubbia, va trasformata in decisione aperta o card board;
- non si cancella il dettaglio tecnico solo perche' non e' piu' stato corrente.

Esempio di formulazione corretta:

> Stato pagina: spec di design con contesto storico. I riferimenti a branch o moduli Python precedenti sono reference design, non inventario affidabile del codice attuale.

## Proposta di sottodomini futuri

La riorganizzazione fisica delle cartelle si fa solo se Luca la approva e aggiornando [[_meta/taxonomy]]. Per ora questi sono sottodomini logici:

| Sottodominio | Pagine candidate |
|---|---|
| `system/agents/` | [[system/modules/agents]], [[system/agent-behaviors]], [[system/system-prompts]], [[system/agent-memory]] |
| `system/data/` | [[system/modules/data-layer]], [[system/data-sources-tool-map]], [[system/data-providers]], [[system/db-access-performance]], [[system/tools-inventory]] |
| `system/execution/` | [[system/modules/execution]], [[system/trigger-engine]], [[system/cost-accounting]], [[system/position-sizing]] |
| `system/frontend/` | [[system/frontend-module]], [[system/observability-dashboard]] |
| `system/orchestration/` | [[system/parallelism-design]], [[system/trigger-engine]], [[system/universe-watchlist]] |
| `system/quant/` | [[system/modules/quant-backtesting]], [[system/rating-scoring]], [[system/learning-feedback-loop]] |
%%ottima disposizione, creerei direttamente i sottodomini e sposterei subito i file nei sottodomini%%
## Deliverable di questo ingest

- board riallineata come hub operativo con colonne per meeting, Salvatore, Luca, coding agent, ricerca, in corso e fatto;
- pagine hub nuove o consolidate per codebase, fonti/tool, frontend e reorg;
- prime correzioni sulle pagine che falsavano di piu' lo stato del progetto;
- backlog esplicito per completare la pulizia delle pagine ancora dense.

## Cosa resta da fare

- Passare una seconda volta su [[system/architecture]] e [[system/canvas-code-mapping]], perche' contengono molte tabelle `✅` nate da sync codice.
- Decidere se [[prior-art/libraries/datapizza-ai]] resta "framework principale" o diventa candidato/reference da riconfermare. %%alla fine ho deciso di usare langgrpah con langsmith%%
- Pulire le pagine strategy senza perdere il lavoro di Salvatore: qui il problema non e' stato software, ma trasformare appunti in decisioni codificabili.
- Dopo ogni pulizia, aggiornare [[artifacts/project-board]], [[_meta/index]], [[_meta/hot-cache]] e [[_meta/log]].
