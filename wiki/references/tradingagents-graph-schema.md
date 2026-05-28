---
title: "TradingAgents — Schema completo grafo, nodi, agenti, tool, stato"
type: reference
tags:
  - reference
  - architecture
  - langgraph
  - agents
created: 2026-05-28
updated: 2026-05-28
status: active
related:
  - "[[tradingagents-code-wiki]]"
  - "[[system-map]]"
  - "[[trading-floor]]"
confidence: high
source: estrazione diretta da `tradingagents/` + graphify-out (2026-05-26)
---

# TradingAgents — Schema completo del grafo

Ricognizione esaustiva del grafo LangGraph implementato in `tradingagents/graph/` e degli agenti in `tradingagents/agents/`. Tutto ciò che segue è verificato leggendo direttamente il sorgente, non inferito.

> Entry point: `TradingAgentsGraph.propagate(company_name, trade_date, asset_type)` in [`tradingagents/graph/trading_graph.py`](../../../../Desktop/trading-agent/tradingagents/graph/trading_graph.py).
> Grafo LangGraph: `StateGraph(AgentState)` montato da `GraphSetup.setup_graph()` in [`setup.py`](../../../../Desktop/trading-agent/tradingagents/graph/setup.py).

Artifact visuale collegato: [[tradingagents-graph.canvas]]

---

## 1. Pipeline lineare ad alto livello

```
START
  → [Analyst chain]  (market → sentiment → news → fundamentals, selezionabile)
  → Bull Researcher ⇄ Bear Researcher   (max_debate_rounds)
  → Research Manager                    (deep LLM, ResearchPlan strutturato)
  → Trader                              (TraderProposal strutturato)
  → Aggressive → Conservative → Neutral (round robin, max_risk_discuss_rounds)
  → Portfolio Manager                   (deep LLM, PortfolioDecision strutturato)
  → END
  → SignalProcessor.process_signal()    (parse rating finale)
  → TradingMemoryLog.store_decision()   (log decisione + reflection differita)
```

Reflection è **differita**: al run successivo sullo stesso ticker, `Reflector.reflect_on_final_decision()` valuta l'esito (raw return + alpha vs benchmark) e aggiorna il memory log via `batch_update_with_outcomes()`.

---

## 2. Stato globale — `AgentState`

Definito in [`tradingagents/agents/utils/agent_states.py`](../../../../Desktop/trading-agent/tradingagents/agents/utils/agent_states.py). Estende `langgraph.graph.MessagesState`.

### Campi principali (`AgentState`)

| Campo | Tipo | Scritto da | Letto da |
|---|---|---|---|
| `messages` | list[BaseMessage] | tutti gli analyst + tool nodes | tutti |
| `company_of_interest` | str | `Propagator.create_initial_state` | tutti |
| `asset_type` | str (`"stock"`/`"crypto"`) | `Propagator.create_initial_state` | tutti (instrument context) |
| `trade_date` | str | `Propagator.create_initial_state` | tutti |
| `sender` | str | ogni agente al termine | logging / debug |
| `market_report` | str | Market Analyst | Bull/Bear, Research Manager, Trader, Risk team, PM |
| `sentiment_report` | str | Sentiment Analyst | Bull/Bear, Research Manager, Trader, Risk team, PM |
| `news_report` | str | News Analyst | Bull/Bear, Research Manager, Trader, Risk team, PM |
| `fundamentals_report` | str | Fundamentals Analyst | Bull/Bear, Research Manager, Trader, Risk team, PM |
| `investment_debate_state` | `InvestDebateState` | Bull, Bear, Research Manager | tutti dopo |
| `investment_plan` | str (markdown da `ResearchPlan`) | Research Manager | Trader, Risk team, PM |
| `trader_investment_plan` | str (markdown da `TraderProposal`) | Trader | Risk team, PM |
| `risk_debate_state` | `RiskDebateState` | Aggressive/Conservative/Neutral, PM | tutti dopo |
| `final_trade_decision` | str (markdown da `PortfolioDecision`) | Portfolio Manager | SignalProcessor, memory log |
| `past_context` | str | injection in `_run_graph` (da memory log) | Portfolio Manager |

