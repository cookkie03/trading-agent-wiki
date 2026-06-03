---
title: "State Schemas — research_state e investment_state"
type: build
tags:
  - build
  - architecture
  - multi-agent
created: 2026-06-03
updated: 2026-06-03
status: draft
priority: high
area: software
related:
  - "[[system/modules/agents]]"
  - "[[system/modules/execution]]"
  - "[[system/architecture]]"
  - "[[system/position-sizing]]"
  - "[[system/rating-scoring]]"
confidence: medium
---

# State Schemas — `research_state` e `investment_state`

> Pagina di lavoro per progettare il **contratto dati** tra gli agenti. È il primo deliverable concordato con Luca (call 2026-06-02): «partiamo dallo state, poi dal position sizing». Schema da raffinare insieme — qui c'è la **prima bozza ragionata**, non la versione definitiva.

Riferimenti d'impianto: lo state in LangGraph è una struttura (TypedDict/Pydantic) che i nodi del grafo leggono e scrivono — vedi la spiegazione di Salvatore in call (*«è come un template Word/Excel dove ogni nodo compila il suo paragrafo/cella»*). Pattern ereditato da TradingAgents → [[prior-art/tradingagents/graph-schema]].

---

## Chiarimento di naming (importante)

Nella call Luca chiede: *«cosa intendi per research_state? Intendi l'investment_state di `architettura.canvas`?»*. Sono **due momenti dello stesso oggetto logico**, non due cose scollegate:

| Nome | Cos'è | Chi scrive | Quando |
|------|-------|-----------|--------|
| **`research_state`** | La **tesi di investimento in lavorazione**: bozza che i desk analisti riempiono e il Risk Analyst contesta. Può essere incompleta, può tornare indietro nel loop. | Desk analisti + Risk Analyst | Durante l'origination/analisi |
| **`investment_state`** | La **versione finale, completa e validata** della stessa tesi: ciò che la funzione Trade legge per eseguire. È il `research_state` quando supera il **gate di completezza** e l'approvazione del Risk Analyst. | Si "sigilla" dal research_state | Pre-trade |

In pratica: **un unico schema**, due stati di maturità. Il `position_sizing` vive **dentro questo state** — è il campo da cui la funzione Trade deterministica ([[system/modules/execution]]) estrae l'ordine. Confermato da Luca: *«il position sizing deve essere un'informazione inclusa in tale state, per estrarne il trade»*.

---

## Principio di compilazione (da Luca)

- **Tutti i campi del `research_state` sono obbligatori.** Nessun trade parte finché lo state non è completo (è il senso del *gate di completezza*).
- Nell'`investment_state` **ogni agente ha il suo spazio da riempire**; alcuni spazi possono essere compilati da più agenti, altri da uno solo. La struttura deve **garantire che ogni agente venga interpellato a sufficienza** (forzare il passaggio per tutti i desk).
- Questo replica il pattern TradingAgents del «template paragrafato dove ogni nodo scrive nel suo paragrafo», ma **strutturato meglio**: niente ripetizioni, informazioni *potenziate* non duplicate (obiezione di Salvatore sui report ridondanti di TradingAgents).

---

## Bozza schema `research_state` (per singolo ticker)

> Pydantic per l'output LLM strutturato; TypedDict per lo state di workflow propagato tra nodi. I tipi sotto sono indicativi.

### Sezione A — Identità & contesto (chi scrive: sistema/extractor)
| Campo | Tipo | Note |
|-------|------|------|
| `ticker` | str | simbolo |
| `as_of_date` | date | data dell'analisi |
| `current_price` | float | dal DB |
| `portfolio_context` | obj | siamo già investiti su questo ticker? quanto? (dalla rendicontazione) |
| `past_context` | str | "lezioni apprese" da analisi precedenti sullo stesso ticker (pattern *past_context* di TradingAgents). **Include il feedback post-trade segmentato per meccanismo di uscita** (come sono andati i trade passati a seconda di TP/SL/trailing/rating-based) → [[system/rating-scoring]] §4 |

