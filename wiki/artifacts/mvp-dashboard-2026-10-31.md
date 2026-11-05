---
title: "MVP — dashboard read-only"
type: artifact
tags: [architecture, infrastructure, roadmap]
created: 2026-10-31
updated: 2026-10-31
status: active
confidence: high
area: software
---

# MVP — dashboard read-only

Owner: 🛠 Luca (software); aggiornamento della pagina affidato alla chat dedicata. Stato: incarico autorizzato, implementazione e verifiche da registrare.

## Obiettivo

React + TypeScript + Vite/npm e backend Python read-only. Mappa completa con sezioni non disponibili/demo esplicite.

## Proprietà dei file

`frontend/`, `src/trading_agent/interface/`, relativi test, `docs/dashboard.md`.

## Criteri di completamento

Concordare contratti con vendor/DB; verificare avvio, API read-only, vuoto/errore/caricamento e fonte/data. Distinguere HMR, dati live e servizio persistente. Coordinare dipendenze Python con DB senza scrivere pyproject/lock.

Coordinamento: [[artifacts/mvp-parallel-work-2026-10-31]]. Nessun ordine, commit o push richiesto. Credenziali locali, mai in chat.

## Evidenze

Verifica esterna eseguita il 2026-10-31 nel worktree isolato `worktree-dashboard-mvp`.

### Scelte e file prodotti

- Scelta corrente applicata: React + TypeScript + Vite/npm, backend Python stdlib read-only; Streamlit resta riferimento storico e non prevale sulla decisione MVP corrente.
- Contratto Python in `src/trading_agent/interface/dashboard.py`: `DashboardReadModel`, snapshot JSON, adapter vuoto esplicito senza persistenza duplicata.
- Server in `src/trading_agent/interface/server.py`: `GET /api/dashboard`, `GET /api/control-surface`, `GET /api/health`; POST/PUT/PATCH/DELETE non espongono scritture e restituiscono 404; bind locale con porta configurabile (default 8000).
- Primo slice control surface: `ControlSurfaceSnapshot` osserva moduli, runtime, configurazione non sensibile, eventi, source e freshness; `EmptyControlSurfaceReadModel` mantiene il caso senza DB esplicito e non introduce persistenza.
- Frontend in `frontend/`: Vite + React + TypeScript, polling UI ogni 15 secondi, stati loading/errore/vuoto, source e freshness visibili, nessun numero finanziario demo.
- Dipendenze richieste all’integratore DB e limiti: `docs/dashboard-dependencies.md`; descrizione MVP: `docs/dashboard.md`.

### Comandi e risultati

- `PYTHONPATH=src python -m pytest tests/interface -q` → **5 passed** (contratti portfolio + control surface).
- `npm --prefix frontend install` → 26 pacchetti, audit **0 vulnerabilità**.
- `npm --prefix frontend run build` → build Vite/TypeScript riuscita (`frontend/dist`).
- Backend: `PYTHONPATH=src python scripts/run_dashboard.py` → ascolto loopback su `http://localhost:8000`.
- Frontend: `npm --prefix frontend run dev -- --host localhost` → URL reale **http://localhost:5173/**.
- `curl http://localhost:8000/api/health` → `{"status":"ok","read_only":true}`.
- `curl http://localhost:8000/api/dashboard` → HTTP 200, `source: "not connected"`, `portfolio.available: false`, `benchmark: "post-mvp"`.
- `GET /api/control-surface` → HTTP 200, `source: "not connected"`, runtime `unavailable`; nessuna configurazione è modificabile dalla UI.
- `curl http://localhost:5173/` → HTML con titolo `Trading Agent / cockpit` e root React.

### Aggiornamento 2026-11-01 — DB, stati e Docker

- Il read model persistente ora legge le ultime barre OHLCV SQLite per simbolo nella watchlist; portfolio resta indisponibile finché non viene integrato il broker snapshot.
- `frontend/src/App.tsx` distingue loading, errore dashboard, errore control-surface e conserva l'ultimo snapshot in stato stale; il Retry è esplicito e accessibile.
- `npm ci --prefix frontend` e `npm --prefix frontend run build` → passati.
- `Dockerfile` e `compose.yaml` aggiunti: build Docker riuscita; smoke runtime su porta temporanea ha verificato `GET /api/health` con `read_only: true` e `GET /api/dashboard` con stato vuoto esplicito. Container e volume smoke rimossi dopo la verifica.

### Aggiornamento portfolio Alpaca — 2026-11-01

Il dashboard read model legge ora lo snapshot `alpaca` dal DB centrale e popola cash, equity, posizioni e ordini; in assenza di snapshot mantiene `portfolio.available=false`. La UI non interroga direttamente il broker e non scrive dati. Per sviluppo usare il launcher locale senza Docker; Docker resta il percorso di deployment persistente.

### Limiti dichiarati

- Il read model persistente/DB non è ancora collegato: portfolio, watchlist, decisioni, trigger e run restano vuoti/non disponibili senza fingere dati.
- Il backend è un runner locale di sviluppo, non un servizio 24/7: Mac spento interrompe entrambi i processi; un host sempre acceso e un deployment gestito sono ancora necessari per persistenza/uptime continui.
- Vite HMR e polling dati sono distinti; polling 15s è una frequenza UI, non una promessa di feed finanziario real-time.
- Nessuna chiamata autenticata broker, nessun ordine, nessuna scrittura e nessuna credenziale usata.
