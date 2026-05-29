---
title: "Trading Floor Canvas"
type: source
tags:
  - source
  - architecture
raw_source_path: "wiki/artifacts/trading-floor.canvas"
created: 2026-05-06
updated: 2026-05-06
confidence: high
status: active
related:
  - "[[system/architecture]]"
---

# Trading Floor Canvas

Questa nota riflette e contestualizza il file strutturato estratto da `raw/notes/Trading Floor.canvas`.
Il diagramma delinea una architettura di una "Trading Floor" basata su agenti specializzati, confermando la direzione multi-agente discussa nelle chiamate.

## Agenti e Responsabilità

1. **News Research Agent**
   - **Compito**: Analizza le news ed elabora un proprio sentiment (bullish/bearish).

2. **Analista**
   - **Compito**: Analisi finanziaria dell'asset class. Ricerca di opportunità tramite ratio finanziari.
   - **Interazioni**: Riceve e valida le informazioni prodotte dal *News Research Agent*. Alimenta il *Quant Agent*.

3. **Quant Agent**
   - **Compito**: Esegue backtest matematico e analisi previsionale (es. tramite modelli LSTM o econometria).
   - **Interazioni**: Riceve input dall'*Analista* e alimenta il *Trader Agent* e/o *Risk Analyst*.

4. **Risk Analyst Agent**
   - **Compito**: Estremamente critico. Fornisce i paletti, le regole e la strategia (Position Sizing, esposizione). 
   - **Metriche**: Calcola commissioni, Expected Shortfall, VaR, e decide quanto limitare i trade.
   - **Interazioni**: Passa le regole e i limiti di validazione finali al *Trader Agent*.

5. **Trader Agent**
   - **Compito**: Raccoglie tutte le info (direzionalità, previsione, limiti di rischio) ed esegue il trade alla miglior condizione possibile di mercato/costo.
   - L'idea è di mantenere la sua esecuzione il più deterministica possibile.

## Tools (Strumenti Esterni / Moduli Informativi)
- Dati per analisi: Tool volumetrici, ratio, market makers.
- Dati per esecuzione: Commissioni, valutazione broker, liquidità dello strumento (spread).
