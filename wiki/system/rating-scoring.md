---
title: "Sistema di Rating & Scoring"
type: build
tags:
  - build
  - architecture
  - multi-agent
created: 2026-06-03
updated: 2026-06-03
status: draft
priority: medium
area: software
related:
  - "[[system/state-schemas]]"
  - "[[system/position-sizing]]"
  - "[[system/modules/agents]]"
  - "[[system/modules/execution]]"
  - "[[system/learning-feedback-loop]]"
confidence: low
---

# Sistema di Rating & Scoring

> Idea emersa nella call 2026-06-02: usare **valutazioni a livelli/punteggi categorizzati** in più punti del sistema. Luca: *«ha senso avere questo sistema di valutazioni a level, anche per la valutazione del lavoro di ogni agent, con punteggi categorizzati che aiutano a capire cosa migliorare e come»*. Questa pagina unifica tre meccanismi di scoring che sono in realtà la stessa idea applicata a oggetti diversi.

---

## 1. Conviction level (sul singolo trade)

Quanto il sistema è convinto di un'idea di investimento. Vive nel `research_state` ([[system/state-schemas]]).

- **Chi lo assegna**: probabilmente il **Portfolio Manager**, date le informazioni degli analisti (Luca: *«probabilmente lo dovrebbe dare il portfolio manager date le info degli analisti»*). Da confermare in fase di mappatura del grafo.
- **Forma**: enum (`Strong Buy` / `Buy` / `Hold` / `Sell` / `Strong Sell`) — eventualmente affiancato da uno **score numerico 0-100** per granularità.
- **Usi**:
  - sblocca la **leva via opzioni** solo sui segnali `Strong` (vedi [[system/modules/agents]]);
  - scala il **position sizing** ([[system/position-sizing]]);
  - stima `p` per un eventuale Kelly frazionario.

---

## 2. Scoring del lavoro degli agenti (meta-valutazione)

Punteggio sulla **qualità del lavoro di ciascun agente/modulo**, per capire cosa funziona e cosa migliorare.

- **Obiettivo**: categorie di punteggio che evidenzino *dove* il sistema sbaglia (quale desk, quale fattore, quale fase). Base per il futuro **RL / Weighting Module** (ponderazione dinamica dei moduli) e per il fine-tuning. È un pezzo del più ampio [[system/learning-feedback-loop]] (§3-§4 lì): lo scoring è insieme *output* della reportistica diagnostica e *input* della ponderazione dei pesi.
- **Su cosa basarlo (proposta)**: confrontare a posteriori la tesi di ogni agente con l'esito reale del trade — l'agente che aveva ragione vede salire il suo score, chi sbaglia sistematicamente lo vede scendere. Richiede il **logging strutturato della chain-of-thought** (già in board) e lo storico esiti.
- **Stato**: richiede storico → realisticamente **post-MVP**, ma lo schema dei log va predisposto da subito perché i dati siano raccolti fin dall'alpha.

---

## 3. Rating degli asset (per il disinvestimento)

Punteggio aggiornato per ogni ticker, usato per decidere **cosa vendere** quando serve liberare liquidità o ribilanciare. È il nodo del problema "selezione asset da disinvestire" (vedi [[system/modules/execution]] e analisi in questa stessa cartella).

- **Idea di Luca**: ogni `next_check_date` (o al bisogno) si rivaluta l'insieme investito e si confrontano le posizioni con dei **rating/score**. Dilemma aperto: *«non so bene su cosa basarli e come tenerli sempre aggiornati»*.
- **Proposte di base per il rating** (da discutere con Salvatore → [[strategy/questions-for-salvatore]]):
  - **forza relativa del segnale corrente** vs quando si è entrati (il segnale è ancora valido?);
  - **distanza dal target / stop**: una posizione vicina al TP o che ha rotto la tesi è candidata all'uscita;
  - **decadimento temporale**: una tesi vecchia non rivalidata pesa meno;
  - **contributo al rischio di portafoglio** (una posizione che gonfia il VaR o concentra un settore è candidata).
- **Come tenerlo aggiornato**: o ricalcolo periodico (mantainer/quant), o "scheda ticker auto-aggiornante" (vedi alternativa in [[system/parallelism-design]]).

### Due livelli di disinvestimento (chiarimento 2026-06-03)
Il disinvestimento non è solo una decisione "ragionata": gran parte avviene **automaticamente**. Distinguere:
1. **Disinvestimento automatico (deterministico)**: scatta da meccanismi già armati sull'ordine — **Take Profit**, **Stop Loss**, **trailing stop loss** e simili. Non richiede valutazione dell'agente: è la funzione Trade/Exchange che li gestisce ([[system/modules/execution]]).
2. **Disinvestimento valutato (rating-based)**: la valutazione **periodica** (ogni `next_check_date` o al bisogno) di cosa conviene chiudere per far spazio a nuove idee, usando i rating sopra. Luca: *«valutare periodicamente cosa poter disinvestire, considerando che ci saranno Take Profit, trailing stop loss e altri meccanismi di disinvestimento automatico»*.

I due livelli convivono: l'automatico protegge in tempo reale, il valutato ottimizza l'allocazione nel medio termine.

---

## 4. Feedback post-trade per meccanismo di uscita (idea 2026-06-03)

> Luca: *«bisognerà inserire un sistema che permette di far notare agli agent come sono andati i trade precedenti a seconda di quali meccanismi di disinvestimento sono stati adottati»*.

Anello di apprendimento: il sistema deve **misurare l'esito dei trade segmentato per tipo di uscita** e **restituirlo agli agenti** perché ne tengano conto. È un caso particolare della reportistica diagnostica del [[system/learning-feedback-loop]] (§2 e §5 lì).

- **Prerequisito (logging)**: ogni transazione registra un campo **`exit_reason`** — `take_profit` / `stop_loss` / `trailing_stop` / `rating_based` (disinvestimento valutato) / `manual_override` / `option_expiry`. Vive in `transactions` → [[system/modules/data-layer]] e [[system/modules/execution]].
- **Analisi**: aggregare P&L, win rate, holding period per `exit_reason` (es. *"i trailing stop ci hanno fatto uscire troppo presto sui trend forti"* / *"gli stop loss hard hanno salvato il -30% in N casi"*).
- **Ritorno agli agenti**: questa sintesi entra nel **`past_context`** dello state ([[system/state-schemas]]) — le "lezioni apprese" che gli analisti e il PM ricevono in input quando rivalutano un ticker. Chiude il loop con lo **scoring del lavoro degli agenti** (§2): un agente che apre tesi chiuse sistematicamente in stop loss perde score.
- **Stato**: richiede storico → il *valore* arriva col tempo, ma il campo `exit_reason` e il logging vanno predisposti **da subito** perché i dati si accumulino dall'alpha.

---

## Filo conduttore

Tutti e tre sono **score categorizzati** che rendono il sistema *interpretabile e migliorabile*: invece di una black-box, ogni decisione porta con sé un punteggio motivato. È un principio di design, non un modulo unico — si implementa pezzo per pezzo.

---

*Tracciato come tema da discutere con Salvatore in [[artifacts/project-board]] e [[strategy/questions-for-salvatore]].*
