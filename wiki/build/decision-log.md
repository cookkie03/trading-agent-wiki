---
title: "Decision Log"
type: build
tags:
  - decision
  - strategy
created: 2026-04-30
updated: 2026-05-13
status: active
related:
  - "[[build/system-map]]"
  - "[[build/mvp-prototype-design]]"
---

# Decision Log

Storico delle decisioni rilevanti del progetto. Quando una scelta smette di essere banale, va registrata qui con la motivazione.

---

## Decisioni chiuse

| Data | Decisione | Motivazione |
|------|-----------|-------------|
| 2026-04-30 | **From scratch** — non fare fork di progetti esistenti | Chi parte da un fork deve comunque studiare il codice altrui; meglio costruire con piena comprensione |
| 2026-04-30 | **Crypto come mercato iniziale** — Binance come exchange | Accesso dati migliore, liquidità, semplicità API rispetto all'equity |
| 2026-04-30 | **Limit order + SL/TP obbligatori**, tutti i trade in leva | Ogni trade deve avere tre numeri definiti: entry, SL, TP. Senza SL/TP, win rate 66% porta comunque a drawdown devastanti |
| 2026-04-30 | **Design-first** prima di qualsiasi coding | Progettare artifact, raccogliere info, definire I/O per ogni modulo |
| 2026-04-30 | **Augmentation → Autonomy**: partire da paper trading autonomo | Prima che il sistema operi con capitale reale, deve dimostrare solidità su Testnet |
| 2026-05-13 | **Architettura**: monolite modulare | Sviluppo veloce, facile debug, path evolutivo verso microservizi. Rispetta il principio deterministico |
| 2026-05-13 | **Orizzonte trade**: swing trading (4h/daily) | Alte aspettative rendimento; analisi complessa richiede tempo; frequenza alta incompatibile con costo token |
| 2026-05-13 | **MVP deployment**: singolo asset su Binance Testnet | Portfolio-first nell'architettura, singolo asset per il primo deployment |
| 2026-05-13 | **Framework backtesting**: VectorBT | Usato da MarketSenseAI (paper più rigoroso). Gestisce costi di transazione in modo preciso |
| 2026-05-13 | **LLM principale**: DeepSeek | Alpha Arena: miglior rapporto costo/performance. 1/30 del costo di GPT-5 |
| 2026-05-13 | **Sequenza sviluppo**: Track 1 (Modulo A) ∥ Track 2 (Modulo C), poi Modulo D | Luca costruisce Exchange+DB mentre progetta con Salvatore il Quant Agent. Modulo D dopo |
| 2026-05-13 | **Risk Analyst upstream** del Trader | Imposta i paletti prima che il Trader decida, non valida dopo. Più adatto allo swing trading |
| 2026-05-13 | **Output LLM = JSON strutturato obbligatorio** | Tutti i framework convergono su questo. Necessario per parsing deterministico |
| 2026-05-13 | **Prophet non usare** come modulo forecast | Non regge sui crolli improvvisi, genera previsioni bullish in mercati bearish |
| 2026-05-13 | **Value investing non scalabile** come strategia primaria ora | Ogni azione richiede analisi diversa; costoso in tempo e token. Da rivalutare in futuro |

---

## Decisioni ancora aperte

| Tema | Contesto | Dove si risolve |
|------|----------|-----------------|
| **Strategia del fondo** | Orientamento: multi-factor fundamentals, ma non formalizzato con Salvatore | [[build/modules/module-c-quant-backtest]] |
| **Frequenza ciclo** | 4h vs 24h — dipende da backtest iniziali | [[build/modules/module-c-quant-backtest]] |
| **Trading singolo vs Portfolio bilanciato** | Architettura portfolio-first, MVP singolo asset. Metriche separate. Parzialmente risolto | [[build/mvp-prototype-design]] |
| **Multi-asset vs solo cripto** | Salvatore propende per asset tradizionali + cripto side | [[build/modules/module-c-quant-backtest]] |
| **Cash-out strategy** | Quale % dei profitti estratta periodicamente? Regola da mettere nello statuto | [[build/modules/risk-analyst]] |
| **Regole portafoglio (statuto)** | Es: max 5% per asset class, vendi a +100%. Hard limits deterministici | [[build/modules/risk-analyst]] |
| **Includere modulo TA?** | Rischio di corrompere il Prediction Module DL. Test A/B con/senza | [[build/modules/module-c-quant-backtest]] |
| **Frequenza invocazione LLM Trader** | Vincolo tecnico + costo API. Dipende da tempo elaborazione moduli | [[build/modules/module-d-prompt-builder-trader]] |
| **Fine-tuning vs Continuous Learning** | Continuous learning real-time è problema aperto; fine-tuning periodico più praticabile | post-MVP |
| **Exchange decentralizzato (DEX)** | Quando ha senso passare a un DEX anonimo (no KYC) rispetto a Binance? | post-MVP |
| **Struttura wiki quant** | Sezione strategie da costruire man mano che Salvatore porta materiale | [[_meta/index]] |
