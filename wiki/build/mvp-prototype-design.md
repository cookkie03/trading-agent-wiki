---
title: MVP Prototype Design
type: build
tags:
  - build
  - architecture
  - mvp
  - design
created: 2026-05-13
updated: 2026-05-13
status: active
related:
  - "[[build/system-map]]"
  - "[[build/decision-log]]"
  - "[[build/stack]]"
  - "[[wiki/artifacts/architecture/trading-floor.canvas]]"
confidence: high
priority: high
area: software
---

# MVP Prototype Design

Design del prototipo funzionante del trading agent. Prodotto nella sessione di brainstorming del 2026-05-13.

## Obiettivo del prototipo

Agente autonomo su **paper trading** (Binance Testnet) con backtesting robusto continuativo e produzione di metriche affidabili a due livelli: per-trade e portfolio.

Nessun capitale reale. Nessuna supervisione umana obbligatoria nel loop. Validazione del sistema su dati storici e in real-time simulato prima di andare live.

## Decisioni fondanti

| Tema | Scelta |
|------|--------|
| Architettura | Monolite modulare (Opzione A) |
| Mercato | Crypto / Binance Testnet |
| Orizzonte trade | Swing trading (candele 4h / daily, giorni-settimane) |
| Portfolio vs Singolo | Portfolio-first nell'architettura, singolo asset nell'MVP deployment |
| Backtesting | Stesso codice del live, Exchange Module cambia backend |
| LLM | DeepSeek (costo 1/20 rispetto a modelli americani) |
| Principio guida | Deterministico: LLM solo per ragionamento, tutto il resto Python |

## Architettura — Ciclo operativo

Il sistema gira come processo Python schedulato (loop interno o cron). Frequenza: ogni 4h o 24h in modalità swing.

```
Data Ingestion
  │
  ├── TAVOLO (moduli analisi, in parallelo):
  │     ├── Analista      → ratio finanziari, validazione news
  │     ├── News Agent    → sentiment elaborato sulle news
  │     └── Quant Agent   → backtest/forecasting sull'asset
  │
  ├── Risk Analyst Agent  ← legge output TAVOLO + stato portafoglio corrente
  │     └── produce: briefing rischio (VaR, esposizione max, range SL/TP ammissibili, go/no-go)
  │
  ├── Prompt Builder      → assembla deterministicamente tutti gli output in un prompt
  │
  ├── Trader Agent (LLM)  ← legge briefing rischio + output TAVOLO via Prompt Builder
  │     └── produce: asset, direction, entry, SL, TP, size (entro i paletti del Risk Analyst)
  │
  ├── Security Module     → hard limits deterministici — statuto del fondo, no LLM
  ├── Portfolio Allocator → size finale in base al portafoglio corrente
  ├── Exchange Module     → Binance Testnet (paper) | replay storico (backtest)
  └── Logger              → trade, chain-of-thought LLM, metriche nel DB
```

### Nota architetturale chiave: Risk Analyst è upstream

Il Risk Analyst Agent *precede* il Trader Agent — non lo valida dopo. Imposta i paletti dinamici per il ciclo corrente (VaR, esposizione massima, range SL/TP ammissibili) in base allo stato del mercato e del portafoglio. Il Trader decide *dentro* quello spazio, non viene corretto fuori da esso.

Fonte: [[wiki/artifacts/architecture/trading-floor.canvas]] — schema del trading floor con Analista, News Agent, Quant Agent (TAVOLO) → Risk Analyst → Trader.

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
- Drawdown corrente e massimo
- Rendimento cumulativo
- Sharpe ratio
- Esposizione per asset e per asset class
- Win rate, average win/loss ratio

## DB centrale

Postgres (produzione) / SQLite (sviluppo locale). Ogni modulo legge e scrive solo le proprie tabelle. Il Prompt Builder ha accesso in lettura a tutto. Il Logger ha accesso in scrittura a tutto.

## Sequenza di sviluppo

### Track 1 — Luca (sviluppo solo)
**Modulo A: Exchange Module + DB**
- Connessione Binance Testnet
- Esecuzione ordini paper (limit order con SL/TP)
- Schema DB con tabelle: market_data, trades, portfolio_state, module_outputs, logs
- Logger base

Obiettivo: pipe vuoto funzionante, dati reali che scorrono nel DB.

### Track 2 — Luca + Salvatore (sessioni di progettazione, in parallelo con Track 1)
**Modulo C: Quant Agent + Backtesting**
- Definizione della strategia quantitativa (multi-factor fundamentals è l'orientamento)
- Scelta framework backtesting: vectorbt vs backtesting.py (da decidere)
- Download dati storici Binance
- Prime metriche su dati reali

### Track 3 — dopo Track 1 completato, Track 2 progettato
**Modulo D: Prompt Builder + LLM Trader**
- Il sistema arriva qui con dati REALI già nel DB (non fittizi)
- Integrazione DeepSeek API
- Primo ciclo completo: dati → prompt → decisione → esecuzione paper → log

## Moduli successivi (post-MVP)
Dopo che A + C + D girano insieme:
1. Risk Analyst Agent (upstream del Trader)
2. News Agent / Analista (completamento TAVOLO)
3. Security Module (hard limits — statuto del fondo)
4. Portfolio Allocator dinamico
5. RL/Weighting Module (ponderazione dinamica dei moduli)
6. Fine-Tuning Module

## Decisioni ancora aperte

| Tema | Stato |
|------|-------|
| Framework backtesting | ~~Da decidere~~ **CHIUSO: vectorbt** (usato da MarketSenseAI — fonte: ricerca NotebookLM 2026-05-13) |
| Strategia del fondo | Formalizzare con Salvatore (orientamento: multi-factor fundamentals) |
| Frequenza ciclo esatta | 4h vs 24h — dipende da backtest iniziali |

## Insights da progetti simili (NotebookLM 2026-05-13)

Dalla ricerca su TradingAgents, MarketSenseAI, Alpha Arena e Simone Rizzo:

- **SL/TP sono hard constraint**: senza di essi, win rate 66% porta comunque a drawdown devastanti (Simone Rizzo, settimana 1 senza SL/TP)
- **Output LLM = JSON obbligatorio**: tutti i sistemi impongono risposta esclusivamente JSON con campi fissi (operazione, simbolo, direzione, leva, reasoning)
- **Pivot Points**: aggiungere al Prompt Builder — tutti i sistemi pratici li usano come riferimenti spaziali per l'LLM
- **Prophet non affidabile**: non regge sui crolli improvvisi, genera previsioni bullish in mercati bearish — non usarlo come modulo di forecast principale
- **Quick Thinker + Deep Thinker**: DeepSeek (economico) per raccolta dati, DeepSeek o modello più capace solo per la decisione finale
- **Rebalancing Gate**: eseguire ordini solo se drift dai pesi target > soglia (es. 5%) — evita overtrading

Vedere [[syntheses/notebooklm-research-2026-05-13]] per la sintesi completa.

## Riferimenti
- [[build/system-map]] — architettura completa del sistema
- [[build/decision-log]] — decisioni prese e aperte
- [[build/stack]] — tech stack scelto
- [[wiki/artifacts/architecture/trading-floor.canvas]] — schema trading floor (fonte del ciclo raffinato)
- Sessione brainstorming: `raw/notes/sessione-brainstorming-2026-05-13.md`
