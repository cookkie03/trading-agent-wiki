---
tags:
  - langgraph-orchestration
  - trading-agent
  - codebase-design
---

# Hot Cache — Trading Agent

> Contesto di sessione recente. Il repository è esterno al vault: qui vivono spec, decisioni e priorità, non lo stato verificato del codice.

## Sessione 2026-11-01 — Formule tecniche su main

- Portato su `main` il commit `02db44e` (`feat: add standard technical indicator formulas`), originato dal branch tecnico `worktree-standard-indicators`.
- `analysis.indicators` espone SMA, EMA, RSI Wilder, MACD, ATR Wilder e Pivot Points classici come funzioni pure testate.
- La materializzazione persistente resta SMA v1: nessuna estensione del worker o della dashboard è stata introdotta senza parametri MVP e versioni formula chiusi.
- Verifica del branch tecnico: suite **64 passed, 1 skipped**; Ruff check e format passati.

## Sessione 2026-11-01 — Verifica coordinatore dello stato repository

- Verificato `/home/luca/trading-agent` su `main`: suite offline **64 passed, 1 skipped** con `uv run pytest`.
- Il repository contiene e verifica il flusso provider → SQLite deduplicato/provenienza → outbox/SMA materializzata → dashboard read-only; agenti, LangGraph, strategia/backtest e execution ordini non sono ancora implementati.
- Rilevato lavoro locale non committato per il bridge Telegram (`telegram-claude/`, test dedicato, extra `telegram` in `pyproject.toml`/`uv.lock`); bridge verificato solo offline, nessuna prova Telegram reale.
- Prossimo ordine raccomandato: chiudere decisioni MVP su strategia/Risk Analyst/Market-Sentiment, consolidare policy vendor/freshness/retention e verificare un flusso end-to-end prima di costruire orchestration agentica.

## Sessione 2026-11-01 — Verifica end-to-end Alpaca paper

- Verificato direttamente con credenziali locali via `uv run --env-file .env`, senza ordini: integration test Alpaca paper **1 passed**.
- Flusso reale su database temporaneo: Alpaca Market Data AAPL/feed IEX → ingestion **84 barre** → SQLite → outbox → **65 SMA materializzate e leggibili** → snapshot portfolio Alpaca → dashboard read model/API; `source=alpaca`.
- Corretto `data/providers/alpaca_market_data.py`: l'SDK restituisce oggetti `Bar`, non solo mapping. Il parser ora supporta entrambi i formati. Verifica Ruff passata.
- Nota operativa: il worker rispetta `available_at`; con un timestamp futuro può materializzare zero eventi immediatamente. È comportamento atteso.

## Sessione 2026-11-01 — Strategia MVP e state generico

- Luca ha corretto/confermato trend following su barre hourly, long-only, azioni USA, USD-only, swing trading.
- Implementato e verificato il primo contratto generico `analysis.strategy_state`: definizione strategia versionata con parametri, contesto mercato con feature/watermark, segnale, piano rischio e readiness; supporta future strategie senza fissare SMA o formule nella forma base.
- Verifica repository: **70 passed, 1 skipped**; Ruff passata. Documentazione nel repository: `docs/strategy-state.md`.
- Definita nella wiki la baseline strategica v0.1: hourly, breakout 20, EMA50, volume relativo 20, ATR14 stop 2x/trailing 3x, uscita EMA20 o stop, ingresso barra successiva, rischio 0.5% e cap posizione 10%; proposta da validare con backtest, non ancora codice di produzione.

## Sessione 2026-11-01 — Implementazione pipeline indicatori SMA

- Implementata nel repository la prima pipeline production-grade per SMA v1: `price_bars` + outbox nella stessa transazione, `indicator_values`, worker idempotente e rebuild deterministico.
- Migration SQLite 004: `indicator_values` con chiave `(symbol, interval, timestamp, indicator_name, parameters, formula_version)` e `outbox_events` con `event_key`, claim atomico, retry e `processed_at`.
- `SQLiteDashboardReadModel.sma()` legge solo derivati `ready`; il calcolo on-the-fly è fuori dal percorso production.
- Comando development: `uv run --env-file .env python -m scripts.materialize_indicators --database data/trading-agent.db --window 20`.
- Verifica repository: `59 passed, 1 skipped`; Ruff check/format attivi passati. Implementazione non estesa agli indicatori wiki RSI/MACD/ATR/Pivot perché formule e parametri MVP non sono ancora chiusi.
- Catalogo canonico: [[system/quant/quant-backtesting]].

