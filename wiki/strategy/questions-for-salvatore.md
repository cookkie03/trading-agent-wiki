---
title: "Domande aperte per Salvatore"
type: synthesis
tags:
  - strategy
  - quant
  - roadmap
created: 2026-06-03
updated: 2026-06-04
status: active
priority: high
area: strategy
related:
  - "[[system/modules/quant-backtesting]]"
  - "[[system/rating-scoring]]"
  - "[[system/position-sizing]]"
  - "[[system/modules/execution]]"
confidence: high
---

# Domande aperte per Salvatore

> Foglio di lavoro per la prossima call con Salvatore. Raccoglie tutti i temi che richiedono la sua competenza di mercato (raccolti dalla risposta di Luca, 2026-06-02). Ognuno è anche tracciato come card in [[artifacts/project-board]].
>
> Aggiornamento 2026-06-23: Luca ha chiesto esplicitamente di **rivederle una per una insieme**, perché oggi non le sente ancora abbastanza chiare. Questa pagina va quindi usata come **agenda del meeting**, non solo come lista di domande sparse.

---

## 1. VaR di portafoglio — quale e come

Il [[_meta/glossario#VaR (Value at Risk)|VaR]] (~10%) è il guardrail principale dello Statuto, ma **il metodo non è definito**. Luca: *«deve capire Salvatore come gestirlo, come renderlo, quale usare»*.

Da decidere:
- **Tipo**: parametrico (varianza-covarianza) / storico / Monte Carlo?
- **VaR o [[_meta/glossario#CVaR (Conditional Value at Risk)|CVaR]]** (CVaR considera il rischio di coda — vedi [[_meta/glossario]])?
- **Lookback** (su quanti dati storici si stima)?
- **VaR incrementale**: come si calcola l'impatto sul VaR di una *nuova* posizione proposta, per il check deterministico pre-trade?

---

## 2. Prevenzione dell'overfitting nel backtesting

Luca: *«non ho idea di come evitare l'[[_meta/glossario#Overfitting|overfitting]]»* → da discutere con Salvatore.

Il rischio: ottimizzare una strategia così bene sui dati storici che funziona solo sul passato e fallisce sul futuro. Tecniche da valutare (vedi glossario):
- **[[_meta/glossario#Walk-Forward Backtesting|Walk-forward]]**: addestra su un periodo, testa sul successivo, avanza.
- **In-sample / out-of-sample split**.
- **[[_meta/glossario#CPCV (Combinatorial Purged Cross-Validation)|CPCV]]** (Combinatorial Purged Cross-Validation).
- Regola pratica: meno parametri liberi = meno overfitting.

---

## 3. Test statistici sul benchmark

Luca: *«non ho idea di che benchmark test statistici usare»*.

Come dimostrare che la strategia **batte il benchmark (S&P / 60-40) in modo statisticamente significativo**, non per fortuna? Da valutare: test di permutazione, bootstrap dei rendimenti, p-value sull'alpha. Serve per non auto-illudersi sui risultati del backtest.

---

## 4. Strategia con le opzioni (leva)

> Luca: *«salva tutto in un foglio per Salvatore, se lo sbologna lui o ne parliamo nella prossima call; non è urgente per mettere il tutto in funzione»*. → **fuori MVP**, ma da chiarire prima di abilitare la leva.

> **Perché opzioni e non margine** (chiarimento per Luca, 2026-06-04 — da confermare con Salvatore): rispetto alla leva a margine (debito), le opzioni *long* hanno **perdita massima limitata al premio** e **nessun rischio di margin call / liquidazione forzata** — cruciale per un sistema autonomo 24/7. In cambio si paga il decadimento temporale (theta) e serve azzeccare il timing: per questo la leva è ammessa **solo sui segnali `Strong`**, dove la convinzione giustifica il premio. Vedi anche [[system/modules/agents]] (Gestione Leva con Opzioni). Resta da confermare con Salvatore che questa sia la motivazione e non ce ne siano altre (es. fiscali/operative).

La decisione "leva solo via opzioni Call/Put su segnali `Strong`" è presa, ma mancano i parametri operativi:
- **Strike**: at-the-money? out-of-the-money? Come si sceglie?
- **Scadenza**: in funzione dell'orizzonte del trade (1 mese? 3 mesi?).
- **Quanti contratti**: il sizing delle opzioni è diverso da quello dell'equity spot.
- **Dati**: chi fornisce la catena delle opzioni? (Non è nei data provider attuali — Alpaca paper non copre opzioni reali, IBKR sì.)
- **Implicazione broker**: se vogliamo opzioni in [[_meta/glossario#Paper Trading / Testnet|paper trading]] serve IBKR, non Alpaca. Per l'MVP **niente opzioni** → semplifica.

---

## 5. Su cosa basare i rating degli asset (per il disinvestimento)

Vedi [[system/rating-scoring]] §3. Il dilemma di Luca: serve un punteggio per decidere quale asset vendere, ma *«non so su cosa basarlo e come tenerlo aggiornato»*.

Domanda a Salvatore: nella pratica di gestione, **come si decide quale posizione chiudere** per far spazio a una nuova idea? Quali criteri usa un gestore (forza relativa del segnale, distanza dal target, decadimento della tesi, contributo al rischio)?

---

## 6. Fattori: il "vocabolario" da consegnare all'agente

Salvatore sta preparando (con l'associazione) due documenti che diventeranno *il vocabolario di metriche* dell'agente:
- **Market driver** (4 macro-categorie + driver dal sito Federal Reserve da monitorare) — PPT→PDF→TXT, da arricchire con descrizioni accurate.
- **Indicatori di valuation delle stock** — cosa analizzare in una stock; ognuno dell'associazione ne cura uno.

Principio (Luca): all'agente si dà *«questa metrica ti indica questo»*, **non** *«usa questa metrica per questo»* — è l'agente a imparare come combinarle. Vedi i 5 tipi di P/E (trailing vs current) come esempio già emerso → [[system/modules/quant-backtesting]].

---

## 7. Indicatori di sentiment — da inventare

Il sentiment non ha indicatori standard propri (solo indici di paura). Posizione ibrida col technical. Da definire insieme cosa misurare e come (vedi [[system/modules/quant-backtesting]]).

---

*Quando un tema è risolto, spostarlo nella pagina di destinazione (quant-backtesting, rating-scoring, ecc.) e marcarlo come chiuso qui.*