### Sotto-stato `InvestDebateState`

`bull_history`, `bear_history`, `history`, `current_response`, `judge_decision`, `count`.

### Sotto-stato `RiskDebateState`

`aggressive_history`, `conservative_history`, `neutral_history`, `history`, `latest_speaker`, `current_aggressive_response`, `current_conservative_response`, `current_neutral_response`, `judge_decision`, `count`.

---

## 3. Nodi del grafo (label LangGraph)

Registrati in `GraphSetup.setup_graph` ([`setup.py:69-86`](../../../../Desktop/trading-agent/tradingagents/graph/setup.py)). Per ogni analyst attivo vengono creati 3 nodi: agente, tool, message-clear.

### Nodi analisti (per ogni `selected_analyst`)

Da `ANALYST_NODE_SPECS` in [`analyst_execution.py`](../../../../Desktop/trading-agent/tradingagents/graph/analyst_execution.py):

| Key | `agent_node` | `tool_node` | `clear_node` | `report_key` |
|---|---|---|---|---|
| `market` | `Market Analyst` | `tools_market` | `Msg Clear Market` | `market_report` |
| `social` | `Sentiment Analyst` | `tools_social` | `Msg Clear Sentiment` | `sentiment_report` |
| `news` | `News Analyst` | `tools_news` | `Msg Clear News` | `news_report` |
| `fundamentals` | `Fundamentals Analyst` | `tools_fundamentals` | `Msg Clear Fundamentals` | `fundamentals_report` |

> La key `social` resta come wire value per back-compat (saved configs), ma l'agente è `Sentiment Analyst` dalla v0.2.5 (ingest news + StockTwits + Reddit).

### Nodi fissi

- `Bull Researcher`
- `Bear Researcher`
- `Research Manager`  ⟵ deep LLM
- `Trader`
- `Aggressive Analyst`
- `Conservative Analyst`
- `Neutral Analyst`
- `Portfolio Manager`  ⟵ deep LLM

### Edge condizionali

| Da | Funzione `ConditionalLogic` | Destinazioni |
|---|---|---|
| `<Analyst>` | `should_continue_<key>` | `tools_<key>` se `tool_calls`, altrimenti `Msg Clear <Label>` |
| `Bull Researcher` | `should_continue_debate` | `Bear Researcher` o `Research Manager` (≥ `2 * max_debate_rounds`) |
| `Bear Researcher` | `should_continue_debate` | `Bull Researcher` o `Research Manager` |
| `Aggressive Analyst` | `should_continue_risk_analysis` | `Conservative Analyst` o `Portfolio Manager` (≥ `3 * max_risk_discuss_rounds`) |
| `Conservative Analyst` | `should_continue_risk_analysis` | `Neutral Analyst` o `Portfolio Manager` |
| `Neutral Analyst` | `should_continue_risk_analysis` | `Aggressive Analyst` o `Portfolio Manager` |

### Edge lineari

- `START → <primo analyst>`
- per ogni coppia consecutiva di analyst: `clear_node_i → agent_node_{i+1}`
- ultimo `clear_node → Bull Researcher`
- `Research Manager → Trader`
- `Trader → Aggressive Analyst`
- `Portfolio Manager → END`

---

## 4. Agenti — factory e responsabilità

Tutti i factory sono importati in [`tradingagents/agents/__init__.py`](../../../../Desktop/trading-agent/tradingagents/agents/__init__.py).

