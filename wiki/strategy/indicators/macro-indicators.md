---
title: "Indicatori per Analisi Macroeconomica"
type: synthesis
tags:
  - strategy
  - market-structure
  - quant
created: 2026-06-05
updated: 2026-06-05
status: draft
area: strategy
confidence: high
related:
  - "[[system/modules/quant-backtesting]]"
  - "[[strategy/questions-for-salvatore]]"
  - "[[strategy/index]]"
  - "[[system/modules/data-layer]]"
---

# Indicatori per Analisi Macroeconomica

> Documento di Salvatore. Lavoro in corso — da completare con le sezioni 2–12.
> Fonte originale: `Indicatori per Analisi Macroeconomica.md` (vault root, non archiviare — è il documento di lavoro di Salvatore).

---

## Indice delle categorie

| # | Categoria | Indicatori principali |
|---|-----------|----------------------|
| 1 | Crescita Economica | PIL, Consumi, PMI, Beni Durevoli |
| 2 | Inflazione | CPI, Core CPI, PPI, PCE |
| 3 | Mercato del Lavoro | NFP, Disoccupazione, Salari |
| 4 | Politica Monetaria | Tassi, FOMC, Dot Plot |
| 5 | Liquidità | M2, QE/QT, Reverse repo |
| 6 | Mercato Immobiliare | Costruzioni, Permessi, Vendite |
| 7 | Mercati Obbligazionari | Curva Rendimenti, TIPS, Term Premium |
| 8 | Condizioni del Credito | Spread IG/HY, Financial Conditions |
| 9 | Valute e Materie Prime | DXY, FX, Petrolio, Metalli |
| 10 | Volatilità e Rischio | VIX, Indice MOVE |
| 11 | Flussi e Posizionamento | Flussi ETF, CFTC Positioning |
| 12 | Driver Azionari | EPS, Revisioni Utili, Guidance |

---

## 1. Crescita Economica

### PIL — la misura più ampia dell'attività economica

**Cos'è e perché è importante**

Il PIL misura il valore monetario totale di beni e servizi prodotti in un paese in un dato periodo. Tra tutti gli indicatori, è il metro di giudizio più ampio del ciclo economico.

Viene pubblicato trimestralmente (prima la stima flash, poi la seconda versione e infine la revisione finale) ed è monitorato da banche centrali, governi e investitori.

**Componenti principali**: C (Consumi) + I (Investimenti) + G (Spesa Pubblica) + NX (Esportazioni Nette)

In USA, i consumi privati rappresentano circa il **70% del PIL** → quindi retail sales, lavoro e salari sono proxy fondamentali.

Un PIL solido conferma l'espansione; due trimestri negativi consecutivi = **recessione tecnica**.

> **Regola fondamentale**: il singolo numero del PIL a sé stante è inutile se non si considera il contesto.

**Scenario: PIL sopra il trend** → rialzista

L'economia è in espansione sopra il potenziale: ricavi aziendali in crescita, equity outperform, spread creditizi in compressione. Finché l'inflazione rimane sotto controllo, le banche centrali tendono a rimanere accomodanti.

`Equity good + Spread creditizi in calo + USD in rafforzamento`

**Scenario: PIL surriscaldato** → rischio inflazione e tassi

Surriscaldamento → inflazione in crescita → banche centrali costrette ad alzare aggressivamente i tassi → rendimenti obbligazionari in rialzo → titoli growth perdono valore → credito si inasprisce.

**Nuance fondamentale**: non è il numero del PIL in sé, ma il PIL in relazione all'inflazione che determina il regime macro.

> **La domanda chiave**: **IL PIL ARRIVA CON O SENZA INFLAZIONE?**
> Questa risposta determina l'intero regime di asset allocation.

---

### Consumi: Vendite al Dettaglio e Consumi Privati — Il Polso del Consumatore

> *(sezione in corso di completamento da Salvatore)*

---

## 2–12. Sezioni successive

> Da completare da Salvatore. Le categorie coperte sono: Inflazione, Mercato del Lavoro, Politica Monetaria, Liquidità, Mercato Immobiliare, Mercati Obbligazionari, Condizioni del Credito, Valute e Materie Prime, Volatilità e Rischio, Flussi e Posizionamento, Driver Azionari.

---

## Note operative per il trading agent

Questi indicatori definiscono il **regime macro** che il desk Analyst Research deve interpretare. Principio (Luca): all'agente si dà *"questa metrica ti indica questo"*, **non** *"usa questa metrica per questo"* — è l'agente a imparare come combinarle. Vedi [[strategy/questions-for-salvatore]] §6.

**Fonte dati**: FRED (gratuito, 800k+ serie storiche) per PIL, tassi, inflazione, occupazione, M2. Alpha Vantage per dati macro US. Vedi [[system/data-providers]] per la mappatura completa.
