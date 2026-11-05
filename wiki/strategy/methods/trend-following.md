---
title: Trend Following
type: synthesis
tags:
  - trend-following
  - strategy
  - market-structure
created: 2026-05-14T00:00:00.000Z
updated: 2026-05-14T00:00:00.000Z
status: active
confidence: medium
area: strategy
related:
  - '[[system/quant/quant-backtesting]]'
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

## Strategia MVP v0.1 — Trend Following Hourly

Stato: **proposta operativa da validare con backtest**, non ancora codice di produzione.

### Perimetro

- Barre: **1 hour**, valutazione alla chiusura della barra.
- Asset: azioni USA liquide, quotate in USD.
- Direzione: long-only, una posizione per simbolo.
- Holding: swing trading; nessun obbligo di chiusura a fine giornata.
- Azioni societarie, sessioni estese e dati con timestamp incoerenti sono esclusi dalla prima validazione; il calendario regular-hours va fissato nel dataset.

### Regole deterministiche

Parametri iniziali congelati per il primo backtest, non scelti dopo aver guardato il risultato:

- `entry_breakout_window = 20` barre: il close supera il massimo delle **20 barre precedenti**, escludendo la barra corrente.
- `trend_window = 50` barre: il close è sopra la EMA a 50 barre.
- `volume_window = 20` barre: il volume della barra è almeno `1.2 ×` la media dei volumi delle 20 barre precedenti.
- `atr_window = 14` barre, `stop_atr_multiplier = 2.0`: stop iniziale a `entry_price - 2 × ATR`.
- `trailing_atr_multiplier = 3.0`: trailing stop al massimo tra lo stop precedente e `highest_close - 3 × ATR`.

**Entry:** quando tutte le tre condizioni (breakout, trend e volume) sono vere alla chiusura della barra `t`, si genera un segnale long e si simula l'ingresso all'open della barra `t+1`.

**Exit:** si chiude all'open della barra successiva al primo evento tra:

1. prezzo della barra che tocca lo stop;
2. close sotto la EMA a 20 barre;
3. fine del dataset/backtest.

Se nella stessa barra sono toccati stop e altri livelli, prevale lo stop. Se l'open della barra è oltre lo stop, l'esecuzione avviene all'open (slippage/gap sfavorevole), non al prezzo teorico dello stop.

**No-lookahead:** nessun valore della barra `t+1` entra nel segnale calcolato su `t`; gli indicatori usano solo dati disponibili alla chiusura di `t`.

### Position sizing MVP

Il segnale non equivale a un ordine. Il sizing riceve un capitale disponibile e un budget di rischio:

`quantity = floor((equity × risk_fraction) / (entry_price - stop_price))`

Il primo backtest usa `risk_fraction = 0.5%`, limite di esposizione per posizione `10%` dell'equity e arrotondamento a quantità intera. Se la quantità risultante è zero, il trade è scartato. Il limite portfolio e il risk gate definitivo restano da chiudere.

### Protocollo di validazione

- Baseline non ottimizzata: parametri sopra riportati, senza scegliere la combinazione migliore a posteriori.
- Dati hourly Alpaca, salvati nel DB con provenance e sessione regular-hours esplicita.
- Costi e slippage devono essere parametri del backtest, non ignorati.
- Split temporale train/validation/test e walk-forward prima di considerare il risultato promettente.
- Benchmark statico: SPY buy-and-hold sullo stesso intervallo.
- Metriche minime: rendimento netto, max drawdown, Sharpe, Sortino, profit factor, win rate, numero trade, esposizione e turnover.
- Risultati confrontati con una baseline buy-and-hold e con una baseline senza filtro volume, per verificare che ogni filtro aggiunga valore.

Questa specifica è una **baseline v0.1**: il backtest può falsificarla, ma non deve modificarla automaticamente. Ogni variazione produce una nuova versione della strategia.

---

## Indicatori usati

La wiki indicava già medie mobili, MACD, RSI, Pivot Points e volume come candidati. Per MVP v0.1 vengono usati solo EMA20, EMA50, ATR14 e volume relativo; MACD, RSI e Pivot restano capability da valutare in versioni successive per evitare di aggiungere filtri senza evidenza.

---

## Metriche di valutazione

- **[[_meta/glossario#Sharpe Ratio|Sharpe ratio]]** — rischio/rendimento
- **[[_meta/glossario#Win Rate|Win rate]]** — % operazioni chiuse in profitto
- **[[_meta/glossario#Drawdown|Max drawdown]]** — perdita massima

*(pagine dedicate in `strategy/metrics/` da creare quando servono; vedi [[strategy/metrics/benchmark]])*

---

## Implementazione software

→ [[system/quant/quant-backtesting]] — il modulo che implementa e backtesta questa strategia

