---
title: TradingAgents Framework
type: source
tags:
  - architecture
  - research
  - multi-agent
raw_source_path: raw/articles/TradingAgents.md
created: 2026-05-12
updated: 2026-05-12
status: active
related:
  - "[[paper-trading-agents]]"
  - "[[build/system-map]]"
---

# TradingAgents Framework

Framework di trading multi-agente open-source sviluppato da Tauric Research (UCLA/MIT). Benchmark architetturale di riferimento per il progetto.

## Struttura

Simula una trading firm reale con 7 ruoli specializzati:
- **Analyst Team** (4 agenti): Fundamental, Sentiment, News, Technical
- **Researcher Team**: Bull e Bear che dibattono per far emergere rischi e opportunità
- **Trader Agent**: sintetizza report e dibattiti per decidere timing e size
- **Risk Management Team**: 3 livelli (aggressivo, neutrale, conservativo)
- **Fund Manager**: approvazione finale

## Pattern adottati nel nostro progetto

- **Comunicazione strutturata via JSON** (non chat free-form) tra agenti — evita l'effetto "telefono senza fili"
- **Quick Thinker + Deep Thinker**: modelli economici per raccolta dati, modelli capaci solo per la decisione finale
- **Risk Management upstream** (nostra variante): nel TradingAgents originale il Risk Team valuta *dopo* il Trader; nel nostro design il Risk Analyst agisce *prima*, impostando i paletti

## Fonte

Paper completo: [[paper-trading-agents]]
