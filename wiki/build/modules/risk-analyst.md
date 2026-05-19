---
title: "Risk Analyst Agent"
type: build
tags:
  - build
  - software
  - strategy
created: 2026-05-13
updated: 2026-05-13
status: active
priority: low
area: software
related:
  - "[[build/system-map]]"
  - "[[build/modules/module-d-prompt-builder-trader]]"
  - "[[build/decision-log]]"
---

# Risk Analyst Agent

**Post-MVP — dopo che Modulo A + C + D girano insieme.**

Il guardiano del rischio. Opera **upstream** del Trader: imposta i paletti dinamici per il ciclo corrente prima che il Trader prenda qualsiasi decisione. Il Trader decide dentro quello spazio, non viene corretto fuori da esso.

---

## Cosa fa

Ogni ciclo, prima del Prompt Builder:

1. Legge lo **stato corrente del portafoglio** (esposizione, liquidità, drawdown corrente)
2. Legge lo **stato del mercato** (volatilità, volume, segnali di regime)
3. Calcola e produce un **briefing rischio** da iniettare nel prompt:
   - VaR (perdita max stimata nel periodo)
   - Esposizione massima ammessa per il ciclo corrente
   - Range SL/TP ammissibili (in % del capitale)
   - Go / No-Go per il ciclo (se le condizioni di mercato lo sconsigliano)

---

## Differenza rispetto al Security Module

| | Risk Analyst (upstream) | Security Module (downstream) |
|-|------------------------|------------------------------|
| Quando | Prima del Trader | Dopo la proposta del Trader |
| Cosa fa | Imposta i paletti dinamici | Valida la proposta contro i paletti fissi |
| Natura | Contestuale (cambia ogni ciclo) | Deterministico (regole fisse — statuto del fondo) |
| Implementazione | LLM o algoritmo | Python puro, no LLM |

---

## Decisioni aperte

- **Cash-out strategy**: quale % dei profitti viene estratta periodicamente? Deve essere codificata come regola del Risk Analyst / statuto del fondo.
- **Regole del portafoglio (statuto)**: max esposizione per asset, regola +100% → vendi, max drawdown tollerato prima di stop. Salvatore porta queste regole dall'esperienza di Starting Finance.
- **Regime detection**: in futuro, usare HMM per adattare la metrica di rischio al regime (varianza in bull, CVaR in bear). Post-MVP avanzato.

---

## Dipendenze

- Legge da: `portfolio_state`, `market_data`
- Scrive in: `module_outputs` (briefing rischio per il Prompt Builder)
- Il Prompt Builder lo include come sezione dedicata nel prompt del Trader

---

## Librerie candidate (post-MVP)

- **cvx-portfolio-optimizer** (skfolio): gestisce Black-Litterman, Entropy Pooling, CVaR, regime detection via HMM. Vedere [[references/external/cvx-portfolio-optimizer]].
