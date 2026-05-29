# Wiki Log — Trading Agent

> Log append-only. Grep utile: `grep "^## \[" wiki/_meta/log.md | tail -10`

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
