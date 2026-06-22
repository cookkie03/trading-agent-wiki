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
  - "[[system/ideas-log]]"
  - "[[system/codebase-architecture]]"
  - "[[strategy/questions-for-salvatore]]"
confidence: high
priority: high
area: ops
kanban-plugin: board
---

# Project Board — Trading Agent

Board unica di progetto. Tiene solo backlog operativo, decisioni aperte e stato reale del lavoro. I dettagli vivono nelle pagine linkate.

## 💡 Idee

- [ ] 🛠 **Desk macro separato dal ticker flow** — usare un agente o desk dedicato per report macro e impatto sul portafoglio, separato dall'analisi sul singolo ticker → [[system/modules/agents]]
- [ ] 🛠 **Frontend intercambiabile** — modulo frontend sostituibile senza toccare il core (Streamlit oggi, TypeScript domani) → [[system/frontend-module]]
- [ ] 🛠 **LLM views + motore quant** — sfruttare pattern Black-Litterman / opinion pooling come ponte tra giudizio LLM e allocazione matematica → [[prior-art/libraries/cvx-portfolio-optimizer]]
- [ ] 📈 **Integrare il meglio dei metodi** — trend following, mean reversion, factor investing e dual portfolio come mattoni componibili, non come alternative monolitiche → [[strategy/index]]
- [ ] 🔀 **Programma di crawl prior-art continuo** — sniff/crawl sistematico di repo e docs utili (OpenBB, FinRL, optimizer, altri) come backlog di ricerca permanente → [[system/data-sources-tool-map]]

## 🔴 Da fare

- [ ] 🛠 **Definire l'architettura della codebase da zero** — tree alto livello, responsabilità dei package, ordine di build e invarianti del codice → [[system/codebase-architecture]]
- [ ] 🛠 **Mappare fonti dati, vendor wrapper e tool layer** — separare chiaramente connectors, capabilities e contratti di estrazione → [[system/data-sources-tool-map]]
- [ ] 🛠 **Riorganizzare `wiki/system/`** — proporre una tassonomia più ordinata per sottodomini (agents, data, execution, frontend, orchestration, quant) senza perdere storia → [[system/system-wiki-reorganization]]
- [ ] 🛠 **Pulire i claim di implementazione residui** — degradare le sezioni che descrivono branch o codice come se fossero stato attuale, mantenendo il contesto storico nei log → [[system/system-wiki-reorganization]]
- [ ] 🛠 **Definire l'harness completo prima degli agenti** — broker, vendor, storage, contracts e test come prima tranche di implementazione reale → [[system/codebase-architecture]]
- [ ] 🛠 **Formalizzare l'handling errori e i feedback al PM** — trade saltato, state incompleto, conferma esecuzione, failure recovery → [[system/modules/execution]]
- [ ] 🛠 **Strutturare il layer tool del coding agent** — backlog operativo specifico per lavoro di implementazione e refactor guidati dall'AI → [[system/codebase-architecture]]
- [ ] 📈 **Rivedere una per una le domande per Salvatore** — Luca vuole trasformarle in agenda esplicita del prossimo meeting → [[strategy/questions-for-salvatore]]
- [ ] 📈 **Produrre una pagina “Metriche (definitivo)”** — rileggere papers e prior-art strategy per consolidare le metriche di valutazione → [[strategy/index]]
- [ ] 📈 **Chiarire factor investing tramite la tesi corporate bond** — usare la tesi di Luca come materiale guida per fattori, fonti e possibili modelli ML/DL → [[strategy/methods/factor-investing]]
- [ ] 🔀 **Studiare Kronos come modulo candidato** — capire se usarlo per il linguaggio dei mercati / time series nel progetto → [[prior-art/papers/kronos-foundation-model]]
- [ ] 🔀 **Studiare OpenBB e FinRL** — backlog di scouting per librerie e repo da cui estrarre moduli o pattern riusabili → [[system/data-sources-tool-map]]

## 🟡 In corso

- [ ] 🛠 **Ingest editoriale commenti wiki + daily notes** — trasformare commenti `%%...%%` e note 2026-06-20/21/22 in board, pagine target e correzioni di stato → [[system/system-wiki-reorganization]]
- [ ] 🛠 **Allineamento della wiki al nuovo framing “design/codebase first”** — la wiki deve descrivere il progetto attuale, non i branch storici come stato corrente → [[system/decision-log]]
- [ ] 🔀 **Raccolta task per coding agent e meeting** — centralizzare in board i task emersi dalla rilettura completa della wiki da parte di Luca → [[artifacts/project-board]]

## 🟠 Decisioni da prendere

- [ ] 🛠 **Framework del nuovo build reale** — quanto riusare della build Datapizza storica e quanto invece tenere solo come reference design → [[system/stack]]
- [ ] 🛠 **Modello del PM** — tenere un frontier model dedicato al PM e modelli più economici per gli altri agenti, oppure uniformare lo stack LLM → [[system/modules/agents]]
- [ ] 🛠 **Separazione macro vs ticker analysis** — macro-desk separato, funzione specializzata o estensione del Market agent → [[system/modules/agents]]
- [ ] 🛠 **Granularità della futura struttura `wiki/system/`** — quanto spingere la scomposizione in sottocartelle senza perdere navigabilità umana → [[system/system-wiki-reorganization]]
- [ ] 📈 **Quali metodi portare per primi a codice** — scegliere il primo set di strategie da codificare e backtestare davvero → [[strategy/index]]

## ✅ Fatto

- [x] 🔀 **Policy editoriale 2026-06-23** — i claim “implementato / ✅ codice fatto” non descrivono più il presente del progetto: restano come storia o reference design, non come stato attuale → [[system/decision-log]]
- [x] 🛠 **Board ricondotta a hub minimo** — task, idee e decisioni ora puntano a pagine dedicate invece di duplicare dettagli sparsi → [[artifacts/project-board]]
- [x] 🛠 **Ingest delle daily notes 2026-06-20/21/22 avviato** — commenti e appunti convertiti in backlog esplicito di wiki e codebase → [[system/system-wiki-reorganization]]



%% kanban:settings
```json
{"kanban-plugin":"board","list-collapse":[false,false,false,false,false]}
```
%%
