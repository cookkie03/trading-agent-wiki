---
title: "Conversazione Luca–Salvatore — Feedback report TradingAgents (2026-05-26)"
type: source
tags:
  - area/market
  - area/software
  - strategy
  - multi-agent
created: 2026-05-27
updated: 2026-05-27
status: active
raw_source_path: "raw/daily-notes/2026-05-26.md"
related:
  - "[[references/whatsapp-luca-salvatore-2026-05-22]]"
  - "[[references/tradingagents-code-wiki]]"
  - "[[build/decision-log]]"
confidence: high
---

# Conversazione Luca–Salvatore — Feedback report TradingAgents (2026-05-26)

Conversazione serale del 26 maggio 2026. Salvatore ha letto con attenzione i report generati da TradingAgents (NVDA + MONC) e fornisce un'analisi esperta su cosa funziona, cosa non funziona e come dovrebbe essere strutturato un report di qualità.

---

## Contesto

Luca e Salvatore si allineano sulla valutazione del report TradingAgents NVDA (generato il 22/05 con effort 1/3, modello free). Salvatore ha letto il report come analista con background in equity research (Starting Finance).

---

## Struttura del report ideale — proposta di Salvatore

Salvatore propone un ordine preciso per un report di analisi aziendale efficace:

### 1. Financial Analysis (core — peso maggiore)
- **Revenue analysis**: andamento ricavi, trend
- **Debt analysis**: struttura del debito, broker debt
- **Patrimoniale/liabilities**: analisi dello stato patrimoniale, passività
- **Fonti obbligatorie**: dati da provider ufficiali (non basta Yahoo Finance) + **relazioni di gestione** + **note integrative**
  - Le relazioni di gestione contengono: intenzioni dell'azienda per i trimestri successivi, lancio nuove divisioni, fatti rilevanti comunicati dalla società → **non si trovano su Yahoo Finance**
  - TradingAgents attuale sembra non leggerle → analisi finanziaria puramente numerica senza contesto strategico

### 2. Technical Analysis
- Medie mobili, indicatori di prezzo
- Analisi del trend: l'azienda è solida, **ma** cosa succede al prezzo del titolo?
- Fatti importanti recenti: notizie rilevanti da provider ufficiali (non social)

### 3. Bull/Bear Case (peso minore)
- Vista strategica: scenari futuri plausibili, cosa può influire sui ricavi o sul prezzo
- **Non** un'analisi dati pura → è soggettiva per definizione
- Va **ridotta**: poche bullet point chiare, non 80 pagine
- La struttura attuale di TradingAgents è confusa: il bull agent parla più volte, sembra che ci siano più bull diversi → "non ho capito se è come se avessero parlato tre bull diversi o uno che faceva tre monologhi"
- Problema: ha aumentato l'effort nella parte sbagliata — più lunghezza nel debate, non più qualità nell'analisi

### 4. Risk Summary
- **4 parametri chiave, non analisi discorsiva**
- Conciso, machine-readable: non serve un papello enorme di testo

---

## Criticità di TradingAgents (feedback esperto)

| Problema | Dettaglio |
|----------|-----------|
| Fonti finanziarie incomplete | Non legge relazioni di gestione e note integrative → manca la parte strategica comunicata dalla società |
| Struttura Bull/Bear confusa | Bull agent parla più volte, struttura non chiara, peso eccessivo al debate |
| Risk Analyst troppo discorsivo | Dovrebbe essere 4 parametri, non paragrafi |
| Dati tecnici: prezzi di apertura | Dovrebbe usare prezzi di chiusura (segnalato già il 22/05) |
| Mancanza calendario economico | Non integra trimestrali, accordi internazionali, eventi che impattano i prezzi |

---

## Il calendario economico

> "I provider seri ti segnano il calendario economico che è importante per capire l'impatto sui prezzi"

**Cosa include il calendario economico:**
- Date delle trimestrali delle aziende in portafoglio
- Accordi internazionali rilevanti
- Date di publication di dati macro (PIL, inflazione, tassi)

Anche provider meno specializzati (es. Investing.com) lo hanno per alcuni titoli.

**Impatto sul progetto**: il sistema dovrebbe avere accesso al calendario economico come dato di input per gli agenti. Luca ha accolto l'idea: "ok mi hai dato una bella idea: avere tra le altre informazioni raccolte una sorta di calendario di date importanti"

---

## Conclusioni di Luca sulla struttura agenti

Sulla base del feedback di Salvatore:
- **Bull/Bear Analyst agents non servono** nella nostra versione
- **La struttura agenti va completamente ripensata** — non basta "più effort", serve "effort nella parte giusta"
- Gli agenti iniziali di research non sono tutti necessari o non devono operare in quel modo
- **Obiettivo**: sistema più efficiente, non più complesso

---

## Contesto sviluppo (Luca)

- Luca sta seguendo il corso LangChain/LangGraph
- Ha confermato che il sistema TauricResearch è costruito con una libreria Python per agenti (LangChain/LangGraph)
- Il corso permette di capire direttamente come verificare se il sistema funziona bene (LangSmith)
- Piano: studiare il codice del progetto TradingAgents, poi pianificare insieme a Salvatore come trasformarlo nel vostro sistema

---

*Vedere [[references/whatsapp-luca-salvatore-2026-05-22]] per il contesto del primo test.*
*Vedere [[build/decision-log]] per le decisioni architetturali derivate.*
