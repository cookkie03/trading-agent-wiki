---
title: "Data Layer — DB centrale + Extraction"
type: build
tags:
  - build
  - infrastructure
  - software
created: 2026-05-13
updated: 2026-07-13
status: active
priority: high
area: software
related:
  - "[[system/foundation/architecture]]"
  - "[[system/foundation/stack]]"
  - "[[system/data/data-providers]]"
  - "[[system/agents/agents]]"
  - "[[system/execution/execution]]"
  - "[[system/quant/quant-backtesting]]"
---

# Data Layer — DB centrale + Extraction

Il componente fondante. Costruisce la pipe vuota su cui poggia tutto il resto: il **DB centrale** (unico punto di verità) e il livello di **estrazione** che lo alimenta. Mappa le due aree sinistre di `architettura.canvas` ([[artifacts/trading-floor]] e i canvas in `artifacts/architecture/`): il grande gruppo **DB** e i tool di estrazione (`Extractors set`, `Adaptive extractor`, `Market Alert`, `calendar tool`, `mantainer`).

> **Stato attuale della pagina (2026-06-23)**: il contenuto qui sotto va letto come **design target con note storiche**, non come descrizione affidabile del codice corrente. La direzione resta valida; i riferimenti a branch, pacchetti o test precedenti sono reference design.

> **Direzione confermata da Luca**: la parte di tool di estrazione va **riprogettata, centralizzata ed efficientata**, separando meglio funzioni, wrapper e contratti.

> L'esecuzione ordini e l'exchange sono trattati in [[system/execution/execution]]. Qui sta solo *come i dati entrano e vivono nel DB*.

> **Contesto storico utile**: una build precedente aveva già esplorato `storage/`, `ingestion/` e una prima copertura di prezzi/news/fondamentali/macro/social. Quelle scelte restano interessanti come benchmark interno, ma non vanno assunte come implementazione esistente.

> **Nuova tassonomia di codebase da esplorare**: `connectors` per i fetcher esterni, `capabilities` per i calcoli/tool deterministici, `database` per schema e API, `agents` per prompt e orchestrazione. Vedi [[system/foundation/codebase-architecture]].

---

## Riferimenti di codice (repo esterni)

- **Schema DB context→operation con FK**: [[prior-art/libraries/rizzo-trading-agent]] — `db_utils.py` (schema Postgres completo) collega ogni decisione del bot al contesto esatto (prompt + indicatori + news + sentiment + forecast) → tracciabilità totale e dataset pronto per backtest/eval.
- **Architettura backend a layer**: [[prior-art/libraries/cvx-portfolio-optimizer]] — `api/` (FastAPI: models→repositories→services→routers, middleware, Alembic, docker-compose).
- **Modello transaction-based** (rendicontazione derivata dalle transazioni): [[prior-art/libraries/sfc-portfolio-tracker]] — `fund_manager.py`, `build_nav_history.py`.

---

## DB centrale — il blocco sempre acceso

Unico punto di verità del sistema: tutti i moduli/extractor scrivono qui, gli agenti ricevono sempre dai moduli/extractor, ma se servono info non live leggono da qui (solo i campi che servono). Ispirato alla dashboard **Streamlit di SFC**; obiettivo dichiarato: una **replica custom di Yahoo Finance** specifica per il progetto.

Le **5 tabelle core** sono la base SQL minima; il design organizza i dati in **4 aree logiche** (i quattro sotto-gruppi del blocco DB nel canvas):

| Area logica                               | Contenuto (nodi canvas)                                                                                                                                                                                        | Tabella core                    |
| ----------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------- |
| **1. Rendicontazione portafoglio**        | Liquidità corrente/investita · distribuzione con più filtri (geo, asset class, **settore**, **duration**) · P/L e metriche di performance. Modello a **oggetti** (riga = posizione, colonna = caratteristica). | `portfolio_state` (esteso)      |
| **2. Dati live** (aggiornati di continuo) | Prezzi di mercato · calendario economico · news · indicatori macro · **insider trading** (institutional positions) · **tassi di cambio**                                                                       | `market_data` (esteso)          |
| **3. Costituzione / Statuto**             | Regole deterministiche del fondo, al **centro** (base di rendicontazione e dati live) → la logica vive in [[system/agents/agents]] (Statuto del Fondo)                                                        | *(nuova)* `charter` / parametri |
| **4. Log**                                | `log`, `states`, `report`, `transactions` — storico completo                                                                                                                                                   | `logs` + `trades`               |

