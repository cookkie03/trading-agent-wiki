---
title: MVP Prototype Design
type: build
tags:
  - build
  - architecture
  - mvp
  - design
created: 2026-05-13
updated: 2026-05-29
status: active
related:
  - "[[system/architecture]]"
  - "[[system/decision-log]]"
  - "[[system/stack]]"
  - "[[trading-floor.canvas]]"
confidence: high
priority: high
area: software
---

# MVP Prototype Design

Design del prototipo funzionante del trading agent. Prodotto nella sessione di brainstorming del 2026-05-13.

## Obiettivo del prototipo

Agente autonomo su **[[_meta/glossario#Paper Trading / Testnet|paper trading]] equity** (exchange stock da scegliere — Alpaca/IB) con backtesting robusto continuativo e produzione di metriche affidabili a due livelli: per-trade e portfolio.

Nessun capitale reale. Nessuna supervisione umana obbligatoria nel loop. Validazione del sistema su dati storici e in real-time simulato prima di andare live.

> **Decisioni fondanti e architettura**: non duplicate qui. Le scelte chiave ([[_meta/glossario#Monolite Modulare|monolite modulare]], [[_meta/glossario#Swing Trading|swing trading]], principio deterministico, stock-only, OpenRouter/DeepSeek, ecc.) sono in [[system/decision-log]]; la **topologia operativa aggiornata** (analisti → research_state → Risk Analyst → Trade deterministico) è in [[system/architecture]]. Questa pagina si concentra su **cosa deve produrre l'MVP** (metriche, sequenza di sviluppo, insight implementativi).

### Backtesting integrato

Nessuna logica duplicata. L'Exchange Module ha due backend:
- **Live**: chiama Binance Testnet API
- **Backtest**: replay su dati storici Binance scaricati

Il resto del ciclo è identico. Questo garantisce che il backtest testa esattamente il codice che gira in produzione.

## Metriche a due livelli

### Per-trade
- Entry / SL / TP effettivi
- Esito (SL triggered / TP triggered / chiuso manualmente)
- P&L per trade
- Chain-of-thought dell'LLM (per analisi post-trade)
- Quali moduli avevano confermato la tesi

### Portfolio
- [[_meta/glossario#Drawdown|Drawdown]] corrente e massimo
- Rendimento cumulativo
- [[_meta/glossario#Sharpe Ratio|Sharpe ratio]]
- Esposizione per asset e per asset class
- [[_meta/glossario#Win Rate|Win rate]], average win/loss ratio

## DB centrale

Postgres (produzione) / SQLite (sviluppo locale). Schema completo (5 tabelle core ↔ 4 aree logiche) in [[system/modules/data-layer]].

## Sequenza di sviluppo

### Track 1 — Luca (sviluppo solo) → [[system/modules/data-layer]]
- Connessione all'exchange equity (paper trading API — Alpaca/IB da scegliere)
- Esecuzione ordini paper ([[_meta/glossario#Limit Order|limit order]] con SL/TP)
- Schema DB con le 5 tabelle core
- Logger base

Obiettivo: pipe vuoto funzionante, dati reali che scorrono nel DB.

### Track 2 — Luca + Salvatore (in parallelo con Track 1) → [[system/modules/quant-backtesting]]
- Definizione della strategia quantitativa (multi-factor fundamentals è l'orientamento)
- Framework backtesting: **[[_meta/glossario#VectorBT|VectorBT]]** (deciso)
- Download dati storici equity
- Prime metriche su dati reali

### Track 3 — dopo Track 1, Track 2 progettato → [[system/modules/agents]]
- Il sistema arriva qui con dati REALI già nel DB (non fittizi)
- Riscrittura del grafo su base TradingAgents + integrazione OpenRouter/DeepSeek
- Primo ciclo completo: dati → analisti → research_state → Risk Analyst → Trade deterministico → log

## Moduli successivi (post-MVP)
Dopo che i tre track girano insieme:
1. Risk Analyst completo (gate bear + guardrail deterministici da Statuto)
2. Desk di monitoring/evaluation delle posizioni
3. Extractor adattivi + Market Alert (calendar tool)
4. Dashboard Streamlit + canale Telegram
5. Reportistica diagnostica "cosa va male" (modulo Python + narrazione) → [[system/learning-feedback-loop]]
6. RL/Weighting Module (ponderazione dinamica dei pesi agenti) → [[system/learning-feedback-loop]]
7. Fine-Tuning Module

> Substrato da predisporre **da subito**: logging strutturato chain-of-thought + match tesi-per-agente↔esito + `exit_reason`. Senza, il loop di apprendimento (punti 5-6) non ha dati. Vedi [[system/learning-feedback-loop]] §1.

## Decisioni ancora aperte

| Tema | Stato |
|------|-------|
| Framework backtesting | ~~Da decidere~~ **CHIUSO: vectorbt** (usato da MarketSenseAI — fonte: ricerca NotebookLM 2026-05-13) |
| Strategia del fondo | Formalizzare con Salvatore (orientamento: multi-factor fundamentals) |
| Frequenza ciclo esatta | 4h vs 24h — dipende da backtest iniziali |

## Insights da progetti simili (NotebookLM 2026-05-13)

Dalla ricerca su TradingAgents, MarketSenseAI, [[_meta/glossario#Alpha Arena|Alpha Arena]] e Simone Rizzo:

- **SL/TP sono hard constraint**: senza di essi, win rate 66% porta comunque a drawdown devastanti (Simone Rizzo, settimana 1 senza SL/TP)
- **Output LLM = JSON obbligatorio**: tutti i sistemi impongono risposta esclusivamente JSON con campi fissi (operazione, simbolo, direzione, leva, reasoning)
- **[[_meta/glossario#Pivot Points|Pivot Points]]**: esporli come tool/contesto agli analisti — tutti i sistemi pratici li usano come riferimenti spaziali per l'LLM
- **Prophet non affidabile**: non regge sui crolli improvvisi, genera previsioni bullish in mercati bearish — non usarlo come modulo di forecast principale
- **[[_meta/glossario#Quick Thinker + Deep Thinker|Quick Thinker]] + Deep Thinker**: [[_meta/glossario#DeepSeek|DeepSeek]] (economico) per raccolta dati, DeepSeek o modello più capace solo per la decisione finale
- **[[_meta/glossario#Rebalancing Gate|Rebalancing Gate]]**: eseguire ordini solo se drift dai pesi target > soglia (es. 5%) — evita overtrading

Vedere [[syntheses/notebooklm-research-2026-05-13]] per la sintesi completa.

## Riferimenti
- [[system/architecture]] — architettura completa del sistema
- [[system/decision-log]] — decisioni prese e aperte
- [[system/stack]] — tech stack scelto
- [[trading-floor.canvas]] — schema trading floor (versione storica; topologia attuale in [[system/architecture]])
- Sessione brainstorming: `raw/archived/notes/sessione-brainstorming-2026-05-13.md`
