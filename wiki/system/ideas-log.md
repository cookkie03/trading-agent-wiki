---
title: "Ideas Log"
type: build
tags:
  - build
  - roadmap
created: 2026-05-21
updated: 2026-06-03
status: active
area: software
---

# Ideas Log

File append-only per le idee emerse durante lo sviluppo del progetto. Non si cancella mai nulla; al massimo si aggiunge una nota di stato o si categorizza.

---

## 2026-06-05 — Sessione design (position sizing)

### Intervento degli agenti sul position sizing (idea da valutare)
Luca tiene **sul piatto** l'idea di permettere agli agenti di **intervenire sul position sizing** calcolato deterministicamente — come *idea da valutare*, non decisione presa: vanno prima indagati rischi e benefici.
- **Benefici potenziali**: l'agente coglie contesto che la formula risk-based non vede (liquidità anomala, event risk, correlazione col portafoglio esistente, sfumature di convinzione oltre l'enum).
- **Rischi potenziali**: rompe il principio deterministico; gli LLM sono deboli sui numeri; rischio di sovraesposizione; più difficile da backtestare/riprodurre.
- **Via di mezzo da indagare**: l'agente non scavalca i cap dello Statuto né calcola la quantità, ma propone un **fattore di aggiustamento limitato** (es. ±X%) che la funzione deterministica **clampa** entro i limiti duri.
→ Dettaglio in [[system/position-sizing]].

---

## 2026-06-04 (sera) — Conversazione Luca↔Salvatore + Claude

*Fonte: audio WhatsApp 2026-06-04 (15 messaggi vocali, 19:59–21:59) + chat export + conversazione Claude in daily-notes.*

### Copy trading come canale di monetizzazione — Darwinex

Modello legale: non gestisci i soldi di nessuno — la piattaforma regolamentata replica le tue operazioni e ti paga una fee. Tu sei un "trader pubblico".

**Darwinex — la scelta principale** (fonte: Claude 2026-06-04):
- Progettata nativamente per **trader algoritmici**: colleghi il bot via Python → MT5 → Darwinex
- Crei un **DARWIN** (prodotto finanziario tuo, verificato da terzi)
- Compenso: **20% performance fee** sui profitti degli investitori (meritocratico — guadagni solo se guadagnano loro)
- Regolatore: FCA (UK)
- Asset: Forex, CFD su azioni, indici, crypto
- Il track record è pubblico e verificabile → valore anche come portfolio professionale

```
Bot Python → MT5 (via lib `MetaTrader5`) → Darwinex account → DARWIN → investitori lo copiano → 20% performance fee
```

**Stack broker definitivo** (Luca 2026-06-04):
- Alpaca: US stocks only, MVP/paper trading
- IBKR: scaling geografico e multi-asset (Darwinex ha integrazione diretta IBKR dal sito)
- Darwinex: layer di monetizzazione copy trading

**Alternative valutate e scartate per il nostro caso**:
- eToro: pensata per trader manuali, API molto limitata/non ufficiale — difficile da agganciare a un bot
- ZuluTrade: principalmente Forex, meno adatto per equity/multi-asset

**Nota Luca** (2026-06-04): *"per ora stai buono, poi in caso lo sentiamo"* — da attivare dopo il paper trading funzionante.

### Collaboratori potenziali identificati (Salvatore, 2026-06-04)

Pipeline di persone da coinvolgere quando il sistema sarà funzionante per review/feedback:

1. **Diego Zappa** (prof. di Statistica) — primo interlocutor ideale: ha fatto trading su mercati come side quest, ha una tesi su trading strategy con Python, è un professore → disponibile, utile, vicino agli studenti.
2. **Dennis Canzi** — incontrato all'esame di Etica, potrebbe facilitare l'introduzione a Zappa.
3. **Trezzi** — "router commerciale": non necessariamente esperto, ma utile per presentarci a persone del settore (es. correlatore di tesi).
4. **Trader della SIM** — traders incontrati da Salvatore in una SIM, sembravano disponibili.

**Principio condiviso** (Luca + Salvatore): il feedback esterno si chiede quando il sistema è **finito** (agenti costruiti, prima della demo live), non durante la build. Salvatore (audio 21:12): *"il parere è da chiedere nel momento in cui hai una cosa finita"*.

