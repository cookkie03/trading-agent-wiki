# Wiki Log — Trading Agent

> Log append-only. Grep utile: `grep "^## \[" wiki/_meta/log.md | tail -10`

## [2026-05-29] lint + update | Ristrutturazione wiki post-call + ingest pending

- **Trigger**: `/wiki-lint` — "rivediamo completamente la struttura della wiki per farla funzionare meglio con le cose discusse nelle ultime call"
- **Lint**: 1 link rotto (`dev-roadmap.canvas`), 1 ambiguo (`trading-floor.canvas` duplicato), 1 orfana (`tradingagents-graph-schema`), 1 conflitto (Trader), 54 file spazzatura, 3 file pending. Freshness: nessun problema >90gg.
- **Riallineamenti contenuto**:
  - [[build/system-map]] riscritta sulla topologia 2026-05-29 (PM orchestratore → analisti → research_state → Risk Analyst gate → Trade deterministico; Layer DB esteso/Extractors/gate; protocollo state+DB con context rot; sequenza di sviluppo "riscrivere il grafo")
  - [[build/modules/llm-agent-system]] **conflitto Trader risolto**: Funzione + sezione Leva riallineate (segnale `Strong` nel research_state validato dal Risk Analyst, esecuzione deterministica); Dipendenze/TODO aggiornati
  - [[build/modules/exchange-db]] **schema DB consolidato** (5 tabelle core ↔ 4 aree logiche, mapping unico)
- **Ingest pending**:
  - daily-note 2026-05-28 (storage SQL vs JSON) → domanda aperta in [[build/modules/exchange-db]] e [[build/decision-log]]
  - daily-note 2026-05-29 (tool per indicatori + SFC) → sezione tool-centric di [[build/modules/llm-agent-system]]
  - transcript 05-13 → pagina [[references/videochiamata-luca-salvatore-2026-05-13]] già completa; archiviato, raw_source_path corretto
