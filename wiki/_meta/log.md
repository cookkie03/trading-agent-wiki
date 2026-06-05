# Wiki Log — Trading Agent

> Log append-only. Grep utile: `grep "^## \[" wiki/_meta/log.md | tail -10`

## [2026-06-06] CODICE — strato dati (alpha v0) implementato nel fork

- **Svolta**: Luca dà il via al codice (*"rendiamo trading-agent una prima versione alpha"*), prende il **grafo** in autonomia, delega a Claude *"vedi cosa ha senso fare ma parti"*. Scelta: costruire lo **strato dati** (M2), il gap più grosso e il contratto su cui il grafo poggia → lavoro parallelo non-collidente.
- **Discussione metodo**: la visione di Luca "wiki-spec → agenti paralleli finché il codice combacia" valutata onestamente — valida come nord, ma da rendere convergente (contratti congelati + test-oracolo + slice verticali + review umana). Lo storage è il **primo contratto congelato**.
- **Implementato** in `/Users/luca/Desktop/trading-agent`, pacchetto `tradingagents/storage/`:
  - `models.py` — 7 tabelle SQLAlchemy 2.0 sulle 4 aree wiki: `instruments`, `ticker_card` (scheda funnel), `price_bars` (time-series, double-date anti look-ahead), `research_states` (JSON, sealing Opzione C), `portfolio_snapshots` (rendicontazione), `trades` (`client_order_id` idempotente), `charter` (Statuto parametrico).
  - `database.py` — engine/session/`init_db`; SQLite default (`~/.tradingagents/`), Postgres/Timescale-ready (hypertable `price_bars` su dialetto postgres).
  - `repository.py` — helper tipati = contratto di accesso (upsert instrument/scheda, top_screened per la coda D, save/latest research_state, insert price bars, snapshot portafoglio, record_trade + lookup idempotente, charter get/set).
  - `tests/test_storage.py` — **7 test di accettazione, tutti verdi** (oracolo del data-layer).
  - deps: `sqlalchemy>=2.0` in `pyproject.toml`; `TRADINGAGENTS_DATABASE_URL` in `.env.example`.
