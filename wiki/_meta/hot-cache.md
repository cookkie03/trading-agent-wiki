---
tags:
  - langgraph-orchestration
  - trading-agent
  - codebase-design
---

# Hot Cache — Trading Agent

> Contesto di sessione recente. Il repository è esterno al vault: qui vivono spec, decisioni e priorità, non lo stato verificato del codice.

## Sessione 2026-10-31 — Convenzione Git e workspace

- Decisione Luca: il lavoro ordinario resta su `main` per il monitoraggio da VS Code. Worktree solo su richiesta o per modifiche radicali, sperimentali o incerte.
- Push su GitHub sempre; merge su `main` a cura di Luca; PR aperte dall'agente quando il lavoro è su branch separato.
- Convenzione completa: [[system/foundation/git-workflow]] e `docs/git-workflow.md` nel repository codice.

## Sessione 2026-10-31 — Workspace ripulito

- Rimosse dal repository codice le copie duplicate `code/` e `wiki/`.
- Stato canonico confermato: codice in `/home/luca/trading-agent/`, wiki in `/home/luca/trading-agent-wiki/`.
- Verificata la presenza dei file entry point della wiki e l'assenza delle due copie eliminate.

## Sessione 2026-10-31 — Convenzioni commenti Python

- Decisione Luca: adottare il metodo pragmatico ispirato ad antirez/Redis. Il codice spiega il cosa; i commenti spiegano perché, invarianti e vincoli non ovvi.
- Docstring brevi per interfacce pubbliche; commenti inline why-first per motivazioni, invarianti e vincoli degli adapter; commenti algoritmici soprattutto per ratio economiche, metriche di rischio, indicatori e backtest quando le feature entrano in vigore.
- Commenti temporali/storici solo per vincoli esterni attuali e verificabili, non come diario. Convenzione completa: [[system/foundation/python-commenting-conventions]].

## Sessione 2026-10-31 — MCP Mempalace

- Configurazione iniziale Docker superata: il server MCP utente in `/home/luca/.claude.json` usa ora `/home/luca/trading-agent/.venv/bin/mempalace-mcp --palace /home/luca/.config/mempalace/palace`.
- Verifica Python: MemPalace `3.11.0`, palace locale già indicizzato con **128.771 drawer**. Wing `trading_agent`: codice, documentazione, test, broker, storage, frontend e chat; wing `trading_agent_wiki`: raw, documentazione, planning e graphify output.
- Test contesto riusciti via CLI Python: la wiki restituisce `hot-cache.md`, `project-board.md` e `overview.md`; il repository restituisce decisioni MVP 2026-10-31 su SQLite, OpenBB/Alpaca, database, deduplicazione e dashboard.
- `claude mcp get mempalace` conferma il nuovo server Python connesso. I tool MCP già caricati in una sessione precedente possono mantenere il vecchio processo Docker fino al riavvio della sessione; la configurazione persistente è corretta.
- Pulizia Docker completata: rimossi i tre container Mempalace residui e l'immagine `ghcr.io/mempalace/mempalace` (~911 MiB di layer unici). Il volume Docker `mempalace-data` è stato conservato, ma non è usato dal server Python; il server attivo resta `/home/luca/trading-agent/.venv/bin/mempalace-mcp` con palace in `/home/luca/.config/mempalace/palace`.
- Dopo `/reload-plugins` il server ha dato `ENOENT` perché il venv non conteneva più `mempalace-mcp`. Il pacchetto `mempalace==3.11.0` è stato reinstallato solo nel venv (senza aggiungerlo a `pyproject.toml`); verificati executable, 128.771 drawer, ricerca contesto e `claude mcp get mempalace` → **Connected**.

## Sessione 2026-10-31 — Accelerazione MVP in quattro chat

- **Richiesta Luca**: guida operativa e avanzamento parallelo; lettura codice non è un gate. Filoni: vendor/schema e primo adapter, database, spiegazione OpenBB, dashboard.
- **Scelte delegate MVP**: SQLite se adeguato al singolo servizio writer; futura PostgreSQL/Timescale tramite repository/migrazioni senza portabilità automatica. Cache esclusa; persistenza/dedup/provenienza restano.
- **Frontend**: React + TypeScript + Vite/npm con backend Python read-only; parti non implementate non disponibili/demo. HMR, dati live e servizio persistente distinti.
- **Vendor**: contratti neutrali confermati; OpenBB è il primo vendor operativo dietro un adapter interno, con adapter diretti mantenuti come sostituti. Ricerca ufficiale Alpaca market-data completata; `AlpacaMarketDataProvider` implementa OHLCV storico equities con feed esplicito. Docker rimane requisito.
- **Layout codice**: merge consolidato su `main`; package applicativi spostati dalla gerarchia `src/trading_agent/` alla root (`data/`, `brokers/`, `storage/`, ecc.). 39 test focalizzati passati il 2026-10-31.
- **Coordinamento**: [[artifacts/mvp-parallel-work-2026-10-31]]. Sono decisioni/incarichi: nuove implementazioni, test e runtime devono ancora essere attestati. Execution e ordini fuori da questi incarichi.
- **Avanzamento ingestion**: `scripts/ingest_market_data.py` implementato nel worktree `worktree-market-data-ingestion`; test offline 42 passati e deduplicazione verificata con fake provider. Yahoo/Alpaca reali non ancora eseguiti; resta task opt-in con credenziali locali → [[artifacts/mvp-database-2026-10-31]].

