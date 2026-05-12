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
├── raw/
│   ├── articles/
│   ├── audio/
│   ├── notes/
│   ├── daily-notes/
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


## Entry Point Operativo

Per il lavoro quotidiano, la pagina di ingresso consigliata è [[ops/dashboard]].

Ordine pratico di lettura a inizio sessione:

1. `wiki/_meta/hot-cache.md`
2. `wiki/overview.md`
3. `wiki/ops/dashboard.md`
4. eventuali pagine operative o build collegate

## Regole Fondamentali

1. `raw/` è la zona di ingresso dei materiali grezzi. I file non si cancellano; dopo ingest si spostano in `raw/archived/`.
2. `wiki/` è la memoria strutturata del progetto e può essere aggiornata liberamente dagli agent.
3. `ops/` descrive cosa stiamo facendo adesso; `build/` descrive il software; il resto del wiki conserva conoscenza e contesto.
4. Ogni operazione rilevante va registrata in `wiki/_meta/log.md`.
5. `wiki/_meta/hot-cache.md` va letto a inizio sessione e aggiornato a fine sessione.
6. La tassonomia dei tag vive in `wiki/_meta/taxonomy.md`; evitare tag arbitrari non registrati.
7. Gli artifact visivi convivono con le note markdown e vanno salvati in `wiki/artifacts/`, con link dalle pagine correlate.
8. Questo vault non usa `daily-notes/` come flusso principale. Se una skill cita le daily notes, trattarlo come opzionale e non come prerequisito operativo.

## Adattamenti Locali alle Wiki Skill

Le skill in `.claude/skills/` sono la base operativa del vault, ma alcune vanno adattate alla struttura locale di `trading-agent-wiki`.

### Mapping cartelle

- Quando una skill cita `raw/pdfs/` o `raw/papers/`, in questo vault va letto come `raw/articles/` (o direttamente nella root `raw/` per file singoli come PDF).
- Quando una skill cita `raw/calls/`, in questo vault va interpretato come combinazione di `raw/audio/` e `raw/notes/`, a seconda del materiale disponibile.
- Quando una skill cita `daily-notes/`, qui va considerato un flusso non usato per default (la cartella `raw/daily-notes/` esiste ma è vuota/non operativa).

### Regola pratica

In caso di conflitto tra una skill generica e la struttura reale del vault, vince sempre la struttura reale dichiarata in questo `CLAUDE.md`.

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

## Skill Operative

### Core wiki workflow

- `wiki-ingest`: skill principale per portare nuova conoscenza nel vault o aggiornare pagine esistenti
- `wiki-query`: per briefing, stato progetto, domande sul vault e recupero conoscenza; per i briefing partire da [[ops/dashboard]]
- `wiki-save`: per trasformare analisi o decisioni emerse in pagine permanenti
- `wiki-lint`: per health check strutturali, tag, link, stale pages e gap di manutenzione
- `wiki-artifact`: per generare canvas, board, Dataview e altri artifact collegati alla wiki

### Preprocessing e ingest multimediale

- `wiki-preprocess`: da usare prima dell’ingest quando arrivano file in formati non immediatamente leggibili, come audio, pdf, ecc...
- `crawl4ai`: da usare quando si parte da URL o articoli web prima di salvarli in `raw/`
### Sintassi e formati Obsidian

- `obsidian-markdown`: obbligatoria per note `.md`, frontmatter, wikilink, callout, embed e Dataview inline
- `json-canvas`: obbligatoria per file `.canvas` in `wiki/artifacts/` o in altre aree del vault
- `obsidian-bases`: per eventuali viste `.base` dinamiche

### Skill non centrali ma disponibili

- `wiki-init`: utile solo per bootstrap iniziale o riprogettazione radicale del vault, non per il lavoro quotidiano
- `docx`, `pptx`, `xlsx`: usare solo quando il progetto richiede output esterni in quei formati

## Trigger Operativi Consigliati

- "ingest [file]" o "processa questo" → `wiki-ingest`
- "briefing", "cosa c'è da fare?", "stato del progetto" → `wiki-query`
- "salva questa risposta" o "formalizza questa decisione" → `wiki-save`
- "lint" o "com'è messo il wiki?" → `wiki-lint`
- "crea uno schema", "fai una mappa", "fammi una board" → `wiki-artifact`
- "preprocessa gli audio" o "trascrivi questi file" → `wiki-preprocess`

## Policy per Artifact

- Mappe concettuali e schemi visuali: preferire `.canvas` con `json-canvas`
- Dashboard o tabelle vive: preferire Dataview inline o `.base` con `obsidian-bases`
- Task board operative: usare `wiki-artifact` e salvare in `wiki/ops/`
- Ogni artifact rilevante va collegato da almeno una pagina markdown e registrato nel log
