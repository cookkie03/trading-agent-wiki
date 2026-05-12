---
title: "Notion Export - Investimento e Trading"
type: source
tags:
  - source
  - strategy
  - market-structure
raw_source_path: "raw/articles/"
created: 2026-05-06
updated: 2026-05-06
confidence: high
status: active
related:
  - "[[theory/trading-fundamentals]]"
  - "[[theory/technical-analysis]]"
  - "[[theory/portfolio-management]]"
---

# Notion Export - Investimento e Trading

Questa pagina sintetizza l'export di Notion trovato nella cartella `raw/articles/Private & Shared 2/Investimento e Trading/`. I documenti forniscono una panoramica estesa su concetti di trading, analisi tecnica e strategie di portafoglio, che saranno fondamentali per definire le regole e le logiche degli agenti del Trading Agent.

## 1. Analisi Fondamentale e Costruzione Portafoglio
- **Elementi di valutazione progetto**: Obiettivo, utilità, tokenomics (supply, inflazione), community, team.
- **Portafoglio**: Un mix tra l'insieme degli asset e regole fisse. 
- **Piani di Ingresso**: 
  - **PIC (Piano Investimento Capitale)**: Investimento in un'unica soluzione.
  - **PAC (Piano Accumulo Capitale)**: Ingressi dilazionati, agnostici al prezzo, mediano il prezzo di carico.
  - Varianti avanzate come Value Averaging o PAC con enfasi ribassista.

## 2. Analisi Tecnica ed Elementi Grafici
L'analisi tecnica viene utilizzata per individuare potenziali zone di inversione (PRZ - Potential Reversal Zones) e non solo per predire il prezzo esatto.

### Indicatori Chiave
- **Bande di Bollinger**: Misurano la volatilità (fasi di espansione vs contrazione). Breakout delle bande indicano direzionalità.
- **MACD**: Indica il momentum (MACD Line, Signal Line, Istogramma). Incroci e divergenze generano segnali.
- **RSI**: Misura forza del momentum (Ipercomprato >70, Ipervenduto <30) e le divergenze prezzo/RSI.

### Immagini Analizzate (Estratte dai documenti)
- `indi-680x309-1.jpeg`: Grafico Bitcoin/USD giornaliero. Rettangoli verdi evidenziano movimenti rialzisti impulsivi seguiti da fasi di consolidamento. Una freccia rossa segna un ritracciamento ribassista.
- `macd-3.jpg`: Grafico Bitcoin a 4h con indicatore MACD (MACD line, Signal line e istogramma) che mostra cross e oscillazioni attorno allo zero.
- `macd2.jpg`: Grafico Bitcoin 1D che mostra una divergenza ribassista tra prezzo (massimi crescenti) e RSI (massimi decrescenti), preannunciando un'inversione di trend.
- `pat10.jpg`: Esempio di candela *Doji* (apertura e chiusura coincidenti, elevata incertezza).
- `pat11.jpg`: Esempio di candela *Marubozu* (corpo pieno senza shadow, forte momentum).
- `pat12.jpg`: Esempio di pattern *Engulfing* (inversione direzionale).
- `Immagine_2022-02-05_143149.png`: Grafico a linee "Compounding Wins", che dimostra l'impatto esponenziale positivo dell'incremento progressivo del rischio dopo una serie di trade vincenti.

## 3. Gestione Operativa e Risk Management
- **Risk to Reward (R/R)** e **Win Rate**: Metriche chiave per misurare un Trading System.
- **Gestione posizione**: Stop Loss (fisso, trailing, a chiusura candela), Take Profit, Break-Even, Parziali.
- **Position Sizing**: Allocazione dinamica tramite *Compounding Wins* (aumentare il rischio dopo successi) e *Cutting Losses* (diminuire il rischio dopo perdite). Formula di Kelly citata per ottimizzare la \% del capitale.

## 4. Rendita Passiva (CeFi e DeFi)
- **Staking e Lending**: Fornire valuta come validatore o prestatore.
- **Liquidity Provider (LP)** nei DEX (es. Uniswap, PancakeSwap) tramite Automated Market Makers (AMM).
- Rischio di **Impermanent Loss**: Perdita potenziale rispetto all'hold semplice se i prezzi degli asset nel pool divergono pesantemente.
- Utilizzo di aggregatori (Combo Farming) e protocolli per asset sintetici.

## 5. Trading System
Costruzione, testing e iterazione di una strategia.
- Progettazione dei setup.
- Backtest sui dati storici e test real-time con capitale ridotto.
- Costante revisione tramite **Trading Journal** per gestire Compound Wins e Cutting Losses.
