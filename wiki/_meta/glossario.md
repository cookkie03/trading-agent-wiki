---
title: "Glossario del Progetto"
type: ops
tags:
  - glossary
  - reference
created: 2026-05-13
updated: 2026-06-03
status: active
area: ops
---

# Glossario del Progetto

Termini usati nel progetto, spiegati in modo semplice. Aggiornare qui quando si introduce un nuovo concetto.

---

## Termini di Trading

**Swing Trading**
Strategia in cui si apre una posizione e la si tiene per giorni o settimane (non ore o minuti). È quello che facciamo noi: analisi profonda, poche operazioni, orizzonti 4h/daily.

**Paper Trading / Testnet**
Operare con denaro virtuale su un ambiente di test. Binance Testnet è il "campo di allenamento" del sistema: zero rischio reale, ma comportamento identico al live.

**SL / TP (Stop Loss / Take Profit)**
Ordini automatici che chiudono una posizione quando il prezzo raggiunge un certo livello.
- **Stop Loss**: limite di perdita (es. "esci se perdi più del 3%")
- **Take Profit**: obiettivo di profitto (es. "esci se guadagni il 7%")
→ Obbligatori nel nostro sistema. Senza di essi, anche con un win rate del 66% si può subire un drawdown devastante (evidenza: progetto Simone Rizzo).

**Long / Short**
- **Long**: scommetto che il prezzo salirà (compro)
- **Short**: scommetto che il prezzo scenderà (vendo allo scoperto)

**Leva finanziaria**
Moltiplicatore dell'esposizione. Con leva 5x e 100€, controllo una posizione da 500€. I profitti (e le perdite) vengono moltiplicati per 5. Usare con cautela.

**Limit Order**
Ordine che si esegue solo al prezzo che specifico (o migliore). Contrario di market order (esegue subito al prezzo corrente, spesso meno favorevole).

---

## Termini di Architettura Software

**Monolite Modulare**
Un singolo programma Python con componenti ben separati (moduli/classi) che comunicano tra loro via database centrale. L'alternativa sono i microservizi (tanti piccoli programmi separati), che sono più complessi da gestire. Noi partiamo con il monolite: più semplice, più veloce da sviluppare, si può evolvere in microservizi poi.

**Principio Deterministico**
Regola fondamentale del nostro progetto: l'LLM fa solo il ragionamento finale. Tutto il resto (calcoli, raccolta dati, esecuzione ordini) è Python puro, prevedibile e testabile. "Deterministico" = dato lo stesso input, ottieni sempre lo stesso output.

**DB Centrale (Database)**
Il cuore del sistema. Tutti i moduli scrivono qui i loro risultati; il Prompt Builder li legge da qui. Usiamo PostgreSQL in produzione, SQLite in sviluppo locale.

**JSON strutturato**
Formato di output obbligatorio per il Trader Agent. Il modello LLM deve rispondere sempre in un formato fisso (es. `{"azione": "open", "asset": "BTCUSDT", "direzione": "long", "leva": 3, "reasoning": "..."}`). Il codice Python può leggerlo automaticamente senza interpretarlo.

**Cron Job**
Task programmato che si esegue automaticamente a intervalli regolari. Il nostro sistema gira ogni 4h o 24h come cron job.

**CCXT**
Libreria Python che ti permette di parlare con quasi tutti gli exchange (Binance, Hyperliquid, ecc.) con lo stesso codice. Cambi exchange cambiando una riga di configurazione.

**Tool parametrizzabile**
Un modulo/funzione che accetta parametri in input invece di avere valori hardcodati. Es: non "calcola media mobile a 50" ma "calcola media mobile con period=N". L'AI può sperimentare diversi parametri senza toccare il codice.

**Adapter / Wrapper (broker)**
Un file che "traduce" l'API di un servizio esterno (es. Alpaca, IBKR) in un'interfaccia interna standard usata dal programma. Cambiare broker = cambiare adapter, senza toccare il resto del codice — come si cambia provider LLM in TradingAgents. Vedi [[system/modules/execution]].

**Time-series DB**
Database ottimizzato per dati indicizzati nel tempo (prezzi, indicatori, serie macro): scrittura/lettura efficiente di sequenze temporali. Forma di storage prevalente scelta per il progetto, affiancata da strutture a oggetti per la rendicontazione. Vedi [[system/modules/data-layer]].

**Subgraph (LangGraph)**
Un grafo annidato dentro un altro, con il proprio state isolato, che restituisce al grafo padre solo il risultato. Utile per analizzare più ticker in parallelo senza mescolarne gli state. Vedi [[system/parallelism-design]].

---

## Termini di Analisi Quantitativa

**Backtesting**
Testare una strategia di trading su dati storici per vedere come avrebbe performato nel passato. Non garantisce il futuro, ma aiuta a escludere le strategie chiaramente cattive. Usiamo **VectorBT** come framework.

**VectorBT**
Libreria Python per il backtesting. È quella usata da MarketSenseAI (progetto di ricerca accademica). Gestisce i costi di transazione in modo preciso — fondamentale per evitare risultati gonfiati.

**Look-Ahead Bias**
Errore nel backtesting: usare informazioni che in realtà non erano ancora disponibili al momento della decisione. Es: usare i risultati di un trimestre per decidere un trade prima che quel trimestre fosse stato pubblicato. Rende i backtest falsi e inutili.

**Sharpe Ratio**
Misura quanto rendimento ottieni per ogni unità di rischio che ti prendi. Più alto è meglio. Formula semplificata: rendimento extra / volatilità. Un Sharpe > 1 è generalmente considerato buono.

**Sortino Ratio**
Simile allo Sharpe, ma penalizza solo la volatilità negativa (le perdite), non quella positiva (i guadagni). Più realistico per valutare il rischio reale.

