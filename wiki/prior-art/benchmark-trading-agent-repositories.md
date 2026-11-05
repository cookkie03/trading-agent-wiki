---
title: Benchmark Repository Trading Agent
type: synthesis
tags:
  - multi-agent-system
  - trading-agent
  - langgraph
  - backtesting
  - risk-management
  - execution
  - dashboard
created: 2026-11-01T00:00:00.000Z
updated: 2026-11-01T00:00:00.000Z
status: active
confidence: medium
priority: high
area: research
related:
  - '[[system/foundation/architecture]]'
  - '[[system/foundation/mvp]]'
  - '[[system/foundation/decision-log]]'
---

## Risultato

Il repository **più simile nel complesso** è:

### [`TauricResearch/TradingAgents`](https://github.com/TauricResearch/TradingAgents)

È il match migliore per la parte centrale della wiki:

- framework multi-agent finanziario;
- **LangGraph** come orchestratore;
- analisti fondamentali, tecnici, news e sentiment;
- bull/bear researchers;
- trader;
- risk-management team;
- portfolio manager;
- checkpoint persistenti;
- decision log;
- backtesting point-in-time;
- supporto a portfolio-aware analysis.

Il repository dichiara esplicitamente di modellare il funzionamento di una trading firm con agenti specializzati e di usare LangGraph. Il suo albero sorgente contiene moduli separati per analyst, researcher, risk management, portfolio manager e stato condiviso.

### Limite principale

`TradingAgents` è soprattutto un **framework di ricerca e decision support**. Non sostituisce il data layer già previsto dalla wiki:

- non è il DB centrale del progetto;
- non implementa il vostro outbox per la materializzazione degli indicatori;
- non offre la stessa provenance locale provider → dato normalizzato → derivato;
- non è un execution engine broker completo;
- il backtest rimane una valutazione del processo decisionale, non una garanzia di strategia profittevole.

Perciò lo userei come **riferimento per la topologia agentica**, non come base da copiare integralmente.

---

## Criteri di confronto

Ho usato questi criteri, ricavati dalla wiki:

1. **Multi-agent e LangGraph**
   - ruoli specializzati;
   - grafo esplicito;
   - stato/checkpoint;
   - routing e human-in-the-loop.

2. **Data layer**
   - dati storici e real-time;
   - normalizzazione provider;
   - persistenza;
   - provenance;
   - point-in-time correctness.

3. **Quant e backtesting**
   - indicatori;
   - backtest deterministico;
   - walk-forward;
   - metriche di rischio;
   - assenza di look-ahead bias.

4. **Risk ed execution**
   - risk gate separato dal modello;
   - position sizing;
   - broker/paper trading;
   - approvazione umana;
   - fail-closed behavior.

5. **Dashboard e operatività**
   - dashboard;
   - decision log;
   - auditabilità;
   - monitoring.

6. **Compatibilità con il target**
   - stock USA;
   - USD-only;
   - workflow screening → deep dive → PM → risk → execution;
   - provider e broker intercambiabili.

---

## Confronto dei candidati

