---
title: "Quantitative Trading Strategies: Alpha, Backtesting & Performance (Brenndoerfer)"
type: source
tags:
  - source
  - quant
  - backtesting
  - strategy
  - research
raw_source_path: "raw/archived/articles/quant strategy/Quantitative Trading Strategies Alpha, Backtesting & Performance - Interactive.md"
created: 2026-05-22
updated: 2026-05-22
confidence: high
status: active
related:
  - "[[strategy/index]]"
  - "[[strategy/methods/trend-following]]"
  - "[[system/modules/quant-backtesting]]"
  - "[[strategy/methods/dual-portfolio]]"
---

# Quantitative Trading Strategies: Alpha, Backtesting & Performance (Brenndoerfer)

Articolo tecnico interattivo di Michael Brenndoerfer (Associate Director of Data Science, EQT Partners). Fonte: mbrenndoerfer.com, pubblicato 2025-12-26. Introduce i fondamentali del quantitative trading: alpha, categorie di strategie, workflow di sviluppo, backtesting, validazione statistica e performance metrics. Include codice Python completo per ogni concetto.

---

## 1. Alpha — Il concetto centrale

**Alpha** = il ritorno in eccesso di un investimento rispetto a quello predetto dall'esposizione al rischio sistematico.

### Formula CAPM

$$r_i - r_f = \alpha_i + \beta_i(r_m - r_f) + \epsilon_i$$

- $r_i$: ritorno dell'investimento
- $r_f$: risk-free rate
- $r_m$: ritorno di mercato
- $\beta_i$: sensibilità ai movimenti di mercato
- $\alpha_i$: **ritorno non spiegato dall'esposizione al rischio** — questo è l'alpha
- $\epsilon_i$: errore idiosincratico

**Interpretazione**: alpha positivo al 3% annuo = il portafoglio ha reso 3 punti percentuali in più di quanto CAPM prevede dato il suo beta. È genuina skill, non semplice esposizione al rischio di mercato.

### Alpha Multi-Factor

Il singolo fattore (mercato) spesso non basta. I modelli multi-factor aggiungono: value, momentum, size. L'alpha in questo contesto è più difficile da generare ma più significativo:

$$r_i - r_f = \alpha_i + \sum_{j=1}^{k} \beta_{ij} f_j + \epsilon_i$$

**Punto critico**: una strategia che sembra generare alpha contro un modello a fattore singolo potrebbe avere alpha zero una volta controllato per momentum o value. Bisogna alzare il bar.

### Fonti di Alpha

- **Informational advantage**: accesso o processing di informazioni più veloci o più efficaci
- **Analytical advantage**: modelli superiori su dati pubblici
- **Behavioral exploitation**: sfruttare bias sistematici di altri investitori
- **Structural inefficiencies**: sfruttare vincoli di altri partecipanti (regulatory limits, benchmark tracking, liquidity needs)
- **Risk transfer**: compenso per fornire assicurazione o liquidità

**Alpha decay**: quando una strategia diventa nota, l'inefficienza che sfrutta diminuisce o scompare. Bisogna evolversi continuamente.

---

## 2. Categorie di Strategie Quantitative

### Statistical Arbitrage e Mean Reversion

Identifica asset i cui prezzi hanno divergito dalla relazione storica/prevista, scommettendo che i prezzi torneranno ai livelli normali.

**Esempio classico**: pairs trading — se due stock storicamente correlati divergono, si shorta il sovraperformante e si compra il sottoperformante, profittando quando la relazione si normalizza.

**Assunzione core**: le deviazioni di prezzo sono temporanee e dovute al rumore, non a cambiamenti fondamentali.

