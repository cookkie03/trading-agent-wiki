---
title: "Canvas → Codice — mappa di allineamento"
type: synthesis
tags:
  - architecture
  - software
created: 2026-06-07
updated: 2026-06-07
status: active
related:
  - "[[artifacts/architettura.canvas]]"
  - "[[system/fork-gap-analysis]]"
  - "[[system/modules/agents]]"
  - "[[system/modules/data-layer]]"
confidence: high
area: software
---

# Canvas → Codice — mappa di allineamento

> Verifica che l'architettura del codice (`/Users/luca/Desktop/trading-agent`, branch `feat/rebuild`) rispetti `architettura.canvas`. ✅ = implementato · 🟡 = parziale · 🔴 = da fare.

## DB (gruppo) → `tradingagents/storage/`
| Canvas | Codice | |
|--------|--------|--|
| market · prezzi di mercato | `price_bars` | ✅ |
| market · indicatori macro | `macro_points` | ✅ |
| market · news | `news_items` | ✅ |
| market · insider trading | — | 🔴 |
| market · calendario economico | — | 🔴 |
| market · tassi di cambio (FX) | — | 🔴 |
| (sentiment social) | `social_posts` | ✅ |
| (fondamentali) | `fundamental_snapshots` | ✅ |
| technical · states | `research_states` | ✅ |
| technical · log | `decision_log` | ✅ |
| technical · transactions | `trades` | ✅ |
| technical · report | — | 🔴 |
| rendicontazione · liquidità/distribuzione/P&L | `portfolio_snapshots` | ✅ |
| costituzione (Statuto) | `charter` | ✅ |
| (scheda ticker / funnel) | `ticker_card` | ✅ |

## Extraction
| Canvas | Codice | |
|--------|--------|--|
| Extractors set (estrai/calcola/immetti) | `ingestion/` + `brain/tooling.py` (tool per-agente) | ✅ |
| `<agent> → Extractors set → DB` (chiamata autonoma) | tool-calling LLM-driven in `brain/llm.py` + `graph.py` | ✅ |
| Warm start: state vuoto → extractor pre-lanciati → 1° contesto iniettato | `brain/warmup.py` (in `analyze_symbol`) | ✅ |
| Context state per-agente (finestra cucita ad hoc, automantenuta nel task) | `brain/agent_context.py` (in `BrainState.contexts`) | ✅ |
| Deduplicazione uniforme di OGNI info salvata | per-famiglia (check-presenza/dedup_key) | 🟡 da rendere sistematica |
| mantainer (technical → rendicontazione) | `execution/mantainer.py` | ✅ |
| Adaptive extractor (rate-limit/frequenza) | — | 🔴 |
| Market Alert / calendar tool → calendario | — | 🔴 |

## Desk (workflow) → `tradingagents/brain/`
| Canvas | Codice | |
|--------|--------|--|
| Analyst Research (Market + Sentiment) | nodi `market`, `sentiment` | ✅ |
| Analyst Technical (Tecnical + Fondamentali) | nodi `technical`, `fundamental` | ✅ |
| Risk Analyst (statuto, bear) | nodo `risk` + `domain/risk.check_guardrails` | ✅ |
| catena desk → Risk → Investment State | edge del `StateGraph` | ✅ |
| ogni agente ha i suoi tool e li chiama | `build_desk_tools` per agente | ✅ |

## Orchestrazione & esecuzione
| Canvas | Codice | |
|--------|--------|--|
| Portfolio manager (CEO) orchestratore | nodo `pm` + `orchestration/` | ✅ (PM autonomo; override umano = futuro) |
| alert → PM | `orchestration/triggers.price_alerts` | ✅ |
| state periodical synthesis → PM | `app.run_forever` (tick) | ✅ |
| calendario economico → alert | — | 🔴 |
| Investment State (gate completezza) | `ResearchState.is_complete` / `seal()` | ✅ |
| Trade (deterministico) | `execution/trade.py` | ✅ |
| Trade → transactions | `trades` (broker + reconcile) | ✅ |
| Broker intercambiabile (paper · Alpaca · IBKR) | `broker/` (PaperBroker · `alpaca.py` · `ibkr.py` TWS via ib_async) | ✅ |
| Configurazione (broker paper/live, modelli, rischio, Statuto, …) | `config.toml` + `config.py` (fonte unica; `.env` = segreti) | ✅ |
| Universo investibile (catalogo broker, riconciliato) | `universe/` (`list_assets`, `sync_universe`) + `instruments` flags | ✅ |
| Watchlist dinamica (working set, membership ibrida) | `ticker_card.in_watchlist` + `seed_watchlist`/`_admit_watchlist` | ✅ |
| Date asset → trigger automatici (auto-scheduling) | `ticker_events` + `event_checkpoints` | ✅ |
| Benchmark da battere (dinamico) | `benchmark.py` + `performance.py` (`[benchmark] symbols`) | ✅ |
| PM = Direttore (cosa analizzare, fan-out, Statuto portafoglio) | `brain/director.py` + `admit_within_statute` | ✅ |
| Valutatore per-ticker (parallelo) | `analyze_batch` → `brain/graph.py` per simbolo | ✅ |

## Sintesi
La spina dorsale del canvas è rispettata: **DB a 4 aree**, **desk → PM → Risk → Investment State → Trade**, e soprattutto **gli agenti chiamano l'Extractors set da soli** (tool-calling LLM-driven) che scrive nel DB. Restano 🔴 minori: tabelle dati FX/insider/calendario/report, adaptive extractor (rate-limit), Market Alert/calendar trigger.

---
## Commenti recuperati da iCloud (2026-07-01)

> Commenti Obsidian `%%...%%` presenti nella vecchia copia iCloud (`7054827`) e reinseriti senza sovrascrivere il contenuto corrente.

%%il ruolo di questo file code mapping è fondamentale per me per capire come leggere il codice, scrivimelo da qualche parte, dopodiché considera che tutta questa cosa è proprio una delle parti che voglio rifare e prestabilire per costruire un codice estremamente personalizzato%%

