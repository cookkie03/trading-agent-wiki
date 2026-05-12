# Wiki Log — Trading Agent

> Log append-only. Grep utile: `grep "^## \[" wiki/_meta/log.md | tail -10`

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
- **Pages created**: [[references/paper-trading-agents]], [[references/paper-alpha-arena]], [[references/library-portfolio-optimizer]], [[references/architecture-handwritten-notes]], [[agents/trading-agents-framework]], [[agents/cvx-portfolio-optimizer]]
- **Pages updated**: [[theory/modular-trading-agent-architecture]], [[build/system-map]], [[_meta/index]]
- **Contradictions**: nessuna
- **Notes**: Ingest completa di materiale tecnico di frontiera. TradingAgents introduce il protocollo di comunicazione strutturata e il team di analisti/debater. Portfolio Optimizer (cvx-optimizer) fornisce il motore per il Portfolio Management quantitativo e l'integrazione di opinioni (views) via Black-Litterman. Alpha Arena fornisce benchmark comparativi tra LLM. La system map ora include esplicitamente il portfolio manager e il protocollo di comunicazione strutturato.