Principio emerso dai commenti di Luca: **non perdere nessun dato fondamentale**. Dove possibile si conservano dati grezzi e si calcolano i derivati in modo deterministico, invece di sostituire il grezzo con la sola sintesi.
> `module_outputs` (5ª core) resta come buffer degli output strutturati per ciclo, confluendo nell'area Log (`states`/`report`).

### Retention / clustering
La memoria cresce troppo → niente troncamento secco: **clusterizzare + riassumere + cancellare progressivamente** tenendo i riassunti. Ipotesi: ~5 anni giornaliero, 5-10 settimanale, 10-30 mensile. Hardware: hard disk esterni (es. 20TB ~500€). Molti dati vecchi sono recuperabili online (Yahoo Finance; Reuters ora a pagamento).

Vincolo richiesto da Luca: mantenere la **retention più alta possibile**. La cancellazione entra solo molto tardi, dopo aver privilegiato dati grezzi, compressione e clusterizzazione.
### Forma di storage (decisione 2026-06-02)
**Principalmente [[_meta/glossario#Time-series DB|time-series]]**, ma con DB e **architetture a oggetti internamente** (Luca: *"qualcosa di time-series, ma con db e architetture anche ad oggetti internamente al db"*). Lettura per area:
- **Dati live / prezzi / macro** → time-series (cuore del sistema);
- **Rendicontazione** → modello a oggetti (riga = posizione, colonne = caratteristiche);
- **States e output LLM annidati** → forma documentale/JSON (forma fine ancora da assegnare).

Resta aperta solo la **forma fine per i singoli stati annidati** (orientamento 2026-06-04: **colonna JSON/JSONB** dentro una tabella — campi-chiave come colonne per filtrare + l'intero state come blob JSON; niente secondo DB documentale). Vedi [[system/foundation/decision-log]] e [[system/investment/state-schemas]] (sezione *Forma fine di storage*).

> **Accesso e performance** — *quando* il DB è interrogato (read/write per attore), tecniche per velocizzare lettura/scrittura, approcci per **interrogarlo il meno possibile** (snapshot di ciclo, read-through cache, check-presenza) e **forma fisica** proposta (PostgreSQL + TimescaleDB, hypertable/oggetti/JSONB): dettaglio in [[system/data/db-access-performance]].

---

## Extraction — come i dati entrano nel DB

Primo set di tool degli agenti. Si agganciano al DB (**DB-first**), non ai vendor direttamente: ogni dato è scritto nel DB prima di essere reso disponibile agli agenti.

| Componente (nodo canvas) | Funzione                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Extractors set**       | Estraggono le info di mercato e le scrivono **sia nel DB sia verso gli agenti**.                                                                                                                                                                                                                                                                                                                                                    |
| **Adaptive extractor**   | Frequenza **adattiva** in base alla vicinanza al target (entro ~30% dal target → alta frequenza/"modalità rischio"; lontano → daily). Risparmia compute e rispetta i **rate limit** delle API. Utile per tenere il DB aggiornato con frequenza sostenibile.                                                                                                                                                           |
| **Market Alert**         | Layer di vigilanza che riceve segnali dagli extractor e richiama il PM quando scattano condizioni rilevanti: variazioni di prezzo, eventi di calendario, `next_check_date`, news anomale. La formulazione precedente era troppo contorta; la direzione da tenere è la **centralizzazione dei trigger**. |
| **calendar tool**        | Scrive/legge gli eventi del calendario economico; alla corrispondenza data/ora scatta l'**alert** verso il Portfolio Manager. Va trattato come componente centralizzato del trigger layer, non come modulo sparso.                                                                                                                                                                                                                                               |

#### Tipi di alert / trigger di attivazione del PM (alternative — da decidere con Salvatore)
Luca: *«come si attivano gli alert lo decidiamo io e Salvatore»*. Alternative da valutare (combinabili e componibili):
1. **Alert di prezzo/target**: il prezzo di una posizione si avvicina al target → l'adaptive extractor entra in "modalità rischio" (alta frequenza) e notifica il PM. *(già previsto)*
2. **Periodical synthesis**: stato sintetico a intervalli fissi (rendicontazione + market) → il PM si attiva comunque a cadenza regolare. *(già previsto)*
3. **Soglia di variazione**: variazione di prezzo oltre ±X% o ±N deviazioni standard (definizione di "prezzo anomalo").
4. **News anomale**: una news rilevante dal blocco `market` come *miccia* dell'origination → terzo trigger ("idea valida, valutala"). Da qui nasce anche l'idea di un **desk macro/news separato** che possa dialogare col PM fuori dal flusso ticker-centrico.
5. **Evento da calendario**: trimestrali, dati macro, eventi schedulati → alert alla scadenza.
6. **`next_check_date` scaduto**: una posizione chiede di essere rivalutata (Dynamic Temporal Checkpoint).
| **mantainer** | Processo di manutenzione (non-LLM, blocco verde/technical sul canvas) che **trasforma i dati `technical`/`transactions` in `rendicontazione`** (portfolio accounting) e la tiene aggiornata nel DB. *Ruolo confermato in call 2026-06-02*: «un mantainer che trasforma i technical in rendicontazione». È il ponte deterministico transazioni → metriche di portafoglio. |

**[[_meta/glossario#Look-Ahead Bias|Look-ahead bias]] — doppia data**: ogni informazione nel DB ha `publication_date` (quando ottenuta/pubblicata) e `reference_date` (data a cui si riferisce). Più preciso del semplice `curr_date` filtering.

**Indicatori calcolati dal DB**: nessun calcolo on-the-fly — gli indicatori si calcolano con formule che richiamano i dati grezzi già nel DB.

### Queue system + check presenza (decisione 2026-06-02)
Parte considerata **fondamentale** da Luca.
Gli extractor si chiamano **solo se l'informazione non è già nel DB**. Flusso:
1. **Check preventivo nel DB**: se il dato c'è → si legge da lì, fine (nessuna richiesta esterna).
2. Se manca → la richiesta entra in una **coda (queue)**; **un extractor per vendor** consuma la sua coda e **autogestisce i rate limit** di estrazione.
3. Il check avviene *prima* di accodare, per non riempire la coda di richieste inutili.


Si estraggono dai vendor **solo le osservazioni grezze**; le metriche derivate (P/E, ratio, ecc.) si **calcolano internamente** dai dati grezzi già nel DB (vedi [[system/quant/quant-backtesting]]).

#### Real-time first + write-through, durante il ragionamento (input di Luca 2026-06-05)
Il check-presenza DB-first **non** significa che l'agente si accontenti del dato in DB quando deve decidere. Distinzione per tipo di dato:
- **Dato live / decision-critical** (prezzo corrente, ultima news, quote opzioni): mentre ragiona su un `investment_state`, l'agente **prova prima il tool real-time** (anche più volte, per verificare aggiornamenti ed esserne sicuro). Il tool **consegna all'agente e scrive una copia nel DB** (*write-through*): il DB resta il **centro unico** delle informazioni, ma l'agente non rischia di decidere su un dato vecchio.
- **Dato storico / immutabile** (barre passate, bilanci depositati): vale il **check-presenza** sopra — non si ri-scarica ciò che non cambia.

Non c'è contraddizione: il check-presenza ottimizza il *bulk* e lo storico; il real-time-first garantisce la *freschezza* nel momento della decisione. I rate limit restano gestiti dall'**adaptive extractor**. Dettaglio del comportamento agente in [[system/agents/agents]].

---

## Operatività & resilienza

- **Deploy**: il sistema gira sul **Minisforum (mini-server) di Luca, acceso 24/7 in casa** (decisione 2026-06-02).
- **Secrets**: chiavi API (OpenRouter, broker, data vendor) in **`.env` locale** per ora.
- **Graceful shutdown & recovery**: design definito 2026-06-04 — vedi sezione dedicata sotto.
- **Orario di mercato / weekend**: gli extractor e gli alert devono conoscere le ore di mercato e i festivi (da definire).

### Graceful shutdown & recovery (design 2026-06-04)

Il sistema gira 24/7 su un mini-server domestico: prima o poi si spegnerà nel momento sbagliato (corrente, riavvio OS, crash da bug). Lo **shutdown gentile** (chiudere le scritture in corso prima di fermarsi) si fa *quando possibile*, ma non è garantibile → il cuore è il **recovery** al riavvio.

**Cosa può rompersi**, per gravità:
1. **Analisi a metà** (nessun ordine emesso): uno `state` parzialmente compilato. *Poco grave* — nulla di reale è successo.
2. **Scrittura DB a metà**: risolta **dal database stesso** — ogni scrittura è una **transazione atomica** (tutto-o-niente), non esistono righe a metà.
3. **Ordine emesso ma non loggato** (crash tra invio al broker e scrittura nel DB): il DB non sa di una posizione che sul broker *esiste davvero*. È il caso pericoloso.

**Strumenti del design:**
- **Transazione atomica** (caso 2): tutte le scritture critiche sono all-or-nothing → niente stato corrotto a metà.
- **Broker = source of truth, DB = specchio** (caso 3): sui soldi/posizioni la verità sta sul broker. → **riconciliazione**.
- **Intent log (diario delle intenzioni)**: prima di inviare un ordine si scrive l'intenzione (`pending`) con un id univoco; dopo conferma si scrive `confirmed`. Al riavvio, ogni `pending` senza `confirmed` → si interroga il broker su quell'id.
- **[[_meta/glossario#Idempotenza|Client order id]] (chiave anti-doppione)**: ogni ordine porta un id univoco generato da noi → un eventuale re-invio dopo il crash **non** esegue due volte (il broker riconosce il duplicato).
- **Checkpoint del grafo**: LangGraph salva già lo `state` dopo ogni nodo (SQLite). Disponibile per *riprendere* un'analisi, ma non necessario nell'MVP (vedi policy sotto).

**Routine di inizializzazione (al boot, sempre, prima del ciclo normale):**
1. **Riconciliazione col broker**: «cosa possiedo davvero? quali ordini sono aperti? quanta cassa?» → si allinea il `portfolio_state` alla realtà.
2. **Controllo intent log**: ogni intenzione `pending` non confermata → verifica sul broker via client order id; aggiorna il DB di conseguenza.
3. Solo dopo, riparte il ciclo normale (timer + alert).

**Policy di recovery (decisa 2026-06-04):**

| Cosa era in corso al crash | Comportamento al riavvio |
|---|---|
| **Analisi** (nessun soldo mosso) | **Scarta e ricomincia pulita** — rifarla costa poco ed è sicuro. *(Il checkpoint LangGraph per riprendere a metà resta ottimizzazione futura, non MVP.)* |
| **Ordine** (soldi reali) | **Riconciliazione**: broker = verità, allinea il DB; intent log + client order id evitano doppioni. |

In caso di **disallineamento DB↔broker** rilevato dalla riconciliazione: il sistema **allinea automaticamente il DB alla realtà del broker e logga lo scostamento**, poi riprende — **senza richiedere intervento umano** (coerente con la decisione *autonomia totale*; Luca 2026-06-04). L'override umano resta possibile nelle prime fasi, non è un requisito.

---

## Tech

- **PostgreSQL** (prod) / **SQLite** (dev locale)
- Provider dati e broker: vedi [[system/data/data-providers]]
- Schema DB versionato (Alembic)

---

## Dipendenze

- **Nessuna dipendenza in ingresso**: è il punto di partenza del sistema.
- **[[system/quant/quant-backtesting]]** legge `market_data` dal DB.
- **[[system/agents/agents]]** legge dal DB **solo** i campi che servono (evita context rot).
- **[[system/execution/execution]]** scrive `transactions` qui e legge `portfolio_state`.

---

*Per l'architettura completa vedi [[system/foundation/architecture]]. Per le decisioni tecniche [[system/foundation/decision-log]].*