## Sessione 2026-10-31 — Primo Broker read-only

- **Implementato** nel repository codice il contratto Broker conto/posizioni/ordini, modelli del progetto e adapter Alpaca paper. SDK ufficiale 0.44.0 e dipendenze bloccate.
- **Verifica**: 38 test offline focalizzati passati il 2026-10-31. Il test Paper read-only raggiunge `https://paper-api.alpaca.markets/v2` ma restituisce HTTP 401 `request is not authorized`; nessun ordine inviato. Le credenziali Paper nel `.env` vanno rigenerate/verificate localmente, mai in chat.
- **Luca ha un conto Alpaca**: predisposto `.env.example` e test opzionale di lettura; chiavi paper da configurare localmente, mai in chat.
- **Documentazione**: README, `docs/brokers.md` e architettura allineati; nessun nuovo commit/push.
- **Indicazione precedente, aggiornata dal piano sopra**: lettura dei tre file e prova paper restano utili, ma non sono gate per i filoni MVP; intent/execution/recovery restano separati.

## Sessione 2026-10-30 — Alberatura approvata, scaffolding e Docker

- Luca approva l'alberatura `src/trading_agent` e richiede deploy produzione con Docker; decisione in [[system/foundation/codebase-architecture#Alberatura approvata e requisito Docker — 2026-10-30]].
- Creati package per le dieci aree approvate, directory test, `pyproject.toml`, `.gitignore` e `.dockerignore`. Nessuna logica broker o runtime di trading ancora implementata.
- Docker è un requisito; Dockerfile, lock dipendenze e prova container restano da completare con il primo flusso eseguibile. Nessun deploy eseguito.
- Prossimo passo: definire e implementare il contratto Broker per lettura conto/posizioni/ordini. Modifiche locali senza commit/push.

## Sessione 2026-10-30 — Struttura, Broker e documentazione (fase precedente)

- **Priorità corrente Luca**: prima discutere struttura repository estremamente modulare, poi Broker e documentazione Alpaca; restare su passi leggibili e discutere il codice insieme.
- **Deleghe**: consulente `wiki_consultant` con fonti esclusivamente wiki, ricerca Alpaca su fonti ufficiali, agente documentazione con ricerca/installazione skill dedicate.
- **Proposta**: monolite modulare `src/trading_agent`, agenti separati dai workflow, analisi separate dai tool, broker intercambiabili. Bozza in `docs/architecture.md` del repo codice; ancora da discutere.
- **Primo slice candidato**: lettura conto/posizioni/ordini con fake offline e Alpaca paper; invio/recovery dopo. Nessuna nuova implementazione.
- **Documentazione**: creati README, `docs/architecture.md`, `docs/documentation.md` e ricerca Alpaca con fonti ufficiali; installate localmente `find-skills` e `readme-blueprint-generator`, preservate le 27 skill Matt Pocock. Routine di manutenzione in `AGENTS.md`; modifiche di questa fase non committate.

## Sessione 2026-10-30 — Ripartenza confermata e classi

