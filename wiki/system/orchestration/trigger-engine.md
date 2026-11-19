---
title: Trigger Engine — centralizzazione dei trigger
type: build
tags:
  - trigger-engine
  - build
  - architecture
created: 2026-06-06T00:00:00.000Z
updated: 2026-07-13T00:00:00.000Z
status: draft
priority: high
area: software
related:
  - '[[system/orchestration/parallelism-design]]'
  - '[[system/agents/agents]]'
  - '[[system/data/data-layer]]'
confidence: medium
---

# Trigger Engine — centralizzazione dei trigger

> **Spec corrente:** centralizzare alert di prezzo, `next_check_date`, calendario e health check in una sola coda di priorità ([[system/orchestration/parallelism-design]]). Le analisi sono event-driven; il controllo di salute/portafoglio resta periodico e costante.

## Il principio

**Il Trigger Engine è il "perché" il sistema si attiva; il funnel è il "come" decide.** Si saldano:

```
[Trigger Engine]  →  TriggerEvent  →  [coda di priorità D]  →  screening (E)  →  deep-dive (A)  →  Trade
   (le sorgenti)        (normalizzato)     (parallelism-design)
```

Il PM / cycle runner **non interroga 5 sorgenti diverse**: consuma una sola coda. Vantaggi: dedup, priorità, rate-limit, e un **audit unico** di *perché* è partito ogni ciclo.
Durante un run, un nuovo evento coerente con la tesi attiva può aggiornare il contesto del PM. Ogni evento iniettato conserva `type`, `reason`, `priority`, timestamp e origine (`price_alert`, `next_check_date`, calendario o health check); gli eventi non coerenti restano in coda per il run successivo.
## Le sorgenti di trigger (tutte centralizzate)

| Sorgente                           | Cos'è                                | Come genera l'evento                                                                      |
| ---------------------------------- | ------------------------------------ | ----------------------------------------------------------------------------------------- |
| **Health / portfolio check**       | controllo periodico separato         | scheduler leggero → verifica portafoglio, staleness e integrità; non forza un deep-dive |
| **Dynamic Temporal Checkpoint**    | `next_check_date` scaduto            | query su `ticker_card`/`research_states` con data ≤ oggi                                  |
| **Price alert**                    | prezzo vs target o movimento anomalo | confronto prezzo corrente vs `entry/stop/tp` salvati o vs soglia ATR (mercati efficienti) |
| **Calendario economico**           | earnings / dati macro imminenti      | `get_calendar` → enqueue i ticker/macro impattati prima/dopo l'evento                     |
| **News anomale** (futuro, PostMVP) | terzo tipo di alert                  | rilevatore news → enqueue il ticker                                                       |

## `TriggerEvent` (forma normalizzata)

```
{ type, symbols[], reason, priority, payload, created_at }
```

Tutte le sorgenti producono lo stesso oggetto → la coda è omogenea e ordinabile per `priority`. L'**idempotenza** evita di accodare due volte lo stesso evento (es. lo stesso `next_check_date` in due scansioni ravvicinate).

## Aggancio all'esistente
- **Coda D**: il Trigger Engine è il produttore; il cycle runner è il consumatore ([[system/orchestration/parallelism-design]]).
- **Autonomia totale**: lo scheduler parte da solo all'accensione (nessun input umano) → [[system/agents/agents]].
- **Mercati efficienti**: gli alert sono numerici/prezzo; le news entrano dagli extractor → coerente con la decisione esistente.
- **Calendar tool & adaptive extractor**: vivono nel [[system/data/data-layer]]; il Trigger Engine li *legge*, non li duplica.

## Implementazione (futura)
- Tabella `trigger_events` (o riuso della coda) con stato `pending`/`consumed` + dedup key.
- Loop scheduler ogni N minuti che valuta le sorgenti e accoda.
- Logging di ogni evento (audit "perché mi sono svegliato") → learning loop.

## Stato
> Gli esempi di `TriggerEvent` e priorità presenti nelle vecchie note sono reference design. La spec da consegnare è la forma normalizzata qui descritta, con dedup, audit dell'origine e policy per gli eventi che arrivano durante un run.

## Alert e trailing a chiusura barra — decisione 2026-11-20

- **Fonte prezzi**: nessuno stream. Il Runtime esegue un job alla chiusura di ogni barra `bar_timeframe` (default 1h, globale e configurabile) durante la seduta: barre REST di posizioni e watchlist, poi trailing stop e valutazione degli Alert.
- **Alert di prezzo**: movimento ≥ 2·ATR14 dal close della seduta precedente; volume ≥ 2× la media della stessa fascia oraria (20 sedute); livelli della tesi (entrata proposta in un Rimando, oppure entro 0,5·ATR da SL/TP); gap in apertura ≥ 1·ATR. Soglie configurabili. Più condizioni sulla stessa barra producono un solo Alert composto.
- **Cooldown**: 3 ore per ticker (configurabile), calcolato dall'Event log. Se il ticker è in analisi, l'Alert entra come messaggio (Q31).
- **Trimestrali**: Alert al PM 3 giorni di borsa prima, solo per titoli in posizione. Il calendario macro resta al Market Analyst.
- **ATR**: calcolato sul timeframe globale anche per ordini e trailing. Con 1h gli stop si stringono, quindi i coefficienti `k` vanno ritarati prima di ordini reali.
- Stato: **deciso, non implementato** (fetta S9 della spec del Runtime nel repository codice).
