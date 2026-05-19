---
title: "Modulo D — Prompt Builder + LLM Trader"
type: build
tags:
  - build
  - software
created: 2026-05-13
updated: 2026-05-13
status: active
priority: medium
area: software
related:
  - "[[build/system-map]]"
  - "[[build/stack]]"
  - "[[build/mvp-prototype-design]]"
  - "[[build/modules/module-a-exchange-db]]"
  - "[[build/modules/module-c-quant-backtest]]"
---

# Modulo D — Prompt Builder + LLM Trader

**Track 3 — inizia solo dopo che Modulo A è completato.**

Il modulo della decisione. Il Prompt Builder assembla deterministicamente tutti gli output dei moduli in un prompt strutturato. L'LLM Trader legge il prompt e produce una proposta di trade in JSON.

---

## Cosa fa

### Prompt Builder (deterministico, no LLM)

- Legge dal DB: output di Modulo C (segnali quant), stato portafoglio, briefing Risk Analyst
- Assembla un prompt secondo un **template fisso** con sezioni:
  1. Ruolo + stato portafoglio (capitale, liquidità, posizioni aperte)
  2. Dati strutturati: indicatori tecnici, Pivot Points, segnali quant
  3. Briefing Risk Analyst: VaR, esposizione max, range SL/TP ammissibili
  4. Regole operative: una posizione per coin, operazioni ammesse (open/close/hold)
  5. Formato output obbligatorio (JSON con campi fissi)
- Salva il prompt assemblato in `module_outputs` (Prompt Store)

### LLM Trader (DeepSeek)

- Legge il prompt dal Prompt Store
- Produce **esclusivamente** un oggetto JSON:
  ```json
  {
    "azione": "open",
    "asset": "BTCUSDT",
    "direzione": "long",
    "entry": 65000,
    "sl": 63000,
    "tp": 70000,
    "leva": 3,
    "reasoning": "..."
  }
  ```
- Non esegue l'ordine — lo propone. L'esecuzione è delegata al Security Module e all'Exchange Module

## Output atteso

> Primo ciclo completo end-to-end: dati reali → prompt → decisione LLM → ordine paper su Binance.

---

## Tech

- **DeepSeek**: LLM principale (costo 1/30 di GPT-5, 2° posto Alpha Arena)
- Output **JSON strutturato** obbligatorio — parsing deterministico
- **Pivot Points** inclusi nel prompt — tutti i sistemi pratici analizzati li usano come riferimenti spaziali
- **Template Prompt**: struttura fissa, campi riempiti deterministicamente dai dati del DB

---

## Decisioni prese

| Tema | Scelta |
|------|--------|
| LLM | DeepSeek |
| Output | JSON strutturato obbligatorio |
| Pivot Points | Inclusi nel prompt (confermato da ricerca NotebookLM) |
| Principio | LLM decide, Python esegue (deterministico) |

## Domande aperte

- **Struttura esatta del template prompt**: quali sezioni, quale ordine, quanti token per sezione?
- **Quick Thinker + Deep Thinker**: usare DeepSeek small per raccolta dati e DeepSeek Chat per la decisione finale?
- **Frequenza di invocazione**: ogni 4h o 24h? Dipende dal costo token per chiamata e dal tempo di elaborazione dei moduli.

---

## Dipendenze

- **Dipende da Modulo A**: legge dati da `market_data` e `portfolio_state`
- **Dipende da Modulo C**: legge segnali da `module_outputs`
- **Dipende da Risk Analyst** (post-MVP): legge il briefing rischio — nel MVP la parte Risk è semplificata

---

*Vedere [[build/mvp-prototype-design]] per il ciclo operativo completo.*
