---
title: "Project Board — Trading Agent"
type: artifact
tags:
  - artifact
  - roadmap
  - execution
  - architecture
created: 2026-04-30
updated: 2026-06-04
status: active
related:
  - "[[system/architecture]]"
  - "[[system/decision-log]]"
  - "[[system/stack]]"
  - "[[system/ideas-log]]"
  - "[[strategy/questions-for-salvatore]]"
confidence: high
priority: high
area: ops
kanban-plugin: board
sources:
  - "[[prior-art/papers/notion-trading-concepts]]"
  - "[[artifacts/trading-floor]]"
---

> # 🧭 Centrale operativa del progetto
> Questo è il **file di partenza** per ogni valutazione umana: ogni voce dice **chi** (owner) e **dove approfondire** (pagina specifica). Da qui si naviga al resto della wiki.
>
> **Owner**: 🛠 Luca (software) · 📈 Salvatore (mercato) · 🔀 condiviso.
> **Convenzione**: ogni card azionabile termina con il link alla pagina di riferimento `→ [[pagina]]`. Le decisioni chiuse sono in [[system/decision-log]]; il dettaglio domande mercato in [[strategy/questions-for-salvatore]].
>
> **🎯 Prossimi due passi concordati (2026-06-02)**: 1) strutturare lo schema dello state → [[system/state-schemas]]; 2) definire la formula di position sizing → [[system/position-sizing]].

## 💡 Idee

- [ ] 🛠 **Sistema di rating/scoring a livelli** — conviction trade + valutazione lavoro agenti + rating asset → [[system/rating-scoring]]
- [ ] 🛠 **Scheda ticker auto-aggiornante nel DB** — ogni ticker ha la sua page con valutazione corrente, gestione staleness → [[system/parallelism-design]]
- [ ] 🛠 **Layer di "valutatori" per ticker** — thread separato per ticker tra PM e desk → [[system/parallelism-design]]
- [ ] 🛠 **"News anomale" come miccia dell'origination** — terzo tipo di alert che attiva il PM → [[system/ideas-log]]
- [ ] 🛠 **"TV/dashboard del DB" (TG24)** — vista in stile news sullo stato del DB → [[system/ideas-log]] · [[prior-art/libraries/sfc-portfolio-tracker]]
- [ ] 🛠 **Auto-finanziamento crediti OpenRouter** — ricarica API dai profitti → [[system/modules/agents]]
- [ ] 🛠 **Volume Spike Detection** — rilevatore picchi anomali di volume (baseline rolling, z-score) → [[system/modules/quant-backtesting]]
- [ ] 🛠 **Reportistica diagnostica "cosa va male"** — modulo Python (metriche) + narrazione LLM, agganciato alla periodical synthesis → [[system/learning-feedback-loop]]
- [ ] 🛠 **Ponderazione dinamica dei pesi degli agenti** — l'agente che ci azzecca pesa di più (Opinion Pooling / Black-Litterman), post-MVP → [[system/learning-feedback-loop]]
- [ ] 🛠 **Feedback post-trade per meccanismo di uscita** — `exit_reason` su ogni trade + sintesi nel `past_context` per gli agenti → [[system/rating-scoring]]
- [ ] 🛠 **Disinvestimento come batch di trade coordinati** — il PM emette vendite+acquisto in un ciclo per far spazio, solo se tutto analizzato a sufficienza → [[system/rating-scoring]]
- [ ] 🛠 **Intervento degli agenti sul position sizing** — idea da valutare (rischi: rompe determinismo, LLM debole sui numeri, sovraesposizione; benefici: contesto non catturato dalla formula; via di mezzo = fattore ±X% clampato dai cap) → [[system/position-sizing]]
- [ ] 🛠 **Continuous Learning real-time** — fine-tuning su streaming (post-fine-tuning batch) → [[system/decision-log]]
- [ ] 📈 **Strategia Sentiment degli Analisti** — replicare il pattern che genera il consenso e tradare prima della folla → [[system/ideas-log]]
- [ ] 📈 **Stop loss istituzionali a domino** — sfruttare le soglie psicologiche degli SL → [[strategy/methods/trend-following]]
- [ ] 📈 **Quantificazione eventi rari** — gestire eventi mai visti (categoria più vicina vs unknown) → [[strategy/questions-for-salvatore]]
- [ ] 📈 **Analisi paper di finanza** — raccogliere e ingestare paper accademici sui fattori → [[strategy/index]]
- [ ] 🔀 **Copy trading come canale di monetizzazione** — Darwinex (20% performance fee, FCA, Python→MT5→DARWIN, integrazione diretta IBKR). Da attivare dopo il paper trading → [[system/ideas-log]]
- [ ] 🔀 **Coinvolgere collaboratori esterni per review** — Pipeline: Diego Zappa (primo, prof. statistico + trader), Trezzi (connector), traders SIM. Solo quando il sistema è funzionante → [[system/ideas-log]]


