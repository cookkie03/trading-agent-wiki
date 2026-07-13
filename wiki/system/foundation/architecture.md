---
title: "Architettura del sistema"
type: build
tags:
  - build
  - architecture
created: 2026-04-30
updated: 2026-07-13
status: active
priority: high
area: software
related:
  - "[[system/foundation/mvp]]"
  - "[[system/foundation/stack]]"
  - "[[system/data/data-layer]]"
  - "[[system/quant/quant-backtesting]]"
  - "[[system/agents/agents]]"
  - "[[system/execution/execution]]"
---

# System Map

Architettura di design del `trading-agent`. Il sistema deve raccogliere informazioni, analizzare, decidere, eseguire e imparare. Per non confondere design e repository esterno, vedi [[system/foundation/implementation-status]].

---

## Principi fondanti

**Principio deterministico**: l'LLM fa solo il ragionamento finale. Tutto il resto (calcoli, raccolta dati, esecuzione ordini) è Python puro. Dato lo stesso input, ottieni sempre lo stesso output.

**Modularità**: ogni modulo è un blocco con input e output definiti, scrivibile e leggibile dal DB centrale. Si può sostituire, pesare dinamicamente o disabilitare senza toccare il resto del sistema.

**DB come hub centrale**: tutti i moduli scrivono qui; gli agenti leggono da qui (solo i campi che servono). L'unica fonte di verità del sistema.

---

## Topologia operativa (design 2026-05-29)

> Vista concreta progettata sulla canvas `wiki/artifacts/architettura.canvas` (call del 2026-05-29). Sostituisce il vecchio ciclo lineare "TAVOLO → Prompt Builder → LLM Trader → Security → Allocator". Dettaglio agenti in [[system/agents/agents]].

```
Portfolio Manager (CEO / orchestratore)  ◄── attivato da: alert numerico | calendario | next_check_date
  │  (tavolo circolare: ha tool verso tutti, decide quando "ho info sufficienti")
  │
  ├─► Desk di origination — chiamati come tool:
  │      Analyst Research  (Market + Sentiment)        ─┐
  │      Analyst Technical (Technical + Fondamentali)  ─┘─► loop conversazione
  │                         │
  │                         ▼
  │                 research_state  =  tesi di investimento completa
  │                 (buy/hold/sell + target entry/exit + stop loss + sizing + pro/contro)
  │                         │
  │                         ▼
  │              Risk Analyst (antitesi bear + guardrail deterministici da Statuto)
  │                 │  approva (~60-70%)        │  rimanda indietro con razionale
  │                 ▼                            └────────► (loop agli analisti)
  │              Investment State  (gate di completezza pre-trade)
  │                 │
  │                 ▼
  │              Trade  =  funzione Python deterministica (estrae proposta → best price → esegue)
  │                 │  (al rilevamento della transazione → reset automatico dello state)
  │                 ▼
  │              Exchange (paper) + scrittura nel DB
  │
  └─► Desk di monitoring/evaluation — sorveglia le posizioni esistenti; se le news cambiano
         la tesi, rifà il processo (evita target obsoleti / posizioni di segno opposto)
```

**Attivazione (mercati efficienti, no push news)**: le API rispondono solo a richiesta. Un **prezzo anomalo** (alert numerico) attiva il monitoring, che poi cerca la spiegazione (news/tassi). Coerente con l'orizzonte mid-term: non serve reazione istantanea.

**Frequenza**: le analisi sono **event-driven** (alert, calendario e `next_check_date`); un health check del portafoglio e del sistema rimane periodico e costante. Gli **adaptive extractor** modulano la frequenza di estrazione per rispettare i rate limit.

---

## Layer 1 — DB Centrale (esteso)

Unico punto di verità (blocco viola della canvas, sempre acceso). Schema completo in [[system/data/data-layer]]. Quattro aree logiche oltre alle 5 tabelle SQL core:

| Area | Contenuto |
|------|-----------|
| **Rendicontazione portafoglio** | Liquidità corrente/investita, distribuzione (geo/asset class/settore/duration), P/L e metriche di performance |
| **Dati live** | Prezzi, calendario economico, news, indicatori macro, insider trading, tassi di cambio |
| **Costituzione / Statuto** | Regole deterministiche del fondo (al centro) → [[system/agents/agents]] |
| **Log** | `states`, `reports`, `transactions` — storico completo, con retention via clustering+riassunto |

---

## Layer 2 — Estrazione dati (Extractors)

Primo set di tool degli agenti. Si agganciano al DB (DB-first), non ai vendor direttamente.

| Componente | Funzione |
|------------|----------|
| **Extractors set** | Estraggono info di mercato → le scrivono sia nel DB sia verso gli agenti |
| **Adaptive extractor** | Frequenza adattiva in base alla vicinanza al target (rispetta i rate limit) |
| **Market Alert agent** | Riceve dagli adaptive extractor; unico tool = *calendar tool* che scrive eventi nel calendario economico → alla scadenza scatta l'alert (solo numerico/prezzo) |
| **mantainer** | Manutenzione (non-LLM) dei dati technical e della rendicontazione nel DB *(nodo nuovo del canvas, ruolo da confermare)* |

---

## Layer 3 — Origination / Analisi

Due **desk** compilano lo `research_state` (decisione consolidata dal canvas, chiude il dubbio "2 vs 4 agenti"): **Analyst Research** (Market + Sentiment) e **Analyst Technical** (Technical + Fondamentali).

