---
title: "State Schemas — research_state e investment_state"
type: build
tags:
  - build
  - architecture
  - multi-agent
created: 2026-06-03
updated: 2026-06-04
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
| `agent_opinions` | list[obj] | **opinione per-agente**: ogni desk lascia la sua `suggested_direction` + `suggested_conviction` + breve razionale. Il **PM le aggrega** nella decisione finale (Sezione C) → vedi *Aggregazione* sotto |

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

### Validazione collettiva dell'`investment_state` (opzione — input di Luca 2026-06-04)
Oltre al gate di completezza (deterministico) e al gate bear del Risk Analyst, si valuta un passo di **validazione da parte di *tutti* gli agenti** prima del sealing: ogni agente del desk ha anche il ruolo di **validatore**, dedito ad assicurare sempre **completezza · correttezza · esaustività delle fonti** dello state.
- **Completezza**: nessun campo obbligatorio lasciato debole o "tanto per"; le sezioni di propria competenza sono davvero coperte.
- **Correttezza**: i numeri e le affermazioni sono coerenti con i dati nel DB (niente valori inventati o contraddittori).
- **Esaustività delle fonti**: sono state consultate *tutte* le fonti rilevanti disponibili, non solo le prime trovate (lega all'istruzione del PM *"nel dubbio, chiedi sempre"* → [[system/modules/agents]]).
- **Esito**: se un validatore segnala una lacuna, lo state **torna indietro** (`send_back`) per essere completato, prima del sealing. È un sign-off collettivo, non solo del Risk.
- **Da decidere in fase di grafo**: se è un passo *esplicito* (un nodo di validazione che interpella ogni agente) o una *responsabilità diffusa* scritta nel system prompt di ciascun agente. Tracciato in [[artifacts/project-board]].

---

## `entry_price` — struttura (✅ approvata 2026-06-04)

> Questo era il punto che Luca voleva *«strutturare bene»*. **Approvato da Luca il 2026-06-04** (*«l'entry price leggendolo mi sembra ok»*). I valori numerici (ATR 14, k_stop=2, k_tp=3, soglia R:R 1.5) restano da **tarare in backtest** ([[system/modules/quant-backtesting]]) — è l'impianto a essere deciso, non i numeri esatti.

### Il problema
Per un [[_meta/glossario#Limit Order|limit order]] non basta «compra ora al prezzo di mercato». Nello [[_meta/glossario#Swing Trading|swing trading]] si entra meglio su un **pullback** o a un **livello tecnicamente sensato**. Ma i criteri ingenui non reggono:
- **% fissa sotto il prezzo** (es. −2%): arbitraria, ignora la volatilità. −2% su un titolo tranquillo è tanto, su uno volatile è rumore.
- **Pivot/supporti**: tecnicamente sensati ("compra al supporto") ma fragili da far calcolare in modo affidabile e oggettivo a un LLM.
- **Range 52 settimane**: è un segnale di *contesto*, non un trigger d'entrata.

### Proposta: backbone deterministico in unità di ATR
Usare l'**[[_meta/glossario#ATR (Average True Range)|ATR]] (Average True Range)** come unità di misura comune a entry, stop e target — la stessa scelta già fatta per il volatility-adjustment del [[system/position-sizing]] (v2). Così i tre prezzi sono coerenti e normalizzati per la volatilità del singolo titolo.

```
entry_price  = current_price − k_entry · ATR     (per un BUY; simmetrico per un SELL)
stop_loss    = entry_price   − k_stop  · ATR
take_profit  = entry_price   + k_tp    · ATR
```

- `ATR` calcolato in modo deterministico in [[system/modules/quant-backtesting]] (es. 14 periodi).
- `k_entry`, `k_stop`, `k_tp` sono coefficienti, **non prezzi inventati dall'LLM**. L'agente ragiona in "quanti ATR", la funzione Python traduce in prezzo. Questo toglie all'LLM il compito fragile di sparare numeri assoluti.

### Come si calcolano ATR e R:R (per capirci)
- **ATR (Average True Range)** = media su N periodi (tipicamente 14) del *True Range* giornaliero, dove `TR = max( high−low ; |high−close_prec| ; |low−close_prec| )`. Misura quanto si muove mediamente il titolo per periodo, **nelle sue unità di prezzo** ($). Titolo "nervoso" → ATR alto; tranquillo → ATR basso. È solo volatilità: per questo lo uso come unità di misura comune.
- **[[_meta/glossario#Risk/Reward Ratio (R:R)|Risk/Reward]] (R:R)** = `(take_profit − entry) / (entry − stop_loss) = k_tp / k_stop`. È quanto puoi guadagnare diviso quanto rischi. Con `k_stop=2`, `k_tp=3` → R:R = 1.5: rischi 1 per puntare a 1.5. La soglia "≥ 1.5" scarta i trade col target troppo vicino allo stop — con un buon R:R si è profittevoli anche azzeccandone <50% (è il `b` di [[_meta/glossario#Kelly Criterion|Kelly]] → [[system/position-sizing]]).

### Due agganci che rendono il tutto sensato
1. **L'entry dipende dalla [[_meta/glossario#Conviction Level|conviction]].** Più sei convinto, meno pretendi lo sconto (sei disposto a "inseguire"); meno sei convinto, più pretendi un pullback profondo prima di entrare. Quindi `k_entry` **decresce** al crescere del `conviction_level`. Esempio indicativo: Strong Buy → `k_entry ≈ 0` (vicino al mercato), Buy → `k_entry ≈ 0.5`, segnale debole → `k_entry ≈ 1.0`.
2. **Vincolo di coerenza Risk/Reward.** Un guardrail deterministico (Sezione D) verifica che `(k_tp / k_stop) ≥ soglia` (es. R:R ≥ 1.5). Se la tesi propone un target troppo vicino rispetto allo stop, lo state **non passa il gate**. Questo impedisce trade con payoff asimmetrico sfavorevole a monte, senza che nessun agente debba "ricordarsi" di controllarlo.

### Ciclo di vita dell'ordine (limit che non viene colpito)
Se il prezzo non raggiunge mai `entry_price`, l'ordine **non è eterno**: scade alla `next_check_date` (il Dynamic Temporal Checkpoint già nello state). Alla scadenza la posizione mancata torna in valutazione — non resta un limit appeso a tempo indeterminato. La gestione concreta (cancel & rivaluta) vive nella funzione Trade → [[system/modules/execution]].

### Cosa cambia nello schema (Sezione C)
`entry_price`, `stop_loss`, `take_profit` restano campi-prezzo nello state (ciò che Trade consuma), ma **a monte** l'agente compila i coefficienti `k_entry / k_stop / k_tp` e la funzione Python deterministica li converte in prezzi usando `current_price` e `ATR`. Da decidere se persistere anche i `k_*` nello state (utile per il feedback post-trade: capire se gli sconti richiesti erano troppo aggressivi).

**Default che propongo per la prima alpha**: ATR(14), `k_stop = 2`, `k_tp = 3` (R:R = 1.5), `k_entry` scalato per conviction come sopra. Numeri da tarare in backtest, ma è uno scheletro che parte.

---

## Aggregazione `direction` + `conviction` (✅ deciso 2026-06-04)

Orientamento di Luca: **ogni agente esprime la propria opinione** — inclusa una proposta di direzione e convinzione — e il **Portfolio Manager raccoglie le opinioni di tutti i desk e prende la decisione finale**. Quindi:
- l'aggregazione che produce `direction` + `conviction_level` **definitivi** avviene al **nodo PM** (non a un nodo desk separato);
- ogni desk lascia nello state anche la **propria proposta** `suggested_direction` + `suggested_conviction` (campo per-agente in Sezione B), che il PM pondera prima di sigillare la decisione.

Coerente con la decisione "conviction assegnato dal PM" → [[system/modules/agents]], [[system/rating-scoring]].

---

## Quanti state annidati? — opzioni a confronto (da decidere insieme)

Domanda: lo state è **un unico oggetto piatto** con tutti i campi (sezioni A–F), oppure un **oggetto padre che contiene sotto-state tipizzati** (un blocco per sezione)?

### Opzione A — State unico "piatto"
Un solo TypedDict/Pydantic con tutti i campi allo stesso livello.
- ✅ Semplice da leggere, serializzare, debuggare; un solo schema.
- ✅ I nodi leggono/scrivono campi senza navigare gerarchie.
- ❌ Diventa grande; meno modulare; un blocco (es. il gate rischio) non è riusabile da solo.
- ❌ Più facile che nodi diversi tocchino campi non loro (meno incapsulamento).

### Opzione B — Sotto-state annidati
Uno state padre con sotto-oggetti tipizzati: `identity`, `portfolio_context`, `desk_analysis`, `proposal`, `risk_gate`, `meta`.
- ✅ Modulare: ogni blocco si valida/passa indipendentemente (es. `risk_gate` come sub-schema riusabile).
- ✅ Rispecchia 1:1 le sezioni A–F; chiaro "chi possiede cosa".
- ✅ È il pattern di TradingAgents (`investment_debate_state`, `risk_debate_state` annidati).
- ❌ Schema più complesso; accesso annidato (`state.proposal.entry_price`); serializzazione un filo più involuta.

### Opzione C — Ibrido / progressivo *(orientamento di partenza)*
A runtime lo state lavora **piatto** (i nodi mutano i campi facilmente); quando viene **sigillato** (`research_state` → `investment_state`) si **struttura in blocchi annidati** per la persistenza.
- ✅ Best of both: nodi semplici a runtime, documento strutturato in storage.
- ✅ Si aggancia alla forma di storage documentale (JSON annidato) → vedi sotto.
- ❌ Serve una funzione di "sealing" che mappa piatto → strutturato.

> **Asse diverso (non confondere)**: i **subgraph per-ticker** ([[system/parallelism-design]]) isolano *uno state per ticker* (isolamento *tra* ticker). Gli state annidati riguardano la struttura *dentro* il singolo ticker. Le due scelte sono indipendenti e componibili.

**Orientamento (2026-06-04): C**, da **validare al massimo** prima di consolidarlo (Luca: *«questa opzione mi piace di più, avviciniamoci, ma cerchiamo di validare la scelta al massimo»*).

> 🟢 **In parole semplici** (da rispiegare a voce a Luca — flag 2026-06-04): pensa allo state come a un **modulo da compilare**. Opzione A = un unico foglio lungo. Opzione B = un raccoglitore con sezioni etichettate. Opzione C = mentre lavori riempi un **foglio di brutta** veloce (A), e solo alla fine lo **archivi ordinato nel raccoglitore** (B) per conservarlo. "Validare la scelta C" vuol dire solo questo: **non ci impegniamo adesso** — partiamo dalla brutta, e se vediamo che serve il raccoglitore lo aggiungiamo dopo. Cambiare idea costa poco perché "l'archiviazione" è **un solo pezzo di codice** da scrivere (la *funzione di sealing*). Tutto qui — niente di più complicato.

**Come validare la scelta** (a basso costo): l'Opzione C ha il pregio che il confine *piatto-a-runtime → annidato-in-storage* è una singola **funzione di sealing**. Quindi si può:
1. partire con lo state piatto (A) durante l'engineering del grafo;
2. introdurre il sealing verso il documento annidato (B) quando si persiste;
3. se in corso d'opera la struttura annidata non serve, si resta su A senza riscrivere i nodi.
Di fatto C **non vincola** in anticipo: valida la scelta *usandola*, con rischio di rework minimo. Decisione finale in fase di mappatura del grafo.

---

## Forma fine di storage dello state (chiarimento 2026-06-04)

La decisione grossa è presa (**time-series + oggetti**, 2026-06-02). Resta da fissare *in che forma concreta* persiste un `investment_state`, che è un **documento ricco e annidato** (liste `pro`/`contro`, sotto-oggetti `guardrail_checks`, …) — non un dato time-series semplice. Opzioni:
- **Colonna JSON/JSONB** *(orientamento)*: tabella con i campi-chiave come colonne (per filtrare) + l'intero state come blob JSON in una colonna. Flessibile, niente secondo DB.
- **DB documentale** (Mongo…): naturale per gli annidati, ma è un secondo database da gestire.
- **Relazionale normalizzato**: una tabella per sotto-struttura — rigido, troppi join, sovra-ingegnerizzato.

Si aggancia all'Opzione C sopra (sealing → documento JSON). Decisione di forma in [[system/modules/data-layer]].

---

## Punti aperti (da risolvere insieme)

- ~~**Granularità `conviction_level`**~~ → **CHIUSO 2026-06-04**: **enum** a 5 livelli (`Strong Buy`/`Buy`/`Hold`/`Sell`/`Strong Sell`), non score 0-100. Vedi [[system/rating-scoring]].
- **Quanti state annidati?** → **orientamento C (ibrido), da validare in fase di grafo** (rework minimo grazie al sealing). Vedi sezione dedicata sopra.
- **Forma fine di storage** dello state → vedi sezione sopra (orientamento JSON/JSONB). → [[system/modules/data-layer]].

---

*Vedi [[system/modules/agents]] per gli agenti che compilano questi campi, [[system/modules/execution]] per chi li consuma, [[system/position-sizing]] per il campo `position_sizing`.*
