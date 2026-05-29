---
title: "LLM Agent System — Prompt Builder + Trader"
type: build
tags:
  - build
  - multi-agent
  - architecture
created: 2026-05-13
updated: 2026-05-29
status: active
priority: medium
area: software
related:
  - "[[build/system-map]]"
  - "[[build/modules/exchange-db]]"
  - "[[build/modules/quant-backtesting]]"
  - "[[build/modules/risk-management]]"
  - "[[references/tradingagents-code-wiki]]"
  - "[[references/external/paper-trading-agents]]"
  - "[[references/videochiamata-luca-salvatore-2026-05-29]]"
---

# LLM Agent System

Il sistema di agenti LLM che produce la tesi di investimento (`research_state`), la sottopone al gate del rischio e la converte in trade. La conversione finale è una **funzione Python deterministica**, non un agente.

---

## Funzione

1. **Analisti (LLM + tool)**: market, sentiment, fondamentali, technical. Leggono dal DB **solo** i campi che servono ed elaborano in un loop di conversazione fino a compilare lo `research_state`.
2. **`research_state`**: tesi di investimento completa — `buy/hold/sell` + target price entrata/uscita + stop loss + sizing + pro/contro + livello di convinzione.
3. **Risk Analyst (LLM reasoning + check Python)**: antitesi bear e guardrail; approva (~60-70%) o rimanda con razionale.
4. **Trade (Python deterministico, NON agent)**: estrae la proposta dallo state, sceglie il miglior prezzo tra broker, esegue.

> **Nota (riconciliazione 2026-05-29)**: il precedente "LLM Trader che produce un JSON `{asset, direction, entry, SL, TP, leverage, reasoning}`" è **superato**. Quei campi non sono più l'output di un agente Trader: sono campi dello `research_state` compilato dagli analisti e validato dal Risk Analyst. L'esecuzione è deterministica (vedi decisione *Trader = funzione Python deterministica* in [[build/decision-log]]).

---

## Topologia agenti (design 2026-05-29)

*Progettata sulla canvas `wiki/artifacts/architecture/agents.canvas` durante la call pomeridiana del 29/05. Vedere [[references/videochiamata-luca-salvatore-2026-05-29]]. Questa è la vista concreta che raffina il principio astratto Ricercatori/Esecutori più in basso.*

Flusso principale (origination → trade):

```
Analyst Research (market + sentiment)  ┐
Analyst Technical (fondamentale + tech)┘→ loop → research_state (alpha)
   → Risk Analyst (guardrail + bear) → approve/decline+razionale
      → [se approve] → Trade (funzione Python deterministica)
```

- **Analisti**: 4 ruoli — **Market**, **Sentiment**, **Fondamentali (financials)**, **Technical**. Aggregazione: sentiment→market, technical→fondamentali. Si valuta se tenerli **4 separati** oppure **2 agenti** con 2 moduli interni ciascuno (`Analyst Research` = market+sentiment, `Analyst Technical` = fondamentale+technical). I due branch fanno un **loop di conversazione** e convergono su un `research_state`.
- **`research_state` = tesi di investimento completa**: non solo l'idea, ma `buy/hold/sell` + **target price entrata + target price uscita + stop loss + sizing** + dati a supporto (pro/contro) + piano operativo. Versionato (`alpha`/v1), esiti `approved`/`declined`.
- **Head of Analyst eliminato**: era previsto un capo-moderatore per scindere il bias bullish degli analisti, ma è stato giudicato **ridondante**. Il contrappeso bearish è il Risk Analyst.
- **Risk Analyst = antitesi bearish + guardrail** (dettaglio in [[build/modules/risk-management]]): se approva (soglia ~60-70%) si va **direttamente al Trade**, senza filtri intermedi. Può rimandare indietro con razionale (es. target price troppo alto).
- **Trade = funzione Python deterministica, NON agent**: estrae la proposta dallo state ed esegue; la selezione del miglior prezzo tra broker è deterministica.
- **Investment State = gate di completezza**: non si fa un trade finché l'`investment_state` non è completo (forza il passaggio per tutti gli analisti). Si **resetta automaticamente** quando il blocco trade rileva la transazione (state pieno → estrae trade → reset).

