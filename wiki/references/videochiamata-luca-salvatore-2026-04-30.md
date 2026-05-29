---
title: Videochiamata Luca-Salvatore (2026-04-30)
type: source
tags:
  - source
  - ingest
  - strategy
  - architecture
sources: []
raw_source_path: ""
created: 2026-04-30
updated: 2026-05-10
confidence: high
status: reviewed
related:
  - "[[references/conversazione-luca-salvatore-2026-04-28-30]]"
  - "[[build/system-map]]"
---

# Videochiamata Luca-Salvatore (2026-04-30)

Conversazione approfondita sulla struttura del progetto, la filosofia della Wiki e l'architettura tecnica del Trading Agent.

## Contesto

Seconda grande sessione di allineamento tra Luca e Salvatore. La prima parte è dedicata alla spiegazione dello strumento (Obsidian + LLM Wiki) e la seconda alla progettazione dei moduli del Trading Agent.

## File sorgenti

- `raw/audio/2026-04-30 11-15-40.m4a`
- `raw/audio/videochimata 30 apri.m4a`
- `raw/audio/così ce l'abbiamo...txt` (trascrizione ad alta fedeltà, 2026-05-10)
- `raw/audio/Invece Obsidian...txt` (trascrizione ad alta fedeltà, 2026-05-10)

---

## 1. Filosofia del Progetto — LLM Wiki

- Ispirazione da **Andrew Karpathy**: struttura a due cartelle (`raw/` e `wiki/`).
- `raw/` contiene tutto il materiale grezzo (audio, paper, note); `wiki/` è il cervello elaborato.
- La Wiki è mantenuta da un **agente** (Codex/Claude Code) che gestisce automaticamente l'organizzazione, evitando il decadimento che affligge le wiki manuali.
- **Codex** è l'agente scelto: si installa puntando una cartella come vault. Da lì, lo slash `/` espone le skill: `/wiki-ingest`, `/wiki-lint`, `/wiki-save`, `/wiki-query`, `/wiki-artifact`, `/wiki-preprocess`.
- Gli **Artifacts** (Kanban, Canvas, Bases) sono file di testo strutturati che Obsidian renderizza visivamente; il LLM li crea come qualsiasi altro file.
- **Obsidian** è solo un visualizzatore ricco: i file sono plain text markdown, leggibili anche con blocco note. La potenza sta nei **wikilink** (parole viola = link ad altre pagine) e nel **grafo** che mostra le connessioni.
- I file `_meta/` (index, hot-cache, taxonomy) sono il sistema di navigazione per l'LLM: l'agente legge l'index, segue i link alle pagine rilevanti e risponde o aggiorna in modo mirato senza dover leggere tutto il vault.

---

## 2. Architettura del Trading Agent — Visione Complessiva

Il sistema è un ecosistema **multi-agente** in cui ogni agente ha compiti granulari, un proprio workspace e strumenti.

### Il DB come cuore centrale

Il database contiene tutto:
- **Market State**: prezzi, volumi, order book.
- **News/Sentiment Store**: feed di notizie pre-elaborate.
- **Factor Store**: coefficienti quantificati per ogni tipologia di evento/fattore.
- **Trade History & Reasoning Log**: ogni trade con tutta la chain-of-thought dell'agente.
- **Portfolio State**: stato corrente delle posizioni (derivato dallo storico trade).
- **Prompt Store**: i prompt costruiti deterministicamente dai moduli, pronti per essere consumati dall'LLM.

### Architettura del Prompt Builder

Il flusso è:
1. I moduli specializzati processano i dati e scrivono i loro output nel DB.
2. Un **Prompt Builder** li assembla deterministicamente in un prompt completo e lo salva nel DB.
3. L'LLM Trader, alla propria frequenza, legge il **prompt più recente disponibile** nel DB e lo usa come system prompt per ragionare sul trade.

Questo separa la fase di raccolta dati (async, può durare minuti) dall'invocazione dell'LLM.

### Esecuzione degli ordini — Binance

- Exchange scelto per la fase iniziale: **Binance**.
  - Motivo: è l'exchange più liquido, fornisce API complete, permette di scaricare l'order book e tutti i prezzi storici, ed è necessario per estrarre i dati grezzi oltre che per eseguire.
  - Futuro: possibilità di switch ad exchange decentralizzati anonimi (nessun KYC) se i profitti superano le soglie che richiedono identificazione. Architettura modulare lo permette senza riscrivere il sistema.
- **Meccanismo di trade**: ogni operazione ha tre numeri obbligatori:
  1. **Prezzo limite** (entry): il prezzo a cui si vuole entrare nel mercato.
  2. **Take Profit**: il prezzo target di uscita in guadagno.
  3. **Stop Loss**: il prezzo di uscita in perdita per limitare i danni.
