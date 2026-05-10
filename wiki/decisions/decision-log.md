---
title: "Decision Log"
type: decision
tags:
  - decision
  - strategy
created: 2026-04-30
updated: 2026-04-30
status: active
related:
  - "[[decisions/decisions]]"
  - "[[ops/dashboard]]"
confidence: high
area: strategy
decision_status: proposed
---

# Decision Log

Registro delle decisioni rilevanti del progetto.

## Uso

Quando una scelta smette di essere banale, registrarla qui o creare una pagina decisione dedicata e linkarla da qui.

## Decisioni chiuse

| Data | Decisione | Motivazione |
|------|-----------|-------------|
| 2026-04-30 | **From scratch** — non fare fork di progetti esistenti | Chi parte da un fork deve comunque studiare il codice altrui per modificarlo; meglio costruire con piena comprensione |
| 2026-04-30 | **Crypto come mercato iniziale** — Binance come exchange | Accesso dati migliore (order book, prezzi storici, API), liquidità, semplicità operativa rispetto all'equity |
| 2026-04-30 | **Meccanismo di trade**: limit order con Stop Loss e Take Profit obbligatori | Ogni trade deve avere tre numeri definiti: entry, SL, TP. Tutti i trade in leva |
| 2026-04-30 | **Design-first** prima di qualsiasi coding | Progettare artifact, raccogliere info su progetti esistenti, definire I/O per ogni modulo |
| 2026-04-30 | **Augmentation → Autonomy**: partire da dashboard di potenziamento | Prima che il sistema operi in autonomia, deve dimostrare di proporre trade sensati con supervisione umana |

## Decisioni non ancora chiuse

- **Crypto vs Equity definitivo**: orientamento su crypto, ma non chiuso — valutare dopo la fase di ricerca
- **Includere o meno il modulo TA**: rischio di corrompere il Prediction Module DL. Decidere solo dopo backtest comparativi con/senza TA
- **Frequenza di trade e invocazione LLM**: dipende dal tempo di elaborazione dei moduli (stima: secondi → minuti → max ~1 ora)
- **Fine-tuning vs Continuous Learning**: continuous learning in real-time è ancora un problema aperto; fine-tuning periodico più praticabile
- **Sentiment degli analisti come modulo**: idea interessante (King), ma richiede studio di fattibilità
