---
title: "Investment State — template completo (menu di definizione con Salvatore)"
type: build
tags:
  - build
  - architecture
  - multi-agent
created: 2026-06-04
updated: 2026-06-04
status: draft
priority: high
area: software
related:
  - "[[system/state-schemas]]"
  - "[[system/position-sizing]]"
  - "[[system/rating-scoring]]"
  - "[[system/modules/agents]]"
  - "[[system/modules/execution]]"
  - "[[strategy/questions-for-salvatore]]"
confidence: low
---

# Investment State — template completo (menu di definizione)

> **A cosa serve questa pagina** (input di Luca, 2026-06-04): è un **foglio di lavoro da affrontare con Salvatore**. Invece di partire dal foglio bianco, qui c'è un **menu il più ampio possibile** di ogni campo che *potrebbe* far parte dell'`investment_state`. Leggendolo si devono **percepire tutte le possibilità**; poi insieme si **cancella, si modifica, si tiene** — è più facile potare che inventare.
>
> Questo NON è lo schema definitivo: lo schema "vivo" e già ragionato è in [[system/state-schemas]]. Qui c'è il **catalogo esteso** da cui quello si raffina.

**Legenda marcatori** (da decidere insieme):
- 🟢 **CORE** — quasi sicuramente serve, candidato obbligatorio.
- 🟡 **OPZIONALE** — utile ma valutabile, può entrare in v1/v2.
- 🔵 **DA VALUTARE** — idea sul tavolo, serve la competenza di Salvatore per decidere se ha senso.
- 🔴 **PROBABILMENTE NO** — incluso per completezza, ma a oggi sembra fuori scope.

> Promemoria: l'`investment_state` è il `research_state` **sigillato** (completo + approvato dal Risk). Qui li trattiamo come un unico oggetto e marchiamo *quando* ogni campo si compila. Vedi naming in [[system/state-schemas]].

---