- Tutti i trade vengono eseguiti in **leva** per rendere significativi i rendimenti.
- Modulo **Security** (deterministico): regole fisse che il trade deve rispettare (es. esposizione massima, leva massima) — non ragionamento LLM, ma guard deterministici.

### Trailing Stop Loss (Risk Management)

Meccanismo di protezione dinamica:
- Scenario: entry a 100, SL a 95, TP a 115.
- Se il prezzo sale a 105 (favorevole ma non ha ancora raggiunto il TP), lo SL viene spostato da 95 → 100 (break-even).
- Risultato: se il prezzo poi scende, al massimo si chiude in pareggio. Se il trend continua, si raggiunge il TP.
- Questo modulo monitora costantemente le posizioni aperte e aggiorna gli SL.

---

## 3. I Moduli in Dettaglio

### News Module

- Si aggancia a provider di news esterni.
- Pre-elabora le notizie e le converte in segnali numerici da inserire nel DB.
- Sfida principale: le news sono dati **non strutturati** — non numeri di per sé.

### Factor Quantification — Metodologia

L'idea chiave (emersa da Salvatore): costruire un **modello econometrico empirico** basato sui dati storici.
- Per ogni tipologia di evento (es. "dimissioni presidente banca centrale", "variazione tasso BCE", "earnings ENI"), si raccolgono gli ultimi N casi storici.
- Si calcola l'impatto medio sul prezzo del titolo/mercato correlato.
- Questo impatto diventa il **coefficiente** di quel fattore nel modello.
- Analogia: regressione multipla in cui i coefficienti non sono stimati analiticamente ma come medie empiriche su dati storici.
- Il modello copre fattori di qualsiasi tipo: macroeconomici (tassi), aziendali (fatturato), ratios (P/E), eventi politici, notizie.

### Prediction Module (Deep Learning)

- Un algoritmo di Deep Learning (come il lavoro di tesi di Luca) addestrato sui factor.
- Trova relazioni **non lineari** che una regressione classica non coglie: es. un rating alto è positivo in certi contesti di mercato ma negativo in altri.
- Input: fattori quantificati dal Factor Store.
- Output: previsione del movimento di prezzo.
- Potenzialmente gestito come **agente separato** collegato al DB.

### Factor Investigation Agent

- Agente dedicato allo studio di quali fattori hanno senso da includere nel modello.
- Lavoro: analizza le correlazioni tra serie storiche di fattori e movimenti di prezzo.
- Usa il Prediction Module per testare ipotesi: "se aggiungo questo fattore, migliora la previsione?"
- Output: lista aggiornata di fattori validati e i loro coefficienti.

### Technical Analysis Module

- Individuazione delle **soglie di prezzo più toccate** (supporti/resistenze).
- Razionale: le soglie psicologiche (es. 1000 USD per Bitcoin) generano comportamenti di mercato prevedibili — sia per bias umani che per stop loss automatici degli istituzionali che si innescano a domino.
- **Attenzione / tensione**: includere la TA nel modello potrebbe **corrompere** l'output del Prediction Module (DL). Se il modello DL è buono, aggiungere TA mal calibrata è come mettere "panna cattiva su un buon gelato". La decisione sull'inclusione va presa dopo aver valutato i trade con e senza.
- Utilità potenziale: non per predire il prezzo esatto, ma per definire il **range** in cui il prezzo si muoverà, aiutando a definire i livelli di SL e TP.

### Reinforcement Learning / Weighting Module

- **Nome tecnico impreciso**: non è RL in senso stretto. È un modulo di **ponderazione dinamica** dei moduli.
- Funzionamento:
  1. Raccoglie l'esito di ogni trade (stop loss = fallito, take profit = successo).
  2. Analizza quale combinazione di moduli aveva "confermato" il trade riuscito.
  3. Aumenta progressivamente il peso (coefficiente) dei moduli che si dimostrano affidabili.
  4. Può anche analizzare la chain-of-thought dell'LLM di trading per capire quali ragionamenti portano a trade migliori.
- Potenzialmente implementato come un **ulteriore LLM agente** che fa sintesi strutturata su ogni trade.

### Fine-tuning Module

- Un piccolo LLM addestrato periodicamente sui dati storici del progetto (trade, ragionamenti, esiti).
- Non è continuous learning in real-time (troppo complesso, ancora aperto nella ricerca).
- Schema: ogni X periodi si lancia un ciclo di fine-tuning su tutti i dati accumulati.
- Con il tempo, questo LLM cresce in precisione man mano che il dataset si arricchisce.
- Agisce come **modulo di input** per il Trader Agent: fornisce pattern e insight derivati dall'esperienza passata.

