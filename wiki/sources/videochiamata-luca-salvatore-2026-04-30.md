---
title: Videochiamata Luca-Salvatore (2026-04-30)
type: source
tags:
  - source
  - ingest
  - strategy
  - architecture
sources: []
raw_source_path: raw/audio/videochimata 30 apri.m4a
created: 2026-04-30
updated: 2026-04-30
confidence: high
status: reviewed
related:
  - "[[sources/conversazione-luca-salvatore-2026-04-28-30]]"
  - "[[concepts/modular-trading-agent-architecture]]"
  - "[[kanban-project-status]]"
  - "[[build/system-map]]"
---

# Videochiamata Luca-Salvatore (2026-04-30)

Conversazione approfondita sulla struttura del progetto, la filosofia della Wiki e l'architettura tecnica del Trading Agent.

## Contesto

Seconda grande sessione di allineamento tra Luca e Salvatore. La prima parte è dedicata alla spiegazione dello strumento (Obsidian + LLM Wiki) e la seconda alla progettazione dei moduli del Trading Agent.

## File sorgenti

- `raw/audio/2026-04-30 11-15-40.m4a` (Trascrizione: `raw/audio/2026-04-30 11-15-40.txt`)
- `raw/audio/videochimata 30 apri.m4a` (Trascrizione: `raw/audio/videochimata 30 apri.m4a.transcription.md`)

## Key Takeaways

### 1. Filosofia del Progetto (LLM Wiki)
- Ispirazione da **Andrew Karpathy**: struttura a due cartelle (`raw/` e `wiki/`).
- La Wiki è il "cervello" del progetto, mantenuta da un agente (Codex/Claude) per evitare il decadimento della documentazione.
- Uso di **Artifacts** (Kanban, Canvas, Bases) per visualizzare lo stato operativo.

### 2. Architettura del Trading Agent (Moduli)
Il sistema è immaginato come un ecosistema **multi-agente** con compiti granulari:
- **News Module**: Scraping e pre-elaborazione news (es. impatto notizie macroeconomiche).
- **Technical Analysis Module**: Individuazione di pattern, soglie di prezzo (supporti/resistenze) e bias di mercato (es. effetto domino degli stop loss).
- **Risk Management Module**: Gestione leva, esposizione, commissioni e **Trailing Stop Loss**.
- **Reinforcement Learning (Weighting)**: Un modulo che decide quanto pesare gli altri moduli nel tempo in base alle performance.
- **Fine-tuning / Continuous Learning**: Idea di addestrare un modello locale sui dati storici e sui ragionamenti passati dell'agente.

### 3. Strategia Operativa
- **Augmentation vs Autonomy**: Partire con una **Dashboard di potenziamento** (augmentazione) del trader umano prima di passare all'autonomia completa.
- **Dati non strutturati**: Focus sulla quantificazione di dati "non quantificabili" (news, sentiment, bias psicologici).
- **Benchmark**: Citati progetti come "Alfa Arena", "Rizzo Trading" e il profilo "NeuroEspresso" (Silvio Baratto).
- **Riferimento accademico**: Citato un paper di ricerca della **Cornell University** (struttura multi-agente con Researcher, Analyst, Trader, Risk Manager).

### 4. Road-map immediata
- **Task 1**: Definire gli artifact (mappe mentali, kanban).
- **Task 2**: Raccolta informazioni e studio di progetti esistenti (senza fare fork, ma partendo "from scratch" per avere pieno controllo).
- **Task 3**: Progettazione granulare Input/Output per ogni modulo.

## Tensioni e Decisioni
- **Decisione**: Non fare un semplice fork, ma costruire "from scratch" usando la conoscenza distillata da altri progetti.
- **Tensione**: Crypto vs Equity. Equity è più spiegabile ma complesso; Crypto è più accessibile tecnicamente. La scelta rimane aperta ma orientata alla ricerca di metriche solide.
- **Innovazione**: L'uso di un agente che analizza i propri ragionamenti passati per migliorare quelli futuri.

## Prossimi Passi
- [ ] Creare la mappa del sistema aggiornata in [[build/system-map]].
- [ ] Inizializzare il registro delle decisioni in [[decisions/decision-log]].
- [ ] Approfondire i moduli nominati (Risk, News, TA).
