---
title: "Portfolio Optimizer (cvx-optimizer)"
type: entity
tags:
  - entity
  - software
  - quant
created: 2026-05-12
updated: 2026-05-12
status: active
related:
  - "[[references/library-portfolio-optimizer]]"
---

# Portfolio Optimizer (cvx-optimizer)

Libreria Python per la costruzione e l'ottimizzazione di portafogli quantitativi, basata su `skfolio` e `scikit-learn`.

## Caratteristiche
- **Pipeline-driven**: Orchestrazione completa prezzi-to-pesi.
- **Black-Litterman & Entropy Pooling**: Permette di integrare opinioni qualitative nell'ottimizzazione quantitativa.
- **Factor Research**: Supporta 17 fattori per la selezione degli asset.
- **Robustness**: Include modelli di ottimizzazione robusta e regimi di mercato (HMM).

## Uso nel Progetto
- Motore di calcolo per il modulo di **Portfolio Management**.
- Implementazione deterministica dello "statuto del fondo" e del ribilanciamento.
- Bridge tra le previsioni dell'LLM (Views) e l'allocazione del capitale.
