---
title: "Portfolio Optimizer (cvx-portfolio-optimizer)"
type: source
tags:
  - quant
  - software
  - optimization
raw_source_path: "raw/articles/optimizer/"
created: 2026-05-12
updated: 2026-05-21
status: active
confidence: high
related:
  - "[[build/modules/risk-analyst]]"
  - "[[build/system-map]]"
---

# Portfolio Optimizer (cvx-portfolio-optimizer)

Libreria Python per la costruzione e l'ottimizzazione di portafogli quantitativi, basata su `skfolio` e `scikit-learn`.

## Architettura e Design

- **Frozen-config + Factory Pattern**: le configurazioni sono dataclass immutabili e serializzabili; le factory creano gli stimatori. Permette di loggare e storicizzare ogni configurazione di trade/ottimizzazione in modo pulito.
- **Pipeline scikit-learn**: ogni componente (preprocessing, selezione, ottimizzazione) è un trasformatore sklearn. L'intera catena è validabile e tunabile come un singolo oggetto.
- **Data Flow**: `prices → returns → [preprocess → pre-select → optimize] → backtest → weights`

## Caratteristiche principali

- **Pipeline-driven**: orchestrazione end-to-end da prezzi a pesi validati
- **Preprocessing**: validazione dati, outlier treatment, imputation
- **Pre-selection**: filtri per varianza, correlazione, dominanza, scadenza
- **Moments**: 5 stimatori di rendimento atteso e 11 di covarianza; supporta HMM per regimi di mercato
- **Views — Black-Litterman & Entropy Pooling**: integra le views (previsioni LLM) nell'ottimizzazione matematica
- **Optimization**: oltre 10 modelli (Mean-Risk, Risk Budgeting, HRP, HERC, NCO, robust ellipsoidal)
- **Validation**: Walk-Forward, Combinatorial Purged CV (CPCV)
- **Regime detection (HMM)**: adatta il modello di rischio al regime di mercato
- **Scoring**: 19 metriche di performance (Sharpe, Sortino, Calmar, ecc.)
- **Factors**: 17 fattori in 9 gruppi per la selezione degli asset

## Ruolo nel progetto

Motore di calcolo candidato per il **Portfolio Allocator** (post-MVP). Implementa deterministicamente:
- Traduzione delle views LLM in pesi portfolio (via Black-Litterman / Entropy Pooling)
- Ribilanciamento con Rebalancing Gate
- Hard limits (statuto del fondo)
- Il design "Config + Factory" è compatibile con il layer DB: la configurazione del portafoglio può essere salvata nel DB e riletta deterministicamente
- Le "Views" sono il punto di contatto ideale tra LLM e Quant: l'LLM produce un'opinione e la libreria la integra matematicamente