| Agente | Factory | LLM | Output di stato | Output strutturato |
|---|---|---|---|---|
| Market Analyst | `create_market_analyst` | quick | `market_report`, `messages`, `sender` | — (prosa) |
| Sentiment Analyst | `create_sentiment_analyst` (alias deprecato `create_social_media_analyst`) | quick | `sentiment_report`, `messages`, `sender` | — |
| News Analyst | `create_news_analyst` | quick | `news_report`, `messages`, `sender` | — |
| Fundamentals Analyst | `create_fundamentals_analyst` | quick | `fundamentals_report`, `messages`, `sender` | — |
| Bull Researcher | `create_bull_researcher` | quick | `investment_debate_state` aggiornato | — |
| Bear Researcher | `create_bear_researcher` | quick | `investment_debate_state` aggiornato | — |
| Research Manager | `create_research_manager` | **deep** | `investment_plan`, `investment_debate_state.judge_decision` | `ResearchPlan` |
| Trader | `create_trader` | quick | `trader_investment_plan`, `messages`, `sender` | `TraderProposal` |
| Aggressive Analyst | `create_aggressive_debator` | quick | `risk_debate_state` aggiornato | — |
| Conservative Analyst | `create_conservative_debator` | quick | `risk_debate_state` aggiornato | — |
| Neutral Analyst | `create_neutral_debator` | quick | `risk_debate_state` aggiornato | — |
| Portfolio Manager | `create_portfolio_manager` | **deep** | `final_trade_decision`, `risk_debate_state.judge_decision` | `PortfolioDecision` |

I message-clear node sono creati da `create_msg_delete()` in [`agent_utils.py`](../../../../Desktop/trading-agent/tradingagents/agents/utils/agent_utils.py): rimuovono tutti i `messages` e iniettano un placeholder `HumanMessage("Continue")` per compatibilità Anthropic.

---

## 5. Schemi strutturati (`tradingagents/agents/schemas.py`)

| Schema | Prodotto da | Campi |
|---|---|---|
| `PortfolioRating` (Enum) | RM, PM | `Buy / Overweight / Hold / Underweight / Sell` |
| `TraderAction` (Enum) | Trader | `Buy / Hold / Sell` |
| `ResearchPlan` | Research Manager | `recommendation: PortfolioRating`, `rationale: str`, `strategic_actions: str` |
| `TraderProposal` | Trader | `action: TraderAction`, `reasoning: str`, `entry_price?: float`, `stop_loss?: float`, `position_sizing?: str` |
| `PortfolioDecision` | Portfolio Manager | `rating: PortfolioRating`, `executive_summary: str`, `investment_thesis: str`, `price_target?: float`, `time_horizon?: str` |

Render helper: `render_research_plan`, `render_trader_proposal`, `render_pm_decision` riconvertono in markdown per memory log, CLI, report salvati.

---

## 6. Tool — `ToolNode` e funzioni

`TradingAgentsGraph._create_tool_nodes()` in [`trading_graph.py:158-192`](../../../../Desktop/trading-agent/tradingagents/graph/trading_graph.py):

| Tool node | Tool LangChain (`@tool`) | Modulo |
|---|---|---|
| `tools_market` | `get_stock_data`, `get_indicators` | `core_stock_tools`, `technical_indicators_tools` |
| `tools_social` | `get_news` | `news_data_tools` |
| `tools_news` | `get_news`, `get_global_news`, `get_insider_transactions` | `news_data_tools` |
| `tools_fundamentals` | `get_fundamentals`, `get_balance_sheet`, `get_cashflow`, `get_income_statement` | `fundamental_data_tools` |

Tutti i tool delegano al **dataflows layer** ([`tradingagents/dataflows/`](../../../../Desktop/trading-agent/tradingagents/dataflows/)) che instrada al vendor scelto in `config["data_vendors"]` (default `yfinance`, alternativa `alpha_vantage`) con override per-tool in `config["tool_vendors"]`.

### Moduli dataflows

`alpha_vantage.py`, `alpha_vantage_common.py`, `alpha_vantage_news.py`, `alpha_vantage_stock.py`, `alpha_vantage_fundamentals.py`, `alpha_vantage_indicator.py`, `y_finance.py`, `yfinance_news.py`, `reddit.py`, `stocktwits.py`, `stockstats_utils.py`, `interface.py`, `config.py`, `utils.py`.

---

## 7. Componenti di supporto

