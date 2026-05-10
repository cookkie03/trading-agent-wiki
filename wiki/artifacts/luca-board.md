---
kanban-plugin: basic
---

## 💡 Idee

- [ ] **Strategia Sentiment degli Analisti** — capire perché gli analisti sono bullish/bearish → tradare ahead of crowd prima che tutti comprino. Richiede un modulo completamente diverso dal factor investing. (emersa in call 04-30 con Salvatore)
- [ ] **Volume Spike Analysis module** — rilevare picchi anomali di volume, capire la causa, costruire pattern per anticipare i prossimi picchi prima che accadano
- [ ] **Continuous Learning real-time** — fine-tuning sul dato che arriva in tempo reale. Ancora problema aperto nella comunità scientifica. Da esplorare in futuro dopo il fine-tuning periodico
- [ ] **Exchange decentralizzato anonimo (DEX)** — quando i profitti superano le soglie che richiedono KYC, valutare switch da Binance a un DEX completamente anonimo. Architettura modulare lo permette senza riscrivere il sistema
- [ ] **Canale Telegram notifiche trade** — ogni trade con parametri completi (entry, SL, TP, leva). Link pubblico in sola lettura, nessuna autenticazione necessaria


## 🔴 Da fare

- [ ] **Analizzare FinAgent (Cornell)** — paper scientifico 38 pagine, ~50k stelle GitHub, ~10k fork, Claude è il 4° contributore. Architettura: Research Team (bullish+bearish) → Analyst → Transaction Proposal → Risk Manager → Execution Manager. Scaricare e ingestare il paper nella wiki
- [ ] **Analizzare AlphaArena** — progetto open source usato da Rizzo Trading (YouTube/TikTok). Ha confrontato 5 LLM su Bitcoin: Grok, DeepSeek, Claude, ChatGPT, Gemini. Capire cosa ha funzionato e cosa no
- [ ] **Analizzare NeuroEspresso (Silvio Baratto)** — profilo Instagram, approccio multi-agente esteso (economista, analista, trader separati), progetto aperto a contribuzioni esterne. Leggere la documentazione del repository
- [ ] **Raccogliere indicatori di analisi tecnica** — studiarli, validarli manualmente, appuntarli come note raw in Obsidian. L'agente li categorizzerà nella wiki. (emerso in call 05-06)
- [ ] **Definire artifact necessari** — decidere quali mappe mentali e kanban board vuoi avere per il progetto. Task 1 della roadmap progettuale
- [ ] **Installare Obsidian sul nuovo PC e collegare Google Drive** — prerequisito per lavorare in autonomia sul vault


## 🟡 In corso

- [ ] **Studio e progettazione architettura trading agent** — fase design-first pura, zero codice. Obiettivo: avere un documento di architettura completo con I/O per ogni modulo prima di scrivere una riga
- [ ] **Studio wiki e materiali raccolti** — imparare a navigare Obsidian, capire come usare Codex per fare query e ingest, esplorare le pagine del vault


## 🟠 Decisioni da prendere

- [ ] **Includere modulo TA?** — rischio concreto: TA mal calibrata può corrompere l'output del Prediction Module DL ("panna cattiva su un buon gelato"). Valutare SOLO dopo backtest comparativi con/senza TA. Non decidere ora
- [ ] **Frequenza ottimale invocazione LLM Trader?** — i moduli richiedono da secondi a circa 1 ora di elaborazione. Qual è il time period minimo sensato? Da decidere dopo aver stimato i tempi dei moduli più pesanti
- [ ] **Strategia Sentiment degli Analisti come modulo** — è realizzabile in pratica? Richiede un approccio completamente diverso dal factor investing. Richiederebbe uno studio dedicato di fattibilità
- [ ] **Fine-tuning periodico vs Continuous Learning?** — il continuous learning real-time è ancora irrisolto nella scienza. Il fine-tuning periodico è più praticabile. Decidere la cadenza (settimanale? mensile?)
- [ ] **Crypto vs Equity definitivo** — orientamento attuale: crypto/Binance. Non chiuso ufficialmente. Decidere dopo aver studiato FinAgent, AlphaArena e NeuroEspresso e avere più contesto


## ✅ Fatto

- [x] Inizializzazione wiki con struttura LLM Wiki (ispirazione Andrew Karpathy) — cartelle raw/ + wiki/, skills, meta files
- [x] Videochiamata 04-30 con Salvatore — architettura multi-agente, filosofia progetto, demo Obsidian, discussione moduli e Figma schema
- [x] Videochiamata 05-06 con Salvatore — analisi tecnica, workflow indicatori, allineamento su indicatori Python
- [x] Ingest conversazioni 04-28-30 — bundle audio e appunti progettuali iniziali
- [x] Decisione: **from scratch** — no fork di progetti esistenti, costruire con piena comprensione
- [x] Decisione: **Crypto/Binance come mercato iniziale** — accesso dati, liquidità, API complete, order book scaricabile
- [x] Decisione: **limit order + Stop Loss + Take Profit obbligatori** per ogni trade, tutti in leva
- [x] Decisione: **design-first** — progettare tutto prima di scrivere codice


%% kanban:settings
```
{"kanban-plugin":"basic","list-collapse":[false,false,false,false,false]}
```
%%
