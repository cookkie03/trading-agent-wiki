# Hot Cache — Trading Agent

> Contesto di sessione recente. Il repository è esterno al vault: qui vivono spec, decisioni e priorità, non lo stato verificato del codice.

## Sessione 2026-07-13 — Ingest editoriale integrale della rilettura

- **Input elaborati**: daily note dal 2026-06-06 al 2026-07-12 e tutte le annotazioni Obsidian `%%…%%` presenti nella wiki; le daily note/raw non sono state modificate.
- **Tracciabilità**: ogni annotazione è stata classificata e assorbita in [[_meta/comment-resolution-2026-07-13]]. Le annotazioni nascoste sono state rimosse dalle pagine operative; le impostazioni Kanban sono rimaste intatte.
- **Struttura**: `wiki/system/` è ora suddivisa in `foundation`, `data`, `tools`, `agents`, `orchestration`, `investment`, `execution`, `quant`, `interface`, `_reference`. Wikilink e index aggiornati. → [[system/foundation/wiki-reorganization]]
- **Policy fondamentale**: le pagine non attestano più implementazioni, branch, test o deploy del repository esterno; gli snapshot restano reference design. → [[system/foundation/implementation-status]]
- **Decisioni consolidate**: LangGraph + LangSmith; state annidato a campi fissi; MVP USD-only senza benchmark dinamico; analisi event-driven + health check periodico; OpenBB-first per catalogo e multi-vendor tramite wrapper. → [[system/foundation/decision-log]]
- **Nuovi artefatti**: [[system/data/data-vendors]], [[artifacts/tool-catalog.base]], [[_meta/comment-resolution-2026-07-13]].

## Stato del progetto nel vault

- **Design operativo**: [[system/foundation/architecture]] · [[system/foundation/mvp]] · [[system/foundation/stack]]
- **Board unica**: [[artifacts/project-board]]
- **Decisioni umane aperte**: ruolo Risk Analyst; confine Market/Sentiment; strategia MVP; revisione prompt/investment state; policy `next_check_date`; retention dati/documenti.
- **Ricerca non bloccante**: copertura vendor, fonti sentiment, optimizer/Black–Litterman, RAG+grafi, benchmark e UI evoluta.

## Nota LightRAG

La KB registrata `trading-agent-wiki` punta alla copia OneDrive ed è spenta; non è stata usata come fonte per questa sessione. Il vault iCloud letto direttamente resta la fonte affidabile.
