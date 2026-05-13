# Sessione Brainstorming — 2026-05-13

**Partecipanti**: Luca, Claude Code
**Obiettivo**: definire la direzione del prototipo e struttura professionale del progetto

## Decisioni emerse

### Orizzonte del prototipo
- **Goal**: prototipo funzionante (non struttura aziendale, non research pura)
- **Tipo**: agente autonomo su **paper trading** + backtesting robusto continuativo + produzione metriche affidabili

### Portfolio vs Trading Singolo — chiarito
- **Scelta**: B in architettura (portfolio-first dal giorno 1), C in deployment (MVP su singolo asset)
- **Rationale (osservazione chiave)**: metriche per-trade e metriche di portfolio misurano cose diverse. Un sistema che fa bene i trade singoli può fare male come portfolio per via delle decisioni di allocazione/correlazione. Le due misure NON sono sovrapponibili — servono entrambe, ma bisogna distinguerle. I trade di ribilanciamento trattati come eventi discreti danno metriche per-trade leggibili DENTRO un framework portfolio.
- **Implicazione architetturale**: il modulo di trading opera su singolo asset, il modulo portfolio lo chiama N volte. I due livelli di metrica sono separati e collezionati indipendentemente.

### Orizzonte temporale dei trade
- **Scelta**: swing trading (giorni/settimane, candele 4h/daily)
- **Rationale**: alte aspettative di rendimento, analisi complessa richiede tempo (minuti), frequenza alta incompatibile con costo token

### Mercato iniziale
- Crypto / Binance (già deciso in precedenza)

## Osservazioni operative
- Il principio deterministico è un vincolo hard: LLM solo per ragionamento, tutto il resto Python
- DeepSeek come provider LLM preferito (costo 1/20 rispetto a modelli americani)
- Salvatore e Luca hanno ruoli distinti: Luca (AI/software), Salvatore (mercati/trading)

## Approcci architetturali valutati

### Opzione A — Monolite modulare (SCELTA)
Un singolo processo Python con moduli ben separati che comunicano via DB centrale (SQLite o Postgres). Ogni modulo è una classe con interfaccia definita. Il Prompt Builder li chiama in sequenza, assembla il prompt, invoca l'LLM, esegue il trade su paper account (Binance Testnet). Backtesting via libreria esistente (vectorbt o backtesting.py), non custom.
- Pro: sviluppo veloce, facile debug, un solo processo, moduli isolati e rimpiazzabili, passaggio a servizi incrementale senza riscrittura
- Contro: modulo lento può bloccare tutto (risolvibile con async), non scala orizzontalmente
- Perché scelta: rispetta il principio deterministico, allineata alla struttura mentale del wiki

### Opzione B — Agent framework (LangGraph / CrewAI) — scartata per ora
- Pro: gestione stato distribuita, logging nativo
- Contro: dipendenza pesante, overhead, rischio di violare principio deterministico
- Quando rivalutare: se si vuole contribuire a ecosistema open source o il monolite diventa ingestibile

### Opzione C — Microservizi dal giorno 1 — in backlog per fase successiva
- Pro: scalabile, ogni modulo rimpiazzabile indipendentemente, path naturale verso produzione
- Contro: overhead infrastrutturale enorme prima di avere un sistema funzionante
- Quando rivalutare: dopo che il monolite funziona e ci sono colli di bottiglia reali da misurare

## Design — Monolite Modulare MVP (Opzione A)

### Struttura del sistema
Processo Python schedulato (loop interno o cron). Ciclo ogni 4h o 24h (swing trading).

### Ciclo raffinato — integrazione Trading Floor Canvas

Il canvas trading-floor.canvas chiarisce una cosa critica: il Risk Analyst Agent è UPSTREAM del Trader, non downstream. Imposta i paletti prima che il Trader decida, non valida dopo.

```
Data Ingestion
  │
  ├── TAVOLO (in parallelo):
  │     ├── Analista      → ratio finanziari, validazione news
  │     ├── News Agent    → sentiment elaborato
  │     └── Quant Agent   → backtest/forecasting sull'asset
  │
  ├── Risk Analyst        ← legge output TAVOLO + stato portafoglio
  │     └── produce: briefing rischio (VaR, esposizione max, range SL/TP, go/no-go)
  │
  ├── Trader Agent        ← legge briefing rischio + output TAVOLO
  │     └── produce: entry, direction, size (entro i paletti del Risk Analyst)
  │
  ├── Security Module     → hard limits deterministici (statuto del fondo, no LLM)
  ├── Portfolio Allocator → size finale in base al portafoglio corrente
  ├── Exchange Module     → Binance Testnet (paper) o replay storico (backtest)
  └── Logger              → trade, reasoning, metriche
```

Il Trader Agent esegue deterministicamente (Python) una volta decisa la logica.
Backtesting: stesso codice, Exchange Module cambia backend (Binance Testnet → replay storico).

### Strategia del fondo — chiarimento
La domanda di Salvatore ("quale strategia se fossimo un fondo") è legittima e va risposta prima di costruire il Quant Agent. Le opzioni:
- Momentum/trend following: più comune in crypto
- Multi-factor fundamentals: ratio + news + macro — quello che avete già progettato
- Mean reversion: funziona in laterale, male in trend forti
L'architettura attuale è già multi-factor fundamentals by design. Non è necessario scegliere una strategia "pura".

## Sequenza di sviluppo — DECISIONE

### Strategia: parallelismo infrastruttura + progettazione quantitativa

**Track 1 — Luca (sviluppo solo)**
- Modulo A: Exchange Module + DB (Binance Testnet, esecuzione ordini paper, logger)
- Obiettivo: avere il pipe vuoto funzionante e dati reali che scorrono nel DB

**Track 2 — Luca + Salvatore (sessioni di progettazione)**
- Modulo C: Quant Agent + Backtesting (richiede sessioni dedicate con Salvatore per definire la strategia quantitativa)
- In parallelo con il Track 1: mentre Luca costruisce l'infrastruttura, si progetta il modulo quantitativo
- Decisione ancora aperta: quale framework backtesting usare (vectorbt vs backtesting.py)
- Decisione ancora aperta: risposta di Salvatore sulla strategia del fondo (multi-factor è l'orientamento, ma va formalizzato)

**Track 3 — dopo A completato, C progettato**
- Modulo D: Prompt Builder + LLM Trader
- Obiettivo: arrivare al Modulo D con dati REALI già nel DB (non fittizi), grazie al Track 1 già in produzione
- Questo è il target per avere il sistema "in funzione"

### Moduli successivi (dopo il core A+C+D)
- Risk Analyst Agent (upstream del Trader, come da canvas trading-floor)
- News Agent / Analista (TAVOLO)
- Security Module (hard limits deterministici)
- Portfolio Allocator

## Da fare
- Rispondere alla domanda di Salvatore sulla strategia del fondo (formalizzare in wiki)
- Chiudere decisione: quale framework di backtesting usare (vectorbt vs backtesting.py)
- Scrivere design doc formale nel wiki (build/)
- Iniziare progettazione Exchange Module (Track 1)

## Note stile di collaborazione
- Luca vuole che le sessioni di lavoro vengano registrate in raw/ e ingestate nella wiki
- Trattare questa wiki come memoria condivisa del progetto, incluse le sessioni con l'agent