### Sezione B — Analisi (chi scrive: i due desk)
| Campo | Tipo | Compilato da |
|-------|------|-------------|
| `market_view` | str | Analyst Research (Market) |
| `sentiment_view` | str | Analyst Research (Sentiment) |
| `fundamental_view` | str | Analyst Technical (Fondamentali) |
| `technical_view` | str | Analyst Technical (Technical) |
| `key_factors` | list[obj] | fattori rilevanti calcolati + come letti (vedi [[system/modules/quant-backtesting]]) |

### Sezione C — Tesi & proposta (chi scrive: aggregazione desk → PM)
| Campo | Tipo | Valori / note |
|-------|------|---------------|
| `direction` | enum | `strong_buy` / `buy` / `hold` / `sell` / `strong_sell` |
| `conviction_level` | enum/score | livello di convinzione → [[system/rating-scoring]]. **Assegnato dal PM** date le info degli analisti |
| `entry_price` | float | prezzo target di entrata per il limit order — **da strutturare bene, punto aperto** (vedi sotto) |
| `stop_loss` | float | obbligatorio (hard constraint) |
| `take_profit` | float | obbligatorio |
| `position_sizing` | float | **% del portafoglio, mai valore assoluto** → [[system/position-sizing]] |
| `pro` | list[str] | tesi a favore (bull) |
| `contro` | list[str] | tesi contro |
| `next_check_date` | date | Dynamic Temporal Checkpoint: quando rivalutare (deciso dall'AI) |

### Sezione D — Gate rischio (chi scrive: Risk Analyst)
| Campo | Tipo | Note |
|-------|------|------|
| `risk_verdict` | enum | `approved` / `declined` / `send_back` |
| `risk_rationale` | str | antitesi bear + razionale |
| `guardrail_checks` | obj | esito dei check Python deterministici da Statuto (VaR, % max area/settore, duration…) |
| `risk_score` | score | soglia di approvazione ~60-70% → [[system/rating-scoring]] |

### Meta-versione
`version` (`alpha`/v1), `status` (`draft`/`complete`/`approved`/`declined`).

---

## Da `research_state` a `investment_state`

Quando: `risk_verdict == approved` **e** tutti i campi obbligatori sono compilati → lo state diventa `investment_state` (sigillato). La funzione Trade ([[system/modules/execution]]) ne estrae `{ticker, direction, entry_price, stop_loss, take_profit, position_sizing, conviction_level}` e costruisce l'ordine. **Reset automatico** dello state quando la transazione è rilevata.

---

## Punti aperti (da risolvere insieme)

- **`entry_price` — come si calcola?** Limit order: pivot points? % sotto il prezzo corrente? Range a 52 settimane? È il punto che Luca vuole *«strutturare bene, da valutare con più attenzione»*. → tracciato in [[artifacts/project-board]].
- **Granularità `conviction_level`**: enum (Strong/Normal) o score 0-100? Vedi [[system/rating-scoring]].
- **Quanti state separati?** Un solo state ricco vs sub-state annidati (TradingAgents usa state dentro state, es. `trade_proposal` contiene `trader_action`). Decidere in fase di engineering del grafo.
- **Schema della tabella DB** che persiste gli state: forma ancora da decidere (Luca: *«non lo so»*) → [[system/modules/data-layer]] (orientamento: JSON/documentale per gli state annidati, vedi decisione storage).
- **Dove avviene l'aggregazione** che produce `direction` + `conviction_level`: nodo PM o nodo di aggregazione desk? → [[system/modules/agents]].

---

*Vedi [[system/modules/agents]] per gli agenti che compilano questi campi, [[system/modules/execution]] per chi li consuma, [[system/position-sizing]] per il campo `position_sizing`.*
