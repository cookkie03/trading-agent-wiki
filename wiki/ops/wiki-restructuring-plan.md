---
title: "Piano di Ristrutturazione Wiki"
type: ops
tags:
  - infrastructure
  - ops
created: 2026-05-13
updated: 2026-05-13
status: draft
priority: high
area: ops
related:
  - "[[_meta/index]]"
  - "[[_meta/taxonomy]]"
  - "[[references/videochiamata-luca-salvatore-2026-05-13]]"
---

# Piano di Ristrutturazione Wiki

> Origine: videochiamata Luca-Salvatore del 2026-05-13. Luca ha mostrato a Salvatore la wiki su Obsidian e hanno concluso che la struttura attuale va ristrutturata. La ristrutturazione sarà fatta con Claude in una sessione dedicata, poi spiegata a Salvatore.

**Stato**: PIANIFICATA — non ancora eseguita.

---

## Problema

La struttura attuale della wiki è generica e orientata al vault-model standard (theory/, references/, agents/...). Non riflette la struttura operativa reale del progetto, che è organizzata per:
- **moduli software** (A, C, D, Risk Analyst...)
- **strategie quantitative** (con parametri, metodi, validazione)
- **workflow del team** (Luca vs Salvatore, con ruoli diversi)

Attualmente manca una sezione dedicata alle strategie quant e alla struttura per moduli nel senso software.

---

## Struttura proposta (da Salvatore, 2026-05-13)

L'idea emersa in call è di creare una sezione wiki che rispecchi la struttura dell'agente stesso:

```
wiki/
├── _meta/          (invariata)
├── overview.md     (invariato)
├── references/     (invariata — fonti e call)
├── theory/         (invariata — concetti generali)
├── decisions/      (invariata)
├── questions/      (invariata)
├── syntheses/      (invariata)
│
├── agents/         (rinominare/espandere → moduli/)
│   └── ...         
│
├── build/          (invariata — design software)
│
├── ops/            (invariata — operativo corrente)
│
├── strategie/      ← NUOVA SEZIONE (o dentro quant/)
│   ├── index.md    ← panoramica di tutte le strategie
│   ├── quant/
│   │   ├── parametri/      ← un file per parametro (P/E, RSI, MACD, OLS...)
│   │   ├── metodi/         ← un file per metodo (regressione, trend-following...)
│   │   ├── obiettivi/      ← cosa si vuole ottimizzare (Sharpe, Sortino...)
│   │   └── validazione/    ← un file per metrica di valutazione
│   └── news/
│       └── ...
│
└── artifacts/      (invariata)
```

### Principio di linking
Ogni file `metodi/regressione.md` contiene:
- descrizione del metodo
- link ai file `parametri/` che usa come input
- link ai file `validazione/` che produce come output

Quando l'agente fa una query, apre tutti i link e legge il contesto completo. Brainstorming diventa possibile.

---

## Cosa deve fare Salvatore (ruolo nella ristrutturazione)

Salvatore non deve ristrutturare la wiki — deve **popolarla di contenuto grezzo**:

1. Cercare strategie quant (value, factor, momentum, research paper)
2. Raccoglierle in Raw/ — sia quelle buone che quelle dubbie (scrivere "penso non sia valida perché...")
3. Usare Daily Notes per appunti volanti e domande
4. NON creare file wiki direttamente

Luca poi farà ingest e costruirà le pagine strutturate.

---

## Checklist per la ristrutturazione

- [ ] Decidere nome finale della sezione: `strategie/` o `quant/` o dentro `wiki/`
- [ ] Aggiornare `taxonomy.md` con i nuovi path
- [ ] Creare le cartelle e i file indice
- [ ] Migrare il contenuto quant esistente (theory/, syntheses/)
- [ ] Aggiornare `index.md` con tutte le nuove voci
- [ ] Aggiornare i link interni
- [ ] Spiegare a Salvatore la nuova struttura

---

## Riferimenti

- [[references/videochiamata-luca-salvatore-2026-05-13]] — sessione in cui è emersa l'esigenza
- [[_meta/taxonomy]] — taxonomy attuale da aggiornare
- [[_meta/index]] — index attuale da aggiornare
