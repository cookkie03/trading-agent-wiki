---
title: "Factor Investing"
type: synthesis
tags:
  - strategy
  - market-structure
created: 2026-05-14
updated: 2026-05-14
status: draft
confidence: medium
area: strategy
related:
  - "[[system/modules/quant-backtesting]]"
---
# Factor Investing

> Nota di ingest 2026-06-23: Luca ha segnalato `raw/articles/CorpBondThesis.pdf` come materiale guida per chiarire cosa intende per factor investing, quali fattori esistono e come potrebbe innestare modelli ML/DeepLearning. Il PDF resta ancora pending ingest completo, ma da ora è riferimento esplicito di questa pagina.

**Idea di base**: costruire un modello che quantifica l'impatto di "fattori" (eventi, dati fondamentali, variabili macro) sul prezzo di un asset. Ogni fattore ha un coefficiente empirico calcolato su serie storiche.

---

## Come funziona

Per ogni fattore rilevante (es. "dimissioni del CEO", "risultato trimestrale sopra le stime", "rialzo tassi Fed"):
1. Si raccolgono gli ultimi N casi storici in cui il fattore si è verificato
2. Si calcola l'impatto medio sul prezzo nei giorni successivi
3. Il coefficiente risultante viene usato dal sistema per pesare quel segnale

> Questo approccio è diverso dalla regressione classica: non si stimano i coefficienti con OLS, si calcolano come media empirica su serie storiche.

---

## Categorie di fattori (orientamento)

| Categoria | Esempi |
|-----------|--------|
| Macro | Tassi Fed/BCE, PIL, inflazione, politiche monetarie |
| Aziendali | Revenue trimestrale, EPS, guidance, dimissioni CEO |
| Ratio | P/E, P/Sales, Debt/Equity, confronto settoriale |
| Tecnici | Volume spike, rottura supporti/resistenze |
| Sentiment | Fear & Greed Index, rating analisti, whale alerts |

---

## Perché non è la strategia primaria ora

Value investing classico **non è scalabile** come approccio primario del sistema per due motivi:

1. **Ogni asset richiede analisi diversa**: quello che si guarda su Moncler (FX exposure asiatica) non è uguale a quello che si guarda su Ferrari. Non c'è un template universale.
2. **Costo elevato**: leggere trimestrali, relazioni di gestione, identificare le voci critiche richiede molti token e molto tempo. L'LLM non può "capire" il contesto come farebbe un analista umano che conosce il settore.

> "Fare value investing è costoso. È escludere per noi [per ora]." — Salvatore, call 2026-05-13

**Può diventare un modulo futuro** (Analista Agent nel TAVOLO) quando il sistema è già funzionante su trend following.

---

## Come si integra nell'architettura

Il factor investing non è un'alternativa al trend following — è un layer aggiuntivo:
- Trend Following = **quando** entrare (timing tecnico)
- Factor Investing = **cosa** comprare (selezione asset su basi fondamentali)

Nel sistema multi-agente, il **Factor Investigation Agent** è il modulo dedicato a mantenere aggiornato il database dei coefficienti per ogni fattore.

---

## Implementazione software

→ [[system/modules/quant-backtesting]] — il Quant Agent integrerà factor signals come input
→ [[system/architecture]] — Factor Investigation Agent nel layer Research & Intelligence (post-MVP)

---
## Commenti recuperati da iCloud (2026-07-01)

> Commenti Obsidian `%%...%%` presenti nella vecchia copia iCloud (`7054827`) e reinseriti senza sovrascrivere il contenuto corrente.

%%a proposito di factor investing, ti ho caricato una tesi personale [[CorpBondThesis.pdf]], da cui puoi prendere spunto per avere le idee più chiare e capire cosa intendo per factor investing, quali factor esistono, citazioni a fonti affidabili sul factor investing (tecnica molto densa e difficile), che io ho in mente di sfruttare tramite modelli di ML o DeepLearning come nella tesi%%

