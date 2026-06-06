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

## Sintesi
La spina dorsale del canvas è rispettata: **DB a 4 aree**, **desk → PM → Risk → Investment State → Trade**, e soprattutto **gli agenti chiamano l'Extractors set da soli** (tool-calling LLM-driven) che scrive nel DB. Restano 🔴 minori: tabelle dati FX/insider/calendario/report, adaptive extractor (rate-limit), Market Alert/calendar trigger.
