---
title: "Videochiamata Luca-Salvatore — 2026-05-13"
type: source
tags:
  - strategy
  - architecture
  - market-structure
  - infrastructure
raw_source_path: "raw/audio/2026-05-13 13-14-17.m4a"
created: 2026-05-13
updated: 2026-05-13
status: active
confidence: high
related:
  - "[[build/mvp-prototype-design]]"
  - "[[build/decision-log]]"
  - "[[build/system-map]]"
---

# Videochiamata Luca-Salvatore — 2026-05-13

Chiamata di aggiornamento tra Luca e Salvatore. Argomenti principali: strategia Trend Following (Moncler come caso d'uso), metodologia di analisi value investing, walk-through dell'architettura e dei canvas creati, struttura proposta per la sezione quant della wiki, workflow di Salvatore in Obsidian, piano di ristrutturazione wiki.

---

## 1. Strategia Trend Following — proposta di Salvatore

**Idea**: seguire i market maker istituzionali, non batterli. Gli istituzionali possono muovere i mercati con milioni di euro in un secondo — non si può competere. Si può però accodarsi ai loro movimenti.

**Meccanismo**:
- Usare gli stessi indicatori che usano loro
- Entrare in ritardo (a metà o nell'ultimo quarto del movimento), guadagnando meno ma con rischio ridotto
- Esempio su Moncler: se entrano in cima e noi entriamo a metà punta, guadagniamo la metà ma è sempre positivo (specialmente in leva)

**Obiettivo primario**: identificare dove sono andati gli istituzionali usando i loro stessi indicatori tecnici, poi accodarsi. Il problema è che nessuno sa cosa fanno, quindi si tratta di reverse-engineering tramite analisi.

---

## 2. Analisi Value Investing — metodologia di Salvatore

Salvatore ha mostrato in call la sua analisi su Moncler (e stava per fare Ferrari). Elementi chiave della sua metodologia:

### Cosa guarda
- **P/E ratio**: quante volte si paga l'earnings della società. Confrontato con P/E settoriale. Soglia minima ~10x, ma varia per settore (Nvidia può essere 50-100x)
- **Revenue trend**: quartale su quartale, anno su anno. Cercare la stabilità post-eventi (es. post-covid Moncler: 3 billion stabili)
- **Effetto valutario** (FX): punto critico. Moncler fa il 50% dei ricavi in Asia → in yen. Se yen è sfavorevole vs euro, il +12% dichiarato nella trimestrale è falso. Bisogna sempre controllare il FX effect
- **Trimestrali**: leggere le relazioni (non solo i numeri), cercare le voci in piccolo. Esempio: "FX cost" o "considerando l'effetto valuta" spesso scritto in piccolo nella relazione

### Processo di stress test
Salvatore non prende i dati per vero — li testa e si fa un'opinione. Esempio:
> "Il 12% di crescita è falso, perché 50% dei ricavi è in yen e lo yen è sfavorevole. Loro lo scrivono FX cost in piccolo."

L'AI di default prenderebbe quel 12% per vero. Per non farlo sbagliare, bisogna o: (a) dargli il contesto giusto nel prompt, oppure (b) costruire tool che calcolano l'effetto FX automaticamente.

### Problema di scalabilità
- Fare value investing su molte azioni è costoso in tempo e token
- Ogni azione richiede analisi diverse (Ferrari ≠ Moncler — non si guardano le stesse cose)
- Conclusione: **value investing non è scalabile per ora** come strategia primaria del sistema

---

## 3. Walk-through architettura con Salvatore

Luca ha mostrato a Salvatore i canvas creati (Dev Roadmap, System Cycle) e spiegato i moduli:

### Moduli confermati
- **Modulo A**: Exchange + DB (Luca, autonomo, inizia subito)
  - Connessione Binance Testnet
  - Paper trading environment
  - DB centrale come "hard disk" del sistema

- **Modulo C**: Quant Agent + Backtesting (Luca + Salvatore in sessioni)
  - VectorBT come framework (Luca lo studia)
  - Strategia quantitativa da definire con Salvatore

- **Modulo D**: Prompt Builder + LLM Trader
  - Output: invece di ordini diretti → target price, SL, TP per asset
  - Confronto deterministico con posizione attuale → decisione se eseguire

### Rebalancing Gate — confermato da Salvatore
Il principio deterministico del Rebalancing Gate: l'AI produce i target, Python deterministicamente confronta con la posizione attuale. Si esegue solo se la differenza supera una soglia (es. 5%). La soglia è parametrizzabile.

### Architettura layer (spiegazione di Salvatore)
```
Layer 1: Estrazione dati (provider 1..N → DB centrale)
Layer 2: Analisi dati (tool parametrizzabili: medie mobili, ratio, regressioni...)
Layer 3: Agenti AI (Analyst → Trader Quant → ordini)
```

**DB come hard disk**: tutti i moduli scrivono qui; tutti i moduli leggono da qui. Unica fonte di verità.

**Tool parametrizzabili**: i tool non devono avere valori hardcodati. Es: non "calcola media mobile a 50" ma "calcola media mobile con period=N". L'AI può così sperimentare diversi parametri.

**Tool complessi = "tavoli"**: tool aggregati da blocchi più semplici. Es: DCF non è un blocco ma un tavolo di sotto-tool (calcola free cash flow, calcola WACC, ecc.) che lavorano in autonomia e il tavolo coordina.

---

## 4. Quant Strategy — struttura proposta per la wiki

Salvatore propone di raccogliere nella wiki tutte le possibili strategie quantitative in modo esaustivo:
- Value, Factor, Momentum, Trend Following
- Strategie da research paper open source
- Metodi statistici: regressioni, OLS, ML, deep learning

### Struttura wiki proposta (da Salvatore)
```
wiki/
└── strategie (o moduli)/
    └── quant/
        ├── strategie/         ← elenco strategie perseguibili
        ├── parametri/         ← ogni parametro ha il suo file
        ├── metodi/            ← ogni metodo ha il suo file (regressione, ecc.)
        │   └── regressione.md ← inputs (linked), outputs (linked a validazione)
        └── validazione/       ← ogni metrica di valutazione ha il suo file
            └── mean-square-error.md
```

**Principio di linking**: ogni file metodo deve linkare i file input (parametri) e i file output (metriche). Quando l'AI fa una query, apre tutti i link e legge tutto il contesto. Brainstorming diventa facile.

**Obiettivo**: avere un prospetto completo, esaustivo, ben strutturato di tutte le strategie possibili con esempi concreti per ogni categoria.

---

## 5. Piano di ristrutturazione wiki

Luca ha mostrato a Salvatore la wiki su Obsidian. Conclusione immediata:

> "Tutta questa parte di Wiki di cartelle delle wiki va ristrutturata da zero. In cui mettiamo tipo la cartella per le strategie, la cartella per i moduli — bisogna rifare tutta la suddivisione."

**Stato**: pianificata, non ancora eseguita. Luca la farà con Claude in una sessione dedicata e poi spiegherà a Salvatore il risultato.

Vedere [[ops/wiki-restructuring-plan]] per il piano dettagliato.

---

## 6. Workflow di Salvatore in Obsidian

Luca ha spiegato a Salvatore come usare il vault:

### Regola principale
- **NON creare file wiki** direttamente. L'agente sa dove mettere le cose grazie all'index
- **Caricare tutto in Raw/** — anche cose che non sembrano valide (con nota "penso non sia valida perché...")
- L'agente poi mette tutto in ordine

### Daily Notes
- Per appunti volanti, usare le Daily Notes (pulsante calendario su Obsidian)
- Si crea un foglio con la data odierna
- Template: sezione "DA LUCA" e "DA SALVO" per distinguere le note
- Può mettere anche domande per wiki-query qui

### Voice dictation
- Sul PC c'è la digitazione vocale (Luca l'ha mostrata)
- Utile per note veloci senza scrivere

### Codex (Claude Code) — free tier
- Salvatore può usare Codex per fare wiki-query da solo
- Free tier: limiti settimanali bassi, ma sufficiente per singole query
- Le skill wiki-* (wiki-query, wiki-ingest) sono disponibili localmente nella cartella `.claude/`

---

## 7. Fine-tuning e RL — spiegazione di Salvatore a Luca

Salvatore ha spiegato concetti avanzati post-MVP in modo chiaro:

**Fine-tuning**: quando hai anni di storico trading (es. 10 anni × 365 giorni × N analisi al giorno = ~10.000 analisi), puoi ritarare i pesi di un modello open source (es. DeepSeek, Qwen) per specializzarlo sui tuoi dati storici. È diverso dal training standard: non dai conoscenza, ma adatti i pesi al tuo dominio specifico.

**Reinforcement Learning**: simile al backtesting ma per gli agenti AI. L'agente testa 1000 volte l'ambiente finché non ottiene il comportamento giusto. Estremamente costoso in termini di compute (è quello che fanno Anthropic/OpenAI/Google). Post-MVP avanzato.

---

## 8. Struttura multi-agente — descrizione verbale di Salvatore

Salvatore ha descritto verbalmente la sua visione di un trading floor come gerarchia di agenti AI, partendo dal paragone con un vero trading room istituzionale.

### Layer del trading floor (visione Salvatore)

**Layer inferiore — Il Tavolo (tre agenti che comunicano tra loro):**
- **News Research Agent**: analizza tutte le news, elabora sentiment, individua opportunità macro. Comunica bilateralmente con l'Analista.
- **Analista Finanziario**: analizza lo strumento specifico individuato dal News Research — P/E, volumi, prezzi, spread del broker, analisi tecnica. Comunica bilateralmente con il News Research Agent e con il Quant.
- **Quant/Conto**: fa analisi previsionale matematica (es. Monte Carlo, processi stocastici). Fornisce previsioni del prezzo futuro. Comunica bilateralmente con gli altri due al tavolo.

I tre comunicano tra loro (frecce bidirezionali) e producono un output congiunto.

**Layer intermedio — Risk Analyst:**
- Riceve l'output del Tavolo
- Analizza il rischio: VaR, expected shortfall, esposizione massima, range SL/TP
- Risponde con approvazione + paletti, oppure rimanda al tavolo con motivazione
- Il Risk Analyst deve essere **molto critico** — "meglio non guadagnare che perdere"
- Fornisce i paletti (stop loss, take profit, max size) al Trader

**Layer superiore — Trader Agent:**
- Riceve il referto approvato del Risk Analyst con tutti i paletti
- Ha un unico compito: **eseguire al miglior prezzo possibile**
- Trova il broker con spread minore e maggiore liquidità per lo strumento
- Non decide la strategia, la esegue deterministicamente nelle condizioni di mercato

**Analogia con trading floor reale:**
- Equity Research → News Research Agent + Analista
- Quant → Conto
- Risk Management → Risk Analyst Agent
- Trader → Trader Agent (che nei fondi reali "chiama i broker, tratta, ottiene il prezzo migliore")

### Metriche di portafoglio — riferimento StreamLit

Salvatore ha mostrato la dashboard StreamLit di Starting Finance (STFC Investment Fund) come riferimento per le metriche di portafoglio. Include tutte le metriche chiave: Sharpe, drawdown, rendimento, analytics avanzate. Può essere presa come ispirazione per la dashboard del nostro sistema.

---

## 9. Order Book e provider — considerazioni operative

### Order Book su Crypto (pubblico)

- Sulle cripto, essendo tutto digitale, l'order book è pubblico
- Si possono aggregare le API di Binance, Coinbase, Kraken per avere l'order book completo di tutti i provider
- Whale Alert: servizio che aggrega gli ordini istituzionali pubblici su crypto → può essere usato come segnale

### Limitazione sulle azioni

- Su azioni tradizionali, il volume aggregato non indica acquisti vs vendite
- I fondi istituzionali devono pubblicare per legge le posizioni (ma in ritardo, settimanalmente)
- "Nancy Pelosi following" / insider tracking: teoricamente fattibile ma con delay

### Provider aggregatori (database aziendali)

- AIDA, Orbis: database aziendali (non discussi in dettaglio)
- AlfaSpread: calcola DCF automaticamente, ma API probabilmente a pagamento o con limiti
- Conclusione: i tool deterministici Python (scritti da noi) che si agganciano alle API sono più efficienti di delegare la ricerca a Claude/ChatGPT

---

## 10. Fork vs From Scratch — stato del dibattito in questa call

Luca ha mostrato a Salvatore il progetto TradingAgents (Cornell, ~50k stelle, Claude 4° contributore). Discussione:

- **Argomento per il fork**: infrastruttura già pronta, 10.000 fork esistenti, open source usabile immediatamente
- **Argomento contro**: partire da un fork significa studiare il codice altrui fino a capirlo come se l'avessi scritto tu, oppure non sapere cosa cambiare quando qualcosa va storto. "A quel punto crealo da zero."
- **Decisione**: non chiusa in questa call. Dipende da ulteriore studio e da quanto il progetto TradingAgents è modificabile efficacemente.

Luca propende per il fork (lo ha detto nel daily note 2026-05-19 dopo aver letto il Code Wiki). Da formalizzare con Salvatore.

---

## 11. Sequenza operativa proposta da Luca (fine call)

1. Decidere gli artifact da creare (mappe mentali, kanban necessari)
2. Fase raccolta informazioni su tutti i progetti open source simili
3. Da quella raccolta → decisioni: fork vs from scratch, architettura, input/output per modulo
4. Progettazione granulare: per ogni modulo, definire input/output precisi
5. Solo dopo → sviluppo con agente coding

**Principio guida**: il codice lo crea l'agente AI, l'importante è sapere al 200% cosa vuoi e come lo vuoi. La qualità del progetto dipende dalla qualità della progettazione.

---

## Decisioni e insight operativi

| Tema | Contenuto |
|------|-----------|
| Value investing scalabilità | Non scalabile per ora: ogni azione richiede analisi diversa, costoso in token e tempo |
| FX effect | Critico: sempre verificare l'effetto valutario su ricavi con forte esposizione internazionale |
| Tool design | Parametrizzabili (no hardcoded), modulari, componibili in aggregazioni ("tavoli") |
| Ruolo Salvatore | Market research, raccolta info, caricamento Raw/; NON creazione pagine wiki |
| Wiki ristrutturazione | Pianificata con Claude, poi spiegata a Salvatore. Vedere [[ops/wiki-restructuring-plan]] |
| Order book crypto | Pubblico su Binance/Coinbase/Kraken — aggregabile via API |
| Struttura agenti | Trading floor: Tavolo (News+Analista+Quant) → Risk Analyst → Trader |
| Fork vs from scratch | Dibattito aperto. Luca propende per fork, da formalizzare |
| Dashboard metriche | StreamLit STFC come riferimento per metriche di portafoglio |
