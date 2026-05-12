---
vault_type: hybrid
vault_name: "trading-agent-wiki"
language: it
---

# Taxonomy

## Ruoli semantici → Path

I ruoli semantici sono fissi. I path sono specifici di questo vault.
Le skill wiki-* non usano mai path hardcodati: leggono sempre questa tabella.

| Ruolo       | Path              | Attivo |
|-------------|-------------------|--------|
| `source`    | `wiki/references/`| sì     |
| `knowledge` | `wiki/theory/`    | sì     |
| `entity`    | `wiki/agents/`    | sì     |
| `synthesis` | `wiki/syntheses/` | sì     |
| `decision`  | `wiki/decisions/` | sì     |
| `question`  | `wiki/questions/` | sì     |
| `operation` | `wiki/ops/`       | sì     |
| `artifact`  | `wiki/artifacts/` | sì     |
| `build`     | `wiki/build/`     | sì     |
| `list`      | `wiki/lists/`     | no     |

## Cartelle raw → Path

| Tipo      | Path              |
|-----------|-------------------|
| default   | `raw/`            |
| audio     | `raw/audio/`      |
| documents | `raw/articles/`   |
| notes     | `raw/notes/`      |
| archived  | `raw/archived/`   |

## Tag Taxonomy — Trading Agent

> Solo questi tag sono canonici all'inizio. Aggiungere qui nuovi tag prima di usarli in modo stabile.

## Type
source · entity · concept · synthesis · question · decision · ops · build · artifact · overview

## Status
draft · active · reviewed · verified · stale · archived · done

## Priority
priority/high · priority/medium · priority/low

## Areas
area/software · area/research · area/market · area/ops · area/strategy

## Project Tags
architecture · strategy · execution · ingest · market-structure · experimentation · infrastructure · roadmap
