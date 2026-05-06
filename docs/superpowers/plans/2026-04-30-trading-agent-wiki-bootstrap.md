# Trading Agent Wiki Bootstrap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Initialize the `trading-agent-wiki` vault with its working folder structure, local operating rules, bootstrap meta files, and an overview page that supports software, research, market, and operational project work.

**Architecture:** Build the vault from the root inward. First create the directory layout, then add the local `AGENTS.md` constitution, then bootstrap the `_meta/` files and `overview.md`, keeping the initial taxonomy and operational model intentionally small. The result should be a usable wiki immediately, with room to expand through future ingest and artifacts.

**Tech Stack:** Obsidian markdown, vault folders, local repository filesystem

---

### Task 1: Create the vault directory skeleton

**Files:**
- Create: `raw/articles/`
- Create: `raw/papers/`
- Create: `raw/audio/`
- Create: `raw/transcripts/`
- Create: `raw/notes/`
- Create: `raw/archived/`
- Create: `wiki/_meta/`
- Create: `wiki/sources/`
- Create: `wiki/concepts/`
- Create: `wiki/entities/`
- Create: `wiki/syntheses/`
- Create: `wiki/questions/`
- Create: `wiki/decisions/`
- Create: `wiki/ops/`
- Create: `wiki/build/`
- Create: `wiki/artifacts/`

- [ ] **Step 1: Create the raw intake folders**

Run: `mkdir -p raw/articles raw/papers raw/audio raw/transcripts raw/notes raw/archived`
Expected: command exits successfully with no output

- [ ] **Step 2: Create the wiki folders**

Run: `mkdir -p wiki/_meta wiki/sources wiki/concepts wiki/entities wiki/syntheses wiki/questions wiki/decisions wiki/ops wiki/build wiki/artifacts`
Expected: command exits successfully with no output

- [ ] **Step 3: Verify the directory skeleton**

Run: `find raw wiki -maxdepth 2 -type d | sort`
Expected:

```text
raw
raw/archived
raw/articles
raw/audio
raw/notes
raw/papers
raw/transcripts
wiki
wiki/_meta
wiki/artifacts
wiki/build
wiki/concepts
wiki/decisions
wiki/entities
wiki/ops
wiki/questions
wiki/sources
wiki/syntheses
```

- [ ] **Step 4: Commit**

```bash
git add raw wiki
git commit -m "chore: create trading agent wiki structure"
```

### Task 2: Write the local vault constitution

**Files:**
- Create: `AGENTS.md`

- [ ] **Step 1: Write the vault-specific operating contract**

Create `AGENTS.md` with:

```markdown
# Trading Agent Wiki

> Vault operativo per il progetto `trading-agent`. Obsidian e il wiki sono la memoria condivisa del progetto; gli agent lavorano sopra questa struttura, non fuori da essa.

## Identità del Vault

Questo vault è una wiki focalizzata sul progetto `trading-agent`.
Serve contemporaneamente come:

- base operativa del progetto
- knowledge base di ricerca
- memoria condivisa per decisioni e stato del software

Il progetto ha una natura ibrida:

- software
- ricerca
- economica e di mercato

Il vault è condiviso da due collaboratori e deve restare leggibile sia per gli umani sia per gli agent.

**Lingua**: italiano come default, inglese per termini tecnici, nomi propri e citazioni.

## Struttura del Vault

```text
vault-root/
├── AGENTS.md
├── raw/
│   ├── articles/
│   ├── papers/
│   ├── audio/
│   ├── transcripts/
│   ├── notes/
│   └── archived/
└── wiki/
    ├── _meta/
    │   ├── index.md
    │   ├── log.md
    │   ├── taxonomy.md
    │   └── hot-cache.md
    ├── overview.md
    ├── sources/
    ├── concepts/
    ├── entities/
    ├── syntheses/
    ├── questions/
    ├── decisions/
    ├── ops/
    ├── build/
    └── artifacts/
