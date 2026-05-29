---
title: "Decision Log"
type: build
tags:
  - decision
  - strategy
created: 2026-04-30
updated: 2026-05-29
status: active
related:
  - "[[build/system-map]]"
  - "[[build/mvp-prototype-design]]"
---

# Decision Log

Storico delle decisioni rilevanti del progetto. Quando una scelta smette di essere banale, va registrata qui con la motivazione.

---

## Decisioni chiuse

| Data | Decisione | Motivazione |
|------|-----------|-------------|
| 2026-04-30 | **From scratch** — non fare fork di progetti esistenti | Chi parte da un fork deve comunque studiare il codice altrui; meglio costruire con piena comprensione. **Contraddizione 2026-05-19**: dopo lettura del Code Wiki di TradingAgents, Luca rivaluta — probabile fork come punto di partenza. Decisione da formalizzare. |
| 2026-04-30 | **Crypto come mercato iniziale** — Binance come exchange | Accesso dati migliore, liquidità, semplicità API rispetto all'equity |
| 2026-04-30 | **Limit order + SL/TP obbligatori**, tutti i trade in leva | Ogni trade deve avere tre numeri definiti: entry, SL, TP. Senza SL/TP, win rate 66% porta comunque a drawdown devastanti |
| 2026-04-30 | **Design-first** prima di qualsiasi coding | Progettare artifact, raccogliere info, definire I/O per ogni modulo |
| 2026-04-30 | **Augmentation → Autonomy**: partire da paper trading autonomo | Prima che il sistema operi con capitale reale, deve dimostrare solidità su Testnet |
| 2026-05-13 | **Architettura**: monolite modulare | Sviluppo veloce, facile debug, path evolutivo verso microservizi. Rispetta il principio deterministico |
| 2026-05-13 | **Orizzonte trade**: swing trading (4h/daily) | Alte aspettative rendimento; analisi complessa richiede tempo; frequenza alta incompatibile con costo token |
| 2026-05-13 | **MVP deployment**: singolo asset su Binance Testnet | Portfolio-first nell'architettura, singolo asset per il primo deployment |
| 2026-05-13 | **Framework backtesting**: VectorBT | Usato da MarketSenseAI (paper più rigoroso). Gestisce costi di transazione in modo preciso |
| 2026-05-13 | **LLM principale**: DeepSeek | Alpha Arena: miglior rapporto costo/performance. 1/30 del costo di GPT-5 |
| 2026-05-13 | **Sequenza sviluppo**: Track 1 (Modulo A) ∥ Track 2 (Modulo C), poi Modulo D | Luca costruisce Exchange+DB mentre progetta con Salvatore il Quant Agent. Modulo D dopo |
| 2026-05-13 | **Risk Analyst upstream** del Trader | Imposta i paletti prima che il Trader decida, non valida dopo. Più adatto allo swing trading |
| 2026-05-13 | **Output LLM = JSON strutturato obbligatorio** | Tutti i framework convergono su questo. Necessario per parsing deterministico |
| 2026-05-13 | **Prophet non usare** come modulo forecast | Non regge sui crolli improvvisi, genera previsioni bullish in mercati bearish |
| 2026-05-13 | **Value investing non scalabile** come strategia primaria ora | Ogni azione richiede analisi diversa; costoso in tempo e token. Da rivalutare in futuro |

---