**Drawdown**
La perdita massima rispetto al picco del portafoglio. Es: se il portafoglio raggiunge 1000€, poi scende a 750€, il drawdown è -25%. Metrica fondamentale: un sistema può avere rendimento medio positivo ma drawdown insostenibile.

**Win Rate**
Percentuale di trade chiusi in profitto. Es: 16 trade in profitto su 24 totali = win rate 66.7%. Un win rate alto non basta: dipende anche dall'entità delle vincite vs perdite.

**VaR (Value at Risk)**
Stima della perdita massima probabile in un dato periodo con una certa probabilità. Es: "con il 95% di probabilità, non perderò più di X€ nei prossimi 5 giorni". Usato dal Risk Analyst Agent per imporre limiti.

**CVaR (Conditional Value at Risk)**
Più prudente del VaR: stima la perdita media nei peggiori scenari (quelli oltre il VaR). Es: "nei peggiori 5% dei casi, perdo in media Y€". Preferito al VaR perché considera il rischio di coda (eventi rari ma devastanti).

**Pivot Points**
Livelli di prezzo calcolati matematicamente dalle candele precedenti (high, low, close). Usati come riferimenti spaziali per l'LLM: "il prezzo è sopra o sotto il pivot? Vicino a supporto o resistenza?". Tutti i sistemi pratici analizzati li includono nel prompt.

**Kelly Criterion**
Formula che dice quale **frazione del capitale** puntare su un'operazione per massimizzare la crescita nel lungo periodo: `f* = p − q/b` (p = prob. vincita, q = prob. perdita, b = rapporto vincita/perdita). Es: 60% di vincita con payoff 1:1 → punta il 20%. Nel progetto lega la **size alla qualità del segnale** (conviction + storico). In pratica si usa *frazionario* (half-Kelly) perché è molto aggressivo e dipende da stime affidabili. Dettagli in [[system/position-sizing]].

**Overfitting**
Quando una strategia è "cucita" così bene sui dati storici che funziona solo sul passato e fallisce sul futuro. Si combatte con walk-forward, split in/out-of-sample, CPCV e pochi parametri liberi. Tema aperto da affrontare con Salvatore.

**Conviction Level**
Quanto il sistema è convinto di un'idea (`Strong Buy`/`Buy`/`Hold`/`Sell`/`Strong Sell`, eventualmente con score numerico). Assegnato dal Portfolio Manager. Scala il position sizing e sblocca la leva via opzioni sui segnali `Strong`. Vedi [[system/rating-scoring]].

---

## Termini Post-MVP (da capire quando si arriva)

**Rebalancing Gate**
Meccanismo che evita l'overtrading (aprire e chiudere posizioni continuamente). Logica: esegui un ordine di ribilanciamento solo se la differenza tra la posizione attuale e quella target supera una soglia (es. 5%). Sotto soglia → non fare niente. Semplice da implementare, molto efficace.

**Quick Thinker + Deep Thinker**
Pattern architetturale: usa un modello LLM economico e veloce (es. DeepSeek small) per le operazioni frequenti di raccolta dati e analisi di superficie. Usa un modello più capace (ma costoso) solo per la decisione finale del Trader. Riduce il costo token senza sacrificare qualità sulla decisione critica.

**Black-Litterman**
Metodo matematico per costruire un portafoglio ottimizzato. Il punto di forza: permette di "iniettare" le previsioni dell'LLM come vincoli matematici nell'ottimizzazione. L'LLM dice "penso che BTC salirà del 5% con confidenza 0.7"; Black-Litterman traduce questo in pesi di portafoglio ottimali. Il calcolo lo fa Python, non l'LLM.

**Entropy Pooling**
Versione più potente di Black-Litterman. Permette viste non solo sui rendimenti attesi, ma su volatilità, correlazioni, scenari di stress. Utile quando si hanno più agenti con previsioni diverse: aggrega tutto con pesi di confidenza.

**Regime Detection (HMM)**
L'HMM (Hidden Markov Model) riconosce automaticamente in quale "stato" si trova il mercato: toro (prezzi in salita), orso (prezzi in discesa), laterale (range). Utile per adattare la metrica di rischio: in toro si può essere più aggressivi, in orso più difensivi (CVaR).

**Opinion Pooling**
In un sistema multi-agent, tecnica per combinare le previsioni di più agenti assegnando pesi di probabilità a ciascuno. I pesi possono essere dinamici (RL module li aggiorna in base ai risultati storici di ogni agente).

**Walk-Forward Backtesting**
Metodo di backtesting più realistico. Si addestra il modello su un periodo, si testa sul successivo, si avanza nel tempo e si ripete.

**CPCV (Combinatorial Purged Cross-Validation)**
Tecnica avanzata per evitare il look-ahead bias nella validazione dei modelli. Elimina i dati adiacenti ai confini tra training e test per evitare autocorrelazione.

---

## Modelli LLM rilevanti

**DeepSeek**
Modello LLM cinese open-source. Scelta principale del progetto. Costo: circa 1/20-1/30 rispetto a GPT-4/GPT-5. Performance in Alpha Arena: 2° posto (+4.76%), unico modello commercialmente accessibile a battere buy-and-hold BTC.

**Qwen 3 Max**
Modello LLM cinese. Vincitore di Alpha Arena (+22.88%). Non ancora accessibile facilmente via API come DeepSeek. Da monitorare.

**Alpha Arena**
Benchmark competitivo in cui 6 LLM di frontiera hanno operato con 10.000$ reali in leva su crypto per 2 settimane. Risultati: Qwen 3 Max e DeepSeek vincono, GPT-5/Gemini/Claude perdono >30-50%.

---

*Aggiornare questo glossario ogni volta che si introduce un nuovo termine nel progetto.*
