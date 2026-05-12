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
- [ ] **Progettare schema del DB** — definire tabelle/collezioni per: Market State, Factor Store, Trade History + Reasoning Log, Portfolio State, Prompt Store. Scegliere tecnologia (PostgreSQL? SQLite? altro?)
- [ ] **Definire I/O spec per ogni modulo** — per ciascun modulo: cosa entra (formato, fonte), cosa esce (formato, destinazione nel DB). Priorità: Prompt Builder, News Module, Factor Quantification, Prediction Module
- [ ] **Installare Obsidian sul nuovo PC e collegare Google Drive** — prerequisito per lavorare in autonomia sul vault


## 🟡 In corso

- [ ] **Modulo analisi documenti** — primo modulo concreto, dichiarato in call 05-06. Legge documenti e ne estrae informazioni strutturate. Iniziato
- [ ] **Progettazione architettura software** — fase design-first pura, zero codice. Obiettivo: documento completo con I/O per ogni modulo, schema DB, flusso end-to-end
- [ ] **Studio wiki da solo** — leggere tutta la wiki prima della prossima sessione con Salvatore; usare /wiki-query per ripassare lo stato del progetto


## 🟠 Decisioni tecniche da prendere

- [ ] **Come implementare il Prompt Builder?** — deterministico in Python puro? Template engine? Quale struttura del prompt finale (JSON strutturato vs testo libero vs sezioni markdown)?
- [ ] **Fine-tuning: quale framework e modello base?** — LoRA/QLoRA su modello open-source? Fine-tuning via API (OpenAI, Anthropic)? Quale modello base ha senso per questo dominio?
- [ ] **Frequenza invocazione LLM Trader** — vincolo tecnico + costo API. I moduli richiedono da secondi a ~1 ora. Qual è il time period minimo che ha senso economicamente e tecnicamente?
- [ ] **Includere modulo TA?** — rischio: TA mal calibrata corrompe il Prediction Module DL. Progettare come modulo opzionale e testare A/B (con/senza). Non decidere ora, ma pianificare il test
- [ ] **Architettura multi-agente: framework o da zero?** — LangGraph, AutoGen, CrewAI, o implementation custom? I framework esistenti danno struttura ma aggiungono dipendenze
- [ ] **Modelli open source cinesi (DeepSeek) su Google Cloud** — valutare costo vs performance per questo use case. Setup: Google Cloud GPU a consumo + modello open source scaricato. Alternativa a Anthropic/OpenAI API per ridurre costi di 20x
- [ ] **Trading singolo vs Portfolio bilanciato** — impatta l'intera architettura. Da decidere insieme a Salvatore prima di costruire qualsiasi cosa


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