## Sessione 2026-11-01 — Decisione sulla materializzazione dei derivati

- **Decisione consolidata di design:** raw normalizzati persistiti nella stessa transazione che determina il source watermark; evento/outbox dopo commit transazionale; worker incrementale idempotente.
- Il contratto `indicator_values` richiede provenance, source watermark, formula_version, parameters e status; il rebuild deve essere deterministico.
- Job schedulati solo per backfill, recovery e reconciliation. In production si leggono derivati `ready`; il calcolo on-the-fly resta fuori dal percorso production.
- **Implementazione:** non attestata. La pagina di dettaglio è [[system/db-access-performance]]; la decisione è registrata in [[system/foundation/decision-log]].

## Sessione 2026-11-01 — SMA collegata alla capability read-only

- Riferimento wiki applicato: DB centrale come source of truth; indicatori deterministici e pre-calcolati sono la direzione consolidata, ma la persistenza dei derivati richiede uno schema dedicato.
- Implementata la seam `SQLiteDashboardReadModel.sma(symbol, window, interval)`: legge le chiusure OHLCV persistite, usa `analysis.indicators.simple_moving_average` e restituisce timestamp finale + valore.
- Aggiunto `MarketDataRepository.history()` per concentrare la query ordinata nel repository; nessuna query SQLite nel chiamante e nessuna chiamata vendor.
- Verifica: test SMA dedicati e suite offline passati; capability read-only confermata senza introdurre ancora una tabella per indicatori derivati.
- Prossimo step coerente con la wiki: decidere e implementare eventualmente il compute-once-store degli indicatori con migrazione e provenance, prima di usarli come output persistente per agenti.

## Sessione 2026-11-01 — MemPalace persistente e verifica operativa

- Dichiarata la dipendenza runtime `mempalace>=3.11,<4` in `pyproject.toml` e `uv.lock`; `uv run mempalace --version` restituisce `3.11.0`.
- README aggiornato con palace condiviso, comandi di ricerca/verifica e procedura MCP.
- Palace verificato: 128.771 drawer, indice entro la flush-lag tolerance, MCP `Connected`.
- Pulizia storica non applicata: `sync` trova 93.254 drawer unresolved e li conserva; l’API MCP espone il basename `source_file`, non un path completo affidabile. Cancellare per basename sarebbe ambiguo e non sicuro.
- Reload: dopo commit/push, riavviare la sessione Claude Code o fare reload del plugin MCP; poi verificare `claude mcp get mempalace` e una ricerca semantica MCP.
- Dettaglio operativo: [[_meta/log]]

## Sessione 2026-11-01 — Ripristino Mempalace MCP

- Causa: l'eseguibile `/home/luca/trading-agent/.venv/bin/mempalace-mcp` non esisteva; venv e palace persistente erano presenti, ma il pacchetto `mempalace` mancava.
- Azione locale: installato `mempalace` (versione PyPI risolta `3.11.0`) nel venv esistente, senza modificare `pyproject.toml` o il codice del repository.
- Configurazione già corretta: `~/.claude.json` punta all'eseguibile ripristinato e a `/home/luca/.config/mempalace/palace`; il palace esiste con database Chroma/SQLite.
- Verifica: `mempalace-mcp --help`, avvio stdio locale con `--palace` e `claude mcp get mempalace` riusciti; ultimo stato `Connected`.
- Dettaglio operativo: [[_meta/log]]

## Sessione 2026-11-01 — Bridge Telegram project-scoped

