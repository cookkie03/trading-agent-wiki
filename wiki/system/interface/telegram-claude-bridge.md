---
title: Telegram Claude Bridge
type: build
status: draft
area: software
owner: Luca
updated: 2026-11-01
related:
  - '[[system/interface/frontend-module]]'
  - '[[system/foundation/codebase-architecture]]'
---

# Telegram Claude Bridge

## Decisione

Il controllo remoto di Claude Code è project-scoped: il bridge vive in `trading-agent/telegram-claude/`, usa il virtualenv del progetto e avvia il comando locale `claude-my-combo` nella root del repository. Non espone Claude Code per tutto il PC.

## Interface

Telegram usa long polling, whitelist tramite `TELEGRAM_ALLOWED_USER_ID` e token esterno al repository tramite `TELEGRAM_BOT_TOKEN`. Le sessioni sono persistenti in SQLite e vengono riprese con `--resume`.

Comandi dedicati: `/new`, `/sessions`, `/resume`, `/model my-combo|gpt|gemini`, `/effort low|medium|high|max`, `/goal`, `/rewind`, `/status`, `/stop`, `/help`. Il menu comandi Telegram è registrato via Bot API.

## Stato

Nota storica: il 2026-11-01 è stata riportata una verifica offline con 46 passed e 1 skipped; non attesta lo stato attuale. Al 2026-11-05 il bridge e i relativi test risultano non tracciati nel workspace del repository: non sono una funzionalità pubblicata né una priorità della ripartenza. La destinazione del codice residuo resta da valutare. Non risulta una prova Telegram reale; non inserire token nel repository.

## Limitazioni note

`/stop` è ancora informativo: non interrompe una subprocess già avviata. `/rewind` viene inoltrato alla CLI e non offre ancora una selezione guidata del checkpoint. Telegram suggerisce i comandi slash tramite il menu Bot API; non offre autocomplete generico affidabile per gli argomenti.
