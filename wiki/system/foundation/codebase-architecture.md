---
title: Codebase Architecture
type: build
tags:
  - codebase-design
  - architecture
  - software
created: 2026-06-23T00:00:00.000Z
updated: 2026-10-31
status: active
confidence: medium
area: software
related:
  - '[[artifacts/project-board]]'
  - '[[system/foundation/architecture]]'
  - '[[system/data/data-layer]]'
  - '[[system/agents/agents]]'
  - '[[system/execution/execution]]'
  - '[[system/quant/quant-backtesting]]'
  - '[[system/data/data-sources-tool-map]]'
---

# Codebase Architecture

Pagina guida per progettare la **nuova codebase reale**. Nasce da un cambio di stato deciso da Luca: il progetto va costruito in modo leggibile da zero, con codice che Luca possa seguire mentre cresce. Le implementazioni e i branch storici restano reference design, non baseline da assumere.

## Decisione e confini — 2026-11-05

Luca decide sei agenti separati: Market, Sentiment, Technical, Fundamental, Risk e Portfolio Manager. Priorità: verificare il codice residuo e definire agenti e contratti, senza presumere che siano già implementati. Il grafo agentico appartiene a `agents`; trigger di attivazione, grafo degli agenti e tool sono concetti distinti. I nomi e la collocazione dei trigger e dei workflow esterni, come pure l'eventuale esistenza delle cartelle `orchestration` e `steps`, restano aperti fino alla valutazione del codice residuo: non crearle ora. Il resto del tree non è approvato.

La portabilità tra backend agentici LangGraph, Hermes, Pi e Claude Code è un obiettivo da ricercare successivamente, non una compatibilità acquisita né una migrazione decisa. LangGraph + LangSmith resta la scelta documentata finché non venga rivalutata. → [[system/foundation/decision-log]] · [[artifacts/project-board]]

## Proposta da discutere — 2026-11-04

> La decisione del 2026-11-05 sopra prevale sui confini e sulla priorità ancora aperti in questa proposta e negli slice storici sotto.