| Analista | Funzione | Tipo |
|----------|----------|------|
| **Market** | Contesto di mercato, macro | LLM + tool |
| **Sentiment** | Sentiment news/social (indicatori da definire) → aggrega su Market | LLM + tool |
| **Fondamentali** | Financials, ratio (es. P/E trailing vs current) | LLM + tool |
| **Technical** | Segnali tecnici/quantitativi → [[system/quant/quant-backtesting]]; aggrega su Fondamentali | LLM + tool (calcoli deterministici) |

Output: `research_state` versionato (`alpha`/v1) con esiti `approved`/`declined`.

---

## Layer 4 — Rischio, gate ed Esecuzione

| Componente | Funzione | Tipo |
|------------|----------|------|
| **Risk Analyst** | Antitesi bearish + guardrail dello Statuto; soglia ~60-70%; approve / decline+razionale → [[system/agents/agents]] | LLM (reasoning) + check Python |
| **Guardrail deterministici** | VaR ~10%, % max per area/settore, diversificazione, duration: check Python, non compiti dell'LLM | Python deterministico |
| **Investment State** | Gate di completezza: nessun trade finché lo state non è completo; reset automatico post-transazione | Python |
| **Trade** | Estrae la proposta dallo state, sceglie il miglior prezzo tra broker, esegue → [[system/execution/execution]] | **Python deterministico (NON agent)** |
| Logger | Logga states/reports/transactions nel DB | Python |

---

## Layer 5 — UI e Apprendimento

| Componente | Funzione | Stato |
|------------|----------|-------|
| Streamlit Dashboard | Sola lettura: equity curve, posizioni, metriche (rif. dashboard SFC) | Post-MVP |
| Canale Telegram "sala segnali" | Calendario, riassunti news, prezzi, trade, variazioni rilevanti | Post-MVP |
| **Reportistica diagnostica** | "Cosa va male": post-mortem periodico (modulo Python + narrazione LLM) → [[system/quant/learning-feedback-loop]] | MVP→post-MVP |
| RL / Weighting Module | Ponderazione dinamica dei pesi degli agenti su esiti storici → [[system/quant/learning-feedback-loop]] | Post-MVP avanzato |
| Fine-Tuning Module | Riaddestramento LLM su storico del progetto | Post-MVP avanzato |

> Questi componenti fanno parte di un unico **loop di valutazione e auto-miglioramento** — substrato di logging, reportistica diagnostica, scoring agenti, ponderazione pesi, feedback post-trade: vedi [[system/quant/learning-feedback-loop]].

---

## Protocollo di comunicazione

Comunicazione via **state condivisi** (Datapizza AI graph) + **DB**, non chiamate dirette:
1. **Moduli/extractor → DB**: ogni componente scrive output strutturati (`module_outputs`, `states`, `reports`)
2. **DB → agenti**: ogni agente riceve dal DB **solo** i campi che gli servono (evitare context rot: degrado oltre ~50-60% di contesto riempito)
3. **Agenti → state**: gli analisti compilano lo `research_state`; l'orchestratore lo legge e decide quando "ho info sufficienti"

Dare a ogni agente solo l'informazione necessaria evita sia l'effetto "telefono senza fili" sia il context rot dei prompt sovraccarichi.

---

## Sequenza di specificazione

| Fase | Specifica da completare nel vault |
|-------|----------------------------------|
| Fondazioni | confini di dominio, retention dati, adapter e contratti tool |
| Analisi | state annidato, ruoli desk, prompt e validazione |
| Orchestrazione | trigger, subgraph per ticker, policy anti-loop e checkpoint |
| Post-MVP | benchmark dinamico, opzioni, UI evoluta, feedback/learning |

**Framework:** LangGraph + LangSmith. Datapizza AI resta un riferimento storico in [[prior-art/libraries/datapizza-ai]].

---

---

## Pattern architetturali (aggiornamento 2026-05-21)

*Emersi dalla lettura del codebase TradingAgents — [[prior-art/tradingagents/code-wiki]]*

**[[_meta/glossario#Look-Ahead Bias|Look-ahead bias]] — doppia data**: ogni informazione nel DB ha due date distinte:
- `publication_date`: quando è stata ottenuta/pubblicata (es. giorno di pubblicazione delle trimestrali)
- `reference_date`: la data a cui l'informazione si riferisce (es. ultimo giorno del trimestre)

**DB-first data strategy**: ogni dato viene scritto nel DB prima di essere reso disponibile agli agenti. I tool si agganciano al DB, non ai vendor direttamente. Eccezione da valutare: dati real-time molto recenti non ancora nel DB.

**Pattern intra-modulo**: ogni subdirectory del progetto è un modulo con un unico file gateway che gestisce tutto il routing input/output intra- e inter-modulo.

**Standardizzazione**: tutti i moduli producono output in formati comuni. L'exchange deve essere intercambiabile (demo ↔ reale).

**Indicatori calcolati dal DB**: nessun calcolo on-the-fly — gli indicatori vengono calcolati con formule che richiamano i dati grezzi già nel DB.

---

*Per le decisioni tecniche vedere [[system/foundation/decision-log]]. Per il piano MVP vedere [[system/foundation/mvp]]. Per idee e brainstorming: [[system/foundation/ideas-log]].*

