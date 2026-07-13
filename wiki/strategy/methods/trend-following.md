---
title: "Trend Following"
type: synthesis
tags:
  - strategy
  - market-structure
created: 2026-05-14
updated: 2026-05-14
status: active
confidence: medium
area: strategy
related:
  - "[[system/quant/quant-backtesting]]"
---

# Trend Following

**Idea di base**: non battere i market maker istituzionali — accodarsi a loro. Gli istituzionali muovono i mercati con volumi enormi; il loro movimento lascia tracce negli indicatori tecnici. Il sistema entra dopo di loro, guadagnando una frazione del movimento.

---

## Logica

1. Gli istituzionali entrano per primi, causando il movimento di prezzo
2. Il sistema rileva il movimento tramite indicatori (stessi che usano loro)
3. Il sistema entra in ritardo — a metà o nell'ultimo quarto del movimento
4. Si guadagna meno degli istituzionali, ma il rischio è inferiore

> "Se loro entrano in cima e noi entriamo a metà punta, guadagniamo la metà. Ma è comunque positivo, soprattutto in leva." — Salvatore, call 2026-05-13

**Esempio concreto (Moncler, 2026-04-20)**: la trimestrale ha battuto le stime dell'80% sugli EPS. Il prezzo è partito da 48. Un sistema trend-following che rilevava il breakout entrava dopo la conferma del movimento, non nel punto esatto di svolta.

---

## Cosa richiede

- Indicatori tecnici per rilevare il trend (MACD, RSI, medie mobili, [[_meta/glossario#Pivot Points|Pivot Points]])
- Segnali di conferma del breakout (volume anomalo, rottura livelli chiave)
- SL/TP definiti per limitare il rischio di falsi segnali
- Capire quali sono effettivamente gli indicatori utilizzati oppure individuare i segnali che permettono di capire quando gli istituzionali stanno entrando o uscendo dal mercato (es: analisi sui volumi di scambio, che però non sono sempre disponibili in quanto gli istituzonali fanno spesso trade su mercati OTC e non pubblici)

---

## Punti di forza

- Semplice da implementare e da backtestare
- Non richiede previsioni sui fondamentali
- Funziona su qualsiasi asset liquido (crypto, equity)
- La strategia più immediata come punto di partenza

Proprio perché è semplice da implementare, resta una candidata forte come **primo blocco codificabile** del layer quant/tooling.

## Limiti

- In mercati laterali (range-bound) genera falsi segnali
- Entra sempre in ritardo — non cattura il massimo del movimento
- Sensibile alla qualità degli indicatori usati e ai loro parametri

---

## Indicatori usati

*(da popolare con Salvatore)*
- Medie mobili (parametro: periodo N)
- MACD
- RSI
- Pivot Points (riferimenti spaziali per capire dove siamo nel movimento)

---

## Metriche di valutazione

- **[[_meta/glossario#Sharpe Ratio|Sharpe ratio]]** — rischio/rendimento
- **[[_meta/glossario#Win Rate|Win rate]]** — % operazioni chiuse in profitto
- **[[_meta/glossario#Drawdown|Max drawdown]]** — perdita massima

*(pagine dedicate in `strategy/metrics/` da creare quando servono; vedi [[strategy/metrics/benchmark]])*

---

## Implementazione software

→ [[system/quant/quant-backtesting]] — il modulo che implementa e backtesta questa strategia