| Repository | Agent/LangGraph | Data layer | Backtest/quant | Risk/execution | Dashboard | Valutazione |
|---|---|---|---|---|---|---|
| [`TauricResearch/TradingAgents`](https://github.com/TauricResearch/TradingAgents) | **Eccellente** | Medio | Buono | Medio | Bassa/media | **Miglior match architetturale** |
| [`Jiangge89/trading-agent`](https://github.com/Jiangge89/trading-agent) | **Eccellente** | Buono: PostgreSQL, pgvector, FTS, RAG | Medio | **Molto buono**: risk checks + approval gate | Bassa | Miglior esempio di paper trading human-in-the-loop |
| [`mhsefidgar/Multi-Agent-Quantitative-Trading-Research`](https://github.com/mhsefidgar/Multi-Agent-Quantitative-Trading-Research) | Buono: LangGraph + MCP | Buono | **Buono** | **Molto buono**: deterministico e fail-closed | Bassa | Miglior riferimento per separare AI, risk ed execution |
| [`ziyadal/multi-agent-trading-system`](https://github.com/ziyadal/multi-agent-trading-system) | Buono: 5 agenti + LangGraph | Buono: SQLite | Buono: walk-forward | Medio: approval gate, ma niente live routing | Bassa | Prototipo molto vicino al funnel, ma BTC/USDT |
| [`Open-Finance-Lab/AgenticTrading`](https://github.com/Open-Finance-Lab/AgenticTrading) | Medio/alto | Buono | Buono | Buono | **Eccellente** | Migliore per dashboard, evaluation e decision inspection |
| [`mocasus/trade-agent`](https://github.com/mocasus/trade-agent) | Medio | **Buono: SQLite** | Buono | **Buono**: exchange execution e risk profiles | **Buono** | Sistema operativo compatto, meno vicino alla topologia LangGraph |
| [`caalopezgo/quantlab`](https://github.com/caalopezgo/quantlab) | Basso | **Buono: SQLite** | **Buono** | Buono: paper trading e risk | Bassa | Buon riferimento per il core quantitativo, non per gli agenti |

### Nota sui repository molto noti

- [`virattt/ai-hedge-fund`](https://github.com/virattt/ai-hedge-fund) resta un buon riferimento concettuale per gli analyst e il portfolio workflow, ma la versione attuale non dichiara LangGraph nelle dipendenze e il README specifica che non esegue realmente trade.
- [`microsoft/qlib`](https://github.com/microsoft/qlib) è molto forte su ricerca quantitativa, dati e modelli, ma non è un sistema multi-agent LangGraph.
- [`openbq-org/OpenBB`](https://github.com/openbq-org/OpenBB) è il riferimento più interessante per provider, data access e strumenti per quants/AI agents, ma non implementa il vostro funnel decisionale completo.
- [`polakowo/vectorbt`](https://github.com/polakowo/vectorbt) è eccellente per backtesting veloce, ma non è un sistema agentico né un execution platform.

---

## Repository starred rilevanti

L’accesso GitHub dell’account è disponibile. Tra gli starred risultano pertinenti:

- [`HKUDS/Vibe-Trading`](https://github.com/HKUDS/Vibe-Trading) — personal trading agent;
- [`TraderAlice/OpenAlice`](https://github.com/TraderAlice/OpenAlice) — gestione end-to-end di ricerca, ingresso, gestione e uscita;
- [`SilvioBaratto/optimizer`](https://github.com/SilvioBaratto/optimizer) — LLM agents, portfolio optimization, market-data pipeline e paper trading;
- [`microsoft/qlib`](https://github.com/microsoft/qlib) — quant research e data pipeline;
- [`openbq-org/OpenBB`](https://github.com/openbq-org/OpenBB) — data platform per analisti, quants e AI agents;
- [`polakowo/vectorbt`](https://github.com/polakowo/vectorbt) — backtesting e ricerca quantitativa;
- [`cvxgrp/cvxportfolio`](https://github.com/cvxgrp/cvxportfolio) — portfolio optimization e risk-aware allocation.

`TauricResearch/TradingAgents` non risulta tra gli starred verificati, ma è comunque il miglior match pubblico trovato per la struttura LangGraph e i ruoli agentici.

---

## Raccomandazione operativa

Userei i repository così:

1. **`TradingAgents`**
   - topologia LangGraph;
   - ruoli Analyst/Researcher/Trader/Risk/PM;
   - gestione dello stato;
   - discussione bull/bear.

2. **`mhsefidgar/Multi-Agent-Quantitative-Trading-Research`**
   - risk manager deterministico;
   - principio fail-closed;
   - separazione tra AI output e autorizzazione al trade;
   - boundary MCP/execution.

3. **`Jiangge89/trading-agent`**
   - `prepare_order`;
   - preview dell’ordine;
   - controlli cash/concentration/trade size;
   - `interrupt()` per approvazione umana;
   - paper broker.

4. **`Open-Finance-Lab/AgenticTrading`**
   - dashboard;
   - decision inspection;
   - valutazione delle run;
   - backend di backtest/paper execution.

5. **`OpenBB` + `Qlib`/`vectorbt`**
   - provider abstraction;
   - ricerca dati;
   - feature/indicatori;
   - backtesting quantitativo.

### Conclusione

La scelta migliore non è adottare un singolo repository, ma combinare:

> **`TradingAgents` per gli agenti + `mhsefidgar/...` per il risk boundary + `OpenBB` per i provider + il data layer SQLite/outbox già costruito in `trading-agent`.**

Questa combinazione è più vicina alla wiki di qualsiasi candidato singolo. In particolare, il differenziale del vostro progetto resta il **DB centrale con provenance, deduplica, outbox e indicatori materializzati**, che non ho trovato replicato insieme a una topologia multi-agent LangGraph completa.

### Sources:

- [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents)
- [Jiangge89/trading-agent](https://github.com/Jiangge89/trading-agent)
- [mhsefidgar/Multi-Agent-Quantitative-Trading-Research](https://github.com/mhsefidgar/Multi-Agent-Quantitative-Trading-Research)
- [ziyadal/multi-agent-trading-system](https://github.com/ziyadal/multi-agent-trading-system)
- [Open-Finance-Lab/AgenticTrading](https://github.com/Open-Finance-Lab/AgenticTrading)
- [mocasus/trade-agent](https://github.com/mocasus/trade-agent)
- [caalopezgo/quantlab](https://github.com/caalopezgo/quantlab)
- [virattt/ai-hedge-fund](https://github.com/virattt/ai-hedge-fund)
- [Microsoft Qlib](https://github.com/microsoft/qlib)
- [OpenBB](https://github.com/openbq-org/OpenBB)
- [VectorBT](https://github.com/polakowo/vectorbt)
- [Vibe-Trading](https://github.com/HKUDS/Vibe-Trading)
- [OpenAlice](https://github.com/TraderAlice/OpenAlice)
- [SilvioBaratto/optimizer](https://github.com/SilvioBaratto/optimizer)

result: Il miglior repository complessivo è `TauricResearch/TradingAgents`; il miglior approccio per il progetto è combinarlo con pattern di risk/execution da `mhsefidgar/...` e mantenere il data layer SQLite/outbox proprietario.
