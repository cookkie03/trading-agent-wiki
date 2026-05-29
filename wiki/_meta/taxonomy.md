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
| `overview`  | `wiki/`                     | sì     | `overview.md` unico, entry point |
| `meta`      | `wiki/_meta/`               | sì     | Navigazione del vault (index, log, hot-cache, taxonomy, glossario, onboarding) |
| `system`    | `wiki/system/`              | sì     | Spec del software: architettura, moduli, stack, decisioni, idee, MVP (dominio Luca) |
| `module`    | `wiki/system/modules/`      | sì     | Un file per **area** del sistema, allineato ad `architettura.canvas`: `data-layer`, `agents`, `execution`, `quant-backtesting` |
| `strategy`  | `wiki/strategy/`            | sì     | Conoscenza di mercato e trading: metodi, indicatori, metriche (dominio Salvatore) |
| `prior-art` | `wiki/prior-art/`           | sì     | Sistemi, paper e librerie esterni studiati o forkati: `tradingagents/`, `libraries/`, `papers/` |
| `synthesis` | `wiki/syntheses/`           | sì     | Analisi trasversali, ricerca multi-fonte |
| `artifact`  | `wiki/artifacts/`           | sì     | Canvas, board, schemi visuali (canvas di design in `artifacts/architecture/`) |
| `build`     | `wiki/build/`               | no     | **Rinominato in `system/`** (2026-05-29) |
| `source`    | `wiki/references/`          | no     | **Eliminato** (2026-05-29): le call sono dissolte nelle pagine tematiche (provenienza inline + grezzi in `raw/archived/`); il prior-art esterno è migrato in `prior-art/` |
| `external`  | `wiki/references/external/` | no     | **Eliminato** → migrato in `prior-art/libraries/` e `prior-art/tradingagents/` |
| `list`      | `wiki/lists/`               | no     | Non usato in questo vault |
| `entity`    | `wiki/agents/`              | no     | Eliminato — contenuto migrato in `prior-art/` |
| `knowledge` | `wiki/theory/`              | no     | Eliminato — contenuto migrato in `system/` |
| `operation` | `wiki/ops/`                 | no     | Eliminato — contenuto migrato in `system/` e `artifacts/` |
| `decision`  | `wiki/decisions/`           | no     | Eliminato — migrato in `system/decision-log.md` |
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
build · synthesis · artifact · overview · source *(usato solo da `prior-art/` per materiale esterno)*

### Status
draft · active · reviewed · verified · stale · archived · done

### Priority
priority/high · priority/medium · priority/low

### Areas
area/software · area/research · area/market · area/ops · area/strategy

### Project Tags
architecture · strategy · execution · ingest · market-structure · infrastructure · roadmap · multi-agent · quant · backtesting
