---

kanban-plugin: board

---

## 💡 Idee tecniche

- [ ] **Volume Spike Detection — algoritmo** — implementare un rilevatore di picchi anomali di volume: baseline rolling, z-score, classificazione causa. Da valutare come modulo separato o parte del News module
- [ ] **Continuous Learning real-time** — fine-tuning sul dato che arriva in streaming. Ancora problema aperto nella ricerca. Esplorare dopo che il fine-tuning batch funziona bene
- [ ] **Logging strutturato della chain-of-thought** — progettare lo schema del log per ogni trade: input moduli → ragionamento LLM → decisione → esito. Fondamentale per poter fare fine-tuning e analisi RL
- [ ] **DEX module intercambiabile** — progettare l'Exchange Module con un'interfaccia astratta (Binance ora, DEX anonimo dopo). Il contratto input/output deve essere identico tra i due adattatori
- [ ] **Costo per trade — vincolo API** — stimare il costo in token (e quindi €) per ogni invocazione dell'LLM Trader con il prompt pieno. Influenza la frequenza massima sostenibile


## 🔴 Da fare

- [ ] **Analizzare architettura tecnica di FinAgent** — clonare la repo, leggere il codice: come sono implementati gli agenti, quali framework usano, come comunicano tra loro, come gestiscono il prompt. ~50k stelle, Claude 4° contributore
- [ ] **Analizzare AlphaArena** — come hanno fatto girare 5 LLM in parallelo su Bitcoin? Struttura del codice, gestione degli output, integrazione con l'exchange
- [ ] **Analizzare NeuroEspresso (Silvio Baratto)** — repository: pattern multi-agente usato, struttura del codice, cosa è rimasto incompleto e perché
- [ ] **Progettare schema del DB esteso** — consolidare il design 2026-05-29: rendicontazione portafoglio (liquidità, distribuzione multi-filtro, P/L), dati live (prezzi, calendario, news, macro, insider, cambi), costituzione/statuto al centro, log (states/reports/transactions) + retention/clustering. Vedere [[build/modules/exchange-db]]
- [ ] **Definire I/O spec per ogni modulo** — per ciascun modulo: cosa entra (formato, fonte), cosa esce (formato, destinazione nel DB). Priorità: Prompt Builder, News Module, Factor Quantification, Prediction Module
- [ ] **Riscrivere il grafo LangGraph** — tenere `dataflows` + LLM clients di TradingAgents; riscrivere node/edge/state/tool secondo la topologia 2026-05-29 (analisti → research_state → Risk Analyst → Trade deterministico; PM orchestratore; investment_state gate). Vedere [[build/modules/llm-agent-system]]
- [ ] **Implementare Extractors** — Extractors set + Adaptive extractor (frequenza per vicinanza al target, rispetto rate limit) + Market Alert agent + calendar tool. Vedere [[build/modules/exchange-db]]
- [ ] **Configurare OpenRouter + DeepSeek V4 Pro** — setup del router e del modello principale
- [ ] **Valutare canale Telegram "sala segnali"** — calendario, riassunti news, prezzi, trade, variazioni rilevanti (orario/giornaliero), alert interattivi
- [ ] **Studiare corsi completi LangGraph e LangSmith** — finora solo i Quickstart; serve il Foundation/completo
- [ ] **Ingestare il file market driver di Salvatore** — quando arriva in `raw/` come TXT (ricordarsi `/wiki-ingest` + aggiornare le board)


## 🟡 In corso

- [ ] **Modulo analisi documenti** — primo modulo concreto, dichiarato in call 05-06. Legge documenti e ne estrae informazioni strutturate. Iniziato
- [ ] **Progettazione architettura software** — fase design-first pura, zero codice. Obiettivo: documento completo con I/O per ogni modulo, schema DB, flusso end-to-end
- [ ] **Studio wiki da solo** — leggere tutta la wiki prima della prossima sessione con Salvatore; usare /wiki-query per ripassare lo stato del progetto


## 🟠 Decisioni tecniche da prendere

- [ ] **Come implementare il Prompt Builder?** — deterministico in Python puro? Template engine? Quale struttura del prompt finale (JSON strutturato vs testo libero vs sezioni markdown)?
- [ ] **Fine-tuning: quale framework e modello base?** — LoRA/QLoRA su modello open-source? Fine-tuning via API (OpenAI, Anthropic)? Quale modello base ha senso per questo dominio?
- [ ] **Frequenza invocazione LLM Trader** — vincolo tecnico + costo API. I moduli richiedono da secondi a ~1 ora. Qual è il time period minimo che ha senso economicamente e tecnicamente?
- [ ] **Includere modulo TA?** — rischio: TA mal calibrata corrompe il Prediction Module DL. Progettare come modulo opzionale e testare A/B (con/senza). Non decidere ora, ma pianificare il test
- [x] **Architettura multi-agente: framework o da zero?** — ✅ 2026-05-29: **LangGraph**, riscrivendo il grafo ma tenendo come base i tool/LLM clients di TradingAgents
- [x] **Provider LLM** — ✅ 2026-05-29: **OpenRouter + DeepSeek V4 Pro** (DeepSeek ~10× più economico di Sonnet; vedi [[build/stack]]). Supera l'ipotesi DeepSeek su Google Cloud
- [x] **Trading singolo vs Portfolio bilanciato** — ✅ 2026-05-29: **portfolio / mid-term**, no day trading
- [ ] **Analisti: 2 o 4 agenti?** — tenere market/sentiment/fondamentale/technical separati o accorpati in 2 agenti con moduli interni. Da decidere a sviluppo


## ✅ Fatto

- [x] Inizializzazione wiki con struttura LLM Wiki (Andrew Karpathy) — cartelle raw/ + wiki/, skills, meta files, Obsidian + Codex setup
- [x] Videochiamata 04-30 — architettura multi-agente, Obsidian demo a Salvatore, discussione moduli e Figma schema
- [x] Videochiamata 05-06 — analisi tecnica, workflow indicatori in Python, allineamento su approccio numerico (no visione grafico)
- [x] Ingest conversazioni 04-28-30 — bundle audio e appunti progettuali iniziali
- [x] Decisione: **from scratch** — no fork, costruire con piena comprensione del codice
- [x] Decisione: **design-first** — documento di architettura completo prima di scrivere una riga
- [x] Decisione: **Binance come exchange iniziale** — API complete, order book, dati storici
- [x] Decisione: **limit order + SL + TP obbligatori**, tutti i trade in leva




%% kanban:settings
```
{"kanban-plugin":"board","list-collapse":[false,false,false,false,false]}
```
%%