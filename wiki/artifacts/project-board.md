---
title: "Project Board — Trading Agent"
type: artifact
tags:
  - artifact
  - roadmap
  - execution
  - architecture
created: 2026-04-30
updated: 2026-05-29
status: active
related:
  - "[[build/system-map]]"
  - "[[build/decision-log]]"
  - "[[build/stack]]"
  - "[[build/ideas-log]]"
  - "[[strategy/metrics/benchmark]]"
confidence: high
priority: high
area: ops
kanban-plugin: board
sources:
  - "[[references/conversazione-luca-salvatore-2026-04-28-30]]"
  - "[[references/notion-export-investimento-trading]]"
  - "[[references/trading-floor-canvas]]"
---

> Board unica di progetto. Marker di dominio per card: 🛠 = tecnico/software (Luca) · 📈 = mercato/strategia (Salvatore) · 🔀 = condiviso/trasversale.
> Consolida le ex board `luca-board`, `salvatore-board` e `kanban-project-status` (2026-05-29). Le decisioni storiche superate sono annotate inline con *aggiornata:*.

## 💡 Idee

- [ ] 🛠 **Volume Spike Detection — algoritmo** — rilevatore di picchi anomali di volume: baseline rolling, z-score, classificazione causa. Da valutare come modulo separato o parte del News module
- [ ] 🛠 **Logging strutturato della chain-of-thought** — schema del log per ogni trade: input moduli → ragionamento LLM → decisione → esito. Fondamentale per fine-tuning e analisi RL
- [ ] 🛠 **Continuous Learning real-time** — fine-tuning sul dato in streaming. Problema ancora aperto nella ricerca: esplorare dopo che il fine-tuning batch funziona
- [ ] 🛠 **Exchange module intercambiabile** — interfaccia astratta, contratto I/O identico tra adattatori (paper → live → eventuale DEX)
- [ ] 🛠 **Costo per trade — vincolo API** — stimare il costo in token (€) di ogni invocazione dell'LLM Trader col prompt pieno. Influenza la frequenza massima sostenibile → token cost estimator in [[build/modules/risk-management]]
- [ ] 📈 **Strategia Sentiment degli Analisti** — capire il *perché* del consenso bullish/bearish: identificare il pattern di metriche che lo genera → il bot lo replica e trada prima della folla. Idea originale, diversa dal factor investing classico
- [ ] 📈 **Stop loss istituzionali a domino** — sfruttare le soglie psicologiche dove si concentrano gli SL degli istituzionali: sotto soglia scatta una cascata prevedibile. Come identificarle in anticipo?
- [ ] 📈 **Quantificazione eventi rari** — come gestire eventi mai visti (prima riunione di un nuovo presidente BCE)? Usare la categoria più vicina o trattarli come unknown?
- [ ] 📈 **Analisi dei paper di finanza** — raccogliere paper accademici rilevanti (anche factor investing crypto) e ingestarli nel wiki per costruire la base teorica dei fattori


## 🔴 Da fare

- [ ] 🛠 **Progettare lo schema del DB esteso** — consolidare il design 2026-05-29: rendicontazione portafoglio (liquidità, distribuzione multi-filtro, P/L), dati live (prezzi, calendario, news, macro, insider, cambi), costituzione/statuto al centro, log (states/reports/transactions) + retention/clustering. Vedi [[build/modules/exchange-db]]
- [ ] 🛠 **Definire I/O spec per ogni modulo** — cosa entra (formato, fonte) e cosa esce (formato, destinazione nel DB) per: Prompt Builder, News Research Agent, Factor Quantification, Prediction Module, Risk Analyst Agent, Analista (Ratio/Grafici)
- [ ] 🛠 **Riscrivere il grafo LangGraph** — tenere `dataflows` + LLM clients di TradingAgents; riscrivere node/edge/state/tool secondo la topologia 2026-05-29 (analisti → research_state → Risk Analyst → Trade deterministico; PM orchestratore; investment_state gate). Vedi [[build/modules/llm-agent-system]]
- [ ] 🛠 **Implementare gli Extractors** — Extractors set + Adaptive extractor (frequenza per vicinanza al target, rispetto rate limit) + Market Alert agent + calendar tool. Vedi [[build/modules/exchange-db]]
- [ ] 🛠 **Configurare OpenRouter + DeepSeek V4 Pro** — setup del router e del modello principale
- [ ] 🛠 **Studiare i corsi completi LangGraph e LangSmith** — finora solo i Quickstart; serve il Foundation/completo
- [ ] 🛠 **Valutare canale Telegram "sala segnali"** — calendario, riassunti news, prezzi, trade, variazioni rilevanti (orario/giornaliero), alert interattivi
- [ ] 🛠 **Ingestare il file market driver di Salvatore** — quando arriva in `raw/` come TXT (`/wiki-ingest` + aggiornare la board)
- [ ] 🛠 **Definire metriche di portafoglio per la dashboard** — drawdown, rendimento, esposizione e KPI per la dashboard Streamlit (catalogo riusabile in [[references/external/sfc-portfolio-tracker]])
- [ ] 🛠 **Registrare la decisione "Dashboard di Augmentazione"** in [[build/decision-log]]
- [ ] 🛠 **Analizzare FinAgent (tecnico)** — clonare la repo: come sono implementati gli agenti, framework, comunicazione, gestione del prompt
- [ ] 🛠 **Analizzare AlphaArena (tecnico)** — 5 LLM in parallelo su Bitcoin: struttura codice, gestione output, integrazione exchange
- [ ] 🛠 **Analizzare NeuroEspresso — Silvio Baratto (tecnico)** — pattern multi-agente, struttura del codice, cosa è rimasto incompleto e perché
- [ ] 🛠 **Studiare il Cornell Paper** — fonte citata, da reperire e analizzare
- [ ] 📈 **Raccogliere e validare indicatori di analisi tecnica** — medie mobili, Fibonacci, supporti/resistenze, volumetrica. Note raw in Obsidian, l'agente le struttura (call 05-06)
- [ ] 📈 **Lista di fattori candidati per il modello** — per ogni fattore: categoria (macro / aziendale / ratio / evento), misurabilità numerica, strumento/mercato impattato (es. tasso BCE, fatturato trimestrale, dimissioni CEO, prezzo petrolio)
- [ ] 📈 **Convertire il file market driver in TXT** — il file dell'associazione (PPT→PDF), 4 macro-categorie di driver + un driver dal sito Federal Reserve da monitorare. Portarlo in `raw/` come TXT e arricchirlo con descrizioni accurate (call 2026-05-29)
- [ ] 📈 **Preparare documento indicatori di valuation** — cosa analizzare nelle stock, con l'associazione (ognuno ne cura uno); poi TXT e ingest. Con i market driver = "il vocabolario" di metriche per l'agent
- [ ] 📈 **Formalizzare i fondamentali** — es. i 5 tipi di P/E e quali usare (trailing vs current); riclassificare/arricchire (call 2026-05-29)
- [ ] 📈 **Descrivere la giornata tipo di un trader** — cosa guarda, in quale ordine, quali decisioni e su quali basi. Serve per capire cosa il bot deve replicare
- [ ] 📈 **Raccogliere casi reali eventi → impatto prezzi** — esempi concreti "quando è successo X, il prezzo di Y ha fatto Z". Dataset grezzo per la factor quantification
- [ ] 📈 **Valutare AlphaArena (trading)** — le 5 LLM su Bitcoin hanno tradato in modo economicamente sensato? Logiche di mercato reale o scelte casuali?
- [ ] 📈 **Valutare NeuroEspresso (trading)** — l'approccio multi-agente (economista, analista, trader separati) ha senso rispetto a come funziona davvero una trading room?


## 🟡 In corso

- [ ] 🛠 **Modulo analisi documenti** — primo modulo concreto (call 05-06): legge documenti ed estrae informazioni strutturate
- [ ] 🛠 **Progettazione architettura software** — fase design-first, zero codice. Obiettivo: documento completo con I/O per ogni modulo, schema DB, flusso end-to-end
- [ ] 🛠 **Studio wiki in autonomia** — leggere tutta la wiki prima della prossima sessione con Salvatore (usare `/wiki-query`)
- [ ] 📈 **Definire cosa replica il bot nel mondo reale** — qual è esattamente il workflow del trader "tipo" che il sistema deve automatizzare?
- [ ] 📈 **Raccolta di meccanismi di mercato** — ogni osservazione sul mercato reale modellabile va portata nel vault come nota raw


## 🟠 Decisioni da prendere

- [ ] 🛠 **Come implementare il Prompt Builder?** — Python puro deterministico? Template engine? Struttura del prompt finale (JSON vs testo vs sezioni markdown)?
- [ ] 🛠 **Fine-tuning: quale framework e modello base?** — LoRA/QLoRA su open-source? Via API? Quale modello base ha senso per il dominio?
- [ ] 🛠 **Includere il modulo TA?** — rischio: TA mal calibrata corrompe il Prediction Module. Progettare come opzionale e testare A/B (con/senza)
- [ ] 🛠 **Analisti: 2 o 4 agenti?** — tenere market/sentiment/fondamentale/technical separati o accorpati in 2 agenti con moduli interni. Da decidere a sviluppo
- [ ] 🔀 **Frequenza ciclo / trading** — angolo tecnico (costo token + latenza moduli upstream, da secondi a ~1 ora) e angolo mercato (intraday/giornaliero/settimanale: quale timeframe ha più segnale vs rumore). Dipende dai primi backtest
- [ ] 📈 **Regole del portafoglio — scrivere lo statuto** — base già definita (riserva 10% cash, vedi [[build/modules/risk-management]]). Da chiudere: max 5% per asset class, +100% → vendi, max drawdown, cash-out periodico
- [ ] 📈 **Cash-out strategy: quale %?** — quanti profitti estratti periodicamente vs reinvestiti?
- [ ] 📈 **Crypto vs Equity definitivo** — dai fondamentali: quale mercato ha più razionalità per un sistema quantitativo? Crypto accessibile ma rumoroso; equity più storia e logica fondamentale
- [ ] 📈 **Strategia Sentiment degli Analisti: vale la pena?** — edge reale o troppo difficile da modellare? Studio di fattibilità prima della valutazione tecnica