### Dashboard e Telegram Bot

- **Dashboard Streamlit**: ispirata a SFC Investment Fund (Starting Finance, ex Azimut). Metriche: drawdown, rendimento annuale, esposizione ai margini, storico trade.
- Link di riferimento salvato: `raw/articles/` → Starting Finance Streamlit dashboard.
- **Telegram Bot**: canale/bot di notifica per ogni trade eseguito, con tutti i parametri. Accesso in sola lettura (no autenticazione, il link è pubblico ma non contiene tasti di azione).

---

## 4. Strategia Alternativa — Sentiment degli Analisti (idea di Salvatore/King)

Una strategia radicalmente diversa rispetto al factor investing classico:
- Obiettivo: capire **perché** in un dato momento 30 analisti su 30 sono bullish su un titolo.
- Identificare il pattern di metriche che genera quel consenso.
- Il bot **non trada in base ai numeri**, ma **in base a cosa penseranno gli altri**: se capisce che il consenso sarà bullish, compra prima che tutti comprino, poi vende prima che la folla inverta.
- Questa strategia richiede un modulo che analizza il sentiment degli analisti e ne modella il processo decisionale.
- **Volume spike analysis**: correlato — rilevare picchi di volume anomali, capire cosa li ha causati, costruire pattern per anticipare i picchi futuri prima che si manifestino.

---

## 5. LLM Context Window — Problema Needle in a Haystack

Un limite noto degli LLM rilevante per l'architettura:
- Gli LLM leggono bene l'inizio e la fine di un prompt lungo, ma le informazioni nel mezzo vengono "perse" (come un umano che legge un documento lungo).
- Benchmark "ago nel pagliaio": testato su informazioni specifiche in prompt molto lunghi — le LLM falliscono quando l'informazione è in posizione centrale.
- **Implicazione architetturale**: ogni agente specializzato deve ricevere informazioni quanto più **pre-elaborate e sintetiche** possibile. Il multi-agente permette di distribuire il carico: ogni agente ha solo le info rilevanti per il suo compito.

---

## 6. Progetti di Riferimento

### FinAgent (Cornell University Paper)
- Progetto open source: ~50.000 stelle GitHub, ~10.000 fork.
- Claude è il **4° contributore** per impatto.
- Struttura: Research Team (bullish + bearish agents) → Analyst → Transaction Proposal → Risk Management Team → Manager (execution).
- Paper: 38 pagine, salvato in `wiki/references/` (da ingestare).
- Usabile: basta clonare e lanciare `trading-agents` da terminale.

### AlphaArena
- Usato da Rizzo Trading (YouTuber/TikToker).
- Ha confrontato 5 LLM su Bitcoin: Grok, DeepSeek, Claude, ChatGPT/OpenAI, Gemini.
- Base di partenza per Rizzo Trading ma progetto non mantenuto.

### NeuroEspresso (Silvio Baratto)
- Profilo Instagram, approccio multi-agente più esteso (economista, analista, trader, etc.).
- Progetto aperto a contribuzioni esterne.
- Documentazione disponibile nella sua repository.

---

## 7. Decisioni Prese in Questa Sessione

- **From Scratch confermato**: non fare fork. Capire bene i progetti esistenti ma costruire da zero per avere piena comprensione e controllo.
- **Crypto prima**: Binance come exchange iniziale (accesso dati, liquidità, API).
- **Trade mechanism**: limit order + stop loss + take profit obbligatori per ogni trade.
- **Design-first**: prima progettazione completa (artifact, I/O dei moduli), poi coding.

## 8. Roadmap Progettuale

1. **Task 1**: Definire gli artifact necessari (mappe mentali, kanban board).
2. **Task 2**: Raccolta e studio di progetti esistenti (FinAgent, AlphaArena, NeuroEspresso); elaborazione via wiki.
3. **Task 3**: Design granulare Input/Output per ogni modulo — definire esattamente cosa entra e cosa esce da ciascun modulo prima di svilupparlo.
4. **Task 4**: Schema architetturale completo (non MVP — più completo possibile nella teoria) con riferimenti alle pagine wiki nei blocchi dello schema.

## Tensioni Aperte

- **Crypto vs Equity**: orientamento su crypto (Binance), ma la scelta non è chiusa definitivamente.
- **TA inclusion**: includere il modulo TA rischia di corrompere il modello predittivo. Valutare solo dopo aver dati di backtest comparativi.
- **Frequenza dei trade**: ancora aperta. Dipende dal tempo di elaborazione dei moduli (secondi → minuti → potenzialmente un'ora con moduli pesanti).
- **Fine-tuning vs Continuous Learning**: il continuous learning in real-time è ancora un problema aperto della comunità scientifica. Fine-tuning periodico è più praticabile.
