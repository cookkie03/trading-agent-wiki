---

title: Project Board — Trading Agent
type: artifact
tags:
  - artifact
  - roadmap
  - execution
  - architecture
created: 2026-04-30
updated: 2026-06-23
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

## 🔀 Meeting Luca + Salvatore

- [ ] 🔀 **Rivedere una per una le domande per Salvatore** — Luca non le considera ancora chiare: trasformarle in decisioni o task comprensibili → [[strategy/questions-for-salvatore]]
- [ ] 🔀 **Decidere come combinare i metodi strategy** — trend following, mean reversion, factor investing e dual portfolio: ordine di implementazione e composizione → [[strategy/index]]
- [ ] 🔀 **Decidere se serve un desk/agent macro separato** — alert macro e report sul portafoglio separati dall'analisi ticker-specifica → [[system/modules/agents]]
- [ ] 🔀 **Stabilire la frequenza operativa come event-driven** — PM attivato da alert e condizioni, non da cadenza rigida come vincolo primario → [[system/trigger-engine]]
- [ ] 🔀 **Chiarire Risk Analyst: desk pari agli altri o gate finale** — mantenere l'idea originaria di Luca/Salvatore o il gate bear separato → [[system/agent-behaviors]]
- [ ] 🔀 **Validare la strategia di metriche e benchmark** — cosa significa davvero battere benchmark e quali test statistici servono → [[strategy/questions-for-salvatore]]


## 📈 Salvatore — Da fare

- [ ] 📈 **Rileggere prior-art/papers e creare “Metriche (definitivo)”** — consolidare metriche di valutazione e performance come fatto per i driver macro → [[strategy/index]]
- [ ] 📈 **Pulire la cartella methods strategy** — chiarire ruolo di dual portfolio, value, trend following e mean reversion come strategie componibili → [[strategy/index]]
- [ ] 📈 **Definire indicatori codificabili per trend following e mean reversion** — quali indicatori usare, come parametrizzarli e come backtestarli → [[strategy/methods/trend-following]]
- [ ] 📈 **Portare gli indicatori di valuation stock** — documento dell'associazione: cosa analizzare in una stock e come spiegarlo agli agenti → [[strategy/questions-for-salvatore]]
- [ ] 📈 **Chiarire factor investing usando la tesi corporate bond** — fattori, fonti affidabili, ML/deep learning e limiti pratici → [[strategy/methods/factor-investing]]


## 📈 Salvatore — In corso

- [ ] 📈 **Studio wiki in autonomia** — leggere la wiki e segnalare dubbi o priorità di mercato da portare in meeting → [[_meta/index]]


## 👤 Luca — Da fare

- [ ] 🛠 **Validare il tree della codebase prima dell'implementazione** — scegliere con il coding agent i rami di alto livello e cosa deve restare stabile nel tempo → [[system/codebase-architecture]]
- [ ] 🛠 **Decidere quanto riusare della build storica Datapizza/branch precedenti** — reference design, codice da copiare, o solo materiale da ripensare → [[system/stack]]
- [ ] 🛠 **Scegliere il primo slice software da costruire** — harness broker/vendor/storage con test, prima di grafo e agenti → [[system/codebase-architecture]]
- [ ] 🛠 **Rivedere le pagine `system/` dopo la pulizia dei claim storici** — controllare se la wiki descrive davvero il progetto che vuoi costruire ora → [[system/system-wiki-reorganization]]
- [ ] 🛠 **Definire il ruolo del frontend come modulo sostituibile** — Streamlit come prima UI, TypeScript futuro, stesso core e contratti di lettura → [[system/frontend-module]]


## 👤 Luca — In corso

- [ ] 🛠 **Rilettura critica della wiki con commenti inline** — i commenti `%%...%%` sono input progettuali da assorbire in pagine e task, non testo da riscrivere superficialmente → [[system/system-wiki-reorganization]]


## 🛠 Coding Agent — Da fare