## ✅ Fatto

- [x] 🔀 **Decisione: portfolio / mid-term** ✅ 2026-05-29 — no day trading (rischio blow-up + mancanza competenze day trading). Chiude "Trading singolo vs Portfolio"
- [x] 🔀 **Decisione: mercato = stock-only, poi multi-asset** ✅ 2026-05-23 — benchmark S&P + 60/40 all-world ([[strategy/metrics/benchmark]]). Chiude "Crypto vs Equity" come scelta d'avvio
- [x] 🛠 **Decisione: framework = LangGraph** ✅ 2026-05-29 — riscrivere il grafo tenendo come base i tool/LLM clients di TradingAgents
- [x] 🛠 **Decisione: provider LLM = OpenRouter + DeepSeek V4 Pro** ✅ 2026-05-29 — ~10× più economico di Sonnet ([[build/stack]]). Supera l'ipotesi "DeepSeek su Google Cloud"
- [x] 🛠 **Decisione: design-first** — documento di architettura completo prima di scrivere codice
- [x] 🛠 **Decisione (storica): from scratch / no fork** — *aggiornata: vedi decisione LangGraph 2026-05-29, si riusano i tool/LLM clients di TradingAgents*
- [x] 🛠 **Decisione (storica): Binance come exchange iniziale** — *aggiornata: con lo scope stock-only l'exchange è da riscegliere (Alpaca / Interactive Brokers)*
- [x] 🛠 **Decisione (storica): limit order + SL + TP obbligatori** — *aggiornata: la leva non è più "su tutti i trade" ma solo via opzioni Call/Put su segnali `Strong`*
- [x] 🛠 **Inizializzazione wiki** (struttura LLM Wiki, Karpathy) + struttura base del vault — cartelle `raw/` + `wiki/`, skills, meta files, setup Obsidian + Codex
- [x] 🛠 **Inizializzazione repository Git** ed esecuzione del primo commit
- [x] 🔀 **Videochiamata 04-30** — architettura multi-agente, demo Obsidian, discussione moduli e schema Figma
- [x] 🔀 **Videochiamata 05-06** — analisi tecnica, workflow indicatori in Python, allineamento su approccio numerico (no visione grafico)
- [x] 🔀 **Ingest conversazioni 04-28-30** — bundle audio e appunti progettuali iniziali
- [x] 🔀 **Ingest export Notion** su Investimenti e Trading (teoria, TA, DeFi, Risk Management)
- [x] 🔀 **Consolidamento architettura multi-agente** nel Trading Floor Canvas e nella wiki
- [x] 🔀 **Snapshot iniziale dello stato di progetto** formalizzato
- [x] 📈 **Presentazione del factor investing** — fattori macro, aziendali, ratio, eventi: ognuno con coefficiente calcolabile su serie storiche
- [x] 📈 **Descrizione dei meccanismi di esecuzione** — limit orders, cascata stop loss, effetto domino istituzionali, soglie psicologiche
- [x] 📈 **Presentazione di FinAgent, AlphaArena, NeuroEspresso** come benchmark di riferimento del settore
- [x] 📈 **Proposta strategia Sentiment degli Analisti** — idea originale per anticipare il consenso
- [x] 📈 **Allineamento: analisi tecnica come serie di segnali numerici** in Python, non visione del grafico (call 05-06)
- [x] 📈 **Introduzione al trading con leva** e perché serve per rendimenti significativi
- [x] 📈 **Proposta portfolio bilanciato con regole anti-bias** stile fondo professionale (max 5% per asset class, +100% → vendi, cash-out periodico)
- [x] 📈 **Proposta partire da asset tradizionali**, cripto come side — più metodologie consolidate
- [x] 📈 **Introduzione alla correlazione intra-crypto** e all'allocazione dinamica nel basket (call 05-06)
- [x] 📈 **Framing del progetto come AI Investment Fund / Factory** — non solo trading bot




%% kanban:settings
```
{"kanban-plugin":"board","list-collapse":[false,false,false,false,false]}
```
%%
