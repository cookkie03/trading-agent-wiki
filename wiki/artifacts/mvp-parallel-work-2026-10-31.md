---
title: "MVP — lavoro parallelo del 2026-10-31"
type: artifact
tags: [architecture, infrastructure, roadmap]
created: 2026-10-31
updated: 2026-10-31
status: active
confidence: high
area: software
---

# MVP — lavoro parallelo del 2026-10-31

Owner: 🛠 Luca (software), coordinamento chat principale. Stato: direzione autorizzata e incarichi assegnati; nuove implementazioni e verifiche non ancora attestate.

## Richiesta e decisioni correnti

Luca chiede di accelerare con guida operativa e quattro chat. Lo studio del codice non è un gate prima di avanzare; spiegazioni Python accompagnano gli output. La verifica autenticata read-only del Broker resta utile ma non blocca questi filoni e non autorizza ordini.

- SQLite per l'MVP se adeguato al workload di un singolo servizio writer. Repository e migrazioni devono permettere una futura evoluzione PostgreSQL/TimescaleDB, senza promessa di portabilità automatica. Questo aggiorna per l'MVP la precedente divisione SQLite-dev/Postgres-prod.
- Cache esclusa dal lavoro corrente. Persistenza, deduplicazione, provenienza e consistenza restano necessarie.
- Dashboard React + TypeScript + Vite/npm e backend Python read-only; questa scelta supera la preferenza iniziale Streamlit per l'MVP.
- La dashboard rappresenta la mappa completa del sistema: sezioni senza dati/funzionalità dichiarate non disponibili o demo. Non deve fingere agenti, workflow o trading in esecuzione.
- HMR aggiorna il codice frontend durante lo sviluppo: aggiornamento dei dati live e servizio persistente richiedono contratti e verifiche distinti.
- Vendor agnostic confermato. OpenBB-first è da riesaminare, non è un SDK obbligatorio da installare prima della valutazione.
- Docker resta requisito; nessuna immagine o servizio verificato è attestato da questo piano.

## Filoni, ownership e coordinamento

| Chat | Obiettivo e file assegnati | Dettaglio wiki |
| --- | --- | --- |
| Vendor/schema | Inventario completo delle capacità wiki, priorità valore/difficoltà e primo adapter con classi neutrali. Possiede `src/trading_agent/data/`, `tests/data/`, `docs/research/vendor-selection.md`, `docs/data-model.md`. | [[system/data/vendor-selection-2026-10-31]] |
| Database | SQLite e migrazioni con confini per futura PostgreSQL/Timescale. Possiede `src/trading_agent/storage/`, `tests/storage/`, `pyproject.toml`, `uv.lock`, `docs/storage.md`; integra per ultimo `README.md` e `docs/architecture.md`. | [[artifacts/mvp-database-2026-10-31]] |
| OpenBB | Spiegazione comprensibile e valutazione del ruolo rispetto agli adapter diretti; solo ricerca in `docs/research/openbb-assessment.md`. | [[artifacts/mvp-openbb-2026-10-31]] |
| Dashboard | Frontend e API Python read-only. Possiede `frontend/`, `src/trading_agent/interface/`, relativi test, `docs/dashboard.md`. | [[artifacts/mvp-dashboard-2026-10-31]] |

Ogni chat aggiorna la propria pagina; board e file wiki comuni hanno come riferimento unico questo coordinamento. Le dipendenze Python sono comunicate al database, unico writer di pyproject e lock. Il coordinatore verifica l'integrazione finale: controlli separati non dimostrano da soli un flusso end-to-end.

## Criteri di completamento

1. Vendor/schema: distinguere capacità richieste, fonti candidate, accessi/licenze; concordare contratto normalizzato con DB e UI. Verificare mapping, provenienza ed errori offline, distinguendo chiamate reali da fake.
2. Database: concordare schema e chiavi con vendor; verificare round trip, dedup, riapertura e migrazioni. Documentare limiti del singolo writer e condizioni per passare a Postgres; nessun livello cache.
3. OpenBB: spiegazione e raccomandazione con fonti ufficiali datate, separate dai requisiti wiki. Nessuna implementazione o approvazione implicita di SDK.
4. Dashboard: avvio documentato, API read-only, stati vuoto/errore/caricamento e fonte/data; demo e parti non implementate esplicite. Smoke test sul flusso realmente disponibile.
5. Integrazione: allineare contratti/dipendenze e documentazione; registrare comandi, risultati e limiti reali. Credenziali solo locali, mai in chat, frontend o log.

## Dipendenze e fuori scope

Lo scope rimane US equity paper USD-only. Strategia con Salvatore e topologia agentica sono decisioni separate. Invio/cancel, trading autonomo, intent log ed execution/recovery restano una slice distinta: prima delle future scritture servono intent persistenti, lookup client ID, esiti incerti e riconciliazione. Un client ID non garantisce da solo exactly-once.

## Stato e relazione con il passato

Queste sono decisioni/incarichi, non prove di software funzionante. Per il Broker precedente vedere [[system/foundation/implementation-status#Broker read-only — verifica 2026-10-31]]. La lettura guidata prima dell'avanzamento non è più un gate. [[artifacts/piano-operativo-trading-agent]] resta roadmap generale; [[system/data/data-vendors]] resta catalogo capacità con OpenBB-first in riesame. Gli snapshot storici non attestano implementazioni.