## 🔴 Da fare

- [ ] 🛠 **Strutturare lo schema dello state** (PROSSIMO PASSO 1) — raffinare campi/tipi di research_state/investment_state → [[system/state-schemas]]
- [ ] 🛠 **Position sizing: tarare i numeri** — impianto risk-based approvato; restano base_risk_%, multiplier per conviction, heat_max_%, cap titolo/settore → backtest → [[system/position-sizing]]
- [ ] 🛠 **Tool agenti: fissare i vendor** — impianto inventario approvato; restano solo i vendor dei dati live (candidato Finnhub) e il vendor opzioni (IBKR vs Tradier), da decidere a implementazione del data-layer → [[system/tools-inventory]]
- [ ] 🔀 **Definire l'`investment_state` con Salvatore** — partire dal template-menu completo, potare/modificare insieme → [[system/investment-state-template]]
- [ ] 🛠 **Tool di iniezione dello stato del portafoglio** — foto aggiornata (cassa, posizioni, P/L) nel contesto dell'agente → [[system/modules/agents]]
- [ ] 🛠 **Backtesting continuo e asincrono come validatore delle soglie** — valida di continuo R:R, k_stop/k_tp e ogni rapporto tarato a monte → [[system/modules/quant-backtesting]]
- [ ] 🛠 **Implementare gli adapter broker** — wrapper Alpaca (MVP) + interfaccia interna standard, IBKR intercambiabile → [[system/modules/execution]]
- [ ] 🛠 **Progettare lo schema del DB esteso** — 4 aree (rendicontazione/dati live/statuto/log), storage time-series + oggetti; accesso/performance/forma fisica → [[system/modules/data-layer]] · [[system/db-access-performance]]
- [ ] 🛠 **Implementare il queue system degli extractor** — un extractor per vendor, check presenza DB, autogestione rate limit → [[system/modules/data-layer]]
- [ ] 🛠 **Riscrivere il grafo LangGraph** — node/edge/state/tool sulla topologia 2026-05-29 → [[system/modules/agents]]
- [ ] 🛠 **Configurare OpenRouter + DeepSeek V4 Pro** — setup router e modello → [[system/stack]]
- [ ] 🛠 **Studiare i corsi completi LangGraph e LangSmith** — finora solo Quickstart → [[system/stack]]
- [ ] 🛠 **Implementare graceful shutdown & recovery** — design fatto (riconciliazione broker + intent log + client order id); resta da scrivere la routine di init → [[system/modules/data-layer]]
- [ ] 🛠 **Predisporre il substrato di logging del learning loop** — chain-of-thought + match tesi-per-agente↔esito + `exit_reason`, **da subito** → [[system/learning-feedback-loop]]
- [ ] 🛠 **Valutare canale Telegram "sala segnali"** — calendario, news, prezzi, trade, alert → [[system/architecture]]
- [ ] 🛠 **Analizzare FinAgent / AlphaArena / NeuroEspresso (tecnico)** — struttura codice, agenti, comunicazione → [[prior-art/papers/alpha-arena]]
- [ ] 🛠 **Studiare il Cornell Paper** — fonte citata, da reperire → [[syntheses/notebooklm-research-2026-05-13]]
- [ ] 📈 **Preparare il foglio "Domande per Salvatore"** — VaR, overfitting, test benchmark, opzioni, rating asset → [[strategy/questions-for-salvatore]]
- [ ] 📈 **Convertire il file market driver in TXT** — 4 macro-categorie + driver Federal Reserve, arricchito → [[strategy/questions-for-salvatore]]
- [ ] 📈 **Preparare documento indicatori di valuation** — cosa analizzare nelle stock (associazione) → [[strategy/questions-for-salvatore]]
- [ ] 📈 **Formalizzare i fondamentali** — es. i 5 tipi di P/E, trailing vs current → [[system/modules/quant-backtesting]]
- [ ] 📈 **Lista di fattori candidati** — categoria, misurabilità, strumento impattato → [[system/modules/quant-backtesting]]
- [ ] 📈 **Raccogliere e validare indicatori di analisi tecnica** — minimi/massimi 52w, range, drawdown, volumi → [[system/modules/quant-backtesting]]
- [ ] 📈 **Descrivere la giornata tipo di un trader** — cosa il bot deve replicare → [[strategy/index]]
- [ ] 📈 **Raccogliere casi reali eventi → impatto prezzi** — dataset grezzo per la factor quantification → [[strategy/index]]