```

## Regole Fondamentali

1. `raw/` è la zona di ingresso dei materiali grezzi. I file non si cancellano; dopo ingest si spostano in `raw/archived/`.
2. `wiki/` è la memoria strutturata del progetto e può essere aggiornata liberamente dagli agent.
3. `ops/` descrive cosa stiamo facendo adesso; `build/` descrive il software; il resto del wiki conserva conoscenza e contesto.
4. Ogni operazione rilevante va registrata in `wiki/_meta/log.md`.
5. `wiki/_meta/hot-cache.md` va letto a inizio sessione e aggiornato a fine sessione.
6. La tassonomia dei tag vive in `wiki/_meta/taxonomy.md`; evitare tag arbitrari non registrati.
7. Gli artifact visivi convivono con le note markdown e vanno salvati in `wiki/artifacts/`, con link dalle pagine correlate.

## Frontmatter Standard

```yaml
---
title: ""
type: source | entity | concept | synthesis | question | decision | ops | build | artifact | overview
tags: []
sources: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: draft | active | reviewed | verified | stale | archived | done
related: []
confidence: low | medium | high
priority: low | medium | high
area: research | market | software | ops | strategy
decision_status: proposed | decided | superseded
---
```

Usare solo i campi rilevanti per la pagina. `priority`, `area` e `decision_status` sono opzionali.

## Query Operative

```dataview
TABLE type, status, updated
FROM "wiki"
WHERE type != "overview"
SORT updated DESC
LIMIT 20
```

```dataview
TABLE title, status, priority, updated
FROM "wiki/ops"
SORT priority DESC, updated DESC
```

```dataview
TABLE title, decision_status, updated
FROM "wiki/decisions"
SORT updated DESC
```

```dataview
TABLE title, area, status, updated
FROM "wiki/build"
SORT updated DESC
```

```dataview
TABLE title, confidence, updated
FROM "wiki/syntheses"
SORT updated DESC
```

## Skill Rilevanti

- `obsidian-markdown`: per tutte le note markdown del vault
- `json-canvas`: per mappe, schemi e canvas in `wiki/artifacts/`
- `obsidian-bases`: per viste strutturate future
- `defuddle`: per pulire contenuti web prima dell’ingest
- `obsidian-cli`: per integrazioni CLI con Obsidian
```

- [ ] **Step 2: Verify the file exists and is readable**

Run: `sed -n '1,260p' AGENTS.md`
Expected: the file prints with sections for identity, structure, rules, frontmatter, queries, and skills

- [ ] **Step 3: Commit**

```bash
git add AGENTS.md
git commit -m "docs: add trading agent wiki instructions"
```

### Task 3: Bootstrap the meta layer

**Files:**
- Create: `wiki/_meta/index.md`
- Create: `wiki/_meta/log.md`
- Create: `wiki/_meta/taxonomy.md`
- Create: `wiki/_meta/hot-cache.md`

- [ ] **Step 1: Create the wiki index**

Create `wiki/_meta/index.md` with:

```markdown
# Wiki Index — Trading Agent

> Catalogo operativo del vault. Aggiornato dall'agent quando la wiki cresce.

## Overview
- [[overview]] — ingresso principale del progetto

## Sources (0)
*(nessun source ancora ingested)*

## Concepts (0)
*(nessun concept ancora registrato)*

## Entities (0)
*(nessuna entity ancora registrata)*

## Syntheses (0)
*(nessuna synthesis ancora registrata)*

## Questions (0)
*(nessuna question ancora registrata)*

## Decisions (0)
*(nessuna decision ancora registrata)*

## Ops (0)
*(nessuna pagina operativa ancora registrata)*

## Build (0)
*(nessuna pagina build ancora registrata)*

## Artifacts (0)
*(nessun artifact ancora registrato)*
```

- [ ] **Step 2: Create the append-only log**

Create `wiki/_meta/log.md` with:

```markdown
# Wiki Log — Trading Agent

> Log append-only. Grep utile: `grep "^## \[" wiki/_meta/log.md | tail -10`

## [2026-04-30] init | Inizializzazione vault
- **Pages created**: [[overview]], [[_meta/index]], [[_meta/log]], [[_meta/taxonomy]], [[_meta/hot-cache]]
- **Vault type**: project wiki
- **Project shape**: software + research + economic
- **Collaborators**: 2
- **Notes**: bootstrap iniziale della wiki
```

- [ ] **Step 3: Create the canonical taxonomy**

Create `wiki/_meta/taxonomy.md` with:

```markdown
# Tag Taxonomy — Trading Agent

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
```

- [ ] **Step 4: Create the hot cache template**

Create `wiki/_meta/hot-cache.md` with:

```markdown
# Hot Cache — Trading Agent

> Contesto di sessione recente. Aggiornare a fine sessione. Tenere entro 300 righe.

## Ultima sessione
- **Data**: 2026-04-30
- **Agent**: Codex
- **Operazioni**: design wiki, piano bootstrap, inizializzazione vault

## Pagine toccate
- [[overview]]
- [[_meta/index]]
- [[_meta/log]]
- [[_meta/taxonomy]]
- [[AGENTS]]

## Pending ingest
*(nessuno ancora)*

## Next steps
- [ ] Iniziare il primo ingest da `raw/`
- [ ] Creare la prima pagina operativa in `wiki/ops/`
- [ ] Creare la prima pagina software in `wiki/build/`
- [ ] Testare il primo artifact in `wiki/artifacts/`
```

- [ ] **Step 5: Verify the meta files**

Run: `find wiki/_meta -maxdepth 1 -type f | sort`
Expected:

```text
wiki/_meta/hot-cache.md
wiki/_meta/index.md
wiki/_meta/log.md
wiki/_meta/taxonomy.md
```

- [ ] **Step 6: Commit**

```bash
git add wiki/_meta
git commit -m "docs: bootstrap trading agent wiki metadata"
```

### Task 4: Create the overview page

**Files:**
- Create: `wiki/overview.md`

- [ ] **Step 1: Write the overview page**

Create `wiki/overview.md` with:

```markdown
---
title: "Trading Agent — Overview"
type: overview
tags:
  - overview
  - strategy
created: 2026-04-30
updated: 2026-04-30
status: active
related: []
confidence: high
---

# Trading Agent

Questa wiki è la base operativa condivisa del progetto `trading-agent`.
Serve a raccogliere fonti, distillare conoscenza, documentare il software e mantenere visibile lo stato del progetto.

## Natura del progetto

Il progetto combina tre dimensioni principali:

- software
- ricerca
- economica e di mercato

La struttura della wiki è pensata per non forzare una separazione artificiale troppo presto, ma per rendere queste dimensioni navigabili man mano che il materiale cresce.

## Stato corrente

Vault appena inizializzato.
Non ci sono ancora source ingestite, ma la struttura base è pronta per iniziare.

## Aree principali

- [[ops]] — stato vivo, priorità e prossimi passi
- [[build]] — conoscenza strettamente software-oriented
- [[sources]] — fonti ingestite
- [[concepts]] — idee, modelli e terminologia
- [[entities]] — soggetti e strumenti rilevanti
- [[syntheses]] — analisi e sintesi ad alto valore
- [[decisions]] — decisioni prese e loro motivazioni
- [[questions]] — dubbi aperti e direzioni di ricerca
- [[artifacts]] — schemi, mappe e rappresentazioni visive

## Uso previsto

Il flusso di base è:

1. mettere materiale nuovo in `raw/`
2. ingestire il materiale importante in `wiki/sources/`
3. propagare i risultati in conoscenza, decisioni, stato operativo e documentazione software

## Prossimo passo consigliato

Iniziare da una prima fonte reale in `raw/`, oppure creare una prima pagina in `wiki/ops/` che descriva il punto di partenza attuale del progetto.
```

- [ ] **Step 2: Verify the page content**

Run: `sed -n '1,260p' wiki/overview.md`
Expected: the file prints valid frontmatter plus sections for project nature, current state, key areas, and next steps

- [ ] **Step 3: Commit**

```bash
git add wiki/overview.md
git commit -m "docs: add trading agent overview page"
```

### Task 5: Final verification pass

**Files:**
- Verify: `AGENTS.md`
- Verify: `wiki/_meta/index.md`
- Verify: `wiki/_meta/log.md`
- Verify: `wiki/_meta/taxonomy.md`
- Verify: `wiki/_meta/hot-cache.md`
- Verify: `wiki/overview.md`

- [ ] **Step 1: Verify the full bootstrap tree**

Run: `find . -maxdepth 3 \\( -type d -o -type f \\) | sort`
Expected: tree includes `raw/`, `wiki/`, meta files, `overview.md`, `AGENTS.md`, and the saved design/plan docs

- [ ] **Step 2: Verify no required bootstrap file is missing**

Run: `test -f AGENTS.md && test -f wiki/overview.md && test -f wiki/_meta/index.md && test -f wiki/_meta/log.md && test -f wiki/_meta/taxonomy.md && test -f wiki/_meta/hot-cache.md`
Expected: command exits with status 0

- [ ] **Step 3: Commit**

```bash
git add AGENTS.md raw wiki docs
git commit -m "feat: initialize trading agent wiki"
```
