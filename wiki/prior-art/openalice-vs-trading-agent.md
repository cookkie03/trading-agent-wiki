---
title: OpenAlice vs Trading Agent — cosa copre delle nostre idee
type: synthesis
tags:
  - prior-art
  - architecture
  - decision-support
created: 2026-11-18T00:00:00.000Z
updated: 2026-11-18T00:00:00.000Z
status: active
confidence: medium
related:
  - '[[prior-art/libraries/openalice]]'
  - '[[system/agents/agent-tools]]'
  - '[[system/foundation/decision-log]]'
---

# OpenAlice vs Trading Agent

Confronto per decidere se partire da un fork di [[prior-art/libraries/openalice|OpenAlice]]. Fonti: README e `docs/` del repo clonato il 2026-11-18 (ultimo commit 2026-11-09), non un'esecuzione dell'app. ✅ c'è · 🟡 parziale o da adattare · ❌ assente.

## Il progetto in numeri

TypeScript, monorepo pnpm/turbo, circa 490k righe in 2.844 file `.ts/.tsx` · AGPL-3.0 · 7,4k stelle, push quasi quotidiani · trading (UTA) dichiarato **beta** · stato su file (`~/.openalice`), niente DB · il loop LLM non è suo: ospita CLI native (Claude Code, Codex, Pi, OpenCode…).

## Copertura delle nostre decisioni

| Nostra idea | OpenAlice | |
|---|---|---|
| Sei agenti con ruoli fissi | Sessioni generiche ("coworker") in Workspace; nessun ruolo predefinito. I ruoli si emulano con template, `AGENTS.md` e skill. | 🟡 |
| Messaggi alla pari tra agenti | `conversation ask` a una Sessione precisa, risposte da Inbox, commenti sugli Issue. Mancano chat per ticker o tema e il recapito sul settore. | 🟡 |
| PM orchestratore, Ciclo di analisi Alert → decisione | Nessun concetto di ciclo né di decisore: l'orchestrazione sarebbe affidata ai prompt, quindi non deterministica. | ❌ |
| Budget del ciclo, Rimando deterministico | Solo `timeout` per run; niente budget di messaggi né esito di default. | ❌ |
| Trigger engine: `next_check_date`, alert di prezzo, trimestrali | Schedule `at`/`every`/`cron`, webhook `POST /headless`, skill di auto-scheduling. Niente alert di prezzo nativi: servirebbe un monitor esterno via webhook. | 🟡 |
| Alert ripetuti: fusione o messaggio | Un Issue non ha run concorrenti; manca la logica di fusione. | ❌ |
| State strutturato + `fill_state`/`suggest_state` | Markdown e file liberi; nessuno state tipizzato per ticker. | ❌ |
| Bozza dell'ordine deterministica (coefficienti ATR) | L'agente scrive prezzi e quantità direttamente in `placeOrder`. Servirebbe un tool custom (TS + Zod). | ❌ |
| Risk Gate deterministico | Guard al push (`max-position-size`, `cooldown`, `symbol-whitelist`), estendibili in TS. Mancano R:R ≥ 1,5, rischio per trade e cassa. | ✅🟡 |
| Bracket order con entrata limite, TP, SL, scadenza | Bracket su Alpaca (TP+SL in OCA), `LMT`, `GTD` per scadere a una data. | ✅ |
| Trailing stop attivato oltre una soglia, senza LLM | Ordine `TRAIL` del broker (segue da subito, senza soglia di attivazione). La logica di attivazione manca. | 🟡 |
| Coda di approvazione umana | Trading as Git: stage → commit → push, approvazione da Web o Telegram `/uta`, legata all'hash, rifiuti nello storico. | ✅ |
| Agenti ignari di paper/live | Il conto è esplicito anche nell'identificativo (`alpaca-paper\|AAPL`): l'agente lo vede. È l'opposto di Q36. | ❌ |
| Kill switch | Modalità Lite / Readonly / Pro, sola lettura per conto. | ✅ |
| Credenziali LLM e broker modificabili | Vault credenziali, sigillate a riposo, da UI. | ✅ |
| Modello e sforzo per agente | `agent`, `credential`, `model`, `effort` per Workspace, Sessione o Issue. | ✅ |
| Token e costi su DB | Registro dei run con durata, esito e metriche; costo per agente non documentato. | 🟡 |
| Esiti delle decisioni e lezioni (Q40) | Rifiuti visibili, memoria su file e git; niente liquidazione deterministica degli esiti. | 🟡 |
| Watchlist gestita dal PM | Entities & Tracking (asset e temi tracciati, grafo di backlink). | 🟡 |
| Dati: OpenBB, macro, calendario, fondamentali, settori, news | `opentypebb` (porting TS di OpenBB), Data Hub senza chiavi, yfinance, FRED, FMP, rotazione settoriale, RSS. Rating degli analisti e insider da verificare. | ✅🟡 |
| Indicatori tecnici | Quant Calculator. | ✅ |
| CLI | CLI `alice` con un altro modello di comandi. | 🟡 |
| SQLite e codice Python | File e TypeScript. Il nostro `analysis/`, `execution/risk.py` e gli adapter Python non si riusano direttamente. | ❌ |
| MCP e portabilità verso Claude Code o Pi | Server MCP già pronto; il modello stesso è fatto di agenti nativi intercambiabili. | ✅ |
| Cockpit | Web UI, app desktop, mappa "Office" degli agenti al lavoro. | ✅ |
| Telegram | Connettore con approvazione `/uta`. | ✅ |
| Backtest e ricerca quant | AutoQuant V2 (repo separato), Time Machine retrospettiva. | 🟡 |

## Lettura

- **Autonomia.** Non è ciò che manca: Issue programmati, run headless, webhook e auto-scheduling ci sono già. L'approvazione umana degli ordini è il default, come abbiamo deciso noi.
- **Cosa manca davvero:** il **processo di trading deterministico**, cioè ciclo, ruoli, budget, state tipizzato, bozza a coefficienti, fusione degli Alert e Rimando. OpenAlice lascia tutto questo al giudizio dell'agente, mentre il nostro design lo vuole nel codice.
- **Cosa ha in più di noi:** ambiente di lavoro (Workspace con git, Inbox, Issue, entità), esecuzione con approvazione già pronta e multi-broker, dati senza chiavi, UI, MCP.
- **Costo di un fork:** circa 490k righe TypeScript in evoluzione quotidiana (restare allineati a upstream è un lavoro a sé), UTA in beta, AGPL (va pubblicato il sorgente se il servizio è offerto in rete ad altri). Esistono punti di estensione documentati (custom tools, custom guards, custom brokers, template di Workspace, skill, webhook, MCP): il nostro processo potrebbe vivere come estensione invece che come fork.