- **Decisione Luca**: rimuovere la codebase precedente, conservare le skill di Matt Pocock e usarle per quanto possibile. Commit locale `88ca413`, working tree del codice pulita, nessun push.
- **Fonte recuperata**: [Notion — Projects → Trading Agent](https://www.notion.so/4012e441b0e581fcb942c109716dfb1f): Agent, Tool, Provider, Data Broker, Broker, documenti e Strategy; primi esempi concreti e test robusti.
- **Prossimo passo**: chiarire il significato di Provider e Data Broker, poi ideare insieme la prima slice infrastrutturale. Proposte non ancora approvate in [[system/foundation/codebase-architecture#Avvio per classi — 2026-10-30]].
- **Codice storico**: leggibile nella cronologia al commit `20bf209`; nessuna nuova classe implementata.

## Sessione 2026-10-30 — Collegamento workspace e consultazione wiki (precedente nella stessa sessione)

- **Workspace locale**: `/Users/luca/Documents/Projects/trading-agent` e `/Users/luca/Documents/Projects/trading-agent-wiki`, clonati rispettivamente da `cookkie03/trading-agent` e `cookkie03/trading-agent-wiki`, su `main` con tracking `origin/main`.
- **Istruzione di Luca**: per ogni richiesta sul progetto consultare prima la wiki, comprese le attività sulla codebase Python. Procedura in `AGENTS.md` dei due repository.
- **Contesto letto**: overview, taxonomy, board, piano operativo, architettura, confini codebase, MVP, stack, decisioni e policy di stato.
- **Punto aperto**: il repository scaricato contiene già codice Python precedente; il piano operativo richiede una ripartenza da zero. Il clone conserva quel codice; la strategia di ripartenza resta da definire, senza assumere il legacy come baseline verificata. Evidenze e limiti in [[system/foundation/implementation-status#Verifica workspace — 2026-10-30]].
- **Limiti**: nessuna esecuzione del sistema o suite di test; nessun commit o push in questa sessione. Le modifiche documentali sono locali.

## Sessione 2026-10-14 — Recupero della rilettura integrale

- **Esito**: ritrovato il registro della rilettura del 2026-07-13 in [[comment-resolution-2026-07-13]]; la board la marca completata. Il task originale non è stato individuato tra le conversazioni recenti o archiviate consultate.
- **Ambito registrato**: daily note dal 2026-06-06 al 2026-07-12 e tutte le annotazioni Obsidian `%%…%%` allora presenti in `wiki/`; i raw non sono stati modificati.

## Sessione 2026-09-02 — Piano Operativo Sviluppo & Risoluzione Git

- **Allineamento Git**: Configurato `core.filemode = false` per azzerare 623 falsi positivi di permessi dovuti al filesystem Synology Drive; verificata l'integrità del repo.
- **Skill Hermes Sbloccate**: Attivate `codebase-design`, `to-spec`, `to-tickets` in `software-development`, con `arxiv` e `competitor-news-monitor` per la ricerca.
- **Piano Operativo Integrato**: Creato [[artifacts/piano-operativo-trading-agent]], documento guida completo per lo sviluppo della codebase da zero con approccio TDD, architettura a imbuto (funnel), data layer OpenBB-first e orchestrazione LangGraph.
- **Project Board**: Aggiornata [[artifacts/project-board]] con i nuovi riferimenti di ricerca (incluso *OpenAlice*) e collegamento diretto al piano operativo.

## Sessione 2026-07-13 — Ingest editoriale integrale della rilettura

- **Input elaborati**: daily note dal 2026-06-06 al 2026-07-12 e tutte le annotazioni Obsidian `%%…%%` presenti nella wiki; le daily note/raw non sono state modificate.
- **Tracciabilità**: ogni annotazione è stata classificata e assorbita in [[comment-resolution-2026-07-13]]. Le annotazioni nascoste sono state rimosse dalle pagine operative; le impostazioni Kanban sono rimaste intatte.
- **Struttura**: `wiki/system/` è ora suddivisa in `foundation`, `data`, `tools`, `agents`, `orchestration`, `investment`, `execution`, `quant`, `interface`, `_reference`. Wikilink e index aggiornati. → [[system/foundation/wiki-reorganization]]
- **Policy fondamentale**: le pagine non attestano più implementazioni, branch, test o deploy del repository esterno; gli snapshot restano reference design. → [[system/foundation/implementation-status]]
- **Decisioni consolidate**: LangGraph + LangSmith; state annidato a campi fissi; MVP USD-only senza benchmark dinamico; analisi event-driven + health check periodico; OpenBB-first per catalogo e multi-vendor tramite wrapper. → [[system/foundation/decision-log]]
- **Nuovi artefatti**: [[system/data/data-vendors]], [[artifacts/tool-catalog.base]], [[comment-resolution-2026-07-13]].

## Stato del progetto nel vault

- **Design operativo**: [[system/foundation/architecture]] · [[system/foundation/mvp]] · [[system/foundation/stack]]
- **Board unica**: [[artifacts/project-board]]
- **Decisioni umane aperte**: ruolo Risk Analyst; confine Market/Sentiment; strategia MVP; revisione prompt/investment state; policy `next_check_date`; retention dati/documenti.
- **Ricerca non bloccante**: copertura vendor, fonti sentiment, optimizer/Black–Litterman, RAG+grafi, benchmark e UI evoluta.

## Nota LightRAG

La KB registrata `trading-agent-wiki` punta alla copia OneDrive ed è spenta; non è stata usata come fonte per questa sessione. Il vault iCloud letto direttamente resta la fonte affidabile.
