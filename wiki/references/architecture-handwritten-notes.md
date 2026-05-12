---
title: "Appunti Architettura (Manoscritti)"
type: source
tags:
  - source
  - architecture
raw_source_path: "raw/notes/Trading Agent — Architecture Overview.md"
created: 2026-04-30
updated: 2026-05-12
confidence: high
status: reviewed
related:
  - "[[build/system-map]]"
---

# Appunti Architettura (Manoscritti)

Trascrizione dello schema grafico iniziale del sistema.

## Moduli Identificati

- **LLM Trader**: Cuore decisionale (JSON template, management models, leverage, stop loss).
- **News Module**: Gestione dei feed informativi.
- **Technical Analysis Module**: Analisi dei segnali tecnici.
- **Risk Management Module**: Basato sul rischio di portafoglio.
- **Prediction Module (LSTM)**: Parte di deep learning predittiva.
- **Reinforcement Learning**: Per pesare gli input degli altri moduli nel prompt.
- **Finance API**: Integrazione con Binance/Prezzi storici.
- **Security Module**: Controllo deterministico basato sul rischio.
- **Dashboard**: Interfaccia di monitoraggio.

## Note Tecniche
- Uso di **OpenRouter** come provider organizzato.
- Possibilità di **Fine-Tuning** persistente.
- Database indicizzato per serie storiche.
