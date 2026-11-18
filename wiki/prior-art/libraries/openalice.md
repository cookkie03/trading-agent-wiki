---
title: OpenAlice (TraderAlice)
type: source
tags:
  - prior-art
  - trading-agent
  - execution
raw_source_path: https://github.com/TraderAlice/OpenAlice (docs/architecture/core-concepts, extending/custom-guards, workspace-issues-and-scheduling)
created: 2026-11-18T00:00:00.000Z
updated: 2026-11-18T00:00:00.000Z
status: active
confidence: high
related:
  - '[[prior-art/benchmark-trading-agent-repositories]]'
  - '[[system/agents/agent-tools]]'
  - '[[prior-art/libraries/cvx-portfolio-optimizer]]'
---

# OpenAlice (TraderAlice)

Reference principale indicata da Luca (2026-11-18). Monorepo TypeScript (pnpm/turbo), licenza **AGPL-3.0**: si copiano idee e forme, non codice. Ospita agenti nativi esistenti (Claude Code, Codex, OpenCode, Pi) invece di avere un suo loop: utile per la ricerca sulla portabilità.

Confronto punto per punto con le nostre decisioni: [[prior-art/openalice-vs-trading-agent]].

## Idee rilevanti per noi

**Trading as Git.** Ogni mutazione del conto segue `stage → commit (messaggio + hash) → push`. Il push di default attende l'**approvazione umana** (Web UI o Telegram `/uta`); un interruttore esplicito, spento di default, permette all'AI di eseguire da sola. Esiti per operazione: `submitted`, `filled`, `rejected`, `cancelled`, `user-rejected`. `tradingSync` riconcilia i fill come commit di sync. I rifiuti restano nello storico e l'agente li rilegge.
→ Da noi: **coda di approvazione** degli ordini dopo il Risk Gate (Q45), storico ordini con motivazione e esiti, rifiuti umani visibili al PM al ciclo successivo.

**Approvazione legata all'hash.** Mentre un commit è in attesa, il conto rifiuta nuovi stage; approvare o rifiutare richiede l'hash mostrato in revisione, così un'azione vecchia non approva operazioni diverse.
→ Da noi: approvazione per `order_id` + hash del contenuto della bozza; se la bozza cambia, l'approvazione decade.

**UTA (Unified Trading Account).** Un oggetto per conto collegato che nasconde il broker (Alpaca, IBKR, CCXT, simulatore): log delle operazioni, politica di esecuzione, snapshot dell'equity, salute del broker (`healthy/degraded/offline/disabled`). L'agente non conosce i dettagli del broker.
→ Conferma Q36: gli agenti lavorano sul "loro broker" senza sapere se è paper o live; credenziali broker modificabili dall'utente come quelle LLM.

**Guard.** Middleware deterministico al push: `check(operation, positions, account) → None | motivo`. Il primo rifiuto vince; non scavalca l'approvazione. Guard incluse: `max-position-size`, `cooldown`, `symbol-whitelist`. Preferire controlli ricalcolabili dallo stato del broker, non contatori in memoria.
→ Forma naturale del nostro **Risk Gate**: lista ordinata di guard pure, configurabili.

**Modalità Lite / Readonly / Pro.** Livelli globali: broker scollegato, sola lettura, scrittura.
→ Simile al nostro **kill switch** (`halt`/`resume`, Q43).

**Issue con schedule e Inbox.** Le attività ricorrenti sono file Markdown con `when` (cron/every); lo scheduler avanza il cursore solo quando il run è accettato e non riprova a raffica. L'Inbox è la superficie dei report verso l'umano.
→ Da noi: scheduler del Trigger engine con cursore persistente e nessun retry automatico a raffica; il Market Analyst lavora su un suo calendario.

**Stato su file.** Niente DB: JSON/JSONL/Markdown/git sotto `~/.openalice`, credenziali sigillate a riposo.
→ Noi restiamo su SQLite (Q39), ma le credenziali vanno comunque cifrate o tenute fuori dal DB.
