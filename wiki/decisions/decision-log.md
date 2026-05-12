---
title: "Decision Log"
type: decision
tags:
  - decision
  - strategy
created: 2026-04-30
updated: 2026-04-30
status: active
related:  - "[[ops/dashboard]]"
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

| Tema | Contesto |
|------|----------|
| **Trading singolo vs Portfolio bilanciato** | Trading singolo: facile da valutare (SL/TP binario). Portfolio bilanciato: più robusto ma difficile da valutare e richiede orizzonte temporale più lungo. Decisione centrale — da chiudere prima di costruire il sistema |
| **Multi-asset vs Solo cripto** | Salvatore propone: partire da asset tradizionali (equity/ETF) + cripto come side. Cripto è un mondo a parte con metodologie diverse. Decidere il mercato principale prima che Salvatore possa approfondire l'analisi |
| **Cash-out strategy** | Quale % dei profitti viene estratta periodicamente? Regola da stabilire a priori come statuto del fondo |
| **Regole del portafoglio (statuto)** | Es: nessuna asset class >5%, vendi quando una posizione supera +100% di profitto. Regole deterministiche anti-bias da implementare nel Security Module |
| **Crypto vs Equity definitivo** | Orientamento su crypto, non chiuso — potrebbe cambiare se si decide di partire da asset tradizionali |
| **Includere il modulo TA** | Rischio di corrompere il Prediction Module DL. Decidere solo dopo backtest comparativi con/senza TA |
| **Frequenza di trade e invocazione LLM** | Dipende dal tempo di elaborazione dei moduli (stima: secondi → ~1 ora) + costo token per chiamata |
| **Fine-tuning vs Continuous Learning** | Il continuous learning in real-time è ancora un problema aperto; fine-tuning periodico più praticabile |
| **Sentiment degli analisti come modulo** | Idea interessante (King/Salvatore), richiede studio di fattibilità |
