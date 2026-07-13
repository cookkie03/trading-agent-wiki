---
title: "TradingAgents Code Wiki"
type: source
tags:
  - architecture
  - multi-agent
  - research
raw_source_path: "raw/articles/TradingAgents Code Wiki.md"
created: 2026-05-21
updated: 2026-05-21
status: active
confidence: high
related:
  - "[[prior-art/tradingagents/paper]]"
  - "[[system/foundation/architecture]]"
  - "[[system/agents/agents]]"
sources:
  - "https://codewiki.google/github.com/tauricresearch/tradingagents"
---

# TradingAgents Code Wiki

Documentazione tecnica auto-generata del codebase [tauricresearch/tradingagents](https://github.com/tauricresearch/tradingagents). Pubblicata il 2026-05-18. Complementa il [[prior-art/tradingagents/paper]] con dettagli implementativi.

---

## Struttura del codebase

```
tradingagents/
├── agents/
│   ├── analysts/        ← fundamentals, market, news, sentiment
│   ├── researchers/     ← bull_researcher, bear_researcher
│   ├── risk_mgmt/       ← aggressive, conservative, neutral debater
│   ├── managers/        ← research_manager, portfolio_manager
│   ├── trader/          ← trader_node
│   ├── schemas.py       ← Pydantic: ResearchPlan, TraderProposal, PortfolioDecision
│   └── utils/
│       ├── agent_states.py   ← TypedDict: AgentState, InvestDebateState, RiskDebateState
│       ├── memory.py         ← TradingMemoryLog (decision log + reflections)
│       └── structured.py     ← bind_structured + fallback a free-text
├── graph/
│   ├── trading_graph.py  ← TradingAgentsGraph (orchestratore centrale)
│   ├── setup.py          ← GraphSetup (costruisce il StateGraph)
│   ├── conditional_logic.py ← ConditionalLogic (routing dinamico tra nodi)
│   ├── propagation.py    ← Propagator (inizializza AgentState)
│   ├── checkpointer.py   ← SQLite per ticker, checkpoint/resume
│   ├── reflection.py     ← Reflector (LLM genera prose reflections sui trade)
│   └── signal_processing.py ← SignalProcessor (estrae rating dagli output)
├── dataflows/
│   ├── interface.py            ← hub centrale: routing verso vendor + fallback
│   ├── alpha_vantage*.py       ← stock, indicators, fundamentals, news
│   ├── y_finance.py            ← OHLCV, indicators, fundamentals, news
│   ├── reddit.py               ← fetch_reddit_posts
│   ├── stocktwits.py           ← fetch_stocktwits_messages
│   └── stockstats_utils.py     ← yf_retry, filter_financials_by_date, load_ohlcv
├── llm_clients/
│   ├── base_client.py          ← BaseLLMClient + normalize_content
│   ├── factory.py              ← create_llm_client (lazy loading per provider)
│   ├── capabilities.py         ← ModelCapabilities (tool_choice, json_mode, ecc.)
│   ├── model_catalog.py        ← MODEL_OPTIONS: quick/deep per provider
│   └── openai_client.py        ← include DeepSeekChatOpenAI (gestisce reasoning_content)
└── default_config.py           ← configurazione centralizzata, override via env vars
```

---

## Architettura: Orchestration e Graph

Il sistema usa **LangGraph** (`StateGraph`) per orchestrare il workflow. L'entry point principale è `TradingAgentsGraph.propagate(company_name, trade_date, asset_type)`.

Componenti chiave:
- **GraphSetup**: costruisce il grafo, definisce nodi (agenti) ed edges (condizionali)
- **ConditionalLogic**: decide il prossimo step basandosi sull'`AgentState` (continua debate vs. passa oltre)
- **Propagator**: inizializza l'`AgentState` con contesto, storico (da TradingMemoryLog), ticker
- **Checkpointer**: SQLite per-ticker, permette resume da ultimo step in caso di crash

---

## Agenti e Ruoli

| Categoria | Agente | Funzione |
|-----------|--------|----------|
| Analysts | `fundamentals_analyst` | Bilancio, cash flow, income statement via get_fundamentals / get_balance_sheet |
| Analysts | `market_analyst` | Selezione e calcolo indicatori tecnici (MACD, RSI, MA, Bollinger, ATR) |
| Analysts | `news_analyst` | News ticker-specific + macro via get_news / get_global_news |
| Analysts | `sentiment_analyst` | Reddit + StockTwits pre-fetched e iniettati nel prompt (non tool-calling) |
| Researchers | `bull_researcher` | Argomenti pro-investimento (debate) |
| Researchers | `bear_researcher` | Argomenti contro (debate) |
| Risk Mgmt | `aggressive_debator` | Prospettiva alto rischio/rendimento |
| Risk Mgmt | `conservative_debator` | Preservazione capitale |
| Risk Mgmt | `neutral_debator` | Bilanciamento aggressivo/conservativo |
| Managers | `research_manager` | Sintetizza debate → `ResearchPlan` (Pydantic) |
| Managers | `portfolio_manager` | Integra ResearchPlan + risk debate → `PortfolioDecision` |
| Trader | `trader_node` | Traduce PortfolioDecision → `TraderProposal` (action, entry, size) |

---

## Persistenza e Memoria

**LangGraph Checkpointing**:
- SQLite per-ticker in `tradingagents/graph/checkpointer.py`
- `get_checkpointer()` → context manager per `SqliteSaver`
- Funzioni: `has_checkpoint`, `checkpoint_step`, `clear_checkpoint`, `clear_all_checkpoints`

**TradingMemoryLog** (`tradingagents/agents/utils/memory.py`):
- Log Markdown append-only di decisioni, esiti e reflections
- `store_decision()` → salva trade pendente con idempotency guard
- `update_with_outcome()` → aggiorna con raw return, alpha return, holding days
- `get_past_context(n_same, n_cross)` → contesto storico per prompt LLM
- `_apply_rotation()` → pruning dei vecchi entry risolti (mantiene pending)
- `batch_update_with_outcomes()` → update multipli in atomic write

**Reflector** (`tradingagents/graph/reflection.py`):
- Dopo che l'esito di un trade è noto, genera prose reflection via LLM
- Focus: accuratezza della call direzionale, validità della tesi, lezioni apprese
- Stored nel TradingMemoryLog, poi recuperato via `get_past_context`

---

## Data Ingestion

**Hub centrale** (`dataflows/interface.py`):
- Mappa tool generici (get_stock_data, get_fundamentals, get_news) → vendor-specific
- Routing configurabile per vendor preferito + fallback automatico (es: AlphaVantageRateLimitError → yfinance)

**Provider supportati**:
- Alpha Vantage: OHLCV daily adjusted, technical indicators (SMA/MACD/RSI), fundamentals, news
- yfinance: OHLCV + caching, bulk indicator calculation, financials, insider transactions; retry mechanism (`yf_retry` con exponential backoff)
- Reddit: `fetch_reddit_posts` da subreddits specifici per ticker
- StockTwits: `fetch_stocktwits_messages` con sentiment bullish/bearish count

**[[_meta/glossario#Look-Ahead Bias|Look-Ahead Bias]] Prevention**:
- `_filter_reports_by_date` (alpha_vantage_fundamentals) → esclude report con `fiscalDateEnding > curr_date`
- `filter_financials_by_date` (stockstats_utils) → filtra colonne yfinance per data
- `load_ohlcv` → tronca OHLCV a `curr_date_dt`
- `get_global_news_yfinance` → filtra news con `publication_date > curr_date`

---

## LLM Integration

**Architettura client**:
- `BaseLLMClient` → interfaccia astratta con `get_llm()` e `validate_model()`
- `create_llm_client(provider, model)` → factory con lazy loading degli SDK
- `normalize_content()` → converte output strutturato in plain string
- Provider [[_meta/glossario#Adapter / Wrapper (broker)|wrapper]]: `NormalizedChatAnthropic`, `NormalizedChatOpenAI`, `NormalizedChatGoogleGenerativeAI`, `NormalizedAzureChatOpenAI`
- `DeepSeekChatOpenAI` → gestisce `reasoning_content` round-trip per thinking-mode

**ModelCapabilities** (capabilities.py): per ogni modello dichiara supporto per `tool_choice`, `json_mode`, `json_schema`, `reasoning_split`. Lookup: exact match → regex → default.

**Structured Output** (structured.py):
- `bind_structured(llm, schema)` → tenta `llm.with_structured_output(schema)`; se non supportato → `None`
- `invoke_structured_or_freetext(structured_llm, plain_llm, prompt)` → prova structured, fallback a free-text se eccezione

---

## Agent State Schemas

**TypedDict** (agent_states.py):
- `InvestDebateState` → history del debate bull/bear
- `RiskDebateState` → history del debate risk management
- `AgentState` → aggregato completo: company, asset_type, trade_date, reports (market/news/fundamentals/sentiment), debate histories, decision

**Pydantic** (schemas.py):
- `ResearchPlan` → output del research_manager (tesi + azioni strategiche)
- `TraderProposal` → output del trader (action: buy/sell/hold, entry, size)
- `PortfolioDecision` → output del portfolio_manager (rating + executive summary)
- `PortfolioRating`, `TraderAction` → Enum per categorical fields
