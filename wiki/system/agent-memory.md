---
title: "Memoria degli agenti — intra-task e inter-task"
type: build
tags:
  - multi-agent
  - architecture
  - learning
created: 2026-06-07
updated: 2026-06-07
status: draft
priority: medium
area: software
related:
  - "[[system/modules/agents]]"
  - "[[system/learning-feedback-loop]]"
  - "[[system/state-schemas]]"
  - "[[system/canvas-code-mapping]]"
confidence: medium
---

# Memoria degli agenti — intra-task e inter-task

> Due livelli distinti. L'**intra-task** è implementato; l'**inter-task** è un tema di design **da affrontare successivamente** (input di Luca 2026-06-07): come ottimizzare la memoria persistente degli agenti *tra* i task, per imparare dai casi/errori precedenti.

## Livello 1 — memoria intra-task ✅ (fatto)
La finestra di contesto **per-agente** durante una singola analisi: `brain/agent_context.py` (`AgentContext`), strutturata a sezioni cucite sul compito, parte dal contesto iniettato (warm start) e accumula i tool result mantenendosi intatta per tutto il task (round + revisioni). Trasportata in `BrainState.contexts`.

## Livello 2 — memoria inter-task 🔵 (da progettare/discutere)
Obiettivo: l'agente ricorda/recupera **come ci si è comportati in casi precedenti** e impara dagli errori, *tra* analisi diverse nel tempo.

### Fondazione già presente
- **`decision_log`**: ogni decisione con opinioni per-agente + esito + link al trade.
- **`trades.exit_reason`** (tp/sl/rating): com'è finito ogni trade.
- **`past_context`** (campo dello state): predisposto, oggi non popolato.
Quindi il *substrato dati* esiste; manca il **layer di recupero/sintesi** sopra.

### Spazio delle opzioni (da valutare, non mutuamente esclusive)
1. **Riassunto rolling nel system prompt** — una parte del system prompt fornisce un *digest standard sempre aggiornato* di tutta l'attività fatta finora (per agente / per ticker). Pro: zero chiamate; sempre presente. Contro: spazio nel prompt, va mantenuto sintetico.
2. **Tool di recupero super-parametrizzati** — istruire (a system prompt) ogni agente che *può interrogare il DB sui casi passati*, con tool dedicati e fortemente parametrici: per **ticker**, per **condizione di mercato**, per **momento storico**, per **esito del trade**, … (letteralmente qualsiasi dimensione). L'agente pesca on-demand le esperienze rilevanti e impara dagli errori. Pro: mirato, scalabile. Contro: l'agente deve *decidere* di guardare (mitigabile da istruzione + dal riassunto rolling che lo invita).
3. **`past_context` popolato deterministicamente** — un modulo (mantainer/learning) riempie `past_context` con le lezioni rilevanti per quel ticker/condizione prima dell'analisi (warm-start della memoria). Ibrido tra 1 e 2.
4. **Memoria semantica / embeddings** — indicizzare decisioni/esiti e recuperare per similarità (RAG sulle esperienze). Post-MVP.
5. **Pesi/scoring degli agenti dal backtest/esiti** — la hit-rate per-agente come *memoria di affidabilità* in input al PM ([[system/learning-feedback-loop]] §4).
6. **Altre** — da discutere insieme.

### Note di design
- Collegare al [[system/learning-feedback-loop]]: la memoria inter-task È il loop di apprendimento operativizzato lato agenti.
- Coerenza con "real-time first": la memoria inter-task è *storica/immutabile* → DB-first (no real-time).
- Va deciso il **confine**: cosa nel prompt (riassunto) vs cosa on-demand (tool) — trade-off costo/token vs copertura.

## Stato
**Aperto / da discutere.** Card in [[artifacts/project-board]]; decisione aperta in [[system/decision-log]]. Prerequisito comodo: la **deduplicazione DB** (anch'essa da fare) per una memoria pulita.

---
## Commenti recuperati da iCloud (2026-07-01)

> Commenti Obsidian `%%...%%` presenti nella vecchia copia iCloud (`7054827`) e reinseriti senza sovrascrivere il contenuto corrente.

%%questa parte della memoria intra task è molto interessante anche svilupparla poi a livello di codice
Tra l’altro, ricordati che qui si cita di nuovo al fatto di implementare già qualcosa e di averla già implementata, Ecco, ricordati che noi partiamo da Zero per il codice%%

%%un altro tipo di memoria semantica è in architettura. a grafi, la quale comincia a risuonarmi molto interessante. individuiamo magari delle librerie che fanno rag e grafi tutto insieme%%