- [ ] 🛠 **Ripulire i claim di codice implementato dalla wiki operativa** — trasformare `🟢 Implementato`/branch/test in contesto storico o reference design, senza perdere l'informazione utile → [[system/system-wiki-reorganization]]
- [ ] 🛠 **Progettare la codebase reale prima di scrivere agenti** — tree alto livello, package boundaries, contratti I/O e ordine di build: harness → moduli core → tool → agenti → job asincroni → [[system/codebase-architecture]]
- [ ] 🛠 **Disegnare l'harness broker/vendor/storage con test** — prima tranche implementativa: adapter broker, wrapper data vendor, DB/repository, contratti e test end-to-end minimi → [[system/codebase-architecture]]
- [ ] 🛠 **Mappare fonti dati e tool per vendor** — Yahoo/yfinance, FRED, Alpaca, IBKR, OpenBB, fonti news/social/options: cosa offrono, wrapper interno, freshness, write-through, dedup → [[system/data-sources-tool-map]]
- [ ] 🛠 **Riorganizzare `wiki/system/` in sottodomini** — proporre struttura ordinata per agents/data/execution/frontend/orchestration/quant, aggiornando taxonomy solo se la migrazione viene fatta → [[system/system-wiki-reorganization]]
- [ ] 🛠 **Centralizzare prompt e linguaggio umano nel futuro codice** — system prompt, istruzioni agenti, schema output e policy operative devono vivere in file dedicati/versionabili → [[system/system-prompts]]
- [ ] 🛠 **Formalizzare error handling dell'execution** — se lo state è incompleto o il trade viene bloccato, il PM riceve feedback strutturato; conferme trade e failure recovery non restano implicite → [[system/modules/execution]]
- [ ] 🛠 **Esplicitare wrapper extra-LLM per broker e vendor** — gli agenti chiedono dati o intent di trade; infrastruttura e adapter gestiscono provider, formati e duplicati → [[system/data-sources-tool-map]]
- [ ] 🛠 **Preparare backlog subtask per eventuali subagent** — trasformare i commenti rimasti e le aree wiki sporche in unità indipendenti assegnabili → [[system/system-wiki-reorganization]]


## 🧪 Ricerca / Futuro

- [ ] 🔀 **Studiare OpenBB come libreria fondamentale** — capire se usarla come fonte dati, SDK di ricerca o riferimento architetturale → [[system/data-sources-tool-map]]
- [ ] 🔀 **Studiare FinRL** — valutare parti sperimentali e moduli riusabili per RL/quant research → [[system/data-sources-tool-map]]
- [ ] 🔀 **Studiare Kronos** — capire se il foundation model per financial markets può diventare modulo o riferimento per time-series/market language → [[prior-art/papers/kronos-foundation-model]]
- [ ] 🛠 **Approfondire `optimizer` come piattaforma full-stack** — BAML views, FastAPI layer, scheduler, broker sync e optimizer quant come riferimento per la nostra architettura → [[prior-art/libraries/cvx-portfolio-optimizer]]
- [ ] 🛠 **Valutare SFC come base della dashboard osservabilità** — leggere DB e stato sistema in sola lettura, senza mescolare UI e core → [[system/observability-dashboard]]
- [ ] 🔀 **Crawl periodico di repo e documentazioni prior-art** — mantenere una pipeline di scouting per evitare di reinventare componenti già maturi → [[system/data-sources-tool-map]]


## 🟡 In corso

- [ ] 🛠 **Allineamento wiki al framing “codebase da costruire”** — separare stato attuale, storia dei branch e design valido nelle pagine più dense → [[system/system-wiki-reorganization]]
- [ ] 🛠 **Ingest commenti wiki + daily notes** — assorbire i commenti come task/decisioni/idee integrate nel sistema, non come frasi riscritte → [[system/system-wiki-reorganization]]


## ✅ Fatto

- [x] 🔀 **Policy editoriale 2026-06-23** — i claim di implementazione storici non descrivono più lo stato corrente; diventano reference design o storia del progetto → [[system/decision-log]]
- [x] 🛠 **Daily notes 2026-06-20/21/22 archiviate dopo ingest** — source spostate in `raw/archived/daily-notes/` → [[_meta/log]]
- [x] 🛠 **Creata pagina codebase architecture** — punto di partenza per progettare tree, harness e ordine di build → [[system/codebase-architecture]]
- [x] 🛠 **Creata pagina data sources & tool map** — punto di raccordo per vendor, wrapper, tool e capability layer → [[system/data-sources-tool-map]]
- [x] 🛠 **Creata pagina frontend module** — frontend come modulo intercambiabile, non logica core → [[system/frontend-module]]




%% kanban:settings
```
{"kanban-plugin":"board","list-collapse":[null,null,null,null,null,null,true,null,true]}
```
%%