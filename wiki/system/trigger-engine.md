---
title: "Trigger Engine — centralizzazione dei trigger"
type: build
tags:
  - build
  - architecture
  - multi-agent
created: 2026-06-06
updated: 2026-06-06
status: draft
priority: high
area: software
related:
  - "[[system/parallelism-design]]"
  - "[[system/modules/agents]]"
  - "[[system/modules/data-layer]]"
confidence: medium
---

# Trigger Engine — centralizzazione dei trigger

> **Proposta (input di Luca 2026-06-06): centralizzare tutti i trigger** che svegliano il sistema. Oggi sono sparsi (alert di prezzo, `next_check_date`, periodical synthesis, calendario economico, news anomale). L'idea: un unico componente che li raccoglie, li normalizza e li immette nella **coda di priorità del funnel** ([[system/parallelism-design]]).

## Il principio

**Il Trigger Engine è il "perché" il sistema si attiva; il funnel è il "come" decide.** Si saldano:

```
[Trigger Engine]  →  TriggerEvent  →  [coda di priorità D]  →  screening (E)  →  deep-dive (A)  →  Trade
   (le sorgenti)        (normalizzato)     (parallelism-design)
```

Il PM / cycle runner **non interroga 5 sorgenti diverse**: consuma una sola coda. Vantaggi: dedup, priorità, rate-limit, e un **audit unico** di *perché* è partito ogni ciclo.

## Le sorgenti di trigger (tutte centralizzate)

| Sorgente | Cos'è | Come genera l'evento |
|----------|-------|----------------------|
| **Periodical synthesis** | intervallo fisso (time-based) | scheduler a cadenza fissa → enqueue scan larga |
| **Dynamic Temporal Checkpoint** | `next_check_date` scaduto | query su `ticker_card`/`research_states` con data ≤ oggi |
| **Price alert** | prezzo vs target o movimento anomalo | confronto prezzo corrente vs `entry/stop/tp` salvati o vs soglia ATR (mercati efficienti) |
| **Calendario economico** | earnings / dati macro imminenti | `get_calendar` → enqueue i ticker/macro impattati prima/dopo l'evento |
| **News anomale** (futuro) | terzo tipo di alert | rilevatore news → enqueue il ticker |

## `TriggerEvent` (forma normalizzata)

```
{ type, symbols[], reason, priority, payload, created_at }
```

Tutte le sorgenti producono lo stesso oggetto → la coda è omogenea e ordinabile per `priority`. L'**idempotenza** evita di accodare due volte lo stesso evento (es. lo stesso `next_check_date` in due scansioni ravvicinate).

## Aggancio all'esistente
- **Coda D**: il Trigger Engine è il produttore; il cycle runner è il consumatore ([[system/parallelism-design]]).
- **Autonomia totale**: lo scheduler parte da solo all'accensione (nessun input umano) → [[system/modules/agents]].
- **Mercati efficienti**: gli alert sono numerici/prezzo; le news entrano dagli extractor → coerente con la decisione esistente.
- **Calendar tool & adaptive extractor**: vivono nel [[system/modules/data-layer]]; il Trigger Engine li *legge*, non li duplica.

## Implementazione (futura)
- Tabella `trigger_events` (o riuso della coda) con stato `pending`/`consumed` + dedup key.
- Loop scheduler ogni N minuti che valuta le sorgenti e accoda.
- Logging di ogni evento (audit "perché mi sono svegliato") → learning loop.

## Stato
> 🟢 **Implementato (alpha v0, 2026-06-06)** — `tradingagents/orchestration/triggers.py`: `TriggerEvent` + `collect_triggers()` che unisce **due checkpoint** (`next_check_date`) + **price alert** (movimento anomalo `|Δ| > k·ATR`, mercati efficienti) + **screening candidates** (top-K da `ticker_card`), con dedup per simbolo e priorità (checkpoint 1.0 > price_alert 0.9 > screening=score). È la coda unica che il `run_cycle` consuma. **Mancano ancora**: calendario come sorgente; persistenza `trigger_events` + scheduler periodico.

Design **proposto** completo sopra; prima fetta implementata. Card in [[artifacts/project-board]]; decisione in [[system/decision-log]].
