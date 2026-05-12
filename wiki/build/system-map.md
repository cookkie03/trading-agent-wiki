---
title: "System Map"
type: build
tags:
  - build
  - architecture
created: 2026-04-30
updated: 2026-05-10
status: draft
related:  - "[[theory/modular-trading-agent-architecture]]"confidence: high
priority: high
area: software
sources:
  - "[[references/conversazione-luca-salvatore-2026-04-28-30]]"
  - "[[references/videochiamata-luca-salvatore-2026-04-30]]"
---

# System Map

Mappa dell'architettura software del `trading-agent`. Il sistema è progettato per essere un ecosistema modulare che supporta inizialmente un workflow di **augmentazione** per il trader.

## Componenti Architetturali

### 1. Data & Persistence Layer (The DB)
- **Market State**: Prezzi, volumi, order book (Binance API).
- **News/Sentiment Store**: Feed di notizie pre-elaborate.
- **Factor Store**: Coefficienti quantificati per ogni tipologia di evento/fattore (medie empiriche su serie storiche).
- **Trade History & Reasoning Log**: Memoria storica di ogni trade + chain-of-thought dell'agente.
- **Portfolio State**: Stato corrente delle posizioni (derivato dallo storico trade). Metriche: drawdown, rendimento annuale, esposizione ai margini.
- **Prompt Store**: Prompt assemblati dal Prompt Builder, pronti per essere consumati dall'LLM Trader.

### 2. Research & Intelligence (Multi-Agent Team)
- **News Analyst**: Agente focalizzato sull'interpretazione delle notizie; converte testo in segnali numerici.
- **Technical Analyst**: Individua soglie psicologiche (supporti/resistenze) e bias di mercato. Attenzione: può corrompere il modello predittivo se mal calibrato.
- **Prediction Agent (DL)**: Algoritmo di deep learning addestrato sui fattori quantificati. Trova relazioni non lineari fattori → prezzo.
- **Factor Investigation Agent**: Agente dedicato allo studio di quali fattori includere; valida i fattori contro la serie storica e aggiorna i coefficienti.
- **RL / Weighting Module**: Ponderazione dinamica dei moduli in base agli esiti storici dei trade.
- **Fine-Tuning Module**: LLM periodicamente addestrato sull'intero storico del progetto.

### 3. Prompt Builder
- Componente deterministica (non LLM).
- Legge gli output di tutti i moduli dal DB.
- Assembla il prompt completo e lo salva nel Prompt Store.
- Disaccoppia la raccolta dati dall'invocazione dell'LLM.

### 4. Execution & Control
- **Trader Agent (LLM)**: Legge il prompt più recente dal Prompt Store. Produce la proposta di trade o di ribilanciamento.
- **Security Module**: Guard deterministici non-LLM. Valida ogni proposta contro lo "statuto del fondo" (esposizione max 5%, vendita a +100%).
- **Risk Manager / Portfolio Manager**: Utilizza la libreria **Portfolio Optimizer** per calcolare i pesi ottimali del paniere. Gestisce il Trailing Stop Loss e il ribilanciamento periodico.
- **Exchange Module (Binance)**: Esegue gli ordini.

## Protocollo di Comunicazione Strutturata

Per mantenere l'integrità del dato ed evitare degradazione nei prompt, il sistema adotta un flusso basato su report:
1. **Modules → DB**: Ogni modulo produce un report strutturato (JSON) nel DB.
2. **DB → Prompt Builder**: Il builder estrae solo i campi rilevanti dei report.
3. **Prompt → Agent**: L'agente riceve un prompt denso di informazioni strutturate, riducendo il rumore discorsivo.

### 5. UI & Monitoring Layer
- **Streamlit Dashboard**: Visualizzazione in sola lettura. Metriche: drawdown, rendimento, esposizione. Ispirata a SFC Investment Fund (link in `raw/articles/`). Accesso pubblico senza autenticazione (no tasti di azione).
- **Telegram Bot/Canale**: Notifica ogni trade con tutti i parametri. Link pubblico in sola lettura.

## Flussi Principali

1. **Ingest & Enrich**: Dati grezzi (market, news, factors) entrano nel DB.
2. **Analysis**: Agenti specializzati producono i loro output nel DB.
3. **Prompt Build**: Prompt Builder assembla un prompt completo nel Prompt Store.
4. **Trader Decision**: LLM Trader legge il prompt → produce proposta (entry, SL, TP).
5. **Validation**: Security Module + Risk Manager validano la proposta.
6. **Execution**: Exchange Module esegue l'ordine su Binance.
7. **Logging**: Esito + ragionamento loggati nel DB → alimentano RL e Fine-Tuning.

## Roadmap di Implementazione
- **Fase 1 (Dashboard)**: Visualizzazione dati e analisi manuale supportata da agenti.
- **Fase 2 (Augmentation)**: Proposte di trade generate dall'agente per l'approvazione umana.
- **Fase 3 (Autonomy)**: Esecuzione automatica con supervisione e kill-switch.
