---
title: "Fork Gap Analysis — TradingAgents fork ↔ il nostro design"
type: synthesis
tags:
  - architecture
  - multi-agent
  - infrastructure
created: 2026-06-06
updated: 2026-06-06
status: active
related:
  - "[[system/modules/agents]]"
  - "[[system/system-prompts]]"
  - "[[system/parallelism-design]]"
  - "[[system/state-schemas]]"
  - "[[system/modules/data-layer]]"
  - "[[system/modules/execution]]"
  - "[[prior-art/tradingagents/code-wiki]]"
confidence: high
area: software
---

# Fork Gap Analysis — TradingAgents fork ↔ il nostro design

> **Ponte design → codice.** Confronto tra il fork già presente in `/Users/luca/Desktop/trading-agent` (repo `cookkie03/trading-agent`, un fork vivo di TradingAgents che già produce decisioni reali — report NVDA, MONC.MI) e le decisioni di design prese nel wiki. Mappa **tengo / elimino-semplifico / aggiungo** + roadmap ordinata dei milestone di codice. Riferimenti a file reali del fork.

## TL;DR
Il fork copre **gran parte dell'impianto**: 4 analisti, PM, grafo LangGraph, tool (inclusi Reddit/StockTwits), structured output, multi-provider, quick/deep think, checkpoint. **Non serve altra progettazione astratta.** Il lavoro è **adattare il fork** al nostro design su pochi assi precisi, più **costruire ciò che il fork non ha** (DB, esecuzione su broker, logica di rischio nostra, funnel multi-ticker).

---

## Già allineato — vittorie gratis (decisioni nostre già implementate)
- **Quick Thinker / Deep Thinker**: `quick_think_llm` vs `deep_think_llm` in `default_config.py` → il pattern dello screening (E) ha già il primitivo.
- **Lingua prompt = inglese**: `output_language` default English, *"internal agent debate stays in English for reasoning quality"* → identico alla nostra decisione 2026-06-06.
- **Checkpoint / graceful resume**: `graph/checkpointer.py` + `checkpoint_enabled` → parte del nostro graceful shutdown già lì.
- **Astrazione vendor**: `data_vendors` / `tool_vendors` in config + `dataflows/interface.py` (`route_to_vendor`) → il nostro principio "vendor intercambiabili".
- **Fonti sentiment social**: `dataflows/reddit.py` + `dataflows/stocktwits.py` → proprio le fonti che Luca voleva per il Sentiment (famiglia D di [[system/tools-inventory]]).
- **Structured output JSON strict**: `agents/utils/structured.py` + `agents/schemas.py` + test → il nostro contratto output.
- **Memory / past_context**: campo `past_context` nello state + `memory_log_path` → il nostro `past_context` del [[system/state-schemas]].

---

## TENGO (riuso quasi diretto)

| Nostro design | Nel fork | Nota |
|---------------|----------|------|
| Tool prezzi/indicatori/news/fondamentali | `agents/utils/*_tools.py`: `get_stock_data`, `get_indicators`, `get_news`, `get_global_news`, `get_insider_transactions`, `get_fundamentals`, `get_balance_sheet`, `get_cashflow`, `get_income_statement` | mappano sull'inventario [[system/tools-inventory]] |
| Vendor dati | `dataflows/`: alpha_vantage, yfinance, stockstats, reddit, stocktwits | + routing per categoria |
| Grafo LangGraph | `graph/`: `setup.py`, `trading_graph.py`, `conditional_logic.py`, `propagation.py` | da ricablare (vedi sotto) |
| Structured output | `agents/utils/structured.py`, `agents/schemas.py` | adattare gli schemi ai nostri campi |
| Multi-provider LLM | `llm_clients/factory.py` (OpenAI/Anthropic/Google/Azure) | OpenRouter via client OpenAI-compatible + `backend_url` |

---

## ELIMINO / SEMPLIFICO

| Nel fork | Cosa farne | Perché |
|----------|-----------|--------|
| `agents/researchers/bull_researcher.py` + `bear_researcher.py` + `managers/research_manager.py` | **Eliminare** | Decisione 2026-05-26: bull/bear eliminati, Head of Analyst eliminato |
| `agents/risk_mgmt/aggressive_debator.py` + `conservative_debator.py` + `neutral_debator.py` | **Collassare in un Risk Analyst gate singolo** | Decisione 2026-05-29: gate bear unico, non un debate a 3 |
| `agents/trader/trader.py` (nodo LLM) | **Sostituire con funzione Python deterministica** | Decisione 2026-05-29: Trader = funzione, non agente |
| 4 analisti **in sequenza** (market→social→news→fundamentals) | **Rimappare sui 2 desk** (Research = Market+Sentiment; Technical = Technical+Fondamentali) | [[system/agent-behaviors]] |
| `InvestDebateState` + `RiskDebateState` (state da debate) | **Rimuovere**, sostituire con il nostro `research_state` strutturato | [[system/state-schemas]] |

