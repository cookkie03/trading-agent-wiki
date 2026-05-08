---
title: "Videochiamata Luca-Salvatore (2026-05-06)"
type: source
tags:
  - source
  - ingest
  - architecture
  - analysis
raw_source_path: "raw/transcripts/2026-05-06 13-29-25.txt"
created: 2026-05-06
updated: 2026-05-06
confidence: high
status: reviewed
related:
  - "[[sources/videochiamata-luca-salvatore-2026-04-30]]"
  - "[[build/system-map]]"
  - "[[ops/kanban-project-status]]"
  - "[[concepts/modular-trading-agent-architecture]]"
---

# Videochiamata Luca-Salvatore (2026-05-06)

Trascrizione dell'allineamento del 6 maggio. La chiamata verte sull'uso dell'AI per fare Analisi Tecnica nel trading di crypto, sulle limitazioni degli LLM rispetto agli algoritmi tradizionali e sul workflow di ingestione della conoscenza tecnica (indicatori e pattern) nel vault.

## Contesto
- **Analisi Tecnica vs Fondamentale**: Luca riassume i due approcci, evidenziando che l'Analisi Tecnica (TA) nel mondo crypto si basa principalmente sull'osservazione di grafici, pattern, e indicatori (es. medie mobili, Fibonacci, supporti, resistenze).
- **Scetticismo iniziale**: C'è incertezza sul fatto che un LLM sia in grado di leggere un grafico e individuare pattern puramente "guardando le candele" rispetto ad avere dei veri dati elaborati.

## Analisi Tecnica e Traduzione in Funzioni AI
- **Dal Grafico ai Numeri**: Salvatore suggerisce che per fare Analisi Tecnica con un'AI non bisogna farle "leggere" le immagini del grafico, ma tradurre gli indicatori visivi (es. incrocio di medie mobili, trend, spike) in **funzioni Python**.
- **Approccio multi-agente**: Un agente isolato si occuperà dell'analisi tecnica, prendendo in input serie storiche processate e tradotte in numeri o pattern discreti dalle funzioni.
- **Validazione dei segnali**: L'AI considererà una serie di indicatori come *segnali*. La coerenza di più segnali (es. medie mobili + pattern di rottura) confermerà la validità di un'ipotesi di trade.

## Workflow per l'Ingestione di Nuovi Indicatori (Obsidian)
- **Definizione della Guida**: Si concorda sulla necessità di creare una sorta di "manuale di Analisi Tecnica" ottimizzato per l'AI, ovvero delle liste strutturate e gerarchiche con istruzioni chiare su cosa cercare.
- **Raccolta manuale**: Luca si occuperà di studiare indicatori e pattern (traendoli anche da appunti passati come quelli presi tramite "Crypto Gateway"), validarli manualmente, e appuntarli in Obsidian.
- **Automatizzazione del Vault**: Salvatore chiarisce che usando strumenti come le *Daily Notes* e l'LLM Wiki, basta scrivere o importare i concetti grezzi; sarà poi l'AI (o un coding agent) a categorizzarli, strutturarli e inserirli nella corretta sezione tecnica (es. "analisi volumetrica").

## Action Items
- Luca: Raccogliere e studiare i principali indicatori di analisi tecnica, creare appunti "raw" su Obsidian.
- Luca/Salvatore: Verificare e validare gli indicatori trovati prima di trasformarli in prompt definitivi.
- Sviluppo: Iniziare a codificare le funzioni Python che traducano in numeri e "eventi" i concetti dell'analisi tecnica (es. rilevamento dell'incrocio di medie).
