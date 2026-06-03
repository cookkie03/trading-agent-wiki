# Trading Agent Wiki

> Vault operativo per il progetto `trading-agent`. Wiki = memoria condivisa del progetto.
> Gli agent lavorano sopra questa struttura, non fuori da essa.

## Identità

Wiki focalizzata sul progetto `trading-agent`. Base operativa, knowledge base, memoria condivisa per decisioni e stato del software. Condivisa da Luca (software) e Salvatore (mercati).

**Lingua**: italiano come default, inglese per termini tecnici, nomi propri e citazioni.

## Source of Truth della struttura

- **Path canonici** → `wiki/_meta/taxonomy.md` — mapping ruoli semantici → path reali.
  Non usare path hardcodati: leggere sempre taxonomy.md prima di scrivere o spostare file.
  Se la struttura cambia, si aggiorna taxonomy.md — **non questo file**.
- **Stato sessione** → `wiki/_meta/hot-cache.md` — leggere all'inizio, aggiornare alla fine.
- **Catalogo pagine** → `wiki/_meta/index.md` — elenco di tutte le pagine attive.

## Entry Point

Inizio sessione — leggere in ordine:
1. `wiki/_meta/hot-cache.md`
2. `wiki/overview.md`
3. pagine operative o build collegate (vedere hot-cache per i link rilevanti)

## Centrale operativa — la Board

`wiki/artifacts/project-board.md` è la **centrale operativa** e il **file di partenza per le valutazioni umane**. Regole:

1. **Riferimento sempre presente**: ogni card azionabile (task, decisione, idea) termina con il link alla pagina di dettaglio `→ [[pagina]]`. Niente voci "orfane": se una cosa va decisa/fatta, deve puntare a dove si approfondisce. Se la pagina non esiste ancora, **crearla**.
2. **Owner esplicito**: ogni card e ogni pagina indica per chi è — 🛠 Luca (software) · 📈 Salvatore (mercato) · 🔀 condiviso. Sulle pagine l'owner si esprime col campo frontmatter `area` (`software`/`strategy`/`market`/…) e, dove utile, col marker nell'index.
3. **La board è uno specchio aggiornato**: ad ogni sessione, ogni nuova decisione/idea/task — anche non richiesto esplicitamente — va riflesso nella board, nella categoria giusta (💡 Idee · 🔴 Da fare · 🟡 In corso · 🟠 Decisioni da prendere · ✅ Fatto). Le decisioni chiuse migrano in ✅ e nel `decision-log`.
4. **Creare pagine quando serve**: salvare le informazioni in pagine dedicate, facilmente consultabili da un umano, ogni volta che è utile — non lasciarle solo nei log o nella chat.

## Regole Fondamentali

1. `raw/` è la zona di ingresso. Dopo l'ingest i file vanno in `raw/archived/` — non si cancellano.
2. `wiki/` è la memoria strutturata. Può essere aggiornata liberamente dagli agent.
3. Ogni operazione rilevante va registrata in `wiki/_meta/log.md` (append-only).
4. Tag canonici in `wiki/_meta/taxonomy.md` — non usare tag arbitrari non registrati lì.

## Skill Operative

Usare sempre le skill in `.claude/skills/` per le operazioni sul vault.

| Trigger | Skill |
|---------|-------|
| "ingest", "processa questo", "aggiungi alla wiki" | `wiki-ingest` |
| "briefing", "stato del progetto", "cosa c'è da fare?" | `wiki-query` |
| "salva questa risposta", "formalizza questa decisione" | `wiki-save` |
| "lint", "com'è messo il wiki?" | `wiki-lint` |
| "crea uno schema", "fai una mappa", "crea una board" | `wiki-artifact` |
| "preprocessa audio/pdf" | `wiki-preprocess` |
| file `.md` o frontmatter | `obsidian-markdown` |
| file `.canvas` | `json-canvas` |

## Frontmatter Standard

```yaml
---
title: ""
type: source | synthesis | build | artifact | overview
tags: []
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: draft | active | reviewed | verified | stale | archived | done
related: []
confidence: low | medium | high
---
```

Campi opzionali (usare solo se rilevanti): `raw_source_path`, `sources`, `priority`, `area`.
Valori canonici per `type` e `tags` → `wiki/_meta/taxonomy.md`.

## Adattamenti Locali alle Skill

- Skill cita `raw/pdfs/` o `raw/papers/` → leggere come `raw/articles/`
- Skill cita `raw/calls/` → leggere come `raw/audio/` e/o `raw/notes/`
- Skill cita `daily-notes/` → flusso non operativo in questo vault
- In conflitto skill ↔ CLAUDE.md → vince CLAUDE.md
- In conflitto CLAUDE.md ↔ taxonomy.md sui path → vince taxonomy.md