> **Differenza strutturale chiave del grafo**: nel fork il flusso è una **pipeline** (analisti → debate ricerca → Trader → debate rischio → **PM come giudice finale**, poi END — vedi `graph/setup.py`). Nel nostro design il **PM è l'orchestratore in cima** (CEO che chiama i desk come tool, *"nel dubbio chiedi sempre"*, aggrega e decide), e il Risk è un **gate** prima del Trade deterministico. → `graph/setup.py` va **riscritto** sulla nostra topologia ([[system/modules/agents]] + [[system/parallelism-design]]).

---

## AGGIUNGO (il fork non ce l'ha)

| Manca | Cosa costruire | Riferimento |
|-------|----------------|-------------|
| **DB centrale** | Il fork è **file/cache-based** (`data_cache_dir`, `results_dir`, `memory_log_path`). Costruire il DB-first: PostgreSQL+TimescaleDB, 4 aree (rendicontazione/market_data/charter/logs) + **scheda ticker** | [[system/modules/data-layer]] · [[system/db-access-performance]] |
| **Esecuzione su broker** | Il fork **produce report, non esegue**. Aggiungere adapter Alpaca (MVP) / IBKR + paper trading | [[system/modules/execution]] |
| **Logica di rischio nostra** | Sizing risk-based, backbone **ATR** per entry/stop/tp, Statuto (guardrail deterministici), leva-via-opzioni | [[system/position-sizing]] · [[system/state-schemas]] |
| **Funnel multi-ticker** | Il fork analizza **un ticker per run** (CLI). Aggiungere screening (E) + coda (D) + subgraph per-ticker (A) + scheda (B/C) | [[system/parallelism-design]] |
| **Conviction enum nostro** | Fork usa `PortfolioRating` (Buy/Overweight/Hold/Underweight/Sell). Rimappare su `Strong Buy/Buy/Hold/Sell/Strong Sell` | [[system/rating-scoring]] |
| **Trigger autonomi** | Alert prezzo + periodical synthesis + `next_check_date`. Il fork parte da CLI manuale | [[system/modules/agents]] |
| **System prompt nostri** | Sostituire i prompt del fork con i 6 nostri | [[system/system-prompts]] |
| **OpenRouter + DeepSeek** | Config lo supporta (`llm_provider`, `backend_url`); da impostare | [[system/stack]] |

---

## Roadmap proposta dei milestone di codice (alpha-first)

Ogni milestone lascia un sistema che gira. Ordine pensato per **validare presto** e ridurre rischio:

- **M0 — Wiring & validazione** (~1 sessione): impostare OpenRouter + DeepSeek (`.env`, config) e far girare il fork **as-is** su un ticker, per confermare che funziona per noi. Quick win, nessuna modifica strutturale.
- **M1 — Grafo "nostro"**: snellire (rimuovere bull/bear + research_manager, collassare risk debate → Risk gate singolo), rimappare i 4 analisti sui **2 desk**, mettere il **PM come orchestratore**, sostituire i **system prompt** con i nostri. Output ancora file-based, single-ticker.
- **M2 — DB layer**: schema concreto 4 aree + **scheda ticker**, persistere gli output, DB-first. È il "ponte" già individuato.
- **M3 — Rischio & Trade deterministico**: Trader Python, sizing risk-based, entry/stop/tp ATR, guardrail Statuto.
- **M4 — Esecuzione**: adapter broker (Alpaca paper) + flusso ordini.
- **M5 — Funnel multi-ticker**: screening (E) + coda (D) + subgraph per-ticker (A) + scheda (B/C).
- **M6+**: leva opzioni, learning loop/backtesting validatore, trigger autonomi completi.

> L'ordine M0→M2 è il punto delicato: si può anche fare il DB **prima** di snellire il grafo. Proposta: prima snellire (M1) perché definisce *cosa* persistere, poi DB (M2). Da confermare con Luca.

## Punto aperto
- **Ordine M1 vs M2** (snellire-grafo-prima vs DB-prima) — da confermare.
- Verificare il dettaglio di `graph/trading_graph.py`, `propagation.py`, `analyst_execution.py` prima di toccare la topologia.