## 🟡 In corso

- [ ] 🛠 **Progettazione architettura software** — design-first, I/O per ogni modulo, schema DB, flusso end-to-end → [[system/architecture]]
- [ ] 🛠 **Studio wiki in autonomia** — leggere tutta la wiki prima della prossima sessione con Salvatore → [[_meta/index]]
- [ ] 🛠 **Modulo analisi documenti** — legge documenti ed estrae info strutturate → [[system/modules/data-layer]]
- [ ] 📈 **Definire cosa replica il bot nel mondo reale** — workflow del trader tipo → [[strategy/index]]
- [ ] 📈 **Raccolta di meccanismi di mercato** — ogni osservazione modellabile nel vault → [[strategy/index]]


## 🟠 Decisioni da prendere

- [ ] 🛠 **Implementare lo slice MVP del parallelismo** — coda di priorità (D) + subgraph per-ticker (A); screening (E) e scheda DB (B/C) come strati successivi → [[system/parallelism-design]]
- [ ] 🔀 **Criteri "info sufficienti" del PM + max iterazioni** — quando fare/non fare un trade → [[system/parallelism-design]]
- [ ] 🛠 **Forma fine di storage per gli state annidati** — JSON/documentale dentro il time-series → [[system/modules/data-layer]]
- [ ] 🔀 **Enumerare le fonti/tool di sentiment** — Reddit/StockTwits/X + news-sentiment + API dedicate, massima copertura; si interseca con "indicatori di sentiment" (Salvatore) → [[system/tools-inventory]] · [[strategy/questions-for-salvatore]]
- [ ] 🛠 **System prompt PM: "nel dubbio, chiedi sempre"** — istruire il PM a interrogare di nuovo i desk a ogni incertezza (anche piccola); no-trade preferibile a basi incerte → [[system/modules/agents]] · [[system/parallelism-design]]
- [ ] 🛠 **Validazione collettiva dell'`investment_state`** — tutti gli agenti validano completezza·correttezza·esaustività fonti prima del sealing (nodo esplicito o responsabilità nel system prompt?) → [[system/state-schemas]]
- [ ] 🛠 **Includere il modulo TA?** — opzionale, test A/B con/senza → [[system/modules/quant-backtesting]]
- [ ] 🛠 **Analisti: 2 o 4 agenti?** — accorpati o separati, da decidere a sviluppo → [[system/modules/agents]]
- [ ] 🛠 **Consolidare il Prompt Builder** — tutti e 6 i system prompt scritti (bozze v0); resta l'assemblaggio prompt+contesto XML+schema strict + la rifinitura iterativa LangSmith → [[system/system-prompts]] · [[prior-art/libraries/rizzo-trading-agent]]
- [ ] 🛠 **Token cost estimator** — tracciamento token + ricarica automatica → [[system/modules/agents]]
- [ ] 🔀 **Frequenza ciclo** — 4h vs 24h, dipende dai backtest → [[system/modules/quant-backtesting]]
- [ ] 🔀 **Desk di monitoring/evaluation** — design, partire da SFC Streamlit → [[system/modules/agents]]
- [ ] 📈 **VaR: quale e come** — parametrico/storico/MonteCarlo, VaR vs CVaR, lookback → [[strategy/questions-for-salvatore]]
- [ ] 📈 **Prevenzione overfitting** — walk-forward, in/out-of-sample, CPCV → [[strategy/questions-for-salvatore]]
- [ ] 📈 **Test statistici sul benchmark** — significatività vs S&P/60-40 → [[strategy/questions-for-salvatore]]
- [ ] 📈 **Base dei rating asset (disinvestimento)** — su cosa basarli e come aggiornarli → [[system/rating-scoring]]
- [ ] 📈 **Strategia opzioni (leva)** — strike/scadenza/contratti/dati, fuori MVP → [[strategy/questions-for-salvatore]]
- [ ] 📈 **Indicatori di sentiment** — da inventare, posizione ibrida col technical → [[strategy/questions-for-salvatore]]
- [ ] 📈 **Regole dello Statuto** — capire quali info dargli e in quale forma (template/wireframe) → [[system/modules/agents]]
- [ ] 📈 **Cash-out strategy: quale %?** — mensile su IBAN, a progetto finito → [[system/modules/agents]]


