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
  - "[[decisions/decision-log]]"
  - "[[ops/wiki-restructuring-plan]]"
  - "[[theory/modular-trading-agent-architecture]]"
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

## Decisioni e insight operativi

| Tema | Contenuto |
|------|-----------|
| Value investing scalabilità | Non scalabile per ora: ogni azione richiede analisi diversa, costoso in token e tempo |
| FX effect | Critico: sempre verificare l'effetto valutario su ricavi con forte esposizione internazionale |
| Tool design | Parametrizzabili (no hardcoded), modulari, componibili in aggregazioni ("tavoli") |
| Ruolo Salvatore | Market research, raccolta info, caricamento Raw/; NON creazione pagine wiki |
| Wiki ristrutturazione | Pianificata con Claude, poi spiegata a Salvatore. Vedere [[ops/wiki-restructuring-plan]] |