- **Verifica**: `uv run pytest tests/test_storage.py` → 7 passed; suite completa colleziona 239 test senza errori (additivo, non rompe nulla).
- **Registrato**: [[system/modules/data-layer]] (callout "Implementato alpha v0"); [[system/fork-gap-analysis]] (M2 avviato, ordine M1/M2 risolto in parallelo); board ✅ Fatto; [[_meta/index]] invariato.
- **NB**: codice **non committato** (Luca non l'ha chiesto) — file nuovi in working tree del fork.

## [2026-06-06] Gap analysis fork TradingAgents ↔ design (ponte verso il codice)

- **Contesto**: Luca ha aggiunto la dir `/Users/luca/Desktop/trading-agent` (fork vivo di TradingAgents, repo `cookkie03/trading-agent`, già produce report NVDA/MONC.MI) e ha chiesto: altra progettazione o codice? Risposta: il fork copre gran parte del design → basta progettazione astratta, serve **adattare il fork**.
- **Ispezione fork**: `tradingagents/` (agents/dataflows/graph/llm_clients), `default_config.py`, `graph/setup.py`, `agent_states.py`, `schemas.py`, `trader.py`, elenco tool. Già presenti: 4 analisti, PM, grafo LangGraph, tool (incl. **reddit + stocktwits**), structured output, multi-provider, quick/deep think, checkpoint, `output_language=English`, `past_context`.
- **Creata** [[system/fork-gap-analysis]]: mappa **TENGO** (tool, vendor, grafo, structured, multi-LLM) / **ELIMINO** (bull/bear + research_manager, risk debate 3→1, LLM trader→Python, 4 analisti→2 desk, debate-state) / **AGGIUNGO** (DB centrale, esecuzione broker, logica rischio nostra, funnel multi-ticker, conviction enum, trigger autonomi, prompt nostri, OpenRouter+DeepSeek). + **roadmap M0→M6** (M0 wiring+validazione · M1 grafo nostro · M2 DB · M3 rischio+trade deterministico · M4 esecuzione · M5 funnel · M6 leva/learning).
- **Differenza strutturale chiave**: nel fork il PM è **giudice finale** (pipeline), nel nostro design è **orchestratore in cima** → `graph/setup.py` da riscrivere.
- **graphify**: `graphify-out/` già presente nel fork (run 2026-05-26, 1192 nodi/818 edge); le community **confermano** la mappa della gap analysis. Da ri-girare dopo le modifiche al grafo.
- **Punto aperto**: ordine **M1 vs M2** (snellire-grafo-prima vs DB-prima) — proposta M1 prima (definisce cosa persistere), da confermare con Luca.
- **Registrato**: [[_meta/index]] (nuova voce); board → 🟡 In corso "Roadmap di adattamento del fork".

## [2026-06-06] Topologia parallelismo multi-ticker — architettura a imbuto

- **Richiesta Luca**: al bivio design/codice, scelto di chiudere l'ultima decisione architetturale (parallelismo). Poi domande puntuali sullo **screening**.
- **Decisione**: le alternative A–E **si compongono** in un **funnel** (non competono): **E** screening deterministico → **D** coda di priorità → **A** deep-dive subgraph per-ticker → **B/C** scheda ticker nel DB. Subgraph vs nodi già deciso (subgraph). Aggiunta sezione "Decisione (2026-06-06): architettura a imbuto" in [[system/parallelism-design]] (status draft→active).
- **Screening — design dettagliato** (risposte alle 6 domande di Luca): **non è un agente** (modulo deterministico Python/quant, Quick Thinker); **usa info passate** (segnali quant nel DB + feedback storico); **lo aggiornano extractor + mantainer** (job periodico, nessun attore nuovo); **2 popolazioni** (portafoglio sempre + universo investibile per origination); **cadenza** periodical synthesis + on-trigger; **scrive nella scheda ticker del DB** (`screening_score`/`rank`/`last_screened_at`), **non** sullo state classico. Confine netto stato-persistente (scheda) vs stato-di-lavorazione (`research_state`).
- **Ordine MVP**: D+A prima, E e B/C come strati successivi senza rework (alpha-first, ma agganci già definiti).
- **Registrato**: decisione chiusa in [[system/decision-log]] (+ riga "ora chiusa"); open row rifocalizzata su "numeri e soglie"; board → ✅ Fatto + card 🟠 trasformata in task MVP; [[system/parallelism-design]] (2 sezioni nuove).
- **Bivio design/codice**: la topologia era l'ultima vera decisione architetturale software. Restano da progettare: schema DB concreto (= ponte al codice) + criteri info-sufficienti/anti-loop (piccolo). Il resto è implementazione o richiede Salvatore.

## [2026-06-06] System prompt degli agenti — metodo + 4 prompt desk

- **Richiesta Luca**: *«proviamo ad andare avanti, per i system prompt bisogna formarsi come veri prompt engineer»*. Sessione condotta da Claude (formazione distillata + proposta + reazione).
- **Creata** [[system/system-prompts]]: (1) **principio di separazione** comportamento/forma-output/tool; (2) **7 principi** di prompt engineering adottati; (3) **scheletro a 7 blocchi** riutilizzabile; (4) i **4 system prompt del desk scritti per intero** (Technical · Market · Sentiment · Fondamentali). Realizza i comportamenti di [[system/agent-behaviors]] usando i tool di [[system/tools-inventory]].
- **Scelte di Luca (AskUserQuestion)**: (1) **lingua dei prompt = inglese** (doc resta IT); (2) scrivere **gli altri 3 desk** adesso (Market/Sentiment/Fondamentali) — fatto. PM e Risk rimandati.
- **Registrato**: decisione chiusa in [[system/decision-log]]; [[_meta/index]] (nuova voce); board → card ✅ Fatto + card Prompt Builder rifocalizzata (restano PM+Risk); [[system/modules/agents]] (decisione aperta Prompt Builder ora linkata).
- **Aggiornamento (stessa sessione)**: scritti anche i **2 prompt speciali** — **PM** (orchestratore: chiama i desk come tool, "nel dubbio chiedi sempre", aggrega e decide direction/conviction, set ATR-coefficient stance + next_check_date, flag leva) e **Risk Analyst** (gate bear: guardrail deterministici binding da `<guardrail_checks>`, verdict approved/declined/send_back soglia ~60-70%, validazione leva). Ora **tutti e 6** i prompt esistono come bozze v0. Open point #4 chiuso; status pagina resta `active`.
- **Prossimo**: consolidamento nel **Prompt Builder** (assemblaggio prompt + contesto XML + JSON-strict, pattern rizzo) + rifinitura iterativa via LangSmith.

## [2026-06-06] Comportamento per-agente del desk — impianto approvato

- **Richiesta Luca**: *«proviamo anche il comportamento per-agente»*. Sessione condotta da Claude (proposta + reazione).
- **Creata** [[system/agent-behaviors]]: per ognuno dei 4 agenti (Market · Sentiment · Technical · Fondamentali) definite **5 dimensioni** — input · tool (dall'inventario [[system/tools-inventory]]) · output nello state ([[system/state-schemas]]) · stile di ragionamento · criterio di stop. + 5 comportamenti trasversali.
- **Scelte di Luca (AskUserQuestion + note)**: (1) **news/sentiment spartiti per tipo di informazione** — Market=catalizzatori macro/settore, Sentiment=mood/posizionamento da **più fonti possibili** (vendor news + social/forum Reddit·StockTwits·X + piattaforme sentiment dedicate); (2) **tutti contribuiscono alla direzione** — ognuno col contributo primario della sua specialità (Market→direzione contesto, Technical→entry/livelli) ma libero di esprimersi su tutto, PM aggrega; (3) **stop = auto-stop + il PM può richiamare**.
- **Sotto-lavoro generato**: enumerare le **fonti/tool di sentiment** (famiglia D di [[system/tools-inventory]] aggiornata: split `get_news`/`get_news_sentiment`/`get_social_sentiment`); si interseca con "indicatori di sentiment" (Salvatore).
- **Registrato**: decisione chiusa in [[system/decision-log]] (+ riga "ora chiusa"); open row trasformata in "fonti sentiment"; TODO in [[system/modules/agents]] barrato e linkato; [[_meta/index]] (nuova voce); board → card ✅ Fatto + 🟠→🔴 "fonti sentiment".
- **Prossimo collegato**: scrivere i **system prompt** che realizzano questi comportamenti (Prompt Builder) → [[system/modules/agents]].

## [2026-06-06] Inventario tool agenti — impianto approvato

- **Richiesta Luca**: scegliere su cosa lavorare; ha scelto **"Tool degli agenti"** (la cosa che aveva messo lui sul piatto il 2026-06-05). Sessione condotta da Claude con proposta concreta + reazione di Luca.
- **Creata** [[system/tools-inventory]]: inventario dei tool che gli agenti possono chiamare. **9 famiglie** (A prezzi & quote · B indicatori tecnici · C fondamentali · D news/sentiment · E macro · F calendario · G portafoglio · H opzioni · I guardrail=non-tool LLM), ognuna con **5 etichette** (cosa · live/storico · write-through · agente · vendor). **2 regole trasversali**: parametrici mai hardcoded · il dato live torna all'agente *e* scrive copia nel DB. Marcata distinzione tool ereditabili da TradingAgents `dataflows` vs da costruire.
- **Scelte di Luca (AskUserQuestion)**: (1) `inject_portfolio_state` = **auto a ogni ciclo + richiamabile**; (2) indicatori tecnici = **un solo tool parametrico** `compute_indicator(ticker, indicator, params)`; (3) vendor live MVP = **decidiamo dopo** (candidato Finnhub annotato). Impianto + 9 famiglie + 2 regole **approvati**.
- **Registrato**: decisione chiusa in [[system/decision-log]] (+ riga "ora chiusa"); open row rifocalizzata su "vendor"; TODO in [[system/modules/agents]] barrato e linkato; [[_meta/index]] (nuova voce); board → card ✅ Fatto + 🔴 reworded "fissare i vendor".
- **Prossimo collegato**: **comportamento per-agente** (quali tool usa ogni desk, in che ordine, criterio di stop) → [[system/modules/agents]].

## [2026-06-05] ingest | Conversazione Luca↔Salvatore 2026-06-04 sera + Indicatori Macro

- **Type**: call (15 messaggi audio WhatsApp + export chat) + documento strategia (Indicatori Macro)
- **Source audio**: `raw/audio/WhatsApp Audio 2026-06-04 at 19.59.54` → `21.59.32` (15 file .txt + .opus)
- **Source chat**: `raw/daily-notes/2026-06-04.md` (chat export Luca↔Salvatore + conversazione Claude su broker)
- **Source documento**: `Indicatori per Analisi Macroeconomica.md` (vault root — non archiviato per istruzione esplicita)
- **Pages created**: [[strategy/indicators/macro-indicators]]
- **Pages updated**: [[system/modules/quant-backtesting]], [[system/decision-log]], [[system/ideas-log]], [[artifacts/project-board]], [[_meta/index]]
- **Archived**: `raw/audio/*.txt` → `raw/archived/audio/` (file .opus lasciati in place)
- **Conflicts**: nessuno
- **Notes**: backtesting equivoco chiarito (deterministico, non AI simulation); policy capitale (no investimento prima della prova); collaboratori pipeline (Zappa, Trezzi, SIM); eToro copy trading come canale monetizzazione futuro; Salvatore sta completando il documento indicatori (12 categorie, per ora PIL completo + Consumi iniziato)

## [2026-06-05] Position sizing (modello risk-based) + autonomia informativa + tool da costruire

- **Position sizing** (passo concordato n°2): proposto in [[system/position-sizing]] il modello **risk-based / fixed-fractional** che si aggancia all'`entry_price` ATR — budget di rischio % (scalato per conviction) → quantità derivata da `stop_distance = k_stop × ATR`, + **portfolio heat** come cap aggregato. Vantaggio: volatility-adjustment *gratis*. Numeri di partenza (1% risk, heat 5–6%, cap titolo 10%) da tarare in backtest. Pagina passata a `status: active`. In attesa di reazione di Luca (decisione aperta aggiornata).
- **Autonomia informativa real-time first + write-through** (input Luca): gli agenti chiamano info aggiornate in autonomia, anche più volte per verificare; **prima il tool real-time** (non il DB), che **consegna all'agente + copia nel DB** (DB = centro unico). Riconciliato col DB-first: check-presenza per lo storico, real-time-first per il live. → decisione chiusa in [[system/decision-log]] + callout in [[system/modules/agents]] + sezione in [[system/modules/data-layer]] + board ✅.
- **Selezione tool da costruire** (input Luca): aggiunto come cosa a cui pensare — inventario tool (real-time/storico, write-through, agente, parametri, vendor), parte dai dataflows TradingAgents + tool propri → TODO in [[system/modules/agents]] + decision-log (aperta) + card board.
- **Prossimo**: spiegazione a voce dell'opzione C (Luca non ricorda cosa sia) — fatta in chat in questa sessione.

## [2026-06-05] approvazioni Luca: sizing impianto + opzione C + idea agenti-sul-sizing

- **Position sizing impianto APPROVATO** (Luca: *«mi convince»*) → decisione chiusa in [[system/decision-log]]; [[system/position-sizing]] sezione marcata approvata; board card → ✅ + reworded "tarare i numeri". Restano solo i numeri da backtest.
- **Opzione C (state annidati) CONFERMATA** (Luca: *«ho capito e secondo me ci sta»*) dopo spiegazione a voce → [[system/state-schemas]] sezione marcata confermata; decisione chiusa in [[system/decision-log]]; board card 🟠→✅.
- **Idea da valutare — intervento agenti sul sizing** (Luca, *sul piatto*): indagare rischi (rompe determinismo, LLM debole sui numeri, sovraesposizione) vs benefici (contesto non catturato); via di mezzo = fattore ±X% clampato dai cap. → [[system/position-sizing]] (sezione) + [[system/ideas-log]] + decision-log (aperta) + card 💡 board.

## [2026-06-04] Graceful shutdown & recovery — design (Luca non conosce i DB → spiegazione dal basso)

- **Richiesta Luca**: discutere graceful shutdown & recovery, premettendo di non aver mai studiato i database. Sessione condotta da Claude con spiegazione in parole semplici.
- **Spiegati** (chat + glossario): transazione/atomicità, broker=source of truth, riconciliazione, intent log (diario delle intenzioni), idempotenza/client order id, checkpoint LangGraph. Aggiunte 3 voci al glossario: **Transazione/Atomicità**, **Riconciliazione**, **Idempotenza/Client order id**.
- **Design deciso** (sezione dedicata in [[system/modules/data-layer]]): routine di init al boot = riconciliazione col broker + controllo intent log; policy = analisi a metà → scarta e ricomincia pulita, ordine a metà → riconciliazione; atomicità copre il crash a metà-scrittura.
- **Scelta di Luca (AskUserQuestion)**: su disallineamento DB↔broker → **allinea da solo + logga, senza intervento umano** (coerente con autonomia totale). Checkpoint LangGraph per riprendere a metà = ottimizzazione futura, non MVP.
- **Registrato**: decisione chiusa in [[system/decision-log]] (+ riga "ora chiusa"); card board 🔴→reworded "Implementare" + card ✅ Fatto; [[_meta/glossario]] (3 voci); [[system/modules/data-layer]] (rimossa apertura, aggiunta sezione design).

## [2026-06-04] DB — accesso, performance, minimizzazione query, forma fisica

- **Domanda Luca**: stato attuale del DB, quando/da chi è interrogato, come gestirlo, tecniche per velocizzare read/write, come interrogarlo il meno possibile, che forma avrebbe.
- **Creata pagina** [[system/db-access-performance]]: stato attuale (design, non implementato) · tabelle read/write per attore · gestione a layer (models→repo→service) · tecniche scrittura (batch/COPY, pooling, partitioning) e lettura (indici mirati, BRIN, GIN su JSONB, materialized view, indicatori pre-calcolati) · **minimizzazione query** (check-presenza, snapshot di ciclo in memoria = tool iniezione portafoglio, periodical synthesis, read-through cache, no N+1) · **forma fisica proposta**: PostgreSQL + **TimescaleDB** (hypertable time-series + relazionale + JSONB).
- **Decisioni CHIUSE da Luca**: **motore DB = PostgreSQL + TimescaleDB**; **cache = in-process per l'MVP, Redis idea futura** (solo se il sistema diventa multi-processo). Spiegato a Luca perché Redis aggiunge un processo+invalidazione separati e non vale finché c'è un solo processo. → [[system/decision-log]] (chiuse) + board (✅).
- **Aggiornati**: [[_meta/index]], [[system/modules/data-layer]] (callout link), [[system/decision-log]], [[artifacts/project-board]], [[system/db-access-performance]].

## [2026-06-04] validazione collettiva investment_state + flag spiegazione opzione C

- **Input Luca**: tra le opzioni del PM/software, includere la **validazione dell'`investment_state` da parte di tutti gli agenti**, dediti ad assicurare sempre **completezza · correttezza · esaustività delle fonti**.
- **Registrato**: sezione *Validazione collettiva* in [[system/state-schemas]] (sign-off di tutti gli agenti, `send_back` su lacuna, da decidere se nodo esplicito o responsabilità nel system prompt) + nota nel gate di [[system/modules/execution]] + card in board.
- **Flag**: Luca segnala di **non aver capito la parte sulla "validazione dello schema dello state"** (opzione C / sealing). Aggiunto un callout *"in parole semplici"* (analogia brutta→raccoglitore) in [[system/state-schemas]]; **da rispiegare a voce** alla ripresa.

## [2026-06-04] istruzione PM "nel dubbio chiedi sempre"

- **Input Luca**: il PM, decisore finale, va istruito (system prompt) a **chiedere SEMPRE ulteriori info ai desk** quando ha dubbi/indecisioni, *anche per le piccolezze*, prima di decidere.
- **Registrato**: bias "nel dubbio, chiedi" in [[system/parallelism-design]] (sezione criteri info-sufficienti) bilanciato coi tetti anti-loop (rete di sicurezza, non scusa per decidere su info parziale; **no-trade preferibile** a basi incerte) + nota nel PM di [[system/modules/agents]] + card in board (system prompt).

## [2026-06-04] chiusura punti state + pesi agenti dal backtest

- **`entry_price` APPROVATO** da Luca (*«leggendolo mi sembra ok»*) → decisione chiusa in [[system/decision-log]], board → ✅, [[system/state-schemas]] sezione marcata approvata.
- **Aggregazione `direction`/`conviction`**: Luca chiarisce il suo modello → **deciso**: ogni desk propone (`suggested_direction`/`suggested_conviction`), il **PM aggrega e decide**. Aggiunto campo `agent_opinions` allo schema; nota in [[system/modules/agents]]; decisione chiusa.
- **State annidati**: Luca non ha preferenza, vuole valutare le opzioni → scritte in [[system/state-schemas]] le **3 opzioni A (piatto) / B (sotto-state) / C (ibrido)**; resta **aperta** (board 🟠).
- **Forma fine di storage**: chiarito cosa significava (come persistere il documento-state annidato) → orientamento **JSON/JSONB** in colonna, niente secondo DB. In [[system/state-schemas]] + [[system/modules/data-layer]].
- **Pesi degli agenti dal backtest** (input Luca): la ponderazione dinamica dei desk è un **output del backtesting validatore** (hit-rate per-agente), non un parametro a mano → [[system/learning-feedback-loop]] §4 + [[system/modules/quant-backtesting]] + board.
- **Precisazione pesi (Luca)**: i pesi sono **indicazione, non regola** — contesto/awareness in input al PM, non automatismo che scavalca il giudizio; aggancio risolto come **(a) input al PM** (scioglie la tensione con "conviction dal PM"). Seconda funzione: **diagnostica** su cosa/come migliorare agenti e tool collegati. Decisione chiusa + §4 e punti aperti aggiornati.
- **State annidati**: Luca sceglie **orientamento C (ibrido)**, da *validare al massimo* → in [[system/state-schemas]] aggiunta la strategia di validazione a basso rework (sealing piatto→annidato). Schema dello state **chiuso a livello di design**.

## [2026-06-04] commenti Luca su entry_price + cross-link glossario

- **Trigger**: Luca legge la proposta `entry_price` e dà 9 commenti + input successivi, poi "aggiorna tutti i riferimenti del glossario".
- **Risposte/spiegazioni**: aggiunti al glossario **ATR** e **Risk/Reward Ratio** con formule complete; spiegato (in chat + pagine) il *perché leva via opzioni e non margine* → nota in [[strategy/questions-for-salvatore]] §4. Aggiunto esplicativo ATR/R:R in [[system/state-schemas]].
- **Decisioni chiuse (2026-06-04)**: **autonomia totale** (nessun input umano oltre l'accensione, auto-start timer+alert); **PM attivato anche dal `next_check_date` scaduto** (terzo trigger); **backtesting = validatore continuo e asincrono** delle soglie (R:R, k_*, ATR, Statuto); **conviction = enum** (non score 0-100). Tutte in [[system/decision-log]] + board.
- **Nuove registrazioni**: disinvestimento come **batch di trade coordinati** del PM (solo se tutto analizzato) → [[system/rating-scoring]]; **tool di iniezione stato portafoglio** obbligatorio → [[system/modules/agents]]; **comportamento per-agente del desk** da approfondire → [[system/modules/agents]] (decisione aperta); **legenda colori canvas** (viola=DB·arancio=agent·verde=tool·azzurro=state) → [[_meta/taxonomy]].
- **Nuova pagina**: [[system/investment-state-template]] — template-menu completo dell'`investment_state` da affrontare con Salvatore (marcatori CORE/OPZIONALE/DA VALUTARE, sezioni A–F + guardrail).
- **Cross-link glossario**: script una-tantum (`tmp/glosslink.py`) → **145 link** al glossario su 27 pagine, prima occorrenza per termine, escluse tabelle (pipe)/code/heading/frontmatter. Verificato: 0 link in tabelle, 0 annidati, anchor tutti validi.
- **Aggiornati**: [[system/modules/agents]], [[system/modules/quant-backtesting]], [[system/rating-scoring]], [[system/state-schemas]], [[system/investment-state-template]], [[strategy/questions-for-salvatore]], [[system/decision-log]], [[_meta/glossario]], [[_meta/taxonomy]], [[_meta/index]], [[artifacts/project-board]] + i 27 file cross-linkati.

## [2026-06-04] design state | Proposta struttura `entry_price` (backbone ATR)

- **Trigger**: "riprendiamo". Ripartenza dallo Step 1 (schema dello state). Sessione condotta da Claude (Luca preferiva reagire più che decidere a freddo).
- **Lavoro**: progettata e scritta in [[system/state-schemas]] la **proposta per `entry_price`** del limit order — chiude il punto che Luca voleva "strutturare bene". Backbone in **unità di ATR** (coerente col volatility-adjustment del [[system/position-sizing]]): `entry/stop/tp` derivati da `current_price` ± `k·ATR`; l'LLM ragiona in coefficienti `k_*` (non prezzi assoluti), la funzione Python traduce in prezzo. Due agganci: `k_entry` **scalato per conviction** (più convinto → meno sconto), e **guardrail R:R** deterministico (`k_tp/k_stop ≥ soglia`, default 1.5) nel gate di rischio. Ciclo di vita del limit non colpito → scadenza alla `next_check_date`. Default prima alpha: ATR(14), `k_stop=2`, `k_tp=3`.
- **Stato**: è una **proposta da approvare**, non una decisione presa. Board aggiornata (card `entry_price` → "proposta pronta"), `entry_price` rimosso dai punti aperti di state-schemas.
- **Aperti residui state**: granularità conviction, n. state annidati, storage state, dove avviene l'aggregazione.

## [2026-06-03] review pre-sviluppo | Risposte di Luca alle lacune → nuove pagine + board come hub

- **Trigger**: "cosa manca da capire/decidere prima dello sviluppo" → analisi lacune → Luca risponde punto per punto (chat 2026-06-02, si ferma a metà) → "sistemami tutto" + "usa la board come centrale operativa con riferimenti" + "salva la convenzione in CLAUDE.md" + "distingui owner pagine/task".
- **Lette le 2 call del 2026-05-29** (`raw/archived/`): confermato ruolo `mantainer` (technical → rendicontazione) e modello di attivazione (alert prezzo/news + periodical synthesis).
- **Nuove pagine create**: [[system/state-schemas]], [[system/position-sizing]] (con spiegazione Kelly), [[system/rating-scoring]], [[system/parallelism-design]], [[strategy/questions-for-salvatore]].
- **Pagine aggiornate**: [[system/decision-log]] (9 decisioni chiuse nuove + tabella aperte con colonna Owner + riferimenti), [[system/modules/data-layer]] (storage time-series, mantainer confermato, queue extractor, deploy/recovery), [[system/modules/execution]] (adapter broker intercambiabili, transaction cost auto-adattivo), [[system/modules/agents]] (conviction dal PM, monitoring da SFC, link), [[system/modules/quant-backtesting]] (calcolo fattori interno, VectorBT, link Salvatore), [[system/stack]] (broker Alpaca→IBKR), [[_meta/glossario]] (Kelly, overfitting, conviction, adapter, time-series, subgraph), [[system/ideas-log]] (sezione 2026-06-02).
- **Board ridisegnata** ([[artifacts/project-board]]): centrale operativa, owner 🛠/📈/🔀 + `→ [[pagina]]` su ogni card, prossimi 2 passi in testa.
- **CLAUDE.md**: nuova sezione "Centrale operativa — la Board" (convenzione board-hub, owner, riferimenti, creare pagine).
- **Meta**: [[_meta/index]] (6 link nuovi), [[_meta/hot-cache]] (sessione + decisioni). `taxonomy.md` invariato.
- **Follow-up 2026-06-03**: Luca conferma di aver commentato l'intera analisi. Aggiunti: **subgraph come pattern granulare** ([[system/parallelism-design]]); **disinvestimento a 2 livelli** automatico/valutato ([[system/rating-scoring]], [[system/modules/execution]]); **alternative di attivazione alert** esplicitate ([[system/modules/data-layer]]); **trailing stop loss** in glossario; punto **legale parcheggiato** ([[system/ideas-log]]). Corretta la nota "fermato a metà" in hot-cache.
- **Follow-up 2026-06-03 (idee iniziali)**: Luca chiede di recuperare le idee iniziali sparse — "agent di reportistica su cosa va male" e "ponderazione pesi degli agent del desk". Ricostruite dalle fonti (ideas-log 2026-05-21, architecture Layer 5, mvp, glossario) e **unificate** in nuova pagina [[system/learning-feedback-loop]] (substrato logging · reportistica diagnostica · scoring agenti · ponderazione pesi · feedback post-trade). Decisione di Luca: **reportistica = modulo deterministico + narrazione** (tenuto come opzione, non agente dedicato). Aggiornati: [[system/rating-scoring]] (§2/§4 → link), [[system/architecture]] (Layer 5 + reportistica), [[system/mvp]] (post-MVP + substrato), [[system/modules/agents]] (TODO), [[_meta/index]], [[system/ideas-log]], [[artifacts/project-board]] (3 card nuove + decisione aperta punto di aggancio pesi).

## [2026-05-29] refactor strutturale | Riorganizzazione completa per argomento + moduli da canvas

- **Trigger**: "rifattorizzare completamente la struttura tree e di file della wiki" → "eliminiamo references" → "i moduli vanno rifatti, non rispettano `architettura.canvas`"
- **Decisioni di struttura (con Luca)**: dissolvi-del-tutto le call (date inline, no `journal/`); naming inglese; PM = agente LLM orchestratore; moduli decomposti per aree del canvas (4 file).
- **Rinominazioni cartelle**: `build/` → `system/`; `references/` **eliminata**.
- **`references/` smistata**: prior-art → `prior-art/{tradingagents,libraries,papers}/`; `tool-set-provider` → [[system/data-providers]]; `onboarding-wiki-workflow` → [[_meta/onboarding]]; `trading-floor-canvas` → [[artifacts/trading-floor]]; `note-audio-salvatore` dissolto in nuova [[strategy/methods/dual-portfolio]].
- **Moduli ricreati su `architettura.canvas`**: eliminati `exchange-db`, `llm-agent-system`, `risk-management`; creati [[system/modules/data-layer]] (DB-hub + extraction + mantainer), [[system/modules/agents]] (PM orchestratore + 2 desk + Risk Analyst/Statuto), [[system/modules/execution]] (Investment State → Trade → Exchange); [[system/modules/quant-backtesting]] mantenuto. [[system/architecture]] riallineata (2 desk, mantainer, PM agente, canvas `architettura.canvas`).
- **Dissolte ed eliminate** (grezzi in `raw/archived/`): 8 call (`conversazione`/`videochiamata`/`whatsapp`) + `architecture-handwritten-notes` + `note-audio-salvatore`.
- **Link**: riscritti tutti i wikilink path-qualified + bare + alias; rimosse le `sources:` verso le call dissolte; provenienza ora inline (date). Verifica: 0 link rotti fuori da questo log (le voci storiche qui sotto conservano i nomi dell'epoca).
- **Meta aggiornati**: [[_meta/taxonomy]] (path nuovi, righe morte marcate), [[_meta/index]] (riscritto), [[overview]], [[_meta/hot-cache]].



- **Trigger**: `/wiki-lint` — "rivediamo completamente la struttura della wiki per farla funzionare meglio con le cose discusse nelle ultime call"
- **Lint**: 1 link rotto (`dev-roadmap.canvas`), 1 ambiguo (`trading-floor.canvas` duplicato), 1 orfana (`tradingagents-graph-schema`), 1 conflitto (Trader), 54 file spazzatura, 3 file pending. Freshness: nessun problema >90gg.
- **Riallineamenti contenuto**:
  - [[system/architecture]] riscritta sulla topologia 2026-05-29 (PM orchestratore → analisti → research_state → Risk Analyst gate → Trade deterministico; Layer DB esteso/Extractors/gate; protocollo state+DB con context rot; sequenza di sviluppo "riscrivere il grafo")
  - [[system/modules/agents]] **conflitto Trader risolto**: Funzione + sezione Leva riallineate (segnale `Strong` nel research_state validato dal Risk Analyst, esecuzione deterministica); Dipendenze/TODO aggiornati
  - [[system/modules/data-layer]] **schema DB consolidato** (5 tabelle core ↔ 4 aree logiche, mapping unico)
- **Ingest pending**:
  - daily-note 2026-05-28 (storage SQL vs JSON) → domanda aperta in [[system/modules/data-layer]] e [[system/decision-log]]
  - daily-note 2026-05-29 (tool per indicatori + SFC) → sezione tool-centric di [[system/modules/agents]]
  - transcript 05-13 → pagina [[references/videochiamata-luca-salvatore-2026-05-13]] già completa; archiviato, raw_source_path corretto
- **Fix link rotti**: `ops/wiki-restructuring-plan` (2×), `external/trading-agents-framework` (2×), `tradingagents-graph.canvas` (2×, canvas eliminato da Luca)
- **Pages updated**: [[system/architecture]], [[system/modules/agents]], [[system/modules/data-layer]], [[system/decision-log]], [[_meta/index]], [[references/videochiamata-luca-salvatore-2026-05-13]], [[prior-art/tradingagents/code-wiki]], [[prior-art/tradingagents/graph-schema]], [[_meta/hot-cache]]
- **Deleted**: 54 frammenti `raw/audio/.txt*.txt`; stub `wiki/artifacts/artifact-workbench.md`
- **Archived**: `raw/archived/daily-notes/2026-05-28.md`, `2026-05-29.md`; `raw/archived/audio/2026-05-13 13-14-17.txt` (+.tmp.mp3)
- **Canvas**: Luca ha riorganizzato in Obsidian in parallelo → tutti sotto `artifacts/` (design in `artifacts/architecture/`); eliminati da lui `mvp-system-cycle.canvas`, `trading-floor.canvas` (root), `tradingagents-graph.canvas`. `wiki/build/architecture/` non esiste più.
- **Conflicts**: il conflitto Trader (segnalato nell'ingest precedente) è stato **risolto** in questa sessione.
- **Notes**: vedi anche il cleanup pass 2 sotto.

## [2026-05-29] cleanup | Rimozione ridondanze + link rotti residui

- **Trigger**: richiesta utente — "tenere tutto pulito, togliere informazioni ridondanti, file non essenziali"
- **Refactor**: [[system/mvp]] — rimossi *Ciclo operativo* (vecchia topologia, duplicava [[system/architecture]]) e *Decisioni fondanti* (duplicavano [[system/decision-log]], con dati stale su crypto/Binance/DeepSeek 1/20); allineato a stock-only + topologia 29/05; **mantenuti** metriche a due livelli, backtesting integrato, sequenza track, insight NotebookLM
- **Deleted**: `wiki/artifacts/kanban-project-status.md` — stale (06/05), `type:ops` (ruolo eliminato dalla taxonomy), "Blocked: Crypto vs Equity" già chiuso, ridondante con [[artifacts/luca-board]] + [[artifacts/salvatore-board]] + [[system/decision-log]]. Riferimenti sistemati in [[_meta/index]] e [[references/videochiamata-luca-salvatore-2026-04-30]]
- **Link rotti risolti**: `[[strategy/]]`→`[[strategy/index]]` (quant-backtesting); 3 stub metriche in [[strategy/methods/trend-following]] → testo semplice; `[[raw/daily-notes/2026-05-19]]` in [[system/ideas-log]] → path archiviato
- **Pages updated**: [[system/mvp]], [[_meta/index]], [[references/videochiamata-luca-salvatore-2026-04-30]], [[system/modules/quant-backtesting]], [[strategy/methods/trend-following]], [[system/ideas-log]], [[_meta/hot-cache]]
- **Stato finale**: 0 link rotti reali nella wiki

## [2026-05-29] ingest | Due videochiamate Luca & Salvatore 29/05 — LangChain/LangGraph + design architettura custom

- **Type**: call (2 videochiamate, trascrizioni audio)
- **Sources raw**:
  - `raw/archived/2026-05-29 11-08-30.txt` — call mattina (TradingAgents/LangGraph spiegato + decisione portfolio vs day-trading)
  - `raw/archived/2026-05-29 14-41-53.txt` — call pomeriggio (design su `agents.canvas`)
- **Pages created**:
  - [[references/videochiamata-luca-salvatore-2026-05-29]]
  - [[strategy/metrics/benchmark]]
- **Pages updated**:
  - [[system/modules/agents]] (topologia agenti, Trade deterministico, PM orchestratore, context rot, OpenRouter/DeepSeek)
  - [[system/modules/data-layer]] (design DB esteso, extractors, market alert, retention)
  - [[system/modules/agents]] (Risk Analyst gate bear + guardrail deterministici)
  - [[system/modules/quant-backtesting]] (posizione TA/fondamentali/sentiment)
  - [[system/decision-log]] (10 decisioni chiuse del 29/05 + aggiornate aperte)
  - [[system/stack]] (OpenRouter, DeepSeek V4 Pro + costi, storage)
  - [[wiki/overview]], [[strategy/index]], [[artifacts/luca-board]], [[artifacts/salvatore-board]], [[_meta/index]], [[_meta/hot-cache]]
- **Conflicts**: segnalato (non risolto automaticamente) — vecchio "LLM Trader produce JSON" + "agente Esecutore gestisce leva" in [[system/modules/agents]] vs nuovo "Trade = funzione Python deterministica". Da riconciliare dove vive la logica leva via opzioni.
- **Skipped**: nessuno (`raw/notes/` conteneva solo `.DS_Store`)
- **Notes**: Sessione di design molto densa. Confermato il pivot definitivo a gestione di portafoglio mid-term stock-only; definita la topologia del grafo da costruire (riscrittura su base TradingAgents), il DB esteso ispirato alla dashboard SFC, e lo stack LLM (OpenRouter + DeepSeek V4 Pro). [[system/architecture]] resta da allineare alla nuova topologia.

## [2026-05-27] update | Decoupling logic segnali Strong Buy/Sell da agenti specifici

- **Change**: Scollegata esplicitamente la logica dei segnali ad alta convinzione (Strong Buy e Strong Sell) per la leva con opzioni da una tipologia rigida di agenti (come i "Ricercatori"). Il calcolo e la validazione della convinzione sono trattati come concetti/task di sistema, e l'assegnazione finale del ruolo all'agente o nodo più idoneo avverrà durante la mappatura granulare del grafo LangGraph.
- **Pages updated**: [[references/conversazione-luca-salvatore-2026-05-27]], [[system/modules/agents]], [[system/modules/agents]], [[system/decision-log]]

## [2026-05-27] ingest | Brainstorming Luca & Salvatore 27/05 — Ricercatori/Esecutori + Statuto 10% + Opzioni Leva + Token Cost Estimator + Piero Site

- **Type**: chat + 18 note vocali WhatsApp (brainstorming architetturale e operativo)
- **Sources raw**:
  - `raw/daily-notes/2026-05-27.md` — log chat WhatsApp del 27 maggio 2026
  - `raw/audio/WhatsApp Audio 2026-05-27 at *` (18 file trascrizioni .md) — note vocali Salvatore trascritte
- **Pages created**:
  - [[references/conversazione-luca-salvatore-2026-05-27]]
- **Pages updated**:
  - [[system/modules/agents]] (suddivisione Ricercatori/Esecutori, opzioni leva, integrazione LangSmith)
  - [[system/modules/agents]] (Statuto deterministico, riserva liquidità 10%, OpenRouter LLM cost estimator)
  - [[system/decision-log]] (aggiunte 5 decisioni chiuse e 4 aperte/aggiornate del 27/05)
  - [[_meta/index]] (collegata nuova source page delle referenze)
  - [[_meta/hot-cache]] (aggiornato contesto sessione, decisioni e pending ingests)
- **Contradictions**: nessuna
- **Notes**: Sessione estremamente prolifica che sposta l'orizzonte operativo verso un modello "Wealth Manager" autonomo ("Piero") basato su stock-only e leva controllata tramite acquisto opzioni (Call/Put), tracciato con LangSmith e regolato da uno Statuto istituzionale rigido con 10% liquidità disinvestita costante.

## [2026-05-27] ingest | Daily Notes 19-22-23-25-26/05 + WhatsApp chat 22/05 + Istruzioni wiki

- **Type**: daily notes (idee tecniche) + chat WhatsApp (test TradingAgents) + istruzioni wiki (scope + struttura)
- **Sources raw**:
  - `raw/daily-notes/2026-05-19.md` — appunti lettura TradingAgents Code Wiki + istruzioni wiki
  - `raw/daily-notes/2026-05-22.md` — idee architetturali e organizzative
  - `raw/daily-notes/2026-05-23.md` — istruzioni wiki: scope stock-only, dismetti moduli sequenziali, LangChain
  - `raw/daily-notes/2026-05-25.md` — LangSmith, Mermaid, evaluation CLI
  - `raw/daily-notes/2026-05-26.md` — conversazione Luca+Salvatore su report TradingAgents NVDA
  - `raw/audio/WhatsApp Chat - Salvatore Luca/_chat.txt` — chat WhatsApp 22/05 test NVDA
  - `raw/audio/WhatsApp Chat - Salvatore Luca/*.opus` (6 file) — audio Salvatore, richiedono wiki-preprocess
- **Pages created**:
  - [[references/whatsapp-luca-salvatore-2026-05-22]]
  - [[references/conversazione-luca-salvatore-2026-05-26]]
- **Pages updated**:
  - [[system/ideas-log]] (aggiunte sezioni 22/05, 25/05, 26/05)
  - [[system/stack]] (aggiunta sezione AI Agent Framework: LangChain, LangSmith, Mermaid, struttura repo)
  - [[system/decision-log]] (aggiunte 7 decisioni chiuse 2026-05-19/23/26; chiuse 3 aperte: fork, multi-asset, debate)
  - [[system/modules/data-layer]] (rinominato da module-a-exchange-db; scope stock-only, exchange da scegliere)
  - [[system/modules/quant-backtesting]] (rinominato da module-c-quant-backtest; aggiornati riferimenti)
  - [[system/modules/agents]] (rinominato da module-d-prompt-builder-trader; Bull/Bear agents eliminati)
  - [[system/modules/agents]] (rinominato da risk-analyst; aggiornati riferimenti)
  - [[_meta/index]] (aggiornati link moduli + aggiunte 2 nuove source page)
- **Contradictions**: Scope decisione 2026-04-30 (crypto) contradetto da 2026-05-23 (stock-only) → risolto a favore della più recente
- **Notes**: 6 file .opus trascritti con Whisper medium in questa sessione. 1 .m4a (2026-05-13) ancora pending. Audio contenevano: valutazione report NVDA, analisi del ragionamento AI vs bias, rischio sistemico AI trading, contesto S&P500 Mag7.

## [2026-05-22] ingest | Tool Set Provider Dati Exchange + Note Quant Salvatore + Brenndoerfer + Update videochiamata-05-13

- **Type**: note (provider dati) + audio notes (strategie quant) + article (quant trading)
- **Sources raw**:
  - `raw/notes/Tool Set, Provider dati, Exchange.md` → archiviato
  - `raw/articles/quant strategy/*.txt` (6 file, 2 trascrizioni uniche) → da archiviare
  - `raw/articles/quant strategy/Quantitative Trading Strategies...md` → da archiviare
  - `raw/audio/Bella, Come tutto bene?...txt` → da archiviare (contenuto extra aggiunto a videochiamata-05-13)
  - `raw/notes/sessione-brainstorming-2026-05-13.md` → archiviato (già ingestato come mvp-prototype-design)
  - `raw/daily-notes/2026-05-13.md` → archiviato (contenuto minimalissimo, già coperto)
  - `raw/daily-notes/2026-05-14.md` → archiviato (contenuto minimalissimo, già coperto)
  - `raw/audio/Come stai tutto bene?...txt` → da archiviare (già ingestato come videochiamata-05-06)
  - `raw/audio/così ce l'abbiamo...txt` → da archiviare (già ingestato come videochiamata-04-30)
  - `raw/audio/Invece Obsidian...txt` → da archiviare (già ingestato come videochiamata-04-30)
- **Pages created**:
  - [[system/data-providers]]
  - [[strategy/methods/dual-portfolio]]
  - [[prior-art/papers/brenndoerfer-quant-trading]]
  - [[strategy/methods/mean-reversion-stat-arb]]
- **Pages updated**:
  - [[references/videochiamata-luca-salvatore-2026-05-13]] (aggiunto sez. 8-11: struttura multi-agente verbale Salvatore, order book crypto, fork vs from scratch, sequenza operativa)
  - [[strategy/index]] (aggiunto mean-reversion-stat-arb)
  - [[_meta/index]] (aggiunte 4 nuove pagine + mean-reversion a strategy)
- **Contradictions**: nessuna
- **Notes**: 4 file audio confermati come già ingestati in sessioni precedenti. File quant strategy contenevano 2 trascrizioni uniche duplicate. Daily notes erano minimalissime. I file audio da archiviare richiedono permesso bash — da completare manualmente.

## [2026-05-22] update | CLAUDE.md riscritto

- **Change**: CLAUDE.md ridotto all'osso e reso resistente a ristrutturazioni future
- **Rimosso**: struttura vault hardcodata, riferimenti a cartelle eliminate (ops/, theory/, decisions/), dataview queries obsolete, tipi frontmatter non più usati
- **Aggiunto**: delega esplicita dei path a taxonomy.md, tabella skill operative, regola di precedenza (taxonomy.md vince su path)
- **Principio**: se la struttura cambia → si aggiorna taxonomy.md, non CLAUDE.md

## [2026-05-21] lint | Wiki health check + fix

- **Link rotti risolti** (~35 link su 12 pagine): `[[theory/*]]` → `[[system/architecture]]`, `[[decisions/decision-log]]` → `[[system/decision-log]]`, `[[ops/*]]` → rimossi o redirectati verso `artifacts/`
- **raw_source_path corretti**: `references/trading-floor-canvas.md` (puntava a file mancante), `references/videochiamata-luca-salvatore-2026-04-30.md` (m4a mancante → svuotato)
- **Merge duplicati**: `references/external/trading-agents-framework.md` → contenuto incorporato in `references/external/paper-trading-agents.md` + eliminato; `references/library-portfolio-optimizer.md` → contenuto incorporato in `references/external/cvx-portfolio-optimizer.md` + eliminato
- **Pagina orfana risolta**: `artifacts/idea architettura.canvas` aggiunto all'index
- **overview.md**: fix link `[[references/_meta/index]]` → `[[_meta/index]]`
- **Index aggiornato**: path completi per paper, rimozione duplicati, aggiunta canvas orfano
- **hot-cache aggiornato**: struttura wiki con ideas-log.md e external/ corretti
- **Pending ingest**: lanciato subagent in background per i raw pendenti (sessione-brainstorming-2026-05-13, quant strategy txts, Tool Set note, daily-notes 13-14 maggio, audio txts)

## [2026-05-21] ingest | TradingAgents Code Wiki + note di lettura Luca

- **Type**: article (code wiki) + note (daily note 2026-05-19)
- **Source raw**: `raw/articles/TradingAgents Code Wiki.md`, `raw/daily-notes/2026-05-19.md`
- **Pages created**: [[prior-art/tradingagents/code-wiki]], [[system/ideas-log]]
- **Pages updated**: [[system/modules/agents]] (riscritto da raw dump a pagina strutturata), [[system/architecture]] (pattern architetturali: look-ahead bias doppia data, DB-first, indicatori dal DB), [[system/decision-log]] (nuove decisioni: DB-first, LangGraph, agent philosophy, look-ahead bias; aperte: fork vs from scratch, self-scheduling, debate architecture)
- **Contradictions**: decisione "From scratch" (2026-04-30) vs. "fork da TradingAgents" (2026-05-19, Luca) — segnalata nel decision-log, da formalizzare
- **Notes**: ideas-log.md creato come file append-only su richiesta di Luca per raccogliere tutte le idee del progetto

## [2026-05-14] update | Aggiunta sezione strategy/
- **Operazione**: recuperata la distinzione build/ (software, Luca) vs strategy/ (conoscenza mercato, Salvatore)
- **Cartelle create**: `strategy/`, `strategy/methods/`, `strategy/indicators/`, `strategy/metrics/`
- **File creati**: [[strategy/index]], [[strategy/methods/trend-following]], [[strategy/methods/factor-investing]]
- **File aggiornati**: [[system/modules/quant-backtesting]] (link a strategy/), [[_meta/taxonomy]], [[_meta/index]], [[overview]]

## [2026-05-13] restructure | Ristrutturazione completa del vault
- **Operazione**: ristrutturazione della wiki da struttura generica a struttura orientata al progetto
- **Cartelle eliminate**: `ops/`, `theory/`, `agents/`, `decisions/`, `questions/`
- **Cartelle create**: `build/modules/`, `references/external/`
- **File creati**: [[system/decision-log]], [[system/stack]], [[system/modules/data-layer]], [[system/modules/quant-backtesting]], [[system/modules/agents]], [[system/modules/agents]], [[references/external/trading-agents-framework]], [[prior-art/libraries/cvx-portfolio-optimizer]], [[_meta/glossario]]
- **File aggiornati**: [[system/architecture]] (merge theory/), [[system/mvp]] (link fix), [[overview]], [[_meta/index]], [[_meta/taxonomy]]
- **Logica**: ops/ → board; theory/ → build/system-map; agents/ → references/external/; decisions/ → build/decision-log; questions/ → inline nei module files e nelle board

## [2026-05-13] ingest | Videochiamata Luca-Salvatore 2026-05-13
- **Type**: call (trascrizione audio)
- **Source**: `raw/audio/2026-05-13 13-14-17.m4a` + trascrizione `.txt`
- **Pages created**: [[references/videochiamata-luca-salvatore-2026-05-13]], [[ops/wiki-restructuring-plan]]
- **Pages updated**: [[decisions/decision-log]], [[_meta/index]]
- **Contradictions**: nessuna
- **Notes**: Temi principali: trend following come strategia (Moncler example), value investing non scalabile per ora, walk-through architettura e canvas con Salvatore, struttura proposta per sezione quant wiki, workflow Salvatore in Obsidian, piano ristrutturazione wiki (pianificato, non eseguito). Insight critico: effetto FX obbligatorio da considerare su asset con ricavi internazionali.

## [2026-05-13] artifact | Canvas + Glossario — artifact duraturi per il team
- **Pages created**: [[artifacts/mvp-system-cycle.canvas]], [[artifacts/dev-roadmap.canvas]], [[ops/glossario]]
- **Pages updated**: [[syntheses/notebooklm-research-2026-05-13]] (aggiunti riferimenti precisi ai paper), [[_meta/index]]
- **Notes**: canvas del ciclo operativo e roadmap di sviluppo per spiegare a Salvatore; glossario aggiornabile in italiano; tabella riferimenti ai paper nella synthesis

## [2026-05-13] synthesis | Ricerca NotebookLM — Approcci da progetti simili AI+Finance
- **Type**: research session (NotebookLM query su 43 fonti)
- **Pages created**: [[syntheses/notebooklm-research-2026-05-13]]
- **Pages updated**: [[system/mvp]], [[decisions/decision-log]], [[_meta/index]]
- **Decisioni chiuse**:
  - Framework backtesting: **VectorBT** (usato da MarketSenseAI)
  - LLM principale: **DeepSeek** confermato (Alpha Arena: miglior costo/perf)
  - SL/TP: obbligatori come hard constraint (Simone Rizzo: senza → drawdown devastante)
  - Output LLM: JSON strutturato obbligatorio (tutti i framework convergono)
  - Prophet: **non usare** come forecast principale (non regge i crolli)
- **Nuovi insight operativi**: Quick+Deep Thinker pattern, Pivot Points nel Prompt Builder, Rebalancing Gate, Black-Litterman per views LLM → pesi portfolio
- **Notes**: Qwen 3 Max +22.88% in Alpha Arena (sorpresa), ma non ancora disponibile facilmente. DeepSeek al secondo posto (+4.76%), Claude -33%.

## [2026-04-30] init | Inizializzazione vault
- **Pages created**: [[overview]], [[_meta/index]], [[_meta/log]], [[_meta/taxonomy]], [[_meta/hot-cache]]
- **Vault type**: project wiki
- **Project shape**: software + research + economic
- **Collaborators**: 2
- **Notes**: bootstrap iniziale della wiki

## [2026-04-30] bootstrap | Hub pages create
- **Pages created**:         
- **Pages updated**: [[overview]], [[_meta/index]]
- **Notes**: resi navigabili i principali ingressi della wiki

## [2026-04-30] update | Skill mapping locale
- **Pages updated**: [[AGENTS]]
- **Notes**: aggiunti adattamenti locali per le skill `wiki-*` e policy d'uso per artifact, preprocess e query

## [2026-04-30] update | Wiki skills generalized
- **Pages updated**: [[AGENTS]]
- **Notes**: refactor delle skill `wiki-init`, `wiki-ingest`, `wiki-query`, `wiki-save`, `wiki-lint`, `wiki-artifact`, `wiki-preprocess` per renderle context-aware e riusabili tra vault di progetto e second brain

## [2026-04-30] update | Operational surface hardened
- **Pages created**: [[ops/dashboard]], [[ops/current-state]], [[ops/backlog]], [[system/architecture]], [[decisions/decision-log]], [[questions/open-questions]], [[artifacts/artifact-workbench]]
- **Pages updated**: [[overview]],      [[_meta/index]], [[AGENTS]]
- **Notes**: aggiunta una superficie operativa pronta all'uso con dashboard, backlog, stato corrente, system map e registri iniziali

## [2026-05-13] brainstorming | Design MVP Prototype
- **Partecipanti**: Luca, Claude Code
- **Pages created**: [[system/mvp]]
- **Pages updated**: nessuna (aggiornamento index pendente)
- **Raw**: `raw/notes/sessione-brainstorming-2026-05-13.md`
- **Decisioni chiuse**:
  - Architettura: monolite modulare (Opzione A)
  - Tipo prototipo: agente autonomo paper trading + backtesting continuativo + metriche
  - Orizzonte trade: swing trading (4h/daily)
  - Sequenza sviluppo: Modulo A (Exchange+DB, Luca solo) in parallelo con progettazione Modulo C (Quant+Backtest, con Salvatore), poi Modulo D (Prompt Builder + LLM Trader)
  - Ciclo raffinato: Risk Analyst è upstream del Trader (fonte: trading-floor.canvas)
  - Portfolio architecture-first, single-asset deployment nel MVP
- **Decisioni ancora aperte**: framework backtesting (vectorbt vs backtesting.py), strategia del fondo (formalizzare con Salvatore)
- **Notes**: prima sessione di design strutturata con agent; raw note contiene tutto il materiale grezzo

## [2026-04-30] ingest | Conversazione progettuale Luca-Salvatore
- **Type**: call / note
- **Pages created**: [[references/conversazione-luca-salvatore-2026-04-28-30]], [[theory/modular-trading-agent-architecture]], [[theory/trader-workflow-automation]]
- **Pages updated**: [[overview]], [[ops/dashboard]], [[ops/current-state]], [[ops/backlog]], [[system/architecture]], [[decisions/decision-log]], [[questions/open-questions]],   [[_meta/index]]
- **Contradictions**: nessuna
- **Notes**: ordinato un bundle di audio, trascrizioni e appunti tra Luca e Salvatore; escluse le parti strettamente personali non rilevanti

## [2026-04-30] artifact | kanban | Stato Progetto
- **File**: [[kanban-project-status]]
- **Based on**: [[ops/dashboard]], [[ops/current-state]], [[ops/backlog]], [[system/architecture]], [[decisions/decision-log]], [[questions/open-questions]], [[references/conversazione-luca-salvatore-2026-04-28-30]]

## [2026-04-30] ingest | Videochiamata Luca-Salvatore (2026-04-30)
- **Type**: video-call
- **Pages created**: [[references/videochiamata-luca-salvatore-2026-04-30]]
- **Pages updated**: [[theory/modular-trading-agent-architecture]], [[system/architecture]], [[kanban-project-status]], [[ops/backlog]], [[_meta/index]]
- **Contradictions**: nessuna
- **Notes**: Ingestiti i due transcript della videochiamata odierna. Definita l'architettura multi-agente e la roadmap verso la dashboard di augmentazione.

## [2026-05-06] artifact | kanban | Kanban — Stato Progetto
- **File**: [[kanban-project-status]]
- **Based on**: aggiornamenti di sessione

## [2026-05-06] update | Correzione file allucinati
- **Change**: Rimossi output AI allucinati da `raw/archived/articles/Private & Shared/Trading Agent 3192e441b0e580d5921bf33f9b559735.md` e riscritta la pagina `[[references/videochiamata-luca-salvatore-2026-05-06]]` basata sul vero transcript `raw/transcripts/2026-05-06 13-29-25.txt`.
- **Pages updated**: [[references/videochiamata-luca-salvatore-2026-05-06]], [[Trading Agent 3192e441b0e580d5921bf33f9b559735]]
- **Notes**: Il file della fonte originariamente conteneva allucinazioni dell'agente che sono state eliminate.

## [2026-05-10] ingest | Videochiamata Luca-Salvatore (2026-05-06) — trascrizione completa
- **Type**: call (trascrizione ad alta fedeltà, versione molto più completa della precedente)
- **Source**: `raw/audio/Come stai tutto bene?...txt`
- **Pages updated**: [[references/videochiamata-luca-salvatore-2026-05-06]], [[theory/modular-trading-agent-architecture]], [[decisions/decision-log]], [[questions/open-questions]], [[artifacts/luca-board]], [[artifacts/salvatore-board]]
- **Contradictions**: nessuna — la nuova trascrizione ha aggiunto molta più sostanza rispetto alla versione breve precedente
- **Notes**: Nuovi contenuti chiave: trading singolo vs portfolio bilanciato (decisione centrale aperta), multi-asset vs solo cripto, principio deterministico (LLM solo per ragionamento, tutto il resto Python deterministico), costo token come vincolo architetturale, modelli cinesi open source (DeepSeek) 1/20 del costo su Google Cloud, correlazione intra-crypto con allocazione dinamica nel basket, regole del portafoglio stile fondo professionale (statuto anti-bias), framing "AI Investment Fund / Factory", Luca inizia modulo analisi documenti

## [2026-05-10] artifact | kanban | Luca Board — board personale (tecnico)
- **File**: [[luca-board]] (in `wiki/artifacts/`)
- **Based on**: [[ops/backlog]], [[decisions/decision-log]], [[questions/open-questions]], [[references/videochiamata-luca-salvatore-2026-04-30]], [[references/videochiamata-luca-salvatore-2026-05-06]]
- **Notes**: riorientata su focus tecnico/AI/programmazione dopo chiarimento ruoli del team

## [2026-05-10] artifact | kanban | Salvatore Board — board personale (economico)
- **File**: [[salvatore-board]] (in `wiki/artifacts/`)
- **Based on**: [[ops/backlog]], [[decisions/decision-log]], [[questions/open-questions]], [[references/videochiamata-luca-salvatore-2026-04-30]], [[references/videochiamata-luca-salvatore-2026-05-06]]
- **Notes**: focus su dominio economico/trading, meccanismi di mercato reale, fattori, strategie

## [2026-05-10] update | Integrazione trascrizioni alta fedeltà — videochiamata 2026-04-30
- **Type**: re-ingest / enrichment
- **Sources**: `raw/audio/così ce l'abbiamo...txt`, `raw/audio/Invece Obsidian...txt` (trascrizioni ad alta fedeltà della videochiamata 2026-04-30)
- **Pages updated**: [[references/videochiamata-luca-salvatore-2026-04-30]], [[theory/modular-trading-agent-architecture]], [[system/architecture]], [[decisions/decision-log]], [[questions/open-questions]], [[ops/backlog]]
- **Contradictions**: nessuna — le nuove trascrizioni hanno aggiunto dettaglio, non contraddetto contenuto esistente
- **Notes**: Le trascrizioni ad alta fedeltà hanno rivelato dettagli non presenti nella versione precedente: Prompt Builder come componente architetturale esplicito, meccanismo di esecuzione (limit order + SL + TP + leva), Binance come exchange scelto, problema needle-in-haystack, Factor Investigation Agent come agente separato, metodologia di quantificazione dei fattori (media empirica su serie storiche), strategia Sentiment degli Analisti (idea di King), Volume Spike module, specifiche su FinAgent (Cornell, ~50k stelle, Claude 4° contributore) e AlphaArena (confronto 5 LLM su Bitcoin). Aggiunte 5 decisioni chiuse nel decision log.

## [2026-05-12] ingest | TradingAgents, Alpha Arena & Portfolio Optimizer
- **Type**: research paper / library documentation
- **Pages created**: [[prior-art/tradingagents/paper]], [[prior-art/papers/alpha-arena]], [[references/library-portfolio-optimizer]], [[references/architecture-handwritten-notes]], [[agents/trading-agents-framework]], [[agents/cvx-portfolio-optimizer]]
- **Pages updated**: [[theory/modular-trading-agent-architecture]], [[system/architecture]], [[_meta/index]]
- **Contradictions**: nessuna
- **Notes**: Ingest completa di materiale tecnico di frontiera. TradingAgents introduce il protocollo di comunicazione strutturata e il team di analisti/debater. Portfolio Optimizer (cvx-optimizer) fornisce il motore per il Portfolio Management quantitativo e l'integrazione di opinioni (views) via Black-Litterman. Alpha Arena fornisce benchmark comparativi tra LLM. La system map ora include esplicitamente il portfolio manager e il protocollo di comunicazione strutturato.

## [2026-05-29] ingest+update | Ingest 3 repo GitHub + consolidamento board (migrazione da copia Downloads)

- **Type**: code-ingest + consolidamento artifact
- **Contesto**: il lavoro era stato fatto per errore su una copia git in `~/Downloads/trading-agent-wiki` (repo senza commit, lineage più vecchio). Migrato qui sul vault vero in modo **chirurgico** (solo i deliverable di sessione, innestati sul contenuto attuale di DST). Backup del vault creato in `~/Downloads/trading-agent-wiki-iCloud-backup-<timestamp>` prima del merge.
- **Pages created**: [[prior-art/libraries/rizzo-trading-agent]], [[prior-art/libraries/sfc-portfolio-tracker]], [[artifacts/project-board]]
- **Pages updated**: [[prior-art/libraries/cvx-portfolio-optimizer]] (sezione piattaforma full-stack + BAML LLM-views + frontmatter), [[system/modules/data-layer]], [[system/modules/quant-backtesting]], [[system/modules/agents]], [[system/modules/agents]] (sezioni "Riferimenti di codice (repo esterni)"), [[_meta/index]], [[overview]]
- **Pages deleted**: artifacts/luca-board.md, artifacts/salvatore-board.md (consolidate in project-board; kanban-project-status già rimossa in precedenza)
- **Sources**: github.com/SilvioBaratto/optimizer, github.com/Rizzo-AI-Academy/rizzo-trading-agent, github.com/Sbirrondi/sfc-portfolio-tracker
- **Consolidamento board**: project-board ricostruita dal contenuto ATTUALE di luca-board + salvatore-board in DST (NON dalle versioni vecchie di Downloads): preserva decisioni risolte 2026-05-29 (LangGraph, OpenRouter+DeepSeek V4 Pro, portfolio/mid-term, stock-only+benchmark) e i task nuovi (grafo LangGraph, Extractors, market driver, valuation, P/E). Colonne per stato + marker dominio (🛠/📈/🔀). Decisioni storiche superate annotate inline (*aggiornata:*).
- **Conflicts**: nessuna perdita. Verificato che DST non conteneva alcun deliverable di sessione; che la kanban-project-status cancellata era la versione generica (nessun item unico); che le board DST erano più recenti delle versioni di Downloads (→ ricostruzione da DST).
- **Skipped**: NON migrati gli altri file divergenti tra le due copie (decision-log, stack, system-map, tradingagents-*, ecc.): appartengono al lineage e non fanno parte di questa sessione.
- **Notes**: i raw non archiviati (sorgenti = URL GitHub). La copia Downloads resta intatta come riferimento.