| Componente | File | Ruolo |
|---|---|---|
| `Propagator` | `graph/propagation.py` | Costruisce stato iniziale, args di `graph.invoke` (`recursion_limit`, `stream_mode`) |
| `ConditionalLogic` | `graph/conditional_logic.py` | 6 funzioni di branching (4 analyst + debate + risk) |
| `GraphSetup` | `graph/setup.py` | Wiring nodi/edge della `StateGraph` |
| `Reflector` | `graph/reflection.py` | Genera reflection 2-4 frasi con `raw_return` + `alpha_return` vs benchmark |
| `SignalProcessor` | `graph/signal_processing.py` | Estrae rating finale (deterministico, no LLM) via `parse_rating` |
| `TradingMemoryLog` | `agents/utils/memory.py` | Persistenza decisioni + outcome; `get_past_context()` inietta lezioni nel PM |
| `TradingAgentsGraph` | `graph/trading_graph.py` | Orchestratore: build LLM client, tool node, compile, propagate |
| Checkpointer | `graph/checkpointer.py` | SqliteSaver per ticker quando `checkpoint_enabled=True` (resume per-step) |
| LLM clients | `tradingagents/llm_clients/` | Factory + adapter per OpenAI, Anthropic, Google, Azure, MiniMax, DeepSeek, Ollama |

### LLM clients disponibili

`openai_client.py`, `anthropic_client.py`, `google_client.py`, `azure_client.py`, più: `base_client.py`, `factory.py` (`create_llm_client`), `model_catalog.py`, `capabilities.py`, `api_key_env.py`, `validators.py`.

Kwargs provider-specifici (`_get_provider_kwargs`): `thinking_level` (Google), `reasoning_effort` (OpenAI), `effort` (Anthropic).

---

## 8. Configurazione — `DEFAULT_CONFIG`

[`tradingagents/default_config.py`](../../../../Desktop/trading-agent/tradingagents/default_config.py). Override via env var `TRADINGAGENTS_*`.

### Chiavi di runtime

- **LLM**: `llm_provider` (default `openai`), `deep_think_llm` (`gpt-5.4`), `quick_think_llm` (`gpt-5.4-mini`), `backend_url`
- **Thinking**: `google_thinking_level`, `openai_reasoning_effort`, `anthropic_effort`
- **Debate**: `max_debate_rounds=1`, `max_risk_discuss_rounds=1`, `max_recur_limit=100`, `analyst_concurrency_limit=1`
- **Checkpoint**: `checkpoint_enabled=False`
- **Output**: `output_language="English"` (controlla `get_language_instruction()` in `agent_utils`)
- **Paths**: `results_dir`, `data_cache_dir`, `memory_log_path` (sotto `~/.tradingagents/`)
- **Memory**: `memory_log_max_entries`
- **News**: `news_article_limit=20`, `global_news_article_limit=10`, `global_news_lookback_days=7`, `global_news_queries` (5 query macro default)
- **Vendor routing**: `data_vendors` per categoria + `tool_vendors` override per-tool
- **Benchmark**: `benchmark_ticker` (override globale) + `benchmark_map` per suffisso exchange (`.NS→^NSEI`, `.T→^N225`, `.HK→^HSI`, `.L→^FTSE`, `.TO→^GSPTSE`, `.AX→^AXJO`, `""→SPY`)

### Env var overrides (`_ENV_OVERRIDES`)

`TRADINGAGENTS_LLM_PROVIDER`, `*_DEEP_THINK_LLM`, `*_QUICK_THINK_LLM`, `*_LLM_BACKEND_URL`, `*_OUTPUT_LANGUAGE`, `*_MAX_DEBATE_ROUNDS`, `*_MAX_RISK_ROUNDS`, `*_CHECKPOINT_ENABLED`, `*_BENCHMARK_TICKER`, più `*_RESULTS_DIR`, `*_CACHE_DIR`, `*_MEMORY_LOG_PATH`.

---

## 9. Report — output su disco

### Layout `reports/<TICKER>_<TIMESTAMP>/`

