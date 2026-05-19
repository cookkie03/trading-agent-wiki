---
vault_type: hybrid
vault_name: "trading-agent-wiki"
language: it
---

# Taxonomy

## Ruoli semantici → Path

I ruoli semantici sono fissi. I path sono specifici di questo vault.
Le skill wiki-* non usano mai path hardcodati: leggono sempre questa tabella.

| Ruolo       | Path                        | Attivo | Note |
|-------------|-----------------------------|--------|------|
| `source`    | `wiki/references/`          | sì     | Fonti ingestite (call, paper, articoli) |
| `external`  | `wiki/references/external/` | sì     | Framework e librerie di terze parti |
| `build`     | `wiki/build/`               | sì     | Spec del progetto: architettura, moduli, decisioni, stack (dominio Luca) |
| `module`    | `wiki/build/modules/`       | sì     | Un file per modulo software del sistema |
| `strategy`  | `wiki/strategy/`            | sì     | Conoscenza di mercato e trading: metodi, indicatori, metriche (dominio Salvatore) |
| `synthesis` | `wiki/syntheses/`           | sì     | Analisi trasversali, ricerca multi-fonte |
| `artifact`  | `wiki/artifacts/`           | sì     | Canvas, board, schemi visuali |
| `meta`      | `wiki/_meta/`               | sì     | Navigazione del vault (index, log, hot-cache, glossario) |
| `overview`  | `wiki/`                     | sì     | overview.md unico |
| `list`      | `wiki/lists/`               | no     | Non usato in questo vault |
| `entity`    | `wiki/agents/`              | no     | Eliminato — contenuto migrato in references/external/ |
| `knowledge` | `wiki/theory/`              | no     | Eliminato — contenuto migrato in build/system-map |
| `operation` | `wiki/ops/`                 | no     | Eliminato — contenuto migrato in build/ e artifacts/ |
| `decision`  | `wiki/decisions/`           | no     | Eliminato — migrato in build/decision-log.md |
| `question`  | `wiki/questions/`           | no     | Eliminato — domande inline nei module files e nelle board |

## Cartelle raw → Path

| Tipo      | Path              |
|-----------|-------------------|
| default   | `raw/`            |
| audio     | `raw/audio/`      |
| documents | `raw/articles/`   |
| notes     | `raw/notes/`      |
| archived  | `raw/archived/`   |

## Tag Taxonomy — Trading Agent

> Solo questi tag sono canonici. Aggiungere qui nuovi tag prima di usarli in modo stabile.

### Type
source · synthesis · build · artifact · overview

### Status
draft · active · reviewed · verified · stale · archived · done

### Priority
priority/high · priority/medium · priority/low

### Areas
area/software · area/research · area/market · area/ops · area/strategy

### Project Tags
architecture · strategy · execution · ingest · market-structure · infrastructure · roadmap · multi-agent · quant · backtesting