## ✅ Fatto

- [x] 🛠 **Topologia parallelismo multi-ticker = architettura a imbuto** ✅ 2026-06-06 — funnel E(screening deterministico)→D(coda)→A(subgraph per-ticker)→B/C(scheda DB); subgraph come pattern; screening = modulo Python non-LLM che scrive `screening_score` nella scheda. MVP parte da D+A → [[system/parallelism-design]]
- [x] 🛠 **Tutti e 6 i system prompt + metodo prompt-eng** ✅ 2026-06-06 — principio "separa comportamento/forma/tool" + 7 principi + scheletro a 7 blocchi + Technical/Market/Sentiment/Fondamentali + PM (orchestratore) + Risk (gate bear) scritti per intero, **in inglese** → [[system/system-prompts]]
- [x] 🛠 **Decisione: comportamento per-agente del desk (impianto)** ✅ 2026-06-06 — Market/Sentiment/Technical/Fondamentali: input·tool·output·ragionamento·stop. News/sentiment per tipo di info (Market=catalizzatori · Sentiment=mood multi-fonte incl. social); tutti contribuiscono alla direzione; stop auto + PM richiama → [[system/agent-behaviors]]
- [x] 🛠 **Decisione: inventario tool agenti (impianto)** ✅ 2026-06-06 — 9 famiglie (prezzi · indicatori · fondamentali · news/sentiment · macro · calendario · portafoglio · opzioni · guardrail) + 2 regole (parametrici · write-through); portfolio auto+richiamabile, `compute_indicator` parametrico; restano solo i vendor → [[system/tools-inventory]]
- [x] 🛠 **Decisione: position sizing = risk-based (impianto)** ✅ 2026-06-05 — rischio % scalato per conviction → quantità dallo stop ATR + portfolio heat; numeri da tarare → [[system/position-sizing]]
- [x] 🛠 **Decisione: state annidati = Opzione C (ibrido)** ✅ 2026-06-05 — piatto a runtime → annidato al sealing; da validare in fase di grafo → [[system/state-schemas]]
- [x] 🛠 **Decisione: autonomia informativa real-time first + write-through** ✅ 2026-06-05 — gli agenti chiamano prima il tool real-time (anche più volte, per verificare); il tool consegna all'agente e copia nel DB (centro unico); check-presenza DB-first resta per lo storico → [[system/modules/agents]] · [[system/modules/data-layer]]
- [x] 🛠 **Decisione: graceful shutdown & recovery (design)** ✅ 2026-06-04 — broker=verità + riconciliazione + intent log + client order id anti-doppione; recovery automatico e loggato (no intervento umano); analisi a metà → ricomincia pulita → [[system/modules/data-layer]]
- [x] 🛠 **Decisione: motore DB = PostgreSQL + TimescaleDB** ✅ 2026-06-04 — un solo motore: hypertable time-series + relazionale/oggetti + JSONB per gli state → [[system/db-access-performance]]
- [x] 🛠 **Decisione: cache in-process per l'MVP, Redis idea futura** ✅ 2026-06-04 — read-through in-process finché singolo processo; Redis solo se multi-processo → [[system/db-access-performance]]
- [x] 🛠 **Decisione: pesi agenti = indicazione, non regola** ✅ 2026-06-04 — il backtest informa il PM (contesto/awareness) + diagnostica "cosa migliorare", non scavalca il giudizio; aggancio come input al PM → [[system/learning-feedback-loop]]
- [x] 🛠 **Decisione: aggregazione `direction`/`conviction` al PM** ✅ 2026-06-04 — ogni desk propone, il PM aggrega e decide → [[system/state-schemas]]
- [x] 🛠 **Decisione: struttura `entry_price`** ✅ 2026-06-04 — backbone ATR (k_entry scalato per conviction, guardrail R:R 1.5); numeri da tarare in backtest → [[system/state-schemas]]
- [x] 🛠 **Decisione: conviction level = enum** ✅ 2026-06-04 — 5 livelli, non score 0-100 → [[system/rating-scoring]]
- [x] 🛠 **Decisione: autonomia totale** ✅ 2026-06-04 — nessun input umano oltre l'accensione (auto-start timer + alert) → [[system/modules/agents]]
- [x] 🛠 **Decisione: PM si attiva anche al `next_check_date` scaduto** ✅ 2026-06-04 — terzo trigger oltre alert + periodical synthesis → [[system/modules/agents]]
- [x] 🔀 **Decisione: broker intercambiabili via adapter** ✅ 2026-06-02 — Alpaca MVP → IBKR prod → [[system/modules/execution]]
- [x] 🔀 **Decisione: storage principalmente time-series + oggetti** ✅ 2026-06-02 → [[system/modules/data-layer]]
- [x] 🔀 **Decisione: approccio incrementale (alpha-first)** ✅ 2026-06-02 → [[system/decision-log]]
- [x] 🔀 **Decisione: extractor DB-first con queue + check presenza** ✅ 2026-06-02 → [[system/modules/data-layer]]
- [x] 🔀 **Decisione: transaction cost auto-adattivo** ✅ 2026-06-02 → [[system/modules/execution]]
- [x] 🔀 **Decisione: conviction level assegnato dal PM** ✅ 2026-06-02 → [[system/rating-scoring]]
- [x] 🔀 **Conferma ruolo `mantainer`** ✅ 2026-06-02 — technical → rendicontazione → [[system/modules/data-layer]]
- [x] 🔀 **Decisione: deploy su mini-server di casa 24/7 + .env locale** ✅ 2026-06-02 → [[system/modules/data-layer]]
- [x] 🔀 **Decisione: portfolio / mid-term, no day trading** ✅ 2026-05-29 → [[system/decision-log]]
- [x] 🔀 **Decisione: stock-only, poi multi-asset** ✅ 2026-05-23 → [[strategy/metrics/benchmark]]
- [x] 🛠 **Decisione: framework = LangGraph (base TradingAgents)** ✅ 2026-05-29 → [[system/stack]]
- [x] 🛠 **Decisione: provider LLM = OpenRouter + DeepSeek V4 Pro** ✅ 2026-05-29 → [[system/stack]]
- [x] 🛠 **Decisione: design-first** → [[system/decision-log]]
- [x] 🔀 **Decisione: backtesting = deterministico Python, non simulazione AI** ✅ 2026-06-04 sera — VectorBT su DB storico interno (yfinance/AlphaVantage); l'AI non gira durante la simulazione → [[system/modules/quant-backtesting]]
- [x] 🔀 **Decisione: nessun investimento di capitale prima della prova** ✅ 2026-06-04 sera — solo reinvestimento dei guadagni → [[system/decision-log]]
- [x] 🔀 **Decisione: feedback esterni solo a sistema finito** ✅ 2026-06-04 sera → [[system/ideas-log]]
- [x] 📈 **Indicatori macro avanzati (PIL, consumi, inflazione…)** ✅ 2026-06-05 — primo draft Salvatore ingestato → [[strategy/indicators/macro-indicators]]
- [x] 🛠 **Inizializzazione wiki + repository Git**
- [x] 🔀 **Videochiamate 04-30, 05-06, 05-29** — architettura, TA, topologia agenti → [[system/architecture]]
- [x] 📈 **Presentazione factor investing / meccanismi di esecuzione / benchmark settore** → [[strategy/methods/factor-investing]]
- [x] 📈 **Allineamento: TA come segnali numerici (no grafico)** → [[system/modules/quant-backtesting]]
- [x] 📈 **Framing come AI Investment Fund** → [[overview]]




%% kanban:settings
```
{"kanban-plugin":"board","list-collapse":[false,false,false,false,false]}
```
%%