### Politica finanziaria — nessun investimento di capitale prima della prova

Posizione esplicita di Luca (audio 21:45, ribadita):
- **NO** investimento di risparmi propri nel progetto prima della prova su demo
- Il progetto nasce per **guadagnare**, non per richiedere capitale
- Percorso: 1) dimostrare che funziona in paper trading → 2) reinvestire i guadagni per migliorare il sistema (es. backtesting, infrastruttura)
- Salvatore (audio 21:48): stessa situazione — 10K per il master, 300€ sul conto corrente, non disponibile a investire

---

## 2026-06-02 — Sessione di review pre-sviluppo (Luca)

*Fonte: chat 2026-06-02 + call 2026-05-29. Idee/spunti emersi mentre Luca rispondeva all'analisi delle lacune.*

### Sistema di rating/scoring a livelli
Valutazioni "a level" con punteggi categorizzati in più punti del sistema: [[_meta/glossario#Conviction Level|conviction]] sul trade, **valutazione del lavoro di ogni agente** (capire cosa migliorare e come), rating degli asset per il disinvestimento. → formalizzata in [[system/rating-scoring]].

### Scheda ticker auto-aggiornante
Un DB dove ogni ticker ha la sua scheda/page con valutazione corrente, che si auto-aggiorna; gli agenti devono distinguere e cancellare le info vecchie/obsolete/confutate. Difficile ma potente. → [[system/parallelism-design]] (alternativa B).

### Layer di "valutatori" per ticker
Layer intermedio tra PM e desk: un valutatore per ticker, ognuno in un thread separato, chiama i desk analisti. Parallelismo + isolamento. → [[system/parallelism-design]] (alternativa A).

### "News anomale" come miccia dell'origination
L'origination di un'idea parte da una miccia: news anomale / cose strane che arrivano dal blocco `market` (viola) verso il centro del grafo. Possibile terzo tipo di alert che attiva il PM (oltre a prezzo-target e periodical synthesis): *"l'idea è valida, facciamola"*.

### "TV/dashboard del DB" (TG24)
Una vista in stile canale di news che mostra lo stato del DB (portafoglio, mercati): nel DB c'è tutto, la dashboard lo espone. Collegata alla periodical synthesis verso il PM e alla dashboard SFC.

### Auto-finanziamento crediti OpenRouter
Prelevare parte dei profitti per ricaricare automaticamente i crediti API (i costi token sono equiparati a commissioni). Prospettiva avanzata.

### Cash-out mensile
Ogni mese trasformare il *tot %* del guadagno del mese (dall'ultimo cash-out) in bonifico verso IBAN/conto deposito. Da formalizzare nello Statuto a progetto finito.

### Feedback post-trade per meccanismo di uscita
Un sistema che fa notare agli agenti **come sono andati i trade precedenti a seconda del meccanismo di disinvestimento** adottato (TP / SL / [[_meta/glossario#Trailing Stop Loss|trailing stop]] / rating-based). Prerequisito: campo `exit_reason` su ogni transazione. La sintesi rientra nel `past_context` degli agenti. → formalizzato in [[system/rating-scoring]] §4.

### Loop di valutazione e auto-miglioramento (unificazione 2026-06-03)
Quattro idee emerse in momenti diversi sono lo stesso macro-blocco e sono state unificate in [[system/learning-feedback-loop]]: **reportistica "cosa va male"** (modulo Python deterministico + narrazione LLM — opzione scelta per ora, non un agente dedicato), **scoring del lavoro degli agenti**, **ponderazione dinamica dei pesi** (l'agente che ci azzecca pesa di più; punto di aggancio aperto, in tensione con "conviction dal PM"), **feedback post-trade per meccanismo di uscita**. Substrato di logging (chain-of-thought + tesi-per-agente↔esito + `exit_reason`) da predisporre **da subito**; report e pesi restano post-MVP.

### ⏸️ Parcheggiato — aspetti legali (B8)
Gestione capitali di terzi (modello "Piero") e privacy dei dati passati agli LLM: **tenuti nel cassetto** per scelta di Luca (2026-06-02), da riprendere *se e quando* il progetto funziona. In Italia gestire denaro di terzi può configurare abusivismo finanziario (art. 166 TUF) → consulenza legale **prima** del live, non blocca lo sviluppo software.

---

## 2026-05-22 — Idee architetturali e organizzative

*Fonte: `raw/daily-notes/2026-05-22.md`*

### Multi-Agent Communication Layer

**Idea chiave**: un team di agenti in grafi che si mantengono costantemente aggiornati e dialogano tra loro su richiesta. Esempio concreto: Trader Agent ha bisogno di conoscere la situazione macroeconomica → usa un tool che richiama il MacroEconomist Agent, costruendo un prompt di richiesta ad hoc → il MacroEconomist risponde con un report cucito sulle esigenze della richiesta, non generico.

### Gestione del costo computazionale LLM

Due strategie complementari per agenti con recall frequente:
- **Sintesi con modelli locali**: per agenti che vengono richiamati costantemente, produrre sintesi compresse con modelli locali prima di passarle agli agenti principali
- **Autocompattazione del contesto**: per agenti che lavorano in modo continuo, necessario un meccanismo di autocompattazione del contesto per non esaurire la finestra

### Materiale da caricare nel wiki

- Documenti dalla triennale di Luca e Salvatore
- Materiale dell'associazione di Luca e Salvatore
- Obiettivo: estrarre tutte le informazioni utili a valutare ogni aspetto del progetto, a partire dalla strategia da implementare

### Merge 3 progetti simili

Caricare nella cartella di lavoro altri due progetti simili a trading-agent, eseguire un'analisi con graphify o strumento simile per:
1. Identificare conflitti tra i tre progetti
2. Produrre una versione unificata (merge) delle idee
3. Usarla come base di lavoro per le decisioni progettuali

---

## 2026-05-25 — LangSmith e tooling di sviluppo

*Fonte: `raw/daily-notes/2026-05-25.md`*

### LangSmith per debug e evaluation

- **LangSmith**: piattaforma di debug degli agenti LangChain/LangGraph — già integrata nell'ecosistema, da usare durante lo sviluppo
- **Funzione Mermaid**: LangGraph supporta la generazione di diagrammi Mermaid dei grafi; usare questa funzione per far verificare al coding agent (Claude Code) se la struttura dei grafi corrisponde al design inteso
- **LangSmith CLI**: strumento per l'evaluation automatica degli agenti direttamente nel terminale (VS Code) — da integrare nel workflow di sviluppo per valutazione continua senza uscire dall'IDE

---

## 2026-05-22 — Rischio sistemico dell'AI trading (Salvatore)

*Fonte: call 2026-05-22 (audio 00000726)*

**Osservazione di Salvatore**: se tutti usano lo stesso sistema AI per le analisi finanziarie, ottengono tutti lo stesso output → price discovery eliminata, mercato privo di senso.

Rischi identificati:
- **Gigabolla**: sentiment uniforme → tutti si muovono nella stessa direzione
- **Vulnerabilità a manipolazione**: informazioni false su internet → bias dell'AI → bolle artificiali targettizzate
- **Implicazione progettuale**: il nostro sistema deve essere differenziante per definizione — più data-driven (dati fondamentali oggettivi) e meno dipendente dal sentiment pubblico (Reddit, social media)

Questa osservazione rafforza la decisione di costruire un sistema orientato all'analisi fondamentale e quantitativa, non al sentiment aggregato.

---

## 2026-05-26 — Calendario economico e struttura report

*Fonte: call 2026-05-26 (feedback Salvatore)*

### Calendario economico come dato di sistema

Il sistema dovrebbe raccogliere e mantenere aggiornato un **calendario economico** contenente:
- Date delle trimestrali delle aziende in portafoglio
- Accordi internazionali rilevanti
- Date di pubblicazione dati macro (PIL, inflazione, tassi, ecc.)

Questo calendario è input rilevante per gli agenti che devono contestualizzare movimenti di prezzo.

---

## 2026-05-21 — Da lettura TradingAgents Code Wiki

*Fonte: `raw/archived/daily-notes/2026-05-19.md` + [[prior-art/tradingagents/code-wiki]]*

### Architettura e Agenti

- **Agente Indicatori DB**: un piccolo agente che periodicamente valuta quali nuovi indicatori o valori aggiungere al DB, con permesso di creare nuovi tipi di oggetti/dati nel DB e ogni altro permesso necessario
- **Agente Market Conditions**: un agente che tiene traccia delle condizioni di mercato su orizzonti più lunghi (es. regime macro, trend di mercato)
- **Agente Single Ticker**: un agente che analizza la situazione di un singolo ticker — complementare all'agente market conditions
- **Agente PDF/Bilanci**: un agente che trasforma PDF (bilanci, report periodici aziendali) in file MD, li gestisce per renderli pronti a qualsiasi richiesta da altri agenti, e popola il DB con le metriche di bilancio (revenues, EBIT, ecc.)

### Self-Scheduling Workflows

Idea: eliminare i [[_meta/glossario#Cron Job|cron job]] fissi. Gli LLM includono nei loro output strutturati **il momento in cui ritengono opportuno eseguire nuove analisi**, usando tool appositi che risvegliano altri agenti quando serve. Esempio: un agente apre una posizione che ritiene debba restare tale per X giorni → nell'output inserisce di essere richiamato tra X giorni per il controllo.

Alternativa ancora aperta: analisi periodica a intervalli prestabiliti (es. ogni 4h) per decidere se aprire/chiudere/hold.

### Data Layer

- **DB-first per tutti i dati**: al posto di chiamare vendor on-demand, ogni dato viene salvato subito nel DB centrale; i tool si agganciano al DB (non ai vendor). Da valutare: gestione informazioni molto recenti non ancora nel DB
- **Workflow deterministici per il fetching**: per ogni provider, sfruttare al massimo i rate limit dei piani gratuiti e caricare dati aggiornati nel DB
- **Gestione [[_meta/glossario#Look-Ahead Bias|look-ahead bias]]**: salvare due date per ogni informazione — (1) data di ottenimento/pubblicazione, (2) data a cui l'informazione si riferisce (es. ultimo giorno del trimestre per i bilanci)
- **Indicatori calcolati automaticamente**: ogni indicatore calcolabile va calcolato dal DB con formule che richiamano i dati grezzi già presenti — no calcolo on-the-fly
- **Deduplicazione deterministica**: per dati provenienti da più vendor, workflow deterministici per gestire i duplicati
- **Standardizzazione formati**: ogni modulo estrae e standardizza in formati comuni all'intero sistema (es. exchange intercambiabile tra demo e reale)

### News e Knowledge Management

- **RAG per le news**: quando un agente vuole informazioni dettagliate, aggiornate e complete deve poterlo fare in modo efficiente e rapido — possibilmente single shot. RAG preferito su AGENT WIKI per le news
- **RAG o tagging multiplo per i social media sentiment**: categorizzazione con tag (ticker, horizon, data/ora, ecc.)

### UI e Monitoring

- **Webapp locale dashboard**: interfaccia locale che espone tutti i parametri e tutte le informazioni disponibili del sistema (equity curve, posizioni aperte, metriche, log, ecc.)
- **Raccolta performance per revisione umana**: raccogliere quali moduli, indicatori e metodi stanno performando meglio — per revisione umana e miglioramento continuo della teoria economica

### Visualizzazione Codebase

- **Schema grafico interattivo di TradingAgents**: un codice HTML/JavaScript che visualizza graficamente lo schema a nodi e grafi del codebase TauricResearch, con tutti gli agenti, nodi, tool, state, variabili, report passati/modificati/creati/usati

### Architettura Intra-Modulo

- **Pattern: un file per subdirectory come gateway**: ogni subdirectory del progetto è un modulo; ogni file interno si interfaccia con un unico file posto all'inizio della subdirectory, che gestisce e instrada input/output intra-modulo e inter-modulo

### Domande per Salvatore

- "Quali sono gli indicatori di performance che possiamo utilizzare per valutare i nostri trade? Li voglio tutti."
- "Quali gli indicatori che possiamo usare come analisi 'tecnica'? Li voglio tutti."
- Brainstorming: come si lavora dentro gli uffici di un investitore istituzionale che investe in questo stile — per replicarne i workflow e gli agenti come se fossero dipendenti dell'ufficio

### Mercati Internazionali

- Nel caso di operazioni anche su mercati extra-americani: capire come gestire la liquidità (opportunità di guadagno + rischio liquidazione in valuta estera)
