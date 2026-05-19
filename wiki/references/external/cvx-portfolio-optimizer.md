---
title: "Portfolio Optimizer (cvx-optimizer)"
type: source
tags:
  - quant
  - software
raw_source_path: "raw/articles/optimizer/"
created: 2026-05-12
updated: 2026-05-12
status: active
related:
  - "[[references/library-portfolio-optimizer]]"
  - "[[build/modules/risk-analyst]]"
---

# Portfolio Optimizer (cvx-optimizer)

Libreria Python per la costruzione e l'ottimizzazione di portafogli quantitativi, basata su `skfolio` e `scikit-learn`.

## Caratteristiche principali

- **Pipeline-driven**: orchestrazione completa prezzi → pesi
- **Black-Litterman & Entropy Pooling**: integra le views (previsioni) dell'LLM nell'ottimizzazione matematica
- **Factor Research**: 17 fattori per la selezione degli asset
- **Walk-Forward + CPCV**: backtesting robusto con purging temporale
- **Regime detection (HMM)**: adatta il modello di rischio al regime di mercato

## Ruolo nel progetto

Motore di calcolo candidato per il **Portfolio Allocator** (post-MVP). Implementa deterministicamente:
- Traduzione delle views LLM in pesi portfolio (via Black-Litterman)
- Ribilanciamento con Rebalancing Gate
- Hard limits (statuto del fondo)

## Fonte

Documentazione completa: [[references/library-portfolio-optimizer]]
