---
title: "Risoluzione commenti wiki — 2026-07-13"
type: artifact
tags:
  - architecture
  - roadmap
  - strategy
  - infrastructure
created: 2026-07-13
updated: 2026-07-13
status: done
related:
  - "[[artifacts/project-board]]"
  - "[[system/foundation/implementation-status]]"
  - "[[system/foundation/wiki-reorganization]]"
  - "[[system/data/data-vendors]]"
confidence: high
area: ops
---

# Risoluzione commenti wiki — 2026-07-13

Registro della rilettura integrale di Luca. La fonte è costituita dalle daily note dal 2026-06-06 al 2026-07-12 e da tutte le annotazioni Obsidian `%%…%%` allora presenti nelle pagine wiki. Le daily note grezze restano in `raw/`; questa pagina conserva la destinazione operativa di ogni annotazione, così le pagine di lavoro possono restare pulite.

## Regola di lettura adottata

- Ciò che Luca non ha commentato è considerato letto, controllato e valido.
- Un commento corregge o integra il testo circostante; non è un task isolato.
- Il repository è esterno al vault: nessuna pagina qui attesta lo stato corrente del codice. I riferimenti a implementazioni, branch, test, URL di dashboard o processi sono **reference design/storia**, salvo verifica esterna esplicitamente riportata in futuro.
- Le idee non prioritarie non sono eliminate: sono state collocate in board, backlog di ricerca o Post-MVP.

## Risoluzioni applicate

| Gruppo di annotazioni | Contesto e interpretazione | Destinazione applicata |
| --- | --- | --- |
| Stato del codice, dashboard, mapping canvas, fork | Il progetto va progettato e costruito fuori dal vault; i claim `✅`/`Implementato` non sono un inventario affidabile qui. | [[system/foundation/implementation-status]]; documenti storici in [[system/_reference/fork-gap-analysis]] e [[system/_reference/canvas-code-mapping]]. |
| Framework e prompt | Il commento più recente chiude la scelta su **LangGraph + LangSmith**. Prompt, template e decisioni restano specifiche da riesaminare con Salvatore. | [[system/foundation/stack]], [[system/agents/system-prompts]], board. |
| State, parallelismo e trigger | State annidato a campi fissi sostituisce l'Opzione C; subgraph per ticker scelto; i trigger devono portare al PM origine e priorità. | [[system/investment/state-schemas]], [[system/orchestration/parallelism-design]], [[system/orchestration/trigger-engine]]. |
| Ruoli agenti | Tool deterministici per ogni output; serve una definizione completa del Risk Analyst; Market tratta macro/catalizzatori e Sentiment mood/posizionamento. | [[system/agents/agent-behaviors]], [[system/agents/agents]], decisioni condivise in board. |
| Dati, vendor e tool | OpenBB è la base del catalogo e dell'analisi di copertura; broker e altri provider restano fonti intercambiabili. Prezzi real-time preferibilmente dal broker. Ogni artefatto estratto/calcolato ha retention e provenienza. | [[system/data/data-vendors]], [[system/tools/tools-inventory]], [[artifacts/tool-catalog.base]]. |
| Schedulazione | Analisi e rivalutazioni sono event-driven (`next_check_date`, alert, calendario); il controllo di salute/portafoglio resta periodico e costante. | [[system/orchestration/trigger-engine]]. |
| Strategia e ricerca | Trend following e mean reversion sono candidati codificabili; factor investing usa anche la tesi corporate bond; metodi e metriche richiedono la validazione di Salvatore. Optimizer, OpenBB, FinRL, Kronos e GraphRAG sono ricerca, non prerequisiti impliciti dell'MVP. | [[strategy/index]], [[strategy/questions-for-salvatore]], [[prior-art/libraries/cvx-portfolio-optimizer]], board. |
| Post-MVP | Benchmark dinamico, rating drift, learning feedback, accounting predittivo, memoria a grafi, UI TypeScript e backtest utente sono conservati come evoluzioni, non come scope MVP. | [[system/orchestration/universe-watchlist]], [[system/quant/learning-feedback-loop]], [[system/interface/frontend-module]], board. |
| Glossario | Black–Litterman, Idzorek alpha e termini del position sizing devono essere trovabili senza appesantire le pagine tecniche. | [[_meta/glossario]]. |

## Decisioni chiuse durante l'ingest editoriale

1. Il vault descrive requisiti e design, non lo stato del repository esterno.
2. Framework di riferimento: **LangGraph + LangSmith**; Datapizza AI rimane prior-art storico.
3. `research_state` / `investment_state`: schema annidato, campi specifici e predeterminati; niente sealing progressivo come design corrente.
4. Il catalogo data/tool è OpenBB-first per copertura e multi-vendor per resilienza; nessun provider è dichiarato unico senza scheda di valutazione.
5. MVP senza benchmark dinamico e senza cost accounting predittivo; si preservano però i dati necessari alla loro evoluzione.

## Decisioni ancora umane

- Ruolo definitivo del Risk Analyst: desk pari agli altri, gate finale, o combinazione dei due.
- Confine esatto Market Analyst / Sentiment Analyst.
- Strategia MVP e ordine di codifica: value, trend following, mean reversion, factor e dual portfolio.
- Criteri e intervalli massimi della `next_check_date`.
- Policy concreta di retention per documenti e dati estratti: DB, object storage e metadata.

## Pulizia eseguita

- Annotazioni `%%…%%` assorbite e rimosse dalle pagine operative; configurazione Kanban esclusa.
- Recuperi iCloud conservati semanticamente in questa pagina, nelle pagine target e nel log; nessuna daily note/raw è stata alterata.
- `wiki/system/` organizzata per dominio; i wikilink sono stati aggiornati alla nuova struttura.

