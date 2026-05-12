---
title: "Modular Trading Agent Architecture"
type: concept
tags:
  - concept
  - architecture
created: 2026-04-30
updated: 2026-05-10
status: reviewed
related:
  - "[[build/system-map]]"
  - "[[sources/conversazione-luca-salvatore-2026-04-28-30]]"
  - "[[sources/videochiamata-luca-salvatore-2026-04-30]]"
confidence: high
area: software
sources:
  - "[[sources/conversazione-luca-salvatore-2026-04-28-30]]"
  - "[[sources/videochiamata-luca-salvatore-2026-04-30]]"
---

# Modular Trading Agent Architecture

Il sistema è concepito come un'architettura modulare e potenzialmente **multi-agente**, ispirata alle strutture delle trading room professionali e della ricerca accademica (es. Cornell University / FinAgent).

## Principio di Modularità

L'architettura deve permettere di aggiungere, sostituire e pesare dinamicamente diversi moduli specializzati. Questo approccio riduce il rischio di fallimento del sistema intero e permette un miglioramento continuo. Sostituire l'exchange (es. Binance → altro) non richiede di riscrivere il sistema.

## Flusso Architetturale — Prompt Builder

Il cuore del sistema non è un LLM che "gira sempre", ma un **ciclo deterministico**:
1. I moduli specializzati raccolgono, processano e scrivono i loro output nel DB.
2. Un **Prompt Builder** assembla deterministicamente tutti gli output in un prompt completo e lo salva nel DB.
3. L'**LLM Trader** legge il prompt più recente disponibile nel DB (come system prompt) e produce la decisione di trade.
4. L'ordine viene salvato nel DB ed eseguito tramite il modulo Exchange (Binance).

Questo disaccoppia la raccolta dati (asincrona, può durare minuti) dall'invocazione dell'LLM.

## Moduli Core

### 1. News & Sentiment Module
- Estrazione e pre-elaborazione di dati non strutturati (news, comunicati, discorsi).
- Sfida: convertire testo in segnali numerici utilizzabili dal Prompt Builder.

### 2. Factor Quantification
- Costruisce un **modello econometrico empirico**: per ogni tipologia di evento/fattore, raccoglie gli ultimi N casi storici e calcola l'impatto medio sul prezzo.
- Il risultato è un **coefficiente** (es. "dimissioni presidente BCE → -0.08 su titoli europei").
- Fattori coperti: macroeconomici (tassi), aziendali (fatturato, P/E), politici, eventi di mercato.
- Questo approccio è diverso dal factor investing classico: non stima i coefficienti con regressione, li calcola come media empirica su serie storiche.

### 3. Factor Investigation Agent
- Agente dedicato allo studio di quali fattori includere nel modello.
- Analizza correlazioni tra serie storiche di fattori e movimenti di prezzo.
- Usa il Prediction Module per testare ipotesi: "aggiungere questo fattore migliora la previsione?"
- Output: lista aggiornata di fattori validati con relativi coefficienti.

### 4. Prediction Module (Deep Learning)
- Algoritmo DL (ispirato al lavoro di tesi di Luca) addestrato sui fattori quantificati.
- Trova relazioni **non lineari** tra fattori e prezzi (es. un rating alto è positivo in certi contesti ma negativo in altri, a seconda delle condizioni macroeconomiche).
- Input: Factor Store nel DB. Output: previsione movimento di prezzo.
- Può essere un agente separato che scrive i propri output nel DB.

### 5. Technical Analysis (TA) Module
- Individua le **soglie di prezzo più toccate** (supporti/resistenze psicologiche).
- Razionale: le soglie round (es. oro a 1000$) generano comportamenti prevedibili — bias umani + stop loss istituzionali a domino.
- Utilità primaria: definire il **range** di movimento del prezzo per calibrare SL e TP, non per predire la direzione.
- **Rischio noto**: includere TA può corrompere l'output del Prediction Module DL se il modulo TA è mal calibrato. Da valutare solo con dati di backtest comparativi (con/senza TA).

### 6. Sentiment degli Analisti / Crowd Trading Module (idea di King)
- Strategia alternativa al factor investing classico.
- Obiettivo: capire **perché** gli analisti sono bullish/bearish su un titolo (pattern di metriche che genera quel consenso).
- Il bot trada non in base ai numeri, ma anticipando il comportamento della folla di analisti.
- Correlato: **volume spike analysis** — rilevare picchi di volume anomali, capire la causa, costruire pattern per anticipare i futuri picchi prima che accadano.

### 7. Risk Management Module
- Gestione leva, esposizione, commissioni.
- **Trailing Stop Loss**: quando il prezzo si muove favorevolmente, lo SL viene spostato al prezzo di entry (break-even). Esempio: entry 100, SL 95, TP 115 → se il prezzo tocca 105, SL → 100.
- Metriche di portafoglio: drawdown, rendimento annuale, esposizione ai margini.
- Monitoraggio costante delle posizioni aperte.