```
reports/MONC.MI_20260526_162528/
├── 1_analysts/
│   ├── market.md          ← market_report
│   ├── sentiment.md       ← sentiment_report
│   ├── news.md            ← news_report
│   └── fundamentals.md    ← fundamentals_report
├── 2_research/
│   ├── bull.md            ← investment_debate_state.bull_history
│   ├── bear.md            ← investment_debate_state.bear_history
│   └── manager.md         ← investment_plan (rendered ResearchPlan)
├── 3_trading/
│   └── trader.md          ← trader_investment_plan (rendered TraderProposal)
├── 4_risk/
│   ├── aggressive.md      ← risk_debate_state.aggressive_history
│   ├── conservative.md    ← risk_debate_state.conservative_history
│   └── neutral.md         ← risk_debate_state.neutral_history
├── 5_portfolio/
│   └── decision.md        ← final_trade_decision (rendered PortfolioDecision)
├── complete_report.md
└── complete_report_it.md  (se output_language="Italian")
```

### Log di stato

`TradingAgentsGraph._log_state` scrive `~/.tradingagents/logs/<safe_ticker>/TradingAgentsStrategy_logs/full_states_log_<trade_date>.json` con l'intero `AgentState` finale.

### Memory log

`memory_log_path` (default `~/.tradingagents/memory/trading_memory.md`). Gestito da `TradingMemoryLog`:
- `store_decision()` registra decisione come **pending**
- al run successivo same-ticker: `_resolve_pending_entries()` chiama `_fetch_returns()` (yfinance per ticker + benchmark), `Reflector.reflect_on_final_decision()`, `batch_update_with_outcomes()`
- `get_past_context(ticker)` viene iniettato in `AgentState.past_context` letto dal Portfolio Manager

### Graphify artefatti

`graphify-out/` contiene un grafo precedente (2026-05-26, 1192 nodi · 818 edge · 610 community): `GRAPH_REPORT.md`, `graph.html`, `graph.json`, `manifest.json`, `cost.json`, label semantiche.

---

## 10. CLI

[`cli/`](../../../../Desktop/trading-agent/cli/). Entry point `main.py`. Auto-detect `asset_type` dal ticker (suffisso `-USD` → crypto). Cartella `cli/static/` contiene asset UI; `assets/cli/` documentazione.

---

## 11. Mappa file → ruolo (sintetica)

```
tradingagents/
├── default_config.py            # DEFAULT_CONFIG + env override
├── agents/
│   ├── __init__.py              # re-export factory
│   ├── schemas.py               # Pydantic + Enum + render helper
│   ├── analysts/                # market / sentiment / news / fundamentals
│   ├── researchers/             # bull / bear
│   ├── managers/                # research_manager / portfolio_manager
│   ├── risk_mgmt/               # aggressive / conservative / neutral
│   ├── trader/                  # trader
│   └── utils/
│       ├── agent_states.py      # AgentState, InvestDebateState, RiskDebateState
│       ├── agent_utils.py       # language/instrument context, msg delete
│       ├── memory.py            # TradingMemoryLog
│       ├── rating.py            # parse_rating deterministico
│       ├── structured.py        # helper structured output
│       ├── core_stock_tools.py
│       ├── technical_indicators_tools.py
│       ├── fundamental_data_tools.py
│       └── news_data_tools.py
├── graph/
│   ├── trading_graph.py         # TradingAgentsGraph orchestrator
│   ├── setup.py                 # GraphSetup
│   ├── propagation.py           # Propagator
│   ├── conditional_logic.py     # ConditionalLogic
│   ├── analyst_execution.py     # ANALYST_NODE_SPECS, plan, tracker
│   ├── reflection.py            # Reflector
│   ├── signal_processing.py     # SignalProcessor
│   └── checkpointer.py          # SqliteSaver wrapper
├── dataflows/                   # vendor adapter (alpha_vantage, yfinance, reddit, stocktwits)
└── llm_clients/                 # factory + adapter per provider
```

---

## 12. Numeri grafify (run 2026-05-26)

- 135 file · ~344k parole
- 1192 nodi · 818 edge · 610 community
- Estrazione 83% EXTRACTED, 17% INFERRED, 0% AMBIGUOUS
- Token cost: 0 (run con LLM fallback)

Vedere [`graphify-out/GRAPH_REPORT.md`](../../../../Desktop/trading-agent/graphify-out/GRAPH_REPORT.md) per la lista completa di community hubs (Portfolio Management & Graph Execution, Analyst Sub-Agents, Multi-Provider LLM Support, ecc.).
