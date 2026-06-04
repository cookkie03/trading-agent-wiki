---
title: "Learning & Feedback Loop — valutazione e auto-miglioramento del sistema"
type: build
tags:
  - build
  - architecture
  - multi-agent
created: 2026-06-03
updated: 2026-06-04
status: draft
priority: medium
area: software
related:
  - "[[system/rating-scoring]]"
  - "[[system/modules/agents]]"
  - "[[system/modules/execution]]"
  - "[[system/modules/data-layer]]"
  - "[[system/architecture]]"
confidence: low
---

# Learning & Feedback Loop — valutazione e auto-miglioramento del sistema

> Pagina di unificazione (2026-06-03). Quattro idee emerse in momenti diversi — **scoring del lavoro degli agenti**, **feedback post-trade per meccanismo di uscita**, **reportistica su "cosa va male"**, **ponderazione dinamica dei pesi degli agenti** — sono in realtà **un unico macro-blocco**: il loop con cui il sistema *si misura, si racconta e si corregge*. Finora erano sparse tra [[system/rating-scoring]], [[system/architecture]] (Layer 5), [[system/mvp]] e il glossario. Qui le si tiene insieme.

Origine delle idee:
- *«raccogliere quali moduli, indicatori e metodi stanno performando meglio — per revisione umana e miglioramento continuo della teoria economica»* (ideas-log 2026-05-21).
- *«ha senso avere un sistema di valutazioni a level, anche per la valutazione del lavoro di ogni agent, con punteggi categorizzati che aiutano a capire cosa migliorare e come»* (Luca, call 2026-06-02).
- *«un sistema che permette di far notare agli agent come sono andati i trade precedenti a seconda di quali meccanismi di disinvestimento sono stati adottati»* (Luca, 2026-06-03).

---

## Principio di design (coerente col resto del sistema)

Stesso principio deterministico applicato ovunque: **le metriche le calcola Python**, l'LLM interviene **solo per la narrazione finale**. Niente black-box: ogni numero è ricostruibile, l'agente non "inventa" performance, le legge.

```
transactions + states + reports (DB)
   → [Python] calcolo metriche segmentate          ← deterministico
      → report diagnostico strutturato (numeri)
         → [LLM] narrazione "cosa è andato bene/male"  ← solo qui
            ├─► umano (dashboard / sintesi)
            └─► agenti (past_context)
```

---

## I quattro pezzi del loop

### 1. Substrato — logging tesi↔esito (prerequisito di tutto)
Niente del resto è possibile senza i dati grezzi. Da predisporre **da subito** (alpha), anche se report e pesi arrivano dopo:
- **chain-of-thought strutturata** di ogni agente (già in board);
- **`exit_reason`** su ogni transazione (già in [[system/modules/execution]]);
- **match tesi-per-agente ↔ esito reale del trade**: per ogni trade chiuso, *cosa aveva detto ciascun desk/agente* vs *com'è andata*. È il pezzo nuovo e mancante: senza questo aggancio, scoring (§3) e pesi (§4) non hanno base.

### 2. Reportistica diagnostica — "cosa va male" → **modulo deterministico + narrazione**
**Opzione scelta (per ora, 2026-06-03)**: *non* un agente LLM dedicato, ma un **modulo Python deterministico** che calcola la diagnosi + un **passo di narrazione LLM** sopra il risultato.

- **Cosa produce**: il post-mortem periodico — non i numeri grezzi della dashboard, ma la *sintesi del perché*: quale desk ha sbagliato sistematicamente, quale fattore non ha tenuto, quale meccanismo di uscita è costato (collegamento a §5), quali settori/regimi ci penalizzano.
- **Metriche**: riusa l'analytics stile SFC (`performance_contribution.py`, attribution vs benchmark, [[_meta/glossario#Win Rate|win rate]] / profit factor / [[_meta/glossario#Drawdown|drawdown]] per categoria) → [[prior-art/libraries/sfc-portfolio-tracker]] e [[system/modules/quant-backtesting]].
- **Innesco**: si aggancia naturalmente alla **periodical synthesis** che già attiva il PM ([[system/modules/agents]]) — la sintesi periodica *contiene* la diagnosi.
- **Destinatari doppi**: (a) **umano** via dashboard/Telegram (Layer 5); (b) **agenti** via `past_context` (§5).
- **Perché modulo e non agente**: coerenza col principio "LLM solo per il reasoning finale"; la diagnosi è fatta di conti, l'agente non deve calcolarli. *Tenuto come opzione, non vincolo definitivo.*

### 3. Scoring del lavoro degli agenti (meta-valutazione)
→ dettaglio in [[system/rating-scoring]] §2. Punteggio categorizzato sulla **qualità del lavoro di ciascun agente/modulo**: confronta a posteriori la tesi di ogni agente (dal §1) con l'esito reale. Evidenzia *dove* il sistema sbaglia (quale desk, quale fattore, quale fase). È sia output del reporting (§2) sia input dei pesi (§4).

