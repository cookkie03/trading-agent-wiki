---
title: "LLM Agent System — Prompt Builder + Trader"
type: build
tags:
  - build
  - multi-agent
  - architecture
created: 2026-05-13
updated: 2026-05-27
status: active
priority: medium
area: software
related:
  - "[[build/system-map]]"
  - "[[build/modules/exchange-db]]"
  - "[[build/modules/quant-backtesting]]"
  - "[[build/modules/risk-management]]"
  - "[[references/tradingagents-code-wiki]]"
  - "[[references/external/trading-agents-framework]]"
---

# LLM Agent System — Prompt Builder + Trader

Il componente che assembla tutti gli output del sistema e invoca l'LLM per la decisione di trade finale.

---

## Funzione

1. **Prompt Builder**: legge dal DB gli output di tutti i moduli (Quant Agent, News Agent, Risk Analyst, ecc.) e li assembla deterministicamente in un prompt strutturato per l'LLM
2. **LLM Trader**: riceve il prompt, ragiona dentro i paletti definiti dal Risk Analyst, produce un JSON con la proposta di trade

Output JSON obbligatorio: `{ asset, direction, entry, SL, TP, leverage, reasoning }`.

---

## Filosofia degli Agenti

*Emersa dalla lettura del codebase TradingAgents (2026-05-19) e consolidata il 2026-05-27. Punti di partenza: [[references/tradingagents-code-wiki]] e [[references/conversazione-luca-salvatore-2026-05-27]]*

### Principio guida: due macro-categorie (Ricercatori ed Esecutori) e pochi agenti LLM con tool potenti

Il sistema TradingAgents usa una proliferazione eccessiva di agenti con ruoli frammentati. La nostra architettura efficienta drasticamente questa struttura dividendo i compiti del software in due macro-fasi logiche (Ricerca ed Esecuzione), supportate da moduli deterministici. L'assegnazione finale dei singoli task agli agenti specifici avverrà solo dopo aver mappato tutti i requisiti del grafo LangGraph:

1. **Fase di Ricerca / Analisi (Ricercatori - conceptual node/agent)**:
   - Conducono l'analisi finanziaria core (fondamentale, macro, settore).
   - Raccolgono ed elaborano dati producendo rating operativi chiari (`Buy`, `Sell`, `Hold`).
   - *Nota*: I vecchi agenti *Bull/Bear Analyst* sono stati **eliminati** (decisione 2026-05-26); il loro lavoro è incorporato nella vista strategica di analisi finanziaria.
2. **Fase di Esecuzione (Esecutori - conceptual node/agent)**:
   - Ricevono lo stato e la proposta, valutano la fattibilità del trade nel rispetto dei limiti di rischio deterministici dello Statuto del portafoglio ed inviano le proposte operative all'exchange.
   - Sono dotati di **tool robusti, veloci e specializzati** per interagire con l'infrastruttura DB e le API del broker.