**Funziona meglio quando**:
- Gli asset hanno forti legami economici (due oil company, un'azione e il suo ADR)
- Esistono meccanismi di arbitraggio per far rispettare le relazioni di prezzo
- Le deviazioni sono causate da fattori temporanei come order flow imbalances

**Holding period**: giorni/settimane. Richiede risk management sofisticato perché l'assunzione di reversione può fallire catastroficamente in regime change.

### Trend Following e Momentum

Approccio opposto alla mean reversion: scommette che i trend esistenti continueranno. Supportato empiricamente da autocorrelazione positiva dei ritorni a orizzonte medio-termine.

**Momentum**: identifica asset con performance recente forte (o debole) e scommette che il trend continua.

**Spiegazioni economiche**:
- Underreaction: gli investitori inizialmente sottoreagiscono alle nuove informazioni, causando aggiustamenti graduali del prezzo
- Behavioral feedback: prezzi in salita attraggono compratori, creando cicli auto-rafforzanti
- Risk-based: i ritorni momentum possono compensare per crash risk durante le inversioni

**Holding period**: settimane/mesi. Applicabile cross-asset. Tende a performare bene durante crisi (quando i trend diventano estremi) — buona diversificazione.

### Factor Investing e Long/Short Equity

Cattura sistematicamente i ritorni associati a caratteristiche come value, quality, momentum, low volatility.

**Long/short equity**: portafoglio long su stock con esposizione favorevole ai fattori, short su stock con esposizione sfavorevole. Market exposure limitata, focus su factor exposure.

Formula del ritorno:
$$r_{\text{portfolio}} = \alpha + \beta_{\text{market}} \cdot r_{\text{market}} + \beta_{\text{value}} \cdot f_{\text{value}} + \beta_{\text{momentum}} \cdot f_{\text{momentum}} + \epsilon$$

### Volatility Trading e Arbitrage

Sfrutta discrepanze nel modo in cui la volatilità è prezzata tra strumenti o periodi temporali.

**Strategie comuni**:
- Variance risk premium harvesting: vendere opzioni per catturare la tendenza di implied volatility ad eccedere la realized volatility
- Volatility surface arbitrage: sfruttare inconsistenze tra strikes e scadenze
- Dispersion trading: tradare la relazione tra volatilità dell'indice e dei singoli stock

### Market Making e Liquidity Provision

I market maker forniscono liquidità offrendo continuamente di comprare e vendere, guadagnando il bid-ask spread. Non si prevede la direzione dei prezzi, si facilita il trading.

**Non applicabile al nostro progetto** (richiede fast execution e inventory management real-time).

### High-Frequency Trading

Opera su timeframe misurati in microsecondi/secondi. Latency arbitrage, electronic market making, statistical patterns nell'order flow. Richiede infrastruttura tecnologica specializzata.

**Non applicabile al nostro progetto** (incompatibile con costo token LLM e orizzonte swing trading).

---

## 3. Workflow di Sviluppo della Strategia

### Fase 1: Idea Generation e Hypothesis Formation

Buone idee vengono da: research accademica, osservazione industry, analisi strutturale, analogie cross-asset.

**Disciplina chiave**: formulare le idee come ipotesi testabili e precise. Non "penso che il momentum funziona" ma "le azioni nel decile superiore di ritorno a 12 mesi, escluso il mese più recente, sovraperformeranno di almeno 6% annui nel mese successivo".

**Importanza dell'intuizione economica**: le strategie più robuste hanno una chiara razionale economica. Se non puoi spiegare perché altri partecipanti perderebbero soldi contro di te, il pattern è probabilmente spurio.

### Fase 2: Data Gathering e Preparation

- Identificare i dati necessari
- Sourcing e acquisizione
- Cleaning e validazione
- **Point-in-time alignment** (critico!): usare solo informazioni disponibili al momento storico della decisione. I dati finanziari vengono spesso rivisti — usare dati revised introduce look-ahead bias.

### Fase 3: Signal Construction

Il segnale traduce i dati grezzi in una previsione sui ritorni futuri.

**Costruzione**:
- Feature engineering: trasformare dati grezzi in variabili predittive
- Normalizzazione: rendere i segnali comparabili tra asset e periodi
- Combinazione: mescolare più segnali in un indicatore composito

**Esempio (momentum signal)**:
```python
def calculate_momentum_signal(prices, lookback=12, skip=1):
    # lookback=12: cattura il trend a medio termine
    # skip=1: esclude il mese più recente (evita reversal a breve)
    momentum = prices.shift(skip) / prices.shift(lookback) - 1
    # Normalizzazione cross-sectional (z-score)
    signal = momentum.sub(momentum.mean(axis=1), axis=0).div(
        momentum.std(axis=1), axis=0
    )
    return signal
```

### Fase 4: Model Building e Backtesting

Applica la strategia ai dati storici. **Fase più pericolosa** per overfitting.

**Framework backtesting rigoroso deve**:
- Rispettare la freccia del tempo: usare solo informazioni disponibili al punto decisionale
- Accountare per i costi di transazione: spread, commissioni, market impact
- Gestire l'esecuzione realistica: prezzi di esecuzione raggiungibili, non idealizzati
- Tracciare le dinamiche complete del portafoglio: posizioni, cash, margine

### Fase 5: Statistical Validation

**Problema principale: multiple testing**. Se testiamo 100 variazioni di strategia, è quasi certo trovarne almeno una che appare buona per caso puro.

$$P(\text{almeno un falso positivo}) = 1 - (1 - \gamma)^N$$

Per 100 test al 5%: probabilità del 99.4% di trovare almeno un falso positivo.

**Soluzioni**:
- Bonferroni correction: dividere la soglia di significatività per il numero di test
- Out-of-sample testing: riservare dati mai usati durante lo sviluppo
- False discovery rate control (Benjamini-Hochberg)

**Bootstrap Sharpe test**: testare statisticamente se lo Sharpe ratio è significativamente maggiore di zero.

### Fase 6: Risk Assessment

**Domande chiave**:
- Drawdown analysis: quali sono le perdite peggiori storiche? Quanto ci ha messo il recovery?
- Tail risk: i ritorni sono normalmente distribuiti o ci sono fat tails?
- Correlation regime: come performa la strategia in diverse condizioni di mercato?
- Leverage implications: come impattano i costi di borrowing e i margin requirements?

---

## 4. Performance Metrics

### Sharpe Ratio (il più usato)

$$\text{Sharpe Ratio} = \frac{E[r_p - r_f]}{\sigma_p}$$

- Misura il ritorno in eccesso per unità di rischio totale
- **Soglie**: Sharpe >1.0 è buono; Sharpe >2.0 è eccezionale e raro in pratica
- **Limite**: tratta la volatilità al rialzo uguale a quella al ribasso

### Sortino Ratio

$$\text{Sortino Ratio} = \frac{E[r_p - r_f]}{\sigma_{\text{down}}}$$

- Come Sharpe ma penalizza solo la volatilità al ribasso
- Migliore per strategie con distribuzione dei ritorni asimmetrica
- Un Sortino > Sharpe indica che la volatilità è principalmente al rialzo (positivo)

### Calmar Ratio

$$\text{Calmar Ratio} = \frac{\text{Annual Return}}{|\text{Max Drawdown}|}$$

- Rapporto ritorno annuo / massimo drawdown
- Ratio >1.0 = il ritorno annuo eccede la peggior perdita peak-to-trough

### Information Ratio

$$\text{Information Ratio} = \frac{E[r_p - r_b]}{\sigma_{r_p - r_b}}$$

- Misura il ritorno attivo rispetto a un benchmark
- Essenziale quando si è giudicati rispetto a un indice specifico

### Win Rate e Profit Factor

- **Win Rate**: percentuale di trade positivi
- **Profit Factor**: gross profit / gross loss. >1 = profittevole

---

## 5. Insidie Comuni

### Look-Ahead Bias

Usare informazioni non disponibili al momento della decisione:
- Usare prezzi fine giornata per decisioni intraday
- Usare dati finanziari revised invece di originally reported
- Assumere conoscenza immediata di index reconstitutions

### Survivorship Bias

Testare solo su titoli che sono sopravvissuti fino ad oggi, ignorando quelli che sono stati delistati, falliti o acquisiti. Sovrastima sistematicamente i ritorni perché i peggiori performer sono esclusi.

### Overfitting e Data Snooping

Segni di overfitting:
- La strategia richiede molti parametri o regole complesse
- La performance è sensibile a piccole variazioni di parametro
- La performance out-of-sample degrada significativamente
- La strategia funziona solo su sottoperiodi specifici

**Antidoto**: semplicità, razionale economica, test rigoroso out-of-sample. Le strategie più semplici con logica economica chiara sono più probabili da sopravvivere in live trading.

### Sottostima dei Costi di Transazione

Costi reali includono:
- Bid-ask spread: costo immediato del crossing
- Market impact: movimento dei prezzi contro di te per posizioni grandi
- Slippage: prezzi di esecuzione peggiori per latenza
- Borrowing costs: commissioni per shorting (possono essere sostanziali per hard-to-borrow names)

---

## 6. Transizione a Live Trading

### Paper Trading e Simulazione

Prima di rischiare capitale reale, testare in ambiente paper trading. Valida:
- L'infrastruttura di execution funziona correttamente
- I data feed sono affidabili e tempestivi
- L'order management gestisce edge cases
- I risk controls si attivano appropriatamente

### Position Sizing — Kelly Criterion

$$f^* = \frac{bp - (1-p)}{b} = \frac{p(b+1) - 1}{b}$$

- $f^*$: frazione ottimale del capitale da allocare
- $p$: probabilità di un trade vincente
- $b$: win/loss ratio (guadagno medio / perdita media)

In pratica si usa **fractional Kelly** (half Kelly o quarter Kelly) per margine di sicurezza contro errori di stima dei parametri.

### Monitoring e Adaptation

Le strategie decadono nel tempo man mano che il mercato apprende e si adatta. Metriche da monitorare continuamente:
- Performance vs. aspettativa: è la strategia dentro i parametri backtestati?
- Factor exposures: l'esposizione al rischio ha driftato dai livelli intesi?
- Execution quality: i fill avvengono ai prezzi attesi?
- Capacity utilization: c'è market impact crescente?

---

## Riferimento originale

- **Autore**: Michael Brenndoerfer (Associate Director of Data Science, EQT Partners, Singapore)
- **URL**: https://mbrenndoerfer.com/writing/quantitative-trading-strategies-overview-alpha-backtesting
- **Data pubblicazione**: 2025-12-26
- **Data ingest**: 2026-05-22