### 8. Security Module (deterministico)
- Regole fisse non ragionate dall'LLM: esposizione massima, leva massima, blacklist strumenti.
- Guard deterministici che validano ogni proposta di trade prima dell'esecuzione.

### 9. Reinforcement Learning / Weighting Module
- Non è RL tradizionale. È un modulo di **ponderazione dinamica** dei moduli.
- Analizza l'esito di ogni trade (SL → fallito, TP → successo) e quale combinazione di moduli aveva confermato la tesi.
- I moduli "giusti" vedono il loro peso aumentare nel prompt successivo.
- Può analizzare la chain-of-thought dell'LLM per identificare i pattern di ragionamento vincenti.
- Implementabile come un LLM agente che produce una **sintesi strutturata** per ogni trade.

### 10. Fine-Tuning Module
- Piccolo LLM addestrato periodicamente (es. ogni settimana/mese) sull'intero storico del progetto.
- Non è continuous learning in real-time (ancora problema aperto nella ricerca scientifica).
- Cresce in precisione man mano che si accumulano dati.
- Agisce come modulo di input al Trader Agent fornendo pattern derivati dall'esperienza passata.

### 11. Exchange Module (Binance)
- Interfaccia con Binance per esecuzione ordini e download dati.
- Binance: più liquido, API complete, order book scaricabile, prezzi storici completi.
- Modulare: sostituibile con altro exchange (equity broker, DEX anonimo) senza riscrivere il sistema.

## Principio Deterministico — Costo Token come Vincolo

Vincolo architetturale critico: **anche i backtest e le demo costano token**. L'LLM deve fare esclusivamente ragionamento. Tutto il resto è Python deterministico a costo zero.

- **Data fetching**: Python scarica i dati, l'LLM non li recupera.
- **Calcoli**: ratio, medie, confronti tra prezzi → Python.
- **Logica di esecuzione**: trovare il prezzo minimo, applicare regole del portafoglio → Python.
- **Solo ragionamento**: interpretare i segnali, pesare i fattori, decidere il trade → LLM.

Conseguenza: i moduli devono essere progettati come "pre-processing deterministico → un'unica chiamata LLM per il ragionamento finale".

## Correlazione tra Cripto — Allocazione Dinamica nel Basket

Le cripto sono altamente correlate. Il sistema deve gestirlo su due livelli:
1. **Trend macro** (es. Bitcoin sale → tutto il basket sale): identificato dal modulo di mercato.
2. **Differenziazione intra-basket** via news: news negativa specifica su Solana → non-investire o shortare Solana anche in trend macro positivo.

Questo permette di aprire **più trade in parallelo** per sessione, allocando dinamicamente nel basket invece di tutto-o-niente.

## Problema LLM: Needle in a Haystack

Gli LLM leggono bene inizio e fine di un prompt lungo, ma perdono le informazioni nel mezzo. Implicazione: ogni agente deve ricevere informazioni **pre-elaborate e sintetiche**. Il multi-agente risolve questo distribuendo il carico: ogni agente ha solo le info rilevanti al suo compito.

## Struttura Operativa (Flusso Multi-Step)

1. **Data Ingestion**: DB raccoglie Market State, News, Factors, Trade History.
2. **Analysis**: Agenti specializzati (Factor Investigation, Prediction, TA, News) producono i loro output.
3. **Prompt Build**: Prompt Builder assembla deterministicamente gli output.
4. **Trader Decision**: LLM Trader legge il prompt e produce la proposta di trade (con entry, SL, TP).
5. **Risk Validation**: Security Module + Risk Manager validano la proposta.
6. **Execution**: Exchange Module esegue l'ordine su Binance.
7. **Logging**: Esito e ragionamento loggati nel DB per alimentare il RL/Fine-Tuning.

## Visualizzazione e Controllo
- **Dashboard Streamlit**: metriche di portafoglio in sola lettura. Ispirata a SFC Investment Fund (Starting Finance / ex Azimut). Link di riferimento salvato in `raw/articles/`.
- **Telegram Bot/Canale**: notifiche per ogni trade con tutti i parametri. Link pubblico, sola lettura (no autenticazione).

## Riferimenti e Ispirazioni
- **FinAgent (Cornell University)**: ~50k stelle GitHub, ~10k fork, Claude come 4° contributore. Struttura: Research Team (bullish+bearish) → Analyst → Transaction Proposal → Risk Management → Manager.
- **AlphaArena**: usato da Rizzo Trading, ha confrontato Grok/DeepSeek/Claude/ChatGPT/Gemini su Bitcoin.
- **NeuroEspresso (Silvio Baratto)**: approccio multi-agente esteso, progetto aperto a contribuzioni.