- **Fix link rotti**: `ops/wiki-restructuring-plan` (2×), `external/trading-agents-framework` (2×), `tradingagents-graph.canvas` (2×, canvas eliminato da Luca)
- **Pages updated**: [[build/system-map]], [[build/modules/llm-agent-system]], [[build/modules/exchange-db]], [[build/decision-log]], [[_meta/index]], [[references/videochiamata-luca-salvatore-2026-05-13]], [[references/tradingagents-code-wiki]], [[references/tradingagents-graph-schema]], [[_meta/hot-cache]]
- **Deleted**: 54 frammenti `raw/audio/.txt*.txt`; stub `wiki/artifacts/artifact-workbench.md`
- **Archived**: `raw/archived/daily-notes/2026-05-28.md`, `2026-05-29.md`; `raw/archived/audio/2026-05-13 13-14-17.txt` (+.tmp.mp3)
- **Canvas**: Luca ha riorganizzato in Obsidian in parallelo → tutti sotto `artifacts/` (design in `artifacts/architecture/`); eliminati da lui `mvp-system-cycle.canvas`, `trading-floor.canvas` (root), `tradingagents-graph.canvas`. `wiki/build/architecture/` non esiste più.
- **Conflicts**: il conflitto Trader (segnalato nell'ingest precedente) è stato **risolto** in questa sessione.
- **Notes**: vedi anche il cleanup pass 2 sotto.

## [2026-05-29] cleanup | Rimozione ridondanze + link rotti residui

- **Trigger**: richiesta utente — "tenere tutto pulito, togliere informazioni ridondanti, file non essenziali"
- **Refactor**: [[build/mvp-prototype-design]] — rimossi *Ciclo operativo* (vecchia topologia, duplicava [[build/system-map]]) e *Decisioni fondanti* (duplicavano [[build/decision-log]], con dati stale su crypto/Binance/DeepSeek 1/20); allineato a stock-only + topologia 29/05; **mantenuti** metriche a due livelli, backtesting integrato, sequenza track, insight NotebookLM
- **Deleted**: `wiki/artifacts/kanban-project-status.md` — stale (06/05), `type:ops` (ruolo eliminato dalla taxonomy), "Blocked: Crypto vs Equity" già chiuso, ridondante con [[artifacts/luca-board]] + [[artifacts/salvatore-board]] + [[build/decision-log]]. Riferimenti sistemati in [[_meta/index]] e [[references/videochiamata-luca-salvatore-2026-04-30]]
- **Link rotti risolti**: `[[strategy/]]`→`[[strategy/index]]` (quant-backtesting); 3 stub metriche in [[strategy/methods/trend-following]] → testo semplice; `[[raw/daily-notes/2026-05-19]]` in [[build/ideas-log]] → path archiviato
- **Pages updated**: [[build/mvp-prototype-design]], [[_meta/index]], [[references/videochiamata-luca-salvatore-2026-04-30]], [[build/modules/quant-backtesting]], [[strategy/methods/trend-following]], [[build/ideas-log]], [[_meta/hot-cache]]
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
  - [[build/modules/llm-agent-system]] (topologia agenti, Trade deterministico, PM orchestratore, context rot, OpenRouter/DeepSeek)
  - [[build/modules/exchange-db]] (design DB esteso, extractors, market alert, retention)
  - [[build/modules/risk-management]] (Risk Analyst gate bear + guardrail deterministici)
  - [[build/modules/quant-backtesting]] (posizione TA/fondamentali/sentiment)
  - [[build/decision-log]] (10 decisioni chiuse del 29/05 + aggiornate aperte)
  - [[build/stack]] (OpenRouter, DeepSeek V4 Pro + costi, storage)
  - [[wiki/overview]], [[strategy/index]], [[artifacts/luca-board]], [[artifacts/salvatore-board]], [[_meta/index]], [[_meta/hot-cache]]
- **Conflicts**: segnalato (non risolto automaticamente) — vecchio "LLM Trader produce JSON" + "agente Esecutore gestisce leva" in [[build/modules/llm-agent-system]] vs nuovo "Trade = funzione Python deterministica". Da riconciliare dove vive la logica leva via opzioni.
- **Skipped**: nessuno (`raw/notes/` conteneva solo `.DS_Store`)
- **Notes**: Sessione di design molto densa. Confermato il pivot definitivo a gestione di portafoglio mid-term stock-only; definita la topologia del grafo da costruire (riscrittura su base TradingAgents), il DB esteso ispirato alla dashboard SFC, e lo stack LLM (OpenRouter + DeepSeek V4 Pro). [[build/system-map]] resta da allineare alla nuova topologia.

## [2026-05-27] update | Decoupling logic segnali Strong Buy/Sell da agenti specifici

- **Change**: Scollegata esplicitamente la logica dei segnali ad alta convinzione (Strong Buy e Strong Sell) per la leva con opzioni da una tipologia rigida di agenti (come i "Ricercatori"). Il calcolo e la validazione della convinzione sono trattati come concetti/task di sistema, e l'assegnazione finale del ruolo all'agente o nodo più idoneo avverrà durante la mappatura granulare del grafo LangGraph.
- **Pages updated**: [[references/conversazione-luca-salvatore-2026-05-27]], [[build/modules/llm-agent-system]], [[build/modules/risk-management]], [[build/decision-log]]

## [2026-05-27] ingest | Brainstorming Luca & Salvatore 27/05 — Ricercatori/Esecutori + Statuto 10% + Opzioni Leva + Token Cost Estimator + Piero Site

- **Type**: chat + 18 note vocali WhatsApp (brainstorming architetturale e operativo)
- **Sources raw**:
  - `raw/daily-notes/2026-05-27.md` — log chat WhatsApp del 27 maggio 2026
  - `raw/audio/WhatsApp Audio 2026-05-27 at *` (18 file trascrizioni .md) — note vocali Salvatore trascritte
- **Pages created**:
  - [[references/conversazione-luca-salvatore-2026-05-27]]
- **Pages updated**:
  - [[build/modules/llm-agent-system]] (suddivisione Ricercatori/Esecutori, opzioni leva, integrazione LangSmith)
  - [[build/modules/risk-management]] (Statuto deterministico, riserva liquidità 10%, OpenRouter LLM cost estimator)
  - [[build/decision-log]] (aggiunte 5 decisioni chiuse e 4 aperte/aggiornate del 27/05)
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
  - [[build/ideas-log]] (aggiunte sezioni 22/05, 25/05, 26/05)
  - [[build/stack]] (aggiunta sezione AI Agent Framework: LangChain, LangSmith, Mermaid, struttura repo)
  - [[build/decision-log]] (aggiunte 7 decisioni chiuse 2026-05-19/23/26; chiuse 3 aperte: fork, multi-asset, debate)
  - [[build/modules/exchange-db]] (rinominato da module-a-exchange-db; scope stock-only, exchange da scegliere)
  - [[build/modules/quant-backtesting]] (rinominato da module-c-quant-backtest; aggiornati riferimenti)
  - [[build/modules/llm-agent-system]] (rinominato da module-d-prompt-builder-trader; Bull/Bear agents eliminati)
  - [[build/modules/risk-management]] (rinominato da risk-analyst; aggiornati riferimenti)
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
  - [[references/tool-set-provider-dati-exchange]]
  - [[references/note-audio-salvatore-quant-strategy]]
  - [[references/quantitative-trading-strategies-brenndoerfer]]
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

- **Link rotti risolti** (~35 link su 12 pagine): `[[theory/*]]` → `[[build/system-map]]`, `[[decisions/decision-log]]` → `[[build/decision-log]]`, `[[ops/*]]` → rimossi o redirectati verso `artifacts/`
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
- **Pages created**: [[references/tradingagents-code-wiki]], [[build/ideas-log]]
- **Pages updated**: [[build/modules/llm-agent-system]] (riscritto da raw dump a pagina strutturata), [[build/system-map]] (pattern architetturali: look-ahead bias doppia data, DB-first, indicatori dal DB), [[build/decision-log]] (nuove decisioni: DB-first, LangGraph, agent philosophy, look-ahead bias; aperte: fork vs from scratch, self-scheduling, debate architecture)
- **Contradictions**: decisione "From scratch" (2026-04-30) vs. "fork da TradingAgents" (2026-05-19, Luca) — segnalata nel decision-log, da formalizzare
- **Notes**: ideas-log.md creato come file append-only su richiesta di Luca per raccogliere tutte le idee del progetto

## [2026-05-14] update | Aggiunta sezione strategy/
- **Operazione**: recuperata la distinzione build/ (software, Luca) vs strategy/ (conoscenza mercato, Salvatore)
- **Cartelle create**: `strategy/`, `strategy/methods/`, `strategy/indicators/`, `strategy/metrics/`
- **File creati**: [[strategy/index]], [[strategy/methods/trend-following]], [[strategy/methods/factor-investing]]
- **File aggiornati**: [[build/modules/quant-backtesting]] (link a strategy/), [[_meta/taxonomy]], [[_meta/index]], [[overview]]

## [2026-05-13] restructure | Ristrutturazione completa del vault
- **Operazione**: ristrutturazione della wiki da struttura generica a struttura orientata al progetto
- **Cartelle eliminate**: `ops/`, `theory/`, `agents/`, `decisions/`, `questions/`
- **Cartelle create**: `build/modules/`, `references/external/`
- **File creati**: [[build/decision-log]], [[build/stack]], [[build/modules/exchange-db]], [[build/modules/quant-backtesting]], [[build/modules/llm-agent-system]], [[build/modules/risk-management]], [[references/external/trading-agents-framework]], [[references/external/cvx-portfolio-optimizer]], [[_meta/glossario]]
- **File aggiornati**: [[build/system-map]] (merge theory/), [[build/mvp-prototype-design]] (link fix), [[overview]], [[_meta/index]], [[_meta/taxonomy]]
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
- **Pages updated**: [[build/mvp-prototype-design]], [[decisions/decision-log]], [[_meta/index]]
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
- **Pages created**: [[ops/dashboard]], [[ops/current-state]], [[ops/backlog]], [[build/system-map]], [[decisions/decision-log]], [[questions/open-questions]], [[artifacts/artifact-workbench]]
- **Pages updated**: [[overview]],      [[_meta/index]], [[AGENTS]]
- **Notes**: aggiunta una superficie operativa pronta all'uso con dashboard, backlog, stato corrente, system map e registri iniziali

## [2026-05-13] brainstorming | Design MVP Prototype
- **Partecipanti**: Luca, Claude Code
- **Pages created**: [[build/mvp-prototype-design]]
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
- **Pages updated**: [[overview]], [[ops/dashboard]], [[ops/current-state]], [[ops/backlog]], [[build/system-map]], [[decisions/decision-log]], [[questions/open-questions]],   [[_meta/index]]
- **Contradictions**: nessuna
- **Notes**: ordinato un bundle di audio, trascrizioni e appunti tra Luca e Salvatore; escluse le parti strettamente personali non rilevanti

## [2026-04-30] artifact | kanban | Stato Progetto
- **File**: [[kanban-project-status]]
- **Based on**: [[ops/dashboard]], [[ops/current-state]], [[ops/backlog]], [[build/system-map]], [[decisions/decision-log]], [[questions/open-questions]], [[references/conversazione-luca-salvatore-2026-04-28-30]]

## [2026-04-30] ingest | Videochiamata Luca-Salvatore (2026-04-30)
- **Type**: video-call
- **Pages created**: [[references/videochiamata-luca-salvatore-2026-04-30]]
- **Pages updated**: [[theory/modular-trading-agent-architecture]], [[build/system-map]], [[kanban-project-status]], [[ops/backlog]], [[_meta/index]]
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
- **Pages updated**: [[references/videochiamata-luca-salvatore-2026-04-30]], [[theory/modular-trading-agent-architecture]], [[build/system-map]], [[decisions/decision-log]], [[questions/open-questions]], [[ops/backlog]]
- **Contradictions**: nessuna — le nuove trascrizioni hanno aggiunto dettaglio, non contraddetto contenuto esistente
- **Notes**: Le trascrizioni ad alta fedeltà hanno rivelato dettagli non presenti nella versione precedente: Prompt Builder come componente architetturale esplicito, meccanismo di esecuzione (limit order + SL + TP + leva), Binance come exchange scelto, problema needle-in-haystack, Factor Investigation Agent come agente separato, metodologia di quantificazione dei fattori (media empirica su serie storiche), strategia Sentiment degli Analisti (idea di King), Volume Spike module, specifiche su FinAgent (Cornell, ~50k stelle, Claude 4° contributore) e AlphaArena (confronto 5 LLM su Bitcoin). Aggiunte 5 decisioni chiuse nel decision log.

## [2026-05-12] ingest | TradingAgents, Alpha Arena & Portfolio Optimizer
- **Type**: research paper / library documentation
- **Pages created**: [[paper-trading-agents]], [[paper-alpha-arena]], [[references/library-portfolio-optimizer]], [[references/architecture-handwritten-notes]], [[agents/trading-agents-framework]], [[agents/cvx-portfolio-optimizer]]
- **Pages updated**: [[theory/modular-trading-agent-architecture]], [[build/system-map]], [[_meta/index]]
- **Contradictions**: nessuna
- **Notes**: Ingest completa di materiale tecnico di frontiera. TradingAgents introduce il protocollo di comunicazione strutturata e il team di analisti/debater. Portfolio Optimizer (cvx-optimizer) fornisce il motore per il Portfolio Management quantitativo e l'integrazione di opinioni (views) via Black-Litterman. Alpha Arena fornisce benchmark comparativi tra LLM. La system map ora include esplicitamente il portfolio manager e il protocollo di comunicazione strutturato.