## A — Identità & contesto del titolo
*(chi scrive: sistema / extractor, prima dell'analisi)*

| Campo | Tipo | Marker | Note / alternative |
|-------|------|--------|--------------------|
| `ticker` | str | 🟢 CORE | simbolo |
| `isin` / `exchange` | str | 🟡 | utile per multi-mercato e disambiguazione |
| `asset_class` | enum | 🟡 | equity / (futuro: commodity, crypto, opzione) — per ora sempre equity |
| `sector` / `industry` | str | 🟢 CORE | serve ai guardrail di diversificazione (Statuto) |
| `geography` / `country` | str | 🟡 | per i limiti per area/continente dello Statuto |
| `as_of_date` | date | 🟢 CORE | data dell'analisi |
| `current_price` | float | 🟢 CORE | dal DB |
| `currency` | str | 🟡 | per i tassi di cambio (titoli non-USD) |
| `liquidity_adv` | float | 🔵 | volume medio scambiato: un titolo poco liquido limita il sizing |
| `market_cap` | float | 🔵 | large/mid/small cap — può vincolare lo Statuto |

---

## B — Contesto di portafoglio
*(chi scrive: tool di iniezione stato portafoglio → [[system/modules/agents]])*

| Campo | Tipo | Marker | Note / alternative |
|-------|------|--------|--------------------|
| `already_invested` | bool | 🟢 CORE | siamo già su questo ticker? |
| `current_position_size` | float % | 🟢 CORE | quanto pesa già in portafoglio |
| `avg_entry_price` | float | 🟡 | prezzo medio di carico, per ragionare su P/L latente |
| `unrealized_pl` | float | 🟡 | P/L aperto sulla posizione |
| `portfolio_cash_pct` | float % | 🟢 CORE | cassa disponibile (rispetto del 10% min) |
| `sector_exposure_now` | float % | 🟡 | esposizione attuale al settore del titolo (per i cap) |
| `correlation_to_book` | float | 🔵 | quanto il titolo è correlato al resto del portafoglio (diversificazione reale) |

---

## C — Analisi dei desk
*(chi scrive: i due desk analisti → [[system/modules/agents]])*

| Campo | Tipo | Marker | Note / alternative |
|-------|------|--------|--------------------|
| `market_view` | str | 🟢 CORE | Analyst Research (Market): macro/contesto |
| `sentiment_view` | str | 🟢 CORE | Analyst Research (Sentiment): news/social |
| `sentiment_score` | float | 🔵 | sentiment quantificato (indicatore da inventare → [[strategy/questions-for-salvatore]] §7) |
| `fundamental_view` | str | 🟢 CORE | Analyst Technical (Fondamentali): financials, ratio |
| `technical_view` | str | 🟢 CORE | Analyst Technical (Technical): segnali quant |
| `key_factors` | list[obj] | 🟢 CORE | fattori rilevanti + valore + come letti → [[system/modules/quant-backtesting]] |
| `valuation_metrics` | obj | 🟡 | P/E (5 tipi), P/B, EV/EBITDA… (vocabolario di Salvatore) |
| `technical_indicators` | obj | 🟡 | ATR, 52w high/low, RSI, volumi, drawdown… (valori grezzi a supporto) |
| `macro_drivers` | list | 🔵 | driver macro pertinenti (4 macro-categorie + Fed → file di Salvatore) |
| `catalysts` | list | 🔵 | eventi attesi (trimestrali, lanci) che possono muovere il prezzo |
| `time_horizon` | enum/int | 🟡 | orizzonte atteso del trade (giorni/settimane) — lega a scadenza opzioni |

---

## D — Tesi & proposta operativa
*(aggregazione desk → PM)*

| Campo | Tipo | Marker | Note / alternative |
|-------|------|--------|--------------------|
| `direction` | enum | 🟢 CORE | `strong_buy`/`buy`/`hold`/`sell`/`strong_sell` |
| `conviction_level` | **enum** (5 livelli) | 🟢 CORE | assegnato dal PM → [[system/rating-scoring]]. **Deciso 2026-06-04: enum, non score 0-100** |
| `pro` (bull) | list[str] | 🟢 CORE | tesi a favore |
| `contro` (bear) | list[str] | 🟢 CORE | tesi contro |
| `entry_mode` | enum | 🟡 | come si entra: `market` / `limit` (default limit) |
| `k_entry` | float (ATR) | 🟢 CORE | coefficiente di sconto d'entrata (scalato per conviction) → [[system/state-schemas]] |
| `k_stop` | float (ATR) | 🟢 CORE | distanza stop in ATR |
| `k_tp` | float (ATR) | 🟢 CORE | distanza target in ATR |
| `entry_price` | float | 🟢 CORE | *derivato* da `current_price` − `k_entry`·ATR (lo scrive Python) |
| `stop_loss` | float | 🟢 CORE | *derivato*; hard constraint |
| `take_profit` | float | 🟢 CORE | *derivato*; hard constraint |
| `trailing_stop` | obj/bool | 🟡 | trailing stop armato? con quale distanza? |
| `position_sizing` | float % | 🟢 CORE | % del portafoglio, mai assoluto → [[system/position-sizing]] |
| `risk_reward` | float | 🟡 | `k_tp/k_stop`, *derivato*; usato dal guardrail (≥ soglia) |
| `expected_return` | float | 🔵 | rendimento atteso (per net performance vs costi) |
| `leverage_instrument` | obj | 🔵 | se `Strong`: tipo opzione (Call/Put), strike, scadenza → fuori MVP, [[strategy/questions-for-salvatore]] §4 |
| `next_check_date` | date | 🟢 CORE | Dynamic Temporal Checkpoint: quando rivalutare (decide l'AI) |
| `linked_trades` | list | 🔵 | eventuali vendite coordinate per far spazio (batch) → [[system/rating-scoring]] |

---

## E — Gate di rischio
*(chi scrive: Risk Analyst → [[system/modules/agents]])*

| Campo | Tipo | Marker | Note / alternative |
|-------|------|--------|--------------------|
| `risk_verdict` | enum | 🟢 CORE | `approved` / `declined` / `send_back` |
| `risk_rationale` | str | 🟢 CORE | antitesi bear + razionale |
| `risk_score` | score | 🟡 | soglia di approvazione ~60-70% → [[system/rating-scoring]] |
| `guardrail_checks` | obj | 🟢 CORE | esito check Python deterministici dallo Statuto (vedi sotto) |

### Dettaglio `guardrail_checks` (Statuto — deterministici)
| Check | Marker | Note |
|-------|--------|------|
| `var_impact_ok` | 🟢 CORE | la nuova posizione tiene il VaR di portafoglio ≤ ~10% → metodo da definire con Salvatore ([[strategy/questions-for-salvatore]] §1) |
| `cash_reserve_ok` | 🟢 CORE | resta ≥ 10% cash dopo il trade |
| `sector_cap_ok` | 🟢 CORE | non si sfora il max % per settore/area |
| `risk_reward_ok` | 🟢 CORE | `k_tp/k_stop` ≥ soglia (default 1.5) |
| `duration_cap_ok` | 🔵 | limiti di duration (se applicabile) |
| `single_name_cap_ok` | 🟡 | max % su singolo titolo |
| `correlation_cap_ok` | 🔵 | non si concentra troppo rischio correlato |

---

## F — Meta & tracciamento
*(sistema)*

| Campo | Tipo | Marker | Note / alternative |
|-------|------|--------|--------------------|
| `state_id` | uuid | 🟢 CORE | identificativo univoco |
| `version` | str | 🟡 | `alpha` / v1 |
| `status` | enum | 🟢 CORE | `draft` / `complete` / `approved` / `declined` |
| `created_by` / `updated_by` | str | 🔵 | quale agente/nodo ha scritto l'ultima volta |
| `agent_contributions` | obj | 🔵 | traccia di chi ha scritto cosa → base per lo scoring agenti ([[system/rating-scoring]] §2) |
| `past_context` | str | 🟢 CORE | lezioni dai trade precedenti sullo stesso ticker, segmentate per `exit_reason` → [[system/rating-scoring]] §4 |
| `cost_estimate` | obj | 🟡 | token cost del ciclo + commissioni stimate (net performance) |
| `chain_of_thought_ref` | ref | 🔵 | puntatore al log del ragionamento (learning loop) → [[system/learning-feedback-loop]] |

---

## Domande di impostazione da sciogliere con Salvatore
1. **Quali campi della Sezione C** (analisi) sono davvero discriminanti e quali sono rumore? Salvatore ha la sensibilità di mercato per potare.
2. ~~Granularità della [[_meta/glossario#Conviction Level|conviction]]~~ → **deciso**: enum a 5 livelli (non score 0-100).
3. **Quali guardrail** mettere nello Statuto e con quali soglie ([[_meta/glossario#VaR (Value at Risk)|VaR]], cap settore, [[_meta/glossario#Risk/Reward Ratio (R:R)|R:R]], duration).
4. **Metriche di valutazione** (`valuation_metrics`): quali entrano nel vocabolario dell'agente (file di Salvatore in arrivo).
5. **Un solo state ricco o sub-state annidati?** (es. blocco `risk` separato) — più una scelta di engineering del grafo → [[system/state-schemas]].
6. **Campi per il futuro multi-asset** (opzioni, commodity): predisporli ora "vuoti" o aggiungerli dopo?

---

*Pagina-compagna di [[system/state-schemas]] (schema vivo). Da consumare in una sessione dedicata con Salvatore; ogni decisione presa torna a raffinare lo schema vivo e migra nel [[system/decision-log]].*