- Implementato `trading-agent/telegram-claude/`: adapter Telegram con `python-telegram-bot`, SQLite per sessioni e invocazione di `claude-my-combo` nella root del progetto.
- Configurazione: `TELEGRAM_BOT_TOKEN` e `TELEGRAM_ALLOWED_USER_ID` in `~/.config/trading-agent/telegram.env`; token non committato.
- Comandi dedicati: new/sessions/resume/model/effort/goal/rewind/status/stop/help; default effort `high`; modelli ammessi `my-combo`, `gpt`, `gemini`.
- Verifica offline: suite completa `46 passed, 1 skipped`; prova Telegram reale non eseguita.
- Limiti correnti: `/stop` non interrompe subprocess; `/rewind` è inoltrato alla CLI; autocomplete argomenti non disponibile oltre al menu Bot API.
- Dettaglio: [[system/interface/telegram-claude-bridge]]

## Sessione 2026-11-01 — Baseline development e primo indicatore

- Convenzione development confermata: usare `uv run --env-file .env ...`; nessun `direnv`, auto-export shell o Docker aggiunto.
- Suite riallineata alla seam corrente `data.ingestion.ingest_ohlcv` / `to_stored_price_bar`; verifica: `51 passed, 1 skipped`.
- Capability read-only già coperta da `SQLiteDashboardReadModel`, che legge portfolio snapshot e latest market data senza duplicazione.
- Slice provider normalizzato → SQLite deduplicato → dashboard read model già verificata dai test offline.
- Aggiunto `analysis.indicators.simple_moving_average`, funzione pura su `Decimal`, con due test dedicati.
- Ruff check/format passati sui package attivi; il legacy `openbb-ui` resta escluso dai controlli globali.

## Sessione 2026-11-01 — Loader `.env` per sync portfolio

- Corretto `scripts/sync_portfolio.py` per caricare automaticamente `.env` dalla directory corrente o dalla root del progetto.
- Sono supportate le sole chiavi `ALPACA_API_KEY`, `ALPACA_SECRET_KEY` e `ALPACA_TRADING_URL`; le variabili già esportate nell'ambiente hanno precedenza.
- Test offline aggiunto in `tests/test_sync_portfolio.py`; verifica: 29 test pertinenti passati, Ruff check/format passati.
- Verifica reale read-only su `main`: `uv run python -m scripts.sync_portfolio --database data/trading-agent.db` → `Portfolio snapshot: inserted`.
- Commit su `main`: `934f670`; il database locale generato resta non tracciato.

## Sessione 2026-11-01 — Launcher dashboard locale

- Aggiunto nel repository codice `scripts/run_dashboard_dev.sh` e wrapper root `run_dashboard.sh`: dalla root si avvia tutto con `./run_dashboard.sh`; gestisce Ctrl+C e non avvia `openbb-ui`.
- Documentazione aggiornata in `README.md` e `docs/dashboard.md` con il comando breve.
- Verifiche: sintassi Bash e `git diff --check` passati; prova end-to-end non eseguita nel worktree perché mancano `frontend/node_modules` e il virtualenv ignorato. Installare con `npm ci --prefix frontend`; il launcher usa `.venv/bin/python`, poi `python3`.

## Sessione 2026-11-01 — Convenzioni test antirez / Redis / DS4

- Ricerca primaria consolidata in [[prior-art/libraries/redis-testing-practices]].
- Regole da applicare ai test: seam pubblico, expected indipendente, casi guidati dal failure mode, stati pass/skip/fail/incomplete distinti, fixture con provenienza, trace solo diagnostiche e misure riproducibili.
- Adattato `tests/data/test_yahoo_finance.py`: expected costruito con `PriceBar` pubblico invece di `bars[0].__class__`.
- Verifica: 1 test isolato passato; suite completa `42 passed, 1 skipped`; Ruff e `git diff --check` passati.

## Sessione 2026-10-31 — OpenBB yfinance operativo

- OpenBB 4.6.0 installato con `uv sync --extra openbb` nel worktree di configurazione.
- Prove reali riuscite: OHLCV e fundamentals AAPL via yfinance; serie GDP via FRED con 319 osservazioni; news yfinance ha restituito dati vuoti.
- `OpenBBProvider` espone `FundamentalMetrics` e `MacroObservation` oltre a `PriceBar`; 44 test passano.
- Fix e adapter sul branch `worktree-configure-openbb`, commit da consultare nel repository codice.

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