**Proposta, non approvata**: definire insieme tree e responsabilità delle aree `agents/`, `steps/` (nome e ruolo da chiarire), `tools/`, `providers/` (broker, dati e possibili modelli), `storage/`, `config/`, `tests/`, `docs/` e `frontend/`. Non prescrive spostamenti né cancella il lavoro preesistente. La distinzione fra steps, grafi e trigger resta in discussione, non è una decisione. Luca sceglie di organizzare i provider per funzione — broker, dati e modelli — anziché per nome vendor; il tree concreto resta da definire. Il riferimento di design prioritario nei dubbi è [[artifacts/architettura.canvas]]; gli altri canvas sono idee o reference. Le priorità operative sono nella [[artifacts/project-board#Priorità operative correnti — 2026-11-04]].

## Principio operativo storico — priorità superata

Il seguente ordine harness-first è conservato come storico, non come sequenza corrente:

1. **Tree e confini dei package**
2. **Harness broker + data vendor + DB + test**
3. **Capability/tool deterministici**
4. **State, prompt e orchestration agentica**
5. **Job asincroni, dashboard, esperimenti**

Questa sequenza tiene insieme tre decisioni gia' presenti nella wiki: DB come hub centrale, principio deterministico e broker/vendor sostituibili via adapter.

## Boundary dei package

| Package / area | Responsabilita' | Dipendenze ammesse | Non deve contenere |
|---|---|---|---|
| `connectors/` | Adapter verso broker e data vendor: Alpaca, IBKR, yfinance, FRED, Finnhub, OpenBB, ecc. | SDK esterni, config, logging tecnico | Prompt, logica agentica, scoring di strategia |
| `database/` | Schema, migrazioni, repository, transazioni, dedup, retention | SQL/ORM, config DB | Chiamate vendor dirette, ragionamento LLM |
| `capabilities/` | Calcoli deterministici su dati normalizzati: indicatori, risk metrics, backtest helpers, transforms | `database/`, librerie quant | Chiamate API raw non wrappate, prompt |
| `tools/` | Interfacce stabili offerte agli agenti o al PM: quote, macro, sentiment, portfolio state, backtest query | `capabilities/`, `database/`, `connectors/` | Dettagli vendor visibili agli agenti |
| `agents/` | Prompt, schemas, context, routing, policy di richiamo tool, PM/desk/Risk | `tools/`, schemas condivisi | Calcoli numerici a mano, SDK broker/vendor |
| `execution/` | Trade deterministico, submit, recovery, costi, exit management, broker intent log | `database/`, `connectors/brokers`, risk capabilities | LLM decision-making |
| `frontend/` | UI read-only o controllata tramite contratti espliciti | API/query layer, read models | Business logic critica |
| `orchestration/` | Cycle runner, trigger engine, job scheduling, daemon | tutti i package tramite interfacce | Logica di dominio nascosta |

I nomi sono orientativi. La decisione da prendere non e' il nome esatto, ma il confine: **gli agenti non devono sapere quale broker o vendor sta dietro una richiesta**.

## Slice 1: harness minimo

Il primo pezzo di codice utile deve dimostrare che l'infrastruttura regge senza agenti:

- config unica per ambiente, broker, vendor, DB e costi;
- database iniziale con migrazioni e repository;
- adapter broker paper e contratto broker;
- almeno un data connector storico (`yfinance`) e uno macro (`FRED`) o mock equivalente;
- dedup/check-presenza per scritture DB;
- test offline con fake connector e fake broker;
- un test end-to-end: fetch dati -> DB -> capability calcola indicatore -> proposta trade finta -> execution paper.

Questo slice rende possibile costruire gli agenti sopra fondamenta osservabili, invece di usarli per coprire buchi infrastrutturali.

## Slice 2: capability e tool layer

Dopo l'harness, si costruisce il layer che rende gli agenti utili:

- `compute_indicator(ticker, indicator, params)` per ATR, RSI, MACD, medie, 52w, drawdown;
- `get_portfolio_state()` e `get_open_positions_risk()` dal DB;
- `get_macro_series(series_id, start, end)` da FRED/DB;
- `get_news` e `get_news_sentiment` dietro wrapper vendor;
- `get_calendar` per earnings e macro events;
- `run_backtest(strategy_id, params, window)` come capability separata dal live trading.

Questo layer deve collegarsi a [[system/tools/tools-inventory]] e [[system/data/data-sources-tool-map]]: la mappa provider decide da dove arrivano i dati, l'inventory decide quali tool espone il sistema.

## Slice 3: agenti e state

Solo quando tool e dati sono stabili si passa a:

- prompt in file dedicati/versionabili;
- schema `research_state` / `investment_state` chiarito e testato;
- PM con policy "nel dubbio chiedi";
- desk Market/Sentiment/Technical/Fondamentali;
- Risk Analyst come desk/gate da decidere con Luca e Salvatore;
- orchestration event-driven tramite trigger engine.

Gli output agentici devono essere verificabili: ogni numero importante viene da tool deterministici, ogni decisione lascia trace nel DB.

## Decisioni aperte da chiudere prima di codice vero

- Framework agentico: Datapizza AI come candidato/reference o scelta confermata per il nuovo build? → [[system/foundation/stack]]
- Schema definitivo dello state e rapporto `research_state` / `investment_state` → [[system/investment/state-schemas]]
- Risk Analyst: desk pari agli altri o gate finale? → [[system/agents/agent-behaviors]]
- Primo set strategy da codificare: trend following, mean reversion, factor/value, dual portfolio → [[strategy/index]]
- Livello e perimetro del frontend nel primo harness: nessuno, CLI o cockpit operativo completo → [[system/interface/frontend-module]]

## Collegamenti operativi

- Board: [[artifacts/project-board]]
- Mappa fonti/tool: [[system/data/data-sources-tool-map]]
- Data layer: [[system/data/data-layer]]
- Execution: [[system/execution/execution]]
- Quant/backtesting: [[system/quant/quant-backtesting]]
- Agents: [[system/agents/agents]]

## Avvio per classi — 2026-10-30

Owner: 🛠 Luca (software). Stato: ideazione, nessuna nuova classe implementata.

### Appunto originale recuperato

Fonte: [Notion — Projects → Trading Agent](https://www.notion.so/4012e441b0e581fcb942c109716dfb1f), letta il 2026-10-30, ultima modifica riportata 2026-10-23.

Luca elenca: `Agent`, `Tool`, `Provider`, `Data Broker`, `Broker`, documenti da compilare per azienda/mercato/strategia e `Strategy`. Propone un primo esempio concreto per provider, data broker, agente, tool e broker, con test robusti attorno a questi esempi. Annota anche una futura UI di monitoraggio e un chatbot per orientare la strategia: il rapporto con la UI read-only e l'autonomia va chiarito prima di implementarlo.

Su Todoist è stato trovato [Trading-Agent](https://app.todoist.com/app/task/6hgrJWVFhfGcGpmX), con il sottotask [trasformare la wiki in una codebase semplice, modulare e leggibile da un principiante Python](https://app.todoist.com/app/task/6hjx2hxw8GVvgW45). Il task e i sottotask letti non contengono la lista di classi: la fonte esatta è Notion.

### Proposta da discutere

Prima slice: richiesta di prezzi storici → fonte dati → normalizzazione → persistenza → lettura, verificabile offline.

| Nome provvisorio | Responsabilità proposta |
|---|---|
| `PriceBar` | Record OHLCV normalizzato, con strumento, valuta, date e provenienza |
| `MarketDataProvider` | Contratto piccolo per recuperare prezzi; primo adapter concreto e fake offline |
| `MarketDataRepository` | Scrittura idempotente e lettura dei dati persistiti |
| `DataBroker` | Coordina presenza/freshness nel DB, fetch, persistenza e restituzione dei dati |

Questa è una proposta, non una decisione di class design. Va chiarito se `Provider` nell'appunto significa provider LLM oppure fonte dati, e se `Data Broker` significa coordinatore interno oppure vendor esterno. In caso di provider LLM, `LLMProvider` resta distinto da `MarketDataProvider`. `Broker` riguarda conto/ordini; `Tool` espone una capacità agli agenti; `Agent`, documenti e `Strategy` seguono dopo la prima slice. Evitare una superclasse universale che mischi dati, LLM ed esecuzione.

Per l'ideazione si applica la skill locale di Matt Pocock `codebase-design`: interfacce piccole, responsabilità profonde e dipendenze sostituibili; le classi non sono obbligatorie dove basta una funzione. Nomi, metodi e primo vendor restano da concordare con Luca.

## Struttura modulare e partenza Broker — proposta 2026-10-30

Owner: 🛠 Luca. Luca chiede di discutere prima l'alberatura della repository e poi il modulo Broker con ricerca Alpaca. La precedente slice prezzi/DataBroker è una proposta alternativa, non una priorità approvata.

La proposta locale è `src/trading_agent/` con `brokers`, `data`, `storage`, `analysis`, `tools`, `agents`, `workflows`, `execution`, `interface`, più configurazione e composizione esplicita. Co-localizza contratto Broker e adapter in `brokers`; separa i comportamenti degli agenti dalla topologia dei workflow e le analisi complesse dai tool che le espongono. I nomi sono proposti: la wiki mantiene i confini canonici di responsabilità descritti sopra.

Prima slice candidata: contratto di lettura conto/posizioni/ordini, fake offline e adapter Alpaca paper. Invio ordini con intent log, ricerca ID cliente, gestione esiti incerti e SL/TP in una slice successiva, prima del trading autonomo. Nessuna nuova classe o test prodotto è stata implementata in questa fase.

Artefatti nel repository codice: `docs/architecture.md` (proposta da discutere) e `docs/research/alpaca-broker.md` (ricerca ufficiale). Non sono decisioni definitive sulla struttura. La ricerca esterna va distinta dai requisiti wiki; in particolare l'ID cliente non va interpretato senza verifica come garanzia automatica di exactly-once.

Luca richiede un sub-agent consultabile che risponda esclusivamente dalla wiki e un sub-agent per la manutenzione della documentazione. Le istruzioni operative sono in `AGENTS.md` del repository codice; le skill di Matt Pocock restano preferite quando pertinenti.

## Alberatura approvata e requisito Docker — 2026-10-30

Owner: 🛠 Luca (software). Decisione esplicita: approvata l'alberatura del monolite modulare e autorizzato l'avvio dello scaffolding. Il progetto deve poter essere distribuito in produzione con Docker.

```text
trading-agent/
├── .agents/skills/
├── AGENTS.md
├── README.md
├── pyproject.toml
├── config.toml
├── docs/
├── src/trading_agent/
│   ├── brokers/       # conto, posizioni, ordini e adapter
│   ├── data/          # fonti e coordinamento acquisizione
│   ├── storage/       # DB, repository e migrazioni
│   ├── analysis/      # capacità analitiche deterministiche
│   ├── tools/         # strumenti esposti agli agenti
│   ├── agents/        # comportamenti e prompt
│   ├── workflows/     # topologia, trigger e scheduling
│   ├── execution/     # guardrail, invio e recovery
│   ├── interface/     # CLI e futura UI
│   ├── config.py
│   └── bootstrap.py
└── tests/
    ├── brokers/
    ├── analysis/
    ├── fakes/
    └── integration/
```

Questa è la struttura di destinazione: `config.toml`, `config.py`, `bootstrap.py` e i contratti di classe si aggiungono quando ne viene definito il comportamento. Lo scheletro iniziale contiene i package e le directory dei test, senza implementare finte classi o servizi.

Il requisito Docker implica packaging installabile, build riproducibile, segreti esterni all'immagine, persistenza esterna al container, log stdout/stderr e arresto corretto con recovery. Il DB può avere un container separato. Dockerfile e verifica immagine devono accompagnare il primo runtime eseguibile; lo scaffolding non attesta production readiness.

La scelta rispetta le responsabilità sopra descritte: `analysis` corrisponde alle capabilities, `workflows` all'orchestration, `brokers` raccoglie contratto e adapter. Non modifica lo scope paper US equity USD-only né approva automaticamente tutti i metodi Broker. Vedi [[system/foundation/implementation-status]] per lo stato verificato.

## Primo Broker di lettura implementato — 2026-10-31

Owner: 🛠 Luca. Il contratto conto/posizioni/ordini e l'adapter Alpaca paper sono ora implementati nel repository codice su richiesta di Luca. Il contratto rimane indipendente dallo SDK; non include invio/cancellazione. Evidenza datata e limiti, senza duplicare stato dei test nelle specifiche: [[system/foundation/implementation-status#Broker read-only — verifica 2026-10-31]].
