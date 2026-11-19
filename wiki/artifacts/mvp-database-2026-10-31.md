---
title: "MVP — database SQLite"
type: artifact
tags: [architecture, infrastructure, roadmap]
created: 2026-10-31
updated: 2026-10-31
status: active
confidence: high
area: software
---

# MVP — database SQLite

Owner: 🛠 Luca (software); aggiornamento della pagina affidato alla chat dedicata. Stato: incarico autorizzato, implementazione e verifiche da registrare.

## Obiettivo

Persistenza SQLite e migrazioni adeguate a singolo servizio writer; futura evoluzione PostgreSQL/Timescale senza portabilità automatica. Cache esclusa, dedup/provenienza conservate.

## Proprietà dei file

`src/trading_agent/storage/`, `tests/storage/`, `pyproject.toml`, `uv.lock`, `docs/storage.md`; integrazione finale `README.md` e `docs/architecture.md`.

## Criteri di completamento

Schema/chiavi concordati con vendor; round trip, dedup, riapertura e migrazioni verificati. Questa chat integra tutte le dipendenze Python.

Coordinamento: [[artifacts/mvp-parallel-work-2026-10-31]]. Nessun ordine, commit o push richiesto. Credenziali locali, mai in chat.

## Evidenze

**Implementazione 2026-10-31 (worktree `worktree-database-mvp`).**

- `src/trading_agent/storage/sqlite.py`: `Observation`, gateway `SQLiteDatabase`, repository, transazione atomica e migrazione `001_create_observations`.
- `tests/storage/test_sqlite.py`: 4 test offline per round-trip con riapertura, precisione `Decimal`/UTC/provenance, deduplica idempotente, rollback e versione schema.
- `docs/storage.md`: avvio/ispezione SQLite, contratto, limiti single-writer e percorso futuro PostgreSQL/TimescaleDB.
- README e `docs/architecture.md` aggiornati per lo stato effettivo.

**Verifiche iniziali:** `uv run pytest tests/storage/test_sqlite.py -q` → **4 passed**; Ruff check/format e `uv run mypy src/trading_agent/storage` → **passati**.

**Avanzamento PriceBar 2026-10-31.** Allineato il repository al contratto vendor-neutral `PriceBar` (OHLCV, `interval`, timestamp, `Decimal`, `source`, `collected_at`) disponibile nel filone Yahoo, senza duplicare l’adapter. La migrazione `002_create_price_bars` aggiunge tabella e indice; `MarketDataRepository` applica deduplica su `(symbol, interval, timestamp, source)` e lettura half-open `[start, end)`. Test aggiunti per round-trip, precisione, deduplica e finestra temporale.

**Verifiche PriceBar:** `uv run pytest tests/storage/test_sqlite.py -q` → **5 passed**; Ruff check/format e `uv run mypy src/trading_agent/storage` → **passati**.

**Ingestion OHLCV guidata — avanzamento 2026-10-31.** Nel worktree `worktree-market-data-ingestion` è stato aggiunto `scripts/ingest_market_data.py` per Yahoo Finance e Alpaca, con simboli predefiniti `AAPL`, `MSFT`, `SPY`, intervallo esplicito, database configurabile e statistiche `fetched`/`inserted`/`duplicates`. `tests/test_ingest_market_data.py` verifica l’adattamento della provenance e due esecuzioni idempotenti sulla chiave `(symbol, interval, timestamp, source)`.

**Verifiche ingestion:** `uv run pytest` → **42 passed, 1 skipped**; `uv run ruff check .` e `uv run ruff format --check .` → **passati**; `uv run python scripts/ingest_market_data.py --help` → **passato**. La suite è offline: non sono state eseguite chiamate reali Yahoo/Alpaca né sono state usate credenziali. Il comando reale è documentato in `README.md`; il secondo avvio sullo stesso intervallo è il controllo operativo della deduplicazione.

**Verifica runtime Yahoo — 2026-10-31:** eseguito due volte nel database temporaneo `/Users/luca/.claude/jobs/8611f365/tmp/real-ingestion.sqlite` su `AAPL`, `MSFT`, `SPY`, intervallo `2026-10-01T00:00:00Z`–`2026-11-01T00:00:00Z`: primo run 22 barre per simbolo, secondo run idempotente; query finale `source=yahoo_finance` → 66 righe totali. Sono comparsi solo warning di deprecazione interni a yfinance. Alpaca non eseguito perché il worktree non contiene credenziali locali configurate.

**Limiti:** non sono stati avviati PostgreSQL/TimescaleDB, servizi autenticati o broker; nessun ordine è stato inviato. L’ingestion Alpaca resta un’azione opt-in da eseguire con credenziali locali e va registrata separatamente come evidenza runtime.

**Decisione implementata:** SQLite è sufficiente per MVP single-host/single-writer. La futura evoluzione PostgreSQL/TimescaleDB richiederà un adapter e migrazioni revisionate; non è garantita la portabilità cambiando soltanto una URL. Questa pagina iniziale non attesta software funzionante.
