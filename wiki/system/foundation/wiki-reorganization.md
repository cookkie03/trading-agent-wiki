---
title: "System Wiki Reorganization"
type: build
tags:
  - architecture
  - roadmap
  - software
created: 2026-06-23
updated: 2026-07-13
status: done
confidence: medium
area: ops
related:
  - "[[artifacts/project-board]]"
  - "[[system/foundation/codebase-architecture]]"
  - "[[system/foundation/decision-log]]"
  - "[[system/data/data-layer]]"
  - "[[system/agents/agents]]"
  - "[[system/execution/execution]]"
  - "[[system/tools/tools-inventory]]"
---
# System Wiki Reorganization

Riorganizzazione completata il 2026-07-13, senza perdere informazione. Il dettaglio di lettura e assorbimento dei commenti è [[_meta/comment-resolution-2026-07-13]].

## Obiettivo

Rendere `wiki/system/` leggibile e ordinata per un umano che deve progettare o implementare il codice oggi, distinguendo bene:

- **design attuale**;
- **contesto storico**;
- **backlog operativo**;
- **idee future**.

## Problemi rilevati

- Molte pagine mischiano design, storia di branch e stato operativo corrente.
- In più punti comparivano claim di implementazione che il vault non può verificare.
- Alcuni task erano rimasti solo in commenti o nelle daily notes.

## Policy editoriale adottata

- I claim di implementazione non vengono cancellati brutalmente: diventano **contesto storico** o **reference design**.
- Le pagine operative devono parlare al presente solo quando descrivono decisioni ancora valide.
- I task escono dai commenti e finiscono in board o in pagine dedicate.
- Le informazioni scartate non si eliminano: si archiviano, si assorbono in pagine migliori o si spostano nei log.

## Mapping operativo dei commenti

I commenti inline e le daily notes non vanno riscritti in prosa piu' pulita: vanno smistati nel punto che governa davvero il comportamento futuro.

| Tipo di input              | Destinazione primaria                                                                                          | Effetto richiesto                                                        |
| -------------------------- | -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Specifica da consegnare al coding agent | [[artifacts/project-board]] + pagina tecnica collegata                                                         | Requisito documentale con owner e link; nessun intervento sul repo esterno |
| Task per Luca              | [[artifacts/project-board]] + pagina decisionale                                                               | Validazione o scelta esplicita, non task tecnico nascosto                |
| Task/domanda per Salvatore | [[strategy/questions-for-salvatore]] o pagina `strategy/` pertinente                                           | Domanda formulata come decisione di mercato o dato da fornire            |
| Idea architetturale        | [[system/foundation/codebase-architecture]], [[system/data/data-sources-tool-map]], [[system/interface/frontend-module]] o pagina modulo | Vincolo o backlog tecnico, non nota sparsa                               |
| Correzione di stato        | Pagina che contiene il claim errato                                                                            | Nota di stato corrente + contesto storico, senza cancellare storia utile |
| Prior-art da studiare      | `wiki/prior-art/` o backlog `raw/articles/`                                                                    | Resta research finche' non produce una decisione o un task               |

## Priorita' di pulizia

1. **Pagine che influenzano la percezione dello stato software**: [[system/foundation/architecture]], [[system/foundation/stack]], [[system/_reference/canvas-code-mapping]], [[system/data/data-layer]], [[system/agents/agents]], [[system/execution/execution]], [[system/tools/tools-inventory]].
2. **Pagine che guidano il nuovo build**: [[system/foundation/codebase-architecture]], [[system/data/data-sources-tool-map]], [[system/interface/frontend-module]], [[system/agents/system-prompts]], [[system/investment/state-schemas]].
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

## Sottodomini applicati

| Sottodominio | Pagine candidate |
|---|---|
| `system/foundation/` | architettura, MVP, stack, decision log, idee e policy di stato |
| `system/data/` | data layer, provider, vendor e performance DB |
| `system/tools/` | inventario dei tool e relativo catalogo |
| `system/agents/` | ruoli, prompt e memoria |
| `system/orchestration/` | parallelismo, trigger e universo/watchlist |
| `system/investment/` | state, sizing, scoring e cost accounting |
| `system/execution/`, `system/quant/`, `system/interface/` | esecuzione, backtesting/feedback e frontend |
| `system/_reference/` | mapping e analisi storiche da non confondere con le spec |
## Deliverable dell'ingest editoriale

- board ridotta a decisioni, azioni, ricerca, idee e fatto;
- ledger che conserva il mapping di tutti i commenti;
- nuove pagine per policy di stato e copertura vendor/tool;
- link, index, taxonomy e hot-cache allineati alla nuova struttura.

## Cosa resta aperto

Le decisioni umane e la ricerca rimaste aperte stanno in [[artifacts/project-board]]. LangGraph + LangSmith è la scelta corrente; Datapizza AI è reference storica.
