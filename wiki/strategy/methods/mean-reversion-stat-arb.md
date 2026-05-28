---
title: "Mean Reversion e Statistical Arbitrage"
type: synthesis
tags:
  - strategy
  - quant
  - mean-reversion
  - backtesting
created: 2026-05-22
updated: 2026-05-22
status: draft
related:
  - "[[strategy/index]]"
  - "[[strategy/methods/trend-following]]"
  - "[[build/modules/quant-backtesting]]"
  - "[[references/note-audio-salvatore-quant-strategy]]"
  - "[[references/quantitative-trading-strategies-brenndoerfer]]"
confidence: medium
area: strategy
---

# Mean Reversion e Statistical Arbitrage

Strategia quantitativa che sfrutta la tendenza di asset correlati a tornare alla loro relazione storica dopo una divergenza. Identificata da Salvatore come potenziale prima strategia codificabile per il progetto.

---

## Principio di base

**Mean Reversion**: quando due asset storicamente correlati divergono dal loro spread normale, si presuppone che la divergenza sia temporanea e che lo spread tornerà ai livelli normali.

**Statistical Arbitrage (Stat Arb) / Pairs Trading**: implementazione operativa della mean reversion su coppie di asset correlati:
1. Identificare due asset altamente correlati
2. Monitorare lo spread tra i due prezzi
3. Entrare in posizione quando lo spread supera una soglia statistica
4. Chiudere la posizione quando lo spread si assottiglia (convergenza)

---

## Esempio concreto

- **Coca-Cola vs Pepsi**: due aziende nel stesso settore, ricavi simili, dovrebbero muoversi in modo quasi identico
- **Gold EUR vs Gold USD**: lo stesso asset in valute diverse — lo spread riflette solo il cambio
- In pratica: se Coca-Cola sale del 5% e Pepsi rimane ferma, c'è una divergenza → long Pepsi, short Coca-Cola, aspettando che Pepsi recuperi (o Coca-Cola torni)

---

## Applicazione al progetto

### Perché è interessante

- **Codificabile facilmente**: la logica è deterministica e basata su correlazione statistica
- **Non richiede velocità elevatissima**: compatibile con orizzonte swing trading (4h/daily)
- **Non usa derivati**: si può implementare con posizioni long/short su equity o crypto
- **Identificabile con funzioni Python semplici**: calcolo spread, z-score, soglie

### Filtri di Salvatore (strategie scartate)

Salvatore ha esplicitamente scartato:
- Strategie che richiedono derivati
- Strategie che richiedono frequenza troppo alta (incompatibili con costo token LLM)
- Strategie incompatibili con le competenze attuali del team

La mean reversion supera questi filtri.

---

## Implementazione tecnica (bozza)

### Step 1: Identificare coppie correlate

```python
import pandas as pd
import numpy as np
from scipy import stats

def find_cointegrated_pairs(prices_df, significance=0.05):
    """Trova coppie cointegrate (correlazione stabile a lungo termine)."""
    n = prices_df.shape[1]
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            asset_i = prices_df.iloc[:, i]
            asset_j = prices_df.iloc[:, j]
            # Test di cointegrazione (es. Engle-Granger)
            # ... [da implementare con statsmodels]
            pairs.append((i, j))
    return pairs
```

### Step 2: Calcolare lo spread e z-score

```python
def calculate_spread_zscore(asset_a, asset_b, window=30):
    """
    Calcola lo spread tra due asset e il suo z-score.
    Lo z-score indica di quante deviazioni standard siamo dalla media.
    """
    spread = asset_a - asset_b  # o ratio: asset_a / asset_b
    rolling_mean = spread.rolling(window).mean()
    rolling_std = spread.rolling(window).std()
    zscore = (spread - rolling_mean) / rolling_std
    return spread, zscore
```

### Step 3: Segnali di trading

```python
def generate_signals(zscore, entry_threshold=2.0, exit_threshold=0.5):
    """
    entry_threshold: entra quando |zscore| > 2 (2 deviazioni standard)
    exit_threshold: esci quando |zscore| < 0.5 (vicino alla media)
    """
    signals = pd.Series(0, index=zscore.index)
    signals[zscore > entry_threshold] = -1   # Short asset_a, long asset_b
    signals[zscore < -entry_threshold] = 1   # Long asset_a, short asset_b
    signals[abs(zscore) < exit_threshold] = 0  # Chiudi posizione
    return signals
```

---

## Rischi e limitazioni

### Rischio principale: regime change

L'assunzione di mean reversion **può fallire catastroficamente** quando:
- La correlazione tra i due asset si rompe definitivamente (es. fallimento di un'azienda)
- Cambia il regime di mercato (es. settore in crisi strutturale)
- L'evento macro è sistemico e colpisce entrambi gli asset

**Gestione**: stop loss rigorosi sul trade; monitorare la correlazione nel tempo; non assumere che la correlazione sia permanente.

### Holding period

Giorni/settimane. Richiede risk management sofisticato (da Brenndoerfer).

---

## Status nel progetto

| Aspetto | Stato |
|---------|-------|
| Identificazione strategia | Completato (Salvatore) |
| Letteratura da studiare | In corso (articolo 80 pagine trovato da Salvatore) |
| Backtesting con VectorBT | Da fare (Modulo C) |
| Decisione inclusione nel Modulo C | Aperta — da discutere con Salvatore |

---

## Prossimi passi

1. Salvatore completa la lettura dell'articolo tecnico trovato
2. Confronto Luca+Salvatore: includere come prima strategia in Modulo C?
3. Se sì: implementare in VectorBT (framework già deciso per backtesting)
4. Testare su cripto (più facile per correlazioni e API pubbliche) o su equity?

---

## Relazione con altre strategie

- **Opposta al trend following**: trend following scommette sulla persistenza del trend, mean reversion scommette sul ritorno alla media
- **Complementare**: un fondo che usa entrambe (idea dual portfolio di Salvatore) ha diversificazione naturale
- Vedere [[references/note-audio-salvatore-quant-strategy]] per l'idea del dual portfolio