| 2026-05-19 | **Data strategy: DB-first** — salvare ogni dato nel DB prima di renderlo disponibile agli agenti | Preferito rispetto al hub routing di TradingAgents (che chiama i vendor on-demand). Consente deduplicazione deterministica e sfruttamento massimo dei rate limit. Trade-off da valutare: latenza su dati molto recenti non ancora nel DB |
| 2026-05-19 | **Framework**: LangGraph + LangChain confermati | LangGraph ben mantenuto; il pattern StateGraph con checkpointing SQLite è adatto al nostro workflow. Potenzialmente poco efficiente ma priorità è avviare. Da imparare |
| 2026-05-19 | **Filosofia agenti**: pochi agenti + tanti tool potenti | Contrario alla moltiplicazione di agenti (Analysts/Researchers/Managers/Trader di TradingAgents). Il layer Analysts diventa moduli deterministici; gli agenti LLM si concentrano solo sul ragionamento finale |
| 2026-05-19 | **Pattern intra-modulo**: un file gateway per subdirectory | Ogni subdirectory = modulo; un file unico gestisce input/output intra- e inter-modulo |
| 2026-05-19 | **Look-ahead bias**: doppia data per ogni informazione | (1) data di ottenimento/pubblicazione, (2) data a cui l'informazione si riferisce. Più preciso del semplice `curr_date` filtering di TradingAgents |
| 2026-05-19 | **Fork da TradingAgents (TauricResearch)** confermato come punto di partenza | Luca ha letto il codice, valuta il fork come più efficiente di partire da zero. Contraddice la decisione 2026-04-30 ma supportata da approfondimento tecnico |
| 2026-05-23 | **Scope: Stock-only prima, poi multi-asset** | Il progetto si sviluppa prima su equity pura (stock), poi si allarga a: commodities, BTC only, derivati futures e opzioni (per copertura, rischio cambio). Crypto rimossa come focus primario. |
| 2026-05-23 | **LangChain come AI agent framework** | Confermato definitivamente. TradingAgents usa già LangChain/LangGraph — coerente con il fork. Struttura repo: subfolder per componente + subfolder liste tool |
| 2026-05-23 | **Struttura build: non più divisione per moduli sequenziali** | La divisione module-A/C/D/risk-analyst era legata alla sequenza di sviluppo. Sostituita con organizzazione per funzione/dominio, non per timeline |
| 2026-05-26 | **Bull/Bear Analyst agents non servono** | Feedback di Salvatore (esperto equity research): la struttura debate del report è confusa, ridondante e aumenta l'effort nella parte sbagliata. La financial analysis è il core; il bull/bear case va ridotto a una vista strategica concisa |
| 2026-05-26 | **Report structure**: financial → tecnica → bull/bear (ridotto) → risk (4 param) | Ordine proposto da Salvatore. Peso maggiore su: revenues, debt, patrimoniale, relazioni di gestione, note integrative. Analisi tecnica su trend. Bull/bear conciso. Risk: 4 parametri, non discorsivo |
| 2026-05-27 | **Suddivisione Ricercatori vs Esecutori** | Gli agenti attivi sono divisi in due gruppi: Ricercatori (generazione idee e rating) ed Esecutori (gestione ordini ed esecuzione con tool robusti). Gli analysts diventano moduli Python deterministici. |
| 2026-05-27 | **Statuto del Fondo & Riserva 10%** | Lo Statuto del portafoglio sarà di tipo istituzionale e conterrò regole rigide deterministiche (Python) a monte. La prima regola impone di tenere il 10% del portafoglio sempre disinvestito in cash puro come riserva strategica. |
| 2026-05-27 | **Leva controllata via Opzioni (Call/Put)** | Leva a debito diretta vietata causa margini elevati. La leva si attiva solo su segnali ad altissima convinzione validati dal sistema (`Strong Buy` / `Strong Sell`), acquistando opzioni Call/Put. L'assegnazione finale del calcolo della convinzione all'agente o nodo più coerente avverrà in fase di costruzione del grafo dopo aver elencato tutti i compiti. |
| 2026-05-27 | **Costo API LLM equiparato a commissioni** | Il costo dei token OpenRouter consumati dagli agenti viene stimato in fiat ($/€) e trattato come una commissione del broker, detratta dal profitto atteso per calcolare la net performance. |
| 2026-05-27 | **Business Model: Open Source + Friends Performance Fee** | Il codice rimarrà open source su GitHub come portfolio per Luca. La monetizzazione avverrà tramite sito performance pubblico ("Piero") gestendo capitali di amici stretti con contratti privati di scarico responsabilità e fee del 1% sui soli profitti generati. |
| 2026-05-29 | **Portfolio / mid-term confermato, NO day trading** | Day trading troppo speculativo (rischio blow-up in leva) e fuori dalle competenze del team; il portafoglio mid-term è gestibile, diversificabile, reso più facile dall'AI e non richiede presenza 24/7. Chiude la decisione aperta "Trading singolo vs Portfolio bilanciato". |
| 2026-05-29 | **DeepSeek V4 Pro via OpenRouter** come modello principale | Su report NVDA reale (163k input + 20k output token): ~$0,09 vs ~10× di Claude Sonnet 4.6. Modelli cinesi ~10× più economici (efficienza forzata dal ban GPU USA), open source/eseguibili in locale. OpenRouter come router unico verso tutti i provider per agilità. Privacy dati non considerata un problema. |
| 2026-05-29 | **Trader = funzione Python deterministica (NON agent)** | La conversione `research_state → transazione` non richiede un LLM: una funzione estrae i campi della proposta ed esegue; la scelta del miglior prezzo tra broker è deterministica. Supera l'idea precedente di "LLM Trader". |
| 2026-05-29 | **Head of Analyst eliminato; Risk Analyst = gate bear unico** | L'Head of Analyst (moderatore anti-bias) è ridondante: gli analisti sono la tesi bullish, il Risk Analyst è l'antitesi bearish. Se il Risk Analyst approva (soglia ~60-70%) si va direttamente al Trade. |
| 2026-05-29 | **Guardrail deterministici da Statuto-schema** | I guardrail misurabili numericamente (VaR ~10%, % max per area/settore, diversificazione, duration) sono check Python deterministici, non compiti dell'agente (l'LLM è bravo nel reasoning, non nei calcoli). Lo Statuto testuale va tradotto in scheda parametri. |
| 2026-05-29 | **Riscrivere il grafo, tenere base TradingAgents** | Si tengono i tool di estrazione (`dataflows`) e gli LLM clients di TradingAgents; si riscrivono da capo node/edge/state/tool, system prompt, si mettono gli output in un DB e si aggiungono agenti (es. backtesting). 4 task di engineering: agenti, state, system prompt, tool. |
| 2026-05-29 | **Avvio con portafoglio già investito** | Il sistema deve **mantenere/ribilanciare**, non costruire da zero. Si parte con un portafoglio investito (es. top 10 in proporzione); l'**universo investibile** si fornisce come **lista** (sottostanti S&P / all-world ETF). Risolve anche l'attivazione (i movimenti di prezzo innescano il monitoraggio). |
| 2026-05-29 | **Benchmark: S&P 500 + 60/40 all-world** | Una gestione attiva ha sempre un benchmark ("numero da superare"): S&P (US, trasparente) + 60/40 Vanguard all-world. Col 10% cash il portafoglio sarà ~50/40÷55/35. Idea: selezione attiva dei titoli S&P (universo ridotto, prendere il percentile migliore). |
| 2026-05-29 | **Investment State come gate di completezza** | Non si fa trade finché l'`investment_state` non è completo (forza il passaggio per tutti gli analisti); si resetta automaticamente quando il blocco trade rileva la transazione. |
| 2026-05-29 | **Attivazione via mercati efficienti (no push news)** | Le API funzionano solo a richiesta (no notifiche push). Soluzione: i prezzi riflettono le informazioni → un prezzo anomalo attiva l'agente di monitoring che cerca la spiegazione. Gli **alert** sono solo numerici/prezzo; le news entrano dagli extractor periodici. Coerente con l'orizzonte long-term. |

