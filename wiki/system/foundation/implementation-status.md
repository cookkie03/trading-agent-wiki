---
title: Implementation Status Policy
type: build
tags:
  - implementation-policy
  - architecture
  - roadmap
created: 2026-07-13T00:00:00.000Z
updated: 2026-10-31
status: active
related:
  - '[[system/foundation/architecture]]'
  - '[[system/_reference/fork-gap-analysis]]'
  - '[[system/_reference/canvas-code-mapping]]'
  - '[[artifacts/project-board]]'
confidence: high
area: software
---

# Implementation Status Policy

Il repository del progetto vive fuori da questo vault. La wiki è la spec condivisa, il registro delle decisioni e il backlog: non è una fonte affidabile per attestare processi attivi, branch, test, URL o moduli effettivamente presenti nel repository.

## Convenzioni

- Una pagina di design descrive un requisito o una decisione valida.
- Un riferimento a codice precedente è marcato **reference design / storico**.
- `Implementato`, `✅`, test verdi e dettagli di deployment compaiono solo con una verifica esterna datata e un link/record che la renda controllabile.
- La board contiene **specifiche da consegnare al coding agent**, non comandi o attività eseguite sul repository.
- Quando il codice esterno verrà verificato, si aggiorna una sola pagina di stato con data, evidenza e impatto sulle spec; non si duplicano claim in ogni pagina.

## Effetto sulla wiki

Le decisioni architetturali restano attive: monolite modulare, dati e tool con confini espliciti, output strutturati, guardrail deterministici, frontend sostituibile. I dettagli di branch o snapshot vengono consultati soltanto nelle pagine di [[system/_reference/fork-gap-analysis|reference design]] e [[system/_reference/canvas-code-mapping|mappatura storica]].

## Verifica workspace — 2026-10-30

Owner: 🛠 Luca (software).

Su richiesta di Luca sono stati clonati integralmente, con cronologia Git, i due repository nelle cartelle locali omonime sotto `/Users/luca/Documents/Projects/`:

| Cartella | Remoto `origin` | HEAD al clone | Tracking |
|---|---|---|---|
| `trading-agent` | `https://github.com/cookkie03/trading-agent.git` | `20bf209` | `main` → `origin/main` |
| `trading-agent-wiki` | `https://github.com/cookkie03/trading-agent-wiki.git` | `1d11798` | `main` → `origin/main` |

Verifica tramite `git remote -v`, `git status --short --branch` e `git log -1` in entrambe le cartelle. Al termine del clone entrambe erano pulite e senza divergenze dal tracking remoto.

Il repository Python contiene già `tradingagents/`, `tests/`, `pyproject.toml` e un README che descrive un'implementazione precedente. Questo attesta soltanto la presenza dei file: i test dichiarati dal README non sono stati eseguiti e il comportamento non è stato verificato.

Il [[artifacts/piano-operativo-trading-agent|piano operativo del 2026-09-02]] richiede una ripartenza da zero. Resta da definire come conservare e separare la codebase precedente durante l'avvio della nuova; questa sessione non modifica il codice né decide di riutilizzarlo.

Luca ha richiesto che ogni attività futura sul progetto inizi dalla consultazione della wiki. La procedura è registrata negli `AGENTS.md` locali. Aggiornati anche board, hot-cache e log; nessun commit o push effettuato.

## Ripartenza confermata — 2026-10-30

Su autorizzazione esplicita di Luca, creato commit locale `88ca413` su `main`: rimossi i file della precedente codebase, preservate le 27 skill di Matt Pocock in `.agents/skills/`, i collegamenti `.claude/skills/` e `.hermes/skills/`, `skills-lock.json` e `AGENTS.md`. Verifica: `git ls-tree --name-only HEAD` mostra solo queste cinque voci; working tree pulita, `main` avanti di un commit rispetto a `origin/main`. Nessun push e nessuna nuova implementazione.

La vecchia codebase è consultabile al [commit precedente `20bf209`](https://github.com/cookkie03/trading-agent/tree/20bf209), anche dopo la rimozione dalla working tree. L'ideazione parte dall'appunto Notion recuperato in [[system/foundation/codebase-architecture#Avvio per classi — 2026-10-30]].

## Scaffolding verificato — 2026-10-30

Dopo approvazione esplicita dell’alberatura da Luca: presenti dieci package Python (package radice più nove aree), `pyproject.toml`, directory test, `.gitignore` e `.dockerignore`. Verificati parsing TOML, sintassi AST e import dei dieci package senza dipendenze runtime; `git diff --check` superato in entrambi i repository. Non sono test del comportamento Broker. Nessuna classe applicativa, immagine Docker o distribuzione produzione ancora verificata. Modifiche locali senza commit/push. Requisito Docker e albero approvato in [[system/foundation/codebase-architecture#Alberatura approvata e requisito Docker — 2026-10-30]].

## Broker read-only — verifica 2026-10-31

Owner: 🛠 Luca. Su richiesta di Luca implementato il primo modulo Broker nel repository codice, ancora in working tree senza commit o push.

- File: `src/trading_agent/brokers/interface.py`, `models.py`, `alpaca.py`; dettagli in `docs/brokers.md` del codice.
- Contratto: conto, posizioni, finestra ordini filtrabile e limitata; importi Decimal, timestamp ordini UTC, gambe annidate ed errori espliciti. Nessun metodo di scrittura sul conto.
- Adapter: SDK ufficiale `alpaca-py` 0.44.0 vincolato e bloccato in `uv.lock`; factory paper. Client iniettato esplicitamente gestito dal chiamante.
- Evidenza eseguita: pytest sul vero SDK con HTTP simulato, fake offline dello stesso contratto e regressioni timeout/JSON invalido; 25 passati, 1 integrazione paper saltata. Mypy senza errori sul modulo; lint e formato verificati nel repository.
- Limite: Luca dichiara di avere un conto Alpaca, ma non risultano credenziali disponibili nell'ambiente letto. Nessuna chiamata autenticata eseguita. Prova read-only opt-in predisposta con `.env` locale.
- Invio/cancel, intent log, recovery, trade autonomo e deploy Docker restano fuori da questo slice.