### Portfolio Manager = orchestratore (CEO / "GOAT")
- All'inizio è **l'umano** (override manuale); concettualmente è l'**agente orchestratore** con potere decisionale ed esecutivo. Metafora del **tavolo circolare**: tutti gli agenti si rifanno a lui, lui ha tool verso tutti e decide quando "ho informazioni sufficienti".
- Si attiva in **2 casi**: (a) un **alert** (solo numerico/prezzo, dal calendario/target), (b) la **periodical synthesis** (state sintetico a intervalli fissi con rendicontazione + market). Resta per lo più libero, si attiva e orchestra (chiama agenti → far ragionare → trade → scrive nel DB). Può fare **override** (news contro l'idea → cancella la posizione).
- **Desk di origination** (analisti) chiamato dal PM come un tool. Serve anche un **desk di monitoring/evaluation** che sorveglia le posizioni esistenti e rifà il processo se le news cambiano la tesi (evita di tenere target obsoleti o posizioni di segno opposto sullo stesso titolo).

### Attivazione e mercati efficienti
- Le **API funzionano solo a richiesta** (no push) → non si può essere notificati automaticamente di una news. Risoluzione: **teoria dei mercati efficienti** — i prezzi riflettono le informazioni; un prezzo anomalo attiva l'agente che monitora il portafoglio, che poi va a cercare la spiegazione (news, tassi). Facendo long-term non serve reazione istantanea.
- Lo **switch di autonomia** si dà nel **system prompt**: un agente ben prompted, visto un prezzo anomalo, va da solo a cercare news/tassi. "Rendere ogni agente quanto più autonomo possibile" è il vero valore aggiunto dell'architettura.

### Provider LLM: OpenRouter + DeepSeek V4 Pro
- **OpenRouter** come router unico verso tutti i provider (agilità nel cambiare modello).
- **DeepSeek V4 Pro** scelto come modello principale: sul report NVDA reale (163k input + 20k output token) costa **~$0,09**, contro ~10× di Claude Sonnet 4.6. Vedere costi in [[build/decision-log]] e [[build/stack]].

### Efficienza ≠ numero di agenti (context rot)
- Non limitare gli agenti per costo: **massimo risultato col minor costo evitando il context rot** (degrado drastico oltre ~50-60% di contesto riempito; benchmark *needle in a haystack*).
- Pattern preferito: **~4 agenti** = 3 specializzati che compilano gli state + 1 **orchestratore** che legge lo state e richiama gli altri secondo necessità. Dare a ogni agente **solo** le info che servono (non troppe/ridondanti né troppo poche). Agenti **asincroni** (timer/eventi). Ruoli definiti **inequivocabilmente** nel system prompt.

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

> **Indirizzo 2026-05-29 (daily note)**: *"dare all'agent tutti gli strumenti per calcolare indicatori ulteriori, con istruzioni a system prompt e tool appositi"*. Cioè: non pre-calcolare solo un set fisso di indicatori, ma esporre **tool parametrici di calcolo** che l'agente invoca on-demand seguendo il system prompt. Riferimento di prodotto: dashboard SFC ([https://sfc-fund.streamlit.app/](https://sfc-fund.streamlit.app/)). Coerente con il principio "tool parametrizzabili" (no valori hardcodati).

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

La leva finanziaria è gestita in modo asimmetrico per mitigare il rischio di liquidità e margine. **Dove vive la logica (riconciliazione 2026-05-29)**: non esiste più un "agente Esecutore" che decide la leva. Il **livello di convinzione** (`Strong Buy`/`Strong Sell`) è un campo dello `research_state` prodotto dagli analisti e **validato dal Risk Analyst**; l'acquisto effettivo delle opzioni è eseguito dalla **funzione Trade deterministica**, che traduce il segnale validato in ordine.

- **Nessuna leva diretta a debito**: evitata all'inizio per i gravosi blocchi di capitale richiesti dai margini del broker.
- **Esposizione derivata**: la leva si realizza acquistando opzioni (derivati).
- **Trigger** (segnale validato nello state → esecuzione deterministica):
  - `Strong Buy` validato → acquisto di opzioni **Call** sul titolo.
  - `Strong Sell` validato → acquisto di opzioni **Put** sul titolo.
  - Segnali standard (`Buy`/`Sell`/`Hold`) → operatività standard in equity pura (spot) senza leva.
- *Nota di design*: la rilevazione/validazione del segnale `Strong` è un **task di sistema** non legato a un tipo di agente specifico; in fase di mappatura del grafo LangGraph verrà assegnato al nodo più coerente (probabilmente l'aggregazione analisti → Risk Analyst). L'esecuzione resta deterministica.

---

## Dipendenze

- Legge da: DB centrale esteso (rendicontazione, dati live, log) → [[build/modules/exchange-db]]
- Produce: `research_state` (tesi completa) → gate del Risk Analyst → funzione Trade deterministica
- Upstream: [[build/modules/exchange-db]] (extractor + DB), [[build/modules/quant-backtesting]] (segnali quant per l'analista technical)
- Downstream: [[build/modules/risk-management]] (gate bear + guardrail) → Trade deterministico → [[build/modules/exchange-db]] (esecuzione)

---

## TODO / Decisioni aperte

- Frequenza di attivazione degli agenti (vincolo costo token + latenza extractor); orientamento: asincrona su alert/periodical synthesis
- Integrare i **Dynamic Temporal Checkpoints** nello `research_state` (l'AI definisce il prossimo check temporale flessibile, es. *tomorrow* vs *1 week*)
- **Analisti: 2 o 4 agenti?** (vedi [[build/decision-log]]) e dove vive l'aggregazione del segnale `Strong`
- Valutare architettura debate: quanti agenti, quali prospettive, se mantenerlo
- Definire schema finale dello `research_state` / `investment_state` (TypedDict + Pydantic)
- Design del **desk di monitoring/evaluation** delle posizioni esistenti
- Brainstorming: replicare i workflow degli uffici di un investitore istituzionale
