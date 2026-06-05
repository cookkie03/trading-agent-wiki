---
title: "Cost Accounting a runtime — commissioni + token"
type: build
tags:
  - build
  - execution
  - software
created: 2026-06-06
updated: 2026-06-06
status: draft
priority: medium
area: software
related:
  - "[[system/modules/execution]]"
  - "[[system/modules/agents]]"
  - "[[system/learning-feedback-loop]]"
  - "[[system/position-sizing]]"
confidence: medium
---

# Cost Accounting a runtime — commissioni + token

> **Da pensare (input di Luca 2026-06-06): come considerare le commissioni quando il software è in running.** Le decisioni d'impianto ci sono già — *transaction cost auto-adattivo* (no hardcoded) e *token cost = commissioni* (net performance) — ma manca il **come** entrano nelle decisioni a runtime. Qui la proposta.

## Le decisioni esistenti (cornice)
- **Transaction cost auto-adattivo**: nessun costo hardcodato; si legge la commissione reale del momento (broker/asset/size). → [[system/decision-log]] (2026-06-02).
- **Token cost = commissione**: il costo dei token OpenRouter, convertito in $/€, è trattato come una commissione del broker e sottratto dal profitto atteso. → [[system/modules/agents]].

## Proposta: gestione in tre momenti

### 1. Pre-trade (stima) — entra come guardrail
- Ogni broker espone un `CommissionModel.estimate(order) -> cost` che legge la fee reale del momento (broker · asset · size · spread). Vive nell'**adapter broker** ([[system/modules/execution]]).
- Si stima anche il **token-cost del ciclo** (token usati × prezzo modello).
- Si calcola il **net expected value** = payoff atteso − commissione − token-cost.
- **Guardrail "R:R al netto dei costi"**: se il payoff non copre i costi (o l'EV netto < soglia), **no-trade**. È un check deterministico nel Trade/Risk gate, accanto al guardrail R:R già esistente.

### 2. Post-fill (consuntivo) — si registra il reale
- Dalla conferma del broker si legge la **commissione effettivamente pagata**; si chiude il **token-cost effettivo** del ciclo.
- Si scrivono sul `trade` (es. campi `commission`, `token_cost`) o in una tabella `costs` dedicata → net performance reale, non stimata.

### 3. Accounting & learning
- La **net performance reale** alimenta la rendicontazione (portfolio_state) e il [[system/learning-feedback-loop]] (un'alpha che non copre i costi va smascherata presto).

## Token metering
- Tracciare i token per ciclo (usage di OpenRouter) → convertire in valuta → **attribuire ai trade del ciclo** (un ciclo può produrre 0..N trade; ripartire o imputare al ciclo).
- **Budget per ciclo** (opzionale): un tetto di token/costo per ciclo come freno anti-overtrading; si lega ai criteri "info sufficienti" del PM ([[system/parallelism-design]]).

## Dove vive (riassunto)
| Pezzo | Dove |
|-------|------|
| `CommissionModel.estimate` | adapter broker (`tradingagents/broker/`) |
| net-EV / R:R-after-cost check | funzione Trade / Risk gate ([[system/modules/execution]]) |
| campi costo (`commission`, `token_cost`) | storage (`trades` o tabella `costs`) |
| token meter | wrapper LLM / client OpenRouter |

## Stato
**Aperto / da progettare** (2026-06-06). Card in [[artifacts/project-board]]; decisione aperta in [[system/decision-log]].