### 4. Ponderazione dinamica dei pesi (RL / Weighting Module)
L'agente che storicamente ci azzecca **pesa di più** nell'aggregazione della tesi; chi sbaglia sistematicamente pesa meno. Pattern concettuale: **[[_meta/glossario#Opinion Pooling|Opinion Pooling]] / [[_meta/glossario#Black-Litterman|Black-Litterman]]** (i pesi/confidence aggiornati sugli esiti storici per-agente) → [[prior-art/libraries/cvx-portfolio-optimizer]], glossario.

- **I pesi li calcola il backtesting system** (input di Luca 2026-06-04): la ponderazione dei vari agenti non è un parametro a mano, ma un **output del [[system/modules/quant-backtesting]] in modalità validatore continuo/asincrono** — lo stesso motore che ri-tara le soglie (R:R, k_*, soglie Statuto) misura anche la *hit-rate per-agente* sullo storico (dal §1) e ne deriva i pesi. Vantaggio: i pesi si aggiornano sui dati reali via via che entrano, con la stessa cautela anti-overfitting (walk-forward / out-of-sample → [[strategy/questions-for-salvatore]]). Sono parametri di configurazione esterni, non hardcodati.
- **⚠️ I pesi sono un'INDICAZIONE, non una REGOLA** (precisazione di Luca 2026-06-04): il backtesting sui pesi **non sostituisce** il giudizio dell'agente. Serve come **informazione/contesto aggiuntivo** che si passa al PM per dargli più *awareness* — "storicamente di questo desk ti puoi fidare di più/di meno" — lasciando a lui la decisione. Non un automatismo che scavalca il reasoning. Questo **scioglie la tensione** con "conviction dal PM": il PM resta decisore, il backtest lo informa.
- **Seconda funzione del backtest sui pesi — diagnostica** (Luca 2026-06-04): oltre a pesare, serve a **capire cosa e come migliorare** gli agenti e i **tool collegati** a ciascuno (quale desk/tool performa peggio e perché). Si lega a §2 (reportistica) e §3 (scoring): la hit-rate per-agente è anche un puntatore a dove intervenire.
- **Stato**: **post-MVP avanzato** (richiede storico significativo). Resta tale.
- **Punto di aggancio — orientamento (a)** (2026-06-04, dato il framing "indicazione non regola"): i pesi entrano come **input/contesto al PM** (il PM resta decisore, ma vede "quanto fidarsi" di ciascun desk). Le alternative scartate restavano: (b) nodo di aggregazione che precede il PM; (c) confidence del Black-Litterman. La (a) è coerente con "il backtest informa, non comanda". Da confermare in fase di mappatura del grafo.

### 5. Feedback post-trade per meccanismo di uscita
→ dettaglio in [[system/rating-scoring]] §4. Esiti dei trade **segmentati per `exit_reason`** (TP / SL / trailing / rating-based), restituiti agli agenti nel `past_context`. È un caso particolare di reporting (§2) che chiude il loop con lo scoring (§3): un agente che apre tesi chiuse sistematicamente in stop loss perde score.

---

## Cosa fare ORA vs DOPO

| Pezzo | Quando | Perché |
|------|--------|--------|
| **§1 logging tesi↔esito + exit_reason** | **Da subito (alpha)** | Substrato: senza, niente è possibile. I dati vanno accumulati dall'inizio. |
| §2 reportistica diagnostica | MVP→post-MVP | Le metriche base (P&L, win rate) sono presto disponibili; la narrazione si aggiunge quando c'è abbastanza storia. |
| §3 scoring agenti | Post-MVP | Richiede storico di trade chiusi. |
| §4 ponderazione pesi | Post-MVP avanzato | Richiede storico ampio + decisione punto di aggancio. |
| §5 feedback per exit | Logging da subito, valore col tempo | Vedi [[system/rating-scoring]] §4. |

---

## Punti aperti (in board)

- **Reporting: modulo deterministico + narrazione vs agente LLM** — tenuto come modulo (preferenza 2026-06-03), non definitivo.
- ~~**Pesi: punto di aggancio**~~ → **risolto 2026-06-04**: i pesi sono **input/contesto al PM** (indicazione, non regola); tensione con "conviction dal PM" sciolta. Resta da implementare in fase di grafo.
- **Schema del log tesi-per-agente↔esito** — forma da definire insieme allo [[system/state-schemas]] (serve poter ricostruire chi ha detto cosa).

---

*Le metriche numeriche vivono in [[system/modules/quant-backtesting]]; gli score categorizzati in [[system/rating-scoring]]; la vista umana nel Layer 5 di [[system/architecture]].*
