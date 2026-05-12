---
title: "Portfolio Optimizer (Library Documentation)"
type: source
tags:
  - source
  - build
  - software
  - optimization
raw_source_path: "raw/articles/optimizer/"
created: 2026-05-12
updated: 2026-05-12
confidence: high
status: reviewed
related:
  - "[[build/system-map]]"
  - "[[theory/modular-trading-agent-architecture]]"
---

# Portfolio Optimizer (Library)

Piattaforma di ottimizzazione e costruzione di portafogli quantitativi costruita su `skfolio` e `scikit-learn`.

## Architettura e Design

- **Frozen-config + Factory Pattern**: Le configurazioni sono dataclass immutabili e serializzabili. Le factory creano gli stimatori. Questo permette di loggare e storicizzare ogni configurazione di trade/ottimizzazione in modo pulito.
- **Pipeline scikit-learn**: Ogni componente (preprocessing, selezione, ottimizzazione) è un trasformatore sklearn. L'intera catena è validabile e tunabile come un singolo oggetto.
- **Data Flow**: `prices → returns → [preprocess → pre-select → optimize] → backtest → weights`.

## Caratteristiche Principali

- **Pipeline**: Orchestrazione end-to-end da prezzi a pesi validati.
- **Preprocessing**: Validazione dati, outlier treatment, imputation.
- **Pre-selection**: Filtri per varianza, correlazione, dominanza, scadenza.
- **Moments**: 5 stimatori di rendimento atteso e 11 di covarianza. Supporta HMM (Hidden Markov Models) per regimi di mercato.
- **Views**: Black-Litterman, Entropy Pooling (per integrare opinioni soggettive/LLM nell'ottimizzazione quantitativa).
- **Optimization**: Oltre 10 modelli (Mean-Risk, Risk Budgeting, HRP, HERC, NCO, robust ellipsoidal).
- **Validation**: Walk-Forward, Combinatorial Purged CV.
- **Scoring**: 19 metriche di performance (Sharpe, Sortino, Calmar, ecc.).
- **Factors**: 17 fattori in 9 gruppi.

## Relazione con il Progetto

- Fornisce il **motore deterministico** per il modulo di Risk/Portfolio Management.
- Permette di implementare l'approccio "Portfolio bilanciato" discusso con Salvatore.
- Il design "Config + Factory" è perfetto per il nostro `Prompt Builder` e `DB` layer: possiamo salvare la configurazione del portafoglio nel DB e rileggerla deterministicamente.
- Le "Views" sono il punto di contatto ideale tra LLM e Quant: l'LLM produce un'opinione (view) e la libreria la integra matematicamente nel portafoglio.
