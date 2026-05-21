---
title: "Ideas Log"
type: build
tags:
  - build
  - roadmap
created: 2026-05-21
updated: 2026-05-21
status: active
area: software
---

# Ideas Log

File append-only per le idee emerse durante lo sviluppo del progetto. Non si cancella mai nulla; al massimo si aggiunge una nota di stato o si categorizza.

---

## 2026-05-21 — Da lettura TradingAgents Code Wiki

*Fonte: [[raw/daily-notes/2026-05-19]] + [[references/tradingagents-code-wiki]]*

### Architettura e Agenti

- **Agente Indicatori DB**: un piccolo agente che periodicamente valuta quali nuovi indicatori o valori aggiungere al DB, con permesso di creare nuovi tipi di oggetti/dati nel DB e ogni altro permesso necessario
- **Agente Market Conditions**: un agente che tiene traccia delle condizioni di mercato su orizzonti più lunghi (es. regime macro, trend di mercato)
- **Agente Single Ticker**: un agente che analizza la situazione di un singolo ticker — complementare all'agente market conditions
- **Agente PDF/Bilanci**: un agente che trasforma PDF (bilanci, report periodici aziendali) in file MD, li gestisce per renderli pronti a qualsiasi richiesta da altri agenti, e popola il DB con le metriche di bilancio (revenues, EBIT, ecc.)

### Self-Scheduling Workflows

Idea: eliminare i cron job fissi. Gli LLM includono nei loro output strutturati **il momento in cui ritengono opportuno eseguire nuove analisi**, usando tool appositi che risvegliano altri agenti quando serve. Esempio: un agente apre una posizione che ritiene debba restare tale per X giorni → nell'output inserisce di essere richiamato tra X giorni per il controllo.

Alternativa ancora aperta: analisi periodica a intervalli prestabiliti (es. ogni 4h) per decidere se aprire/chiudere/hold.

### Data Layer

- **DB-first per tutti i dati**: al posto di chiamare vendor on-demand, ogni dato viene salvato subito nel DB centrale; i tool si agganciano al DB (non ai vendor). Da valutare: gestione informazioni molto recenti non ancora nel DB
- **Workflow deterministici per il fetching**: per ogni provider, sfruttare al massimo i rate limit dei piani gratuiti e caricare dati aggiornati nel DB
- **Gestione look-ahead bias**: salvare due date per ogni informazione — (1) data di ottenimento/pubblicazione, (2) data a cui l'informazione si riferisce (es. ultimo giorno del trimestre per i bilanci)
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