*Decoupling di Design*: La rilevazione dei segnali di forte convinzione (**`Strong Buy`** e **`Strong Sell`**) è definita come un *concetto/task di sistema* ed è completamente **scollegata dal tipo di agente specifico** che lo eseguirà. Quando mapperemo il grafo di LangGraph, definiremo il team di agenti più efficiente ed assegneremo questo compito (l'emissione e validazione del rating Strong) al nodo più idoneo e coerente.

- **Analysts (layer deterministico, NO LLM)**:
  - News: gestite con RAG deterministico.
  - Indicatori tecnici: calcolati automaticamente lato database.
  - Sentiment social/fondamentali: pre-aggregati in record indicizzati nel DB centrale.
- **Risk Management Debaters** → da riesaminare; ipotesi preferita: un agente strategia + un agente rules (portfolio constraints), entrambi orientati a massimizzare profitto analizzando scenari con tool appositi
- **Managers + Trader** → ridurre al minimo; riformulare ispirandosi ai workflow degli investitori istituzionali reali

### Tool-centric design

Ogni agente deve potersi collegare a tool completi e versatili. La selezione e progettazione dei tool è di **fondamentale rilevanza**: dare quanta più completezza di informazioni possibili con quanta meno latenza possibile.

Per ogni tool ereditato dal fork TradingAgents: valutare se tenerlo, potenziarlo o riscriverlo da zero.

Fonti di ispirazione per i tool: sezione "Data Retrieval Tools and Utilities" di [[references/tradingagents-code-wiki]] — Fundamental Data e News/Insider Transactions tools sono buoni punti di partenza.

---

## State Management e Schemas

Obiettivo: **pochi schema molto potenti e dettagliati**, non tanti schema frammentati.

Pattern da TradingAgents da adottare:
- **TypedDict** per gli state di workflow (propagati tra i nodi del grafo)
- **Pydantic** per gli output strutturati degli LLM (con field descriptions come istruzioni)
- **Fallback a free-text** quando structured output non è disponibile o fallisce

Ogni state deve salvare automaticamente le informazioni rilevanti nella memoria del sistema (log).

Buona la gestione degli structured output con fallback in plain text: prevenire interruzioni del pipeline.

---

## Multi-Agent Debate: Mantenerlo o No?

Il debate a 3 agenti per il Risk Management (aggressivo, neutrale, conservativo) ha un vantaggio reale: copertura di angolazioni estreme che un singolo agente potrebbe ignorare (es. extraterritorialità dei ricavi, rischio cambio su mercati esteri).

**Ipotesi**: mantenere il debate se efficientato — ridurre il numero di agenti e affinare i system prompt. Non eliminarlo a priori.

Da investigare: pro e contro della struttura a debate rispetto a un singolo agente multi-prospettiva.

---

## Orchestrazione e Tracciamento: LangGraph + LangSmith

Il progetto utilizza **LangGraph** per orchestrare i workflow multi-agente e **LangChain** per la definizione dei nodi/agenti, partendo come fork di TradingAgents.

### Pattern di LangGraph
- `StateGraph` con nodi = agenti, edges = logica condizionale.
- `ConditionalLogic` per routing dinamico in base all'`AgentState`.
- `Propagator` per inizializzare lo state con contesto storico.
- Checkpointing SQLite per-ticker per riprendere l'esecuzione in caso di crash.

### Integrazione LangSmith (Tracciamento ed Evaluation)
- Adozione del portale **LangSmith (UI/CLI)** come interfaccia centrale per il debug, il logging e il monitoraggio degli agenti in esecuzione.
- Consente la configurazione di metriche di valutazione (evaluation) e il raffinamento dei prompt visualmente sulla piattaforma prima di consolidarli nel codice sorgente, riducendo la complessità di sviluppo manuale delle routine di debug.

---

## Gestione Leva con Opzioni (Call/Put)

L'agente **Esecutore** (o il nodo esecutore preposto) gestisce la leva finanziaria in modo asimmetrico per mitigare il rischio di liquidità e margine:
- **Nessuna leva diretta a debito**: evitata all'inizio per i gravosi blocchi di capitale richiesti dai margini del broker.
- **Esposizione derivata**: la leva si realizza acquistando opzioni (derivati).
- **Trigger**:
  - Segnale `Strong Buy` validato nel grafo → si propone l'acquisto di opzioni **Call** sul titolo.
  - Segnale `Strong Sell` validato nel grafo → si propone l'acquisto di opzioni **Put** sul titolo.
  - Segnali standard (`Buy`/`Sell`/`Hold`) → operatività standard in equity pura (spot) senza leva.
- *Nota*: La logica di trigger della leva tramite derivati è legata unicamente al segnale di convinzione `Strong` prodotto dal sistema, indipendentemente da quale specifico agente lo genererà.

---

## Dipendenze

- Legge da: DB centrale (`module_outputs`, `market_data`, `portfolio_state`)
- Produce: proposta trade JSON → Security Module
- Upstream: [[build/modules/risk-management]] (paletti dello Statuto e limiti dinamici), [[build/modules/quant-backtesting]] (segnali quant)
- Downstream: Security Module → Portfolio Allocator → [[build/modules/exchange-db]]

---

## TODO / Decisioni aperte

- Frequenza di invocazione dell'LLM Trader (vincolo costo token + latenza moduli upstream)
- Definire lo schema JSON dell'Esecutore per integrare i **Dynamic Temporal Checkpoints** (l'AI definisce il prossimo check temporale flessibile, es. *tomorrow* vs *1 week*)
- Valutare architettura debate: quanti agenti, quali prospettive, se mantenerlo
- Definire schema finale AgentState e output JSON del Trader
- Brainstorming: replicare i workflow degli uffici di un investitore istituzionale