---

## Decisioni ancora aperte

| Tema | Contesto | Dove si risolve |
|------|----------|-----------------|
| **Strategia del fondo** | Orientamento: multi-factor fundamentals, ma non formalizzato con Salvatore | [[build/modules/quant-backtesting]] |
| **Frequenza ciclo** | 4h vs 24h — dipende da backtest iniziali | [[build/modules/quant-backtesting]] |
| **Trading singolo vs Portfolio bilanciato** | ~~Aperta~~ → **CHIUSA 2026-05-29**: portfolio / mid-term confermato, no day trading. Vedere decisioni chiuse. | — |
| **Multi-asset vs solo cripto** | ~~Aperta~~ → **CHIUSA 2026-05-23**: stock-only prima, poi multi-asset (commodities, BTC only, derivati). Vedere decisioni chiuse. | — |
| **Cash-out strategy** | Quale % dei profitti estratta periodicamente? Regola da mettere nello statuto | [[build/modules/risk-management]] |
| **Regole specifiche dello Statuto** | Esposizione massima per asset, vendite automatiche, max drawdown consentito. Statuto in stile istituzionale generico | [[build/modules/risk-management]] |
| **Meccanismo di disinvestimento ottimale** | Come calcolare deterministicamente quale asset vendere per fare spazio a nuove idee senza intaccare il 10% cash | [[build/modules/risk-management]] |
| **Algoritmo token cost estimator** | Implementazione del tracciamento token e logica di ricarica automatica API | [[build/modules/risk-management]] |
| **Includere modulo TA?** | Rischio di corrompere il Prediction Module DL. Test A/B con/senza | [[build/modules/quant-backtesting]] |
| **Frequenza invocazione LLM Trader** | Vincolo tecnico + costo API. Dipende da tempo elaborazione moduli | [[build/modules/llm-agent-system]] |
| **Dynamic Temporal Checkpoints** | Definizione dell'autolimitazione temporale del Trader nel JSON structured (prossimo check controllato dall'AI) | [[build/modules/llm-agent-system]] |
| **Fine-tuning vs Continuous Learning** | Continuous learning real-time è problema aperto; fine-tuning periodico più praticabile | post-MVP |
| **Exchange decentralizzato (DEX)** | Quando ha senso passare a un DEX anonimo (no KYC) rispetto a Binance? | post-MVP |
| **Struttura wiki quant** | Sezione strategie da costruire man mano che Salvatore porta materiale | [[_meta/index]] |
| **Fork vs from scratch** | ~~Aperta~~ → **CHIUSA 2026-05-19**: fork da TradingAgents (TauricResearch) confermato. Vedere decisioni chiuse. | — |
| **Self-scheduling vs cron** | Orientamento 2026-05-29: agenti **asincroni** attivati da **alert** (numerici/prezzo) o da **periodical synthesis** a intervalli fissi; adaptive extractor con frequenza variabile per rispettare i rate limit | [[build/modules/llm-agent-system]] |
| **Analisti: 2 o 4 agenti?** | Tenere 4 ruoli separati (market, sentiment, fondamentale, technical) o 2 agenti con 2 moduli interni ciascuno. Da decidere a sviluppo | [[build/modules/llm-agent-system]] |
| **Indicatori di sentiment** | Il sentiment non ha indicatori propri standard (solo indici di paura) → da inventare/definire. Posizione ibrida col technical | [[build/modules/quant-backtesting]] |
| **Desk di monitoring/evaluation** | Serve un agente/desk che sorvegli le posizioni esistenti e rifaccia il processo quando le news cambiano la tesi (evita target obsoleti e posizioni di segno opposto). Design da definire | [[build/modules/llm-agent-system]] |
| **Forma di storage per area** | SQL relazionale vs JSON/documentale vs time-series: quale per quale dato (rendicontazione, states, dati live)? Forme non ancora considerate? (daily note 2026-05-28) | [[build/modules/exchange-db]] |
| **Debate architecture** | ~~Aperta~~ → **CHIUSA 2026-05-26**: Bull/Bear agents eliminati. Risk debate da ridisegnare con meno agenti e system prompt mirati (la struttura a 3 agenti Risk potrebbe restare se efficientata). Vedere decisioni chiuse. | — |
