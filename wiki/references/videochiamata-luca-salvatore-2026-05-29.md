---
title: "Videochiamata Luca & Salvatore 2026-05-29 (due call)"
type: source
tags:
  - source
  - architecture
  - multi-agent
  - infrastructure
created: 2026-05-29
updated: 2026-05-29
raw_source_path: "raw/archived/2026-05-29 11-08-30.txt, raw/archived/2026-05-29 14-41-53.txt"
confidence: high
status: active
related:
  - "[[build/modules/llm-agent-system]]"
  - "[[build/modules/exchange-db]]"
  - "[[build/modules/risk-management]]"
  - "[[build/decision-log]]"
  - "[[references/tradingagents-code-wiki]]"
  - "[[agents.canvas]]"
---

# Videochiamata Luca & Salvatore — 2026-05-29

Due videochiamate nello stesso giorno (mattina + pomeriggio), in continuità. La mattina Luca spiega a Salvatore **come funziona TradingAgents** (il progetto di riferimento) sotto LangChain/LangGraph; il pomeriggio progettano insieme la **loro architettura custom** sulla canvas `wiki/build/architecture/agents.canvas`, lavorandoci direttamente.

> Fonti: `raw/archived/2026-05-29 11-08-30.txt` (call mattina) e `raw/archived/2026-05-29 14-41-53.txt` (call pomeriggio).

---

## Call 1 — Mattina · TradingAgents spiegato + decisione Portfolio vs Day-trading

### Materiale di Salvatore: market driver + indicatori di valuation
- Salvatore ha un file (PowerPoint → PDF) di **market driver macro** fatto con la sua associazione, diviso in **4 macro-categorie** di driver. Vuole portarlo nel vault convertendolo in **TXT/Obsidian** e **arricchendolo** con descrizioni più accurate (così l'agent ha "il vocabolario" delle metriche).
- C'è **un driver specifico** che ritiene utile da monitorare (non ricorda esattamente dove l'avessero messo); proviene dal **sito della Federal Reserve** (dato pubblico → l'agent potrebbe collegarcisi direttamente).
- Vuole inoltre creare un **secondo documento** sugli **indicatori di valuation** delle stock, da fare in collaborazione con l'intera associazione (ognuno ne cura uno, come per il file market driver). Una volta pronto, lo trasforma in TXT e lo inserisce. Idea: i due documenti (market driver + cosa analizzare nelle stock) diventano l'insieme di metriche che servono all'agent — "deve solo imparare ad applicarle".

### Decisione strategica: Portfolio (mid-term), NON day trading
- Riconoscono il pattern: "ogni settimana facciamo una call, arriviamo a una conclusione, la settimana dopo la stravolgiamo". Era partito come intraday/day trading, ora è diventato un **portafoglio**.
- **Day trading**: troppo speculativo e rischioso (leva, rischio blow-up: un'operazione sbagliata in leva può azzerare il capitale e creare debito). Inoltre **non hanno le competenze** per fare day trading e dovrebbero studiarle.
- **Portfolio / mid-term**: hanno le competenze (Salvatore con la triennale ha le basi; serve solo informarsi su indicatori), si può diversificare e mediare, l'AI lo rende più facile/veloce/h24, e **non devono starci dietro 24/7**.
- Salvatore = "l'insegnante dell'AI delle cose economiche": gli insegna i concetti, poi l'AI esegue. Non serve passione nell'AI, serve istruirla bene.
- Differenza chiarita: rendimento mensile vs valore nel tempo → conta la **crescita costante** (non un payout one-shot). Concludono: fanno la cosa "più semplice da gestire, a più alto potenziale".

### Come funziona LangChain (architettura base dell'agente)
Spiegazione di Luca a Salvatore (con analogie):
- **Libreria Python** = insieme di comandi/funzioni fatti da altri, importati nel proprio codice. **Funzione** = istruzioni composte che danno un comando.
- **LangChain** (azienda *LangChain AI*, prodotto di punta) = libreria open source per **creare un agente**.
- Architettura di un agente: dato un **input** (prompt), l'agente — caricato con il suo **LLM** e il suo **system prompt** — entra in un **loop di reasoning**: ragiona → chiama un **tool** → il tool ritorna una risposta → ragiona di nuovo → … fino a quando "ho abbastanza informazioni" → produce la **risposta finale**.
- **System prompt** = il prompt iniziale ("sei un assistente, dato l'input dell'utente rispondi così"). Ce l'hanno tutti (GPT, Claude, Claude Code).
- **Tool** = funzioni Python richiamabili; ognuno ha **name** e **description**; l'agente decide quali chiamare in base a quelle.
- **Analogia chiave**: system prompt = **personalità**; LLM = **cervello**; agent = **corpo umano**; tool = **il PC** davanti a cui il corpo si mette; input = mail dal capo; output = mail al capo. → "Questo è il dipendente."
- Il grande lavoro di TradingAgents è stato sui **system prompt**: "il nostro lavoro più grande sarà sui system prompt". Il system prompt deve indirizzare il ragionamento dell'agente **agnosticamente** (valido per qualsiasi tool/condizione di mercato), senza influenzarlo con la personalità degli autori. Gli si dice **come** usare i tool, a prescindere da quali tool gli vengono dati.

### Come funziona LangGraph (collegare gli agenti)
- **LangGraph** = libreria (stessa azienda) per **collegare gli agenti tra loro** e dargli memoria. Ogni agente (con LLM + system prompt + tool) è un **node** del grafo; i collegamenti sono **edge**.
- **State** = output strutturato condiviso, una **memoria di breve termine** tra i nodi. È come un **template Word/Excel paragrafato** in cui ogni nodo scrive nel suo paragrafo / compila le sue variabili. Es. `investment_plan`: ogni agente aggiorna la sua sezione.
- Gli agenti **non scrivono testo libero**: compilano **variabili tipizzate** dello state (stringa, numero, scelta…). Se la variabile è un numero, l'LLM la compila con un numero. Gli state sono **componibili** e possono essere **annidati** (state dentro state, es. `trade_proposal` contiene `trader_action`).
- **Edge condizionale**: il passaggio da un nodo all'altro può essere subordinato a condizioni (deterministiche o no). Es. se il risk analyst dice "non conviene investire", al trader non si arriva proprio.
- **Memory** (≠ state): memoria esterna, es. il **DB**. Lo state può essere la conversazione completa, la memory un DB con solo riassunti/campi specifici. Due tipi di memoria gestibili a piacere.
- **LangSmith** = sito che si collega al progetto per vedere **graficamente** l'esecuzione: i nodi che si "accendono", i tool chiamati, gli input/output, le **statistiche** (quanto spendi, in che fase sei, quanto ci mette), e creare **metriche di valutazione**. È l'observability/tracing. (Luca deve ancora fare il corso completo di LangGraph e di LangSmith — finora solo i Quickstart; LangChain ha fatto sia Quickstart sia Foundation.)

### Il flusso di TradingAgents (così com'è)
Input: **ticker + data** (+ tipo asset autorilevato; funziona anche su crypto). Poi:
1. **Team di analisti** (sequenziale): market, sentiment, news, fondamentali → ognuno produce il suo **report** (uno state). Il `complete_report` è la **somma** dei report individuali (cartella `reports/<ticker>/` con sottocartelle).
2. **Researchers Bull / Bear + Research Manager (neutral)**: ricevono i 4 report, dibattono aggiornando l'`investment_debate_state` (bull history / bear history), poi il research manager produce l'**investment_plan** (research plan).
3. **Trader**: riceve investment_plan + i 4 report → produce la **trader_proposal** = `Final Transaction Proposal` (action, reasoning, entry price, stop loss, sizing). "Ragiona come trader di desk".
4. **Comitato di rischio** (aggressive, conservative, neutral): dibattono aggiornando il `risk_debate_state`.
5. **Portfolio Manager**: riceve tutto (4 report + investment_plan + trader_proposal + intero dibattito rischio + `past_context`) → produce la **portfolio_decision** con razionale dettagliato portfolio-oriented.

I "tre livelli di impegno" dei debate agiscono solo su **quanto a lungo** gli agenti dibattono.

**Inefficienze identificate da Luca** (da rifare nel loro progetto):
- Analisti **sequenziali** invece che **asincroni** (dovrebbero agire "per i fatti loro", attivarsi su eventi — es. all'uscita delle trimestrali).
- Report **ripetitivi**: ognuno ripete le stesse cose pur occupandosi di temi diversi. Meglio **un unico state** ben strutturato in cui ogni agente arricchisce/conferma invece di 4 report separati (rischio: se mal fatto gli agenti si sovrascrivono e si perdono info → serve template perfetto).
- Bull/Bear **sequenziali e condizionati** l'uno dall'altro (il bear si "attacca" al dato del bull). Dovrebbero presentare **separatamente e indipendentemente**, e il manager leggerli **non confrontati**, per non essere condizionati. Possibile limite caratteri (es. ~100) per forzare sintesi efficiente; approvazione del bear non al 100% (sennò non approva mai).

### Past context (lezioni apprese)
- Il **past_context** è un mini-report estratto dai dati principali degli state di un'analisi precedente sullo stesso ticker. Quando si rianalizza il ticker, oltre a ticker+data viene iniettato il past_context = **"lezioni apprese"** / analisi già fatte da cui partire.
- I **log** sono la versione raw (grezza) di tutto ciò che succede.

### Struttura del codice TradingAgents
- Cartella **`dataflows`**: tutti gli script Python per **estrarre informazioni** dalle fonti. Da tenere così com'è; intercettare dove vanno le info e modificare a valle.
- **`LLM clients`**: script per ogni provider (Anthropic, Azure/Microsoft, Google, OpenAI…). Multi-LLM, già fatti bene → tenere.
- **Tool** (funzioni `def`): es. `get_YFin_data_online` (input: symbol, start_date → estrae OHLCV da Yahoo Finance, salva CSV, ritorna all'agente), `get_stock_stats_indicators_window` (indicatori tecnici, offerti da YFinance), balance sheet / cash flow / income statement (annuali, da YFinance, in CSV), **insider transactions** (es. tipo Nancy Pelosi — non comparse nel report Moncler perché poco rilevanti per quel titolo), scraping **Reddit/news** (subreddit del ticker + default come WallStreetBets, stocks, investing, ordinati per signal density). Alcuni tool chiamano altre funzioni Python per ordine.
- **State** (classi `class`): es. `risk_debate_state` (aggressive_history, conservative_history, neutral_history — tutte `str` con etichetta statica), `trade_proposal`, `portfolio_rating` (con variabile `buy`, ecc.). Più agenti possono scrivere sullo stesso state.

### Le 4 cose su cui fare engineering
Per costruire il loro progetto, Luca individua **4 task di engineering**:
1. **Engineering degli agenti**: quali agenti, come collegarli (node/edge).
2. **Engineering degli state**: quante variabili, come comporle, ogni state **completo ed esaustivo ma non ridondante** (evitare inefficienze).
3. **Engineering dei system prompt** (il vero prompt engineering serio — sui system prompt, non sugli input).
4. **Engineering dei tool**.

→ Si **tiene** TradingAgents come base (tool di estrazione + LLM clients), e si **riscrive da capo il grafo** (node/edge/state/tool), i system prompt, si aggiungono **nuovi tool** (per dati più elaborati), si mettono gli **output in un DB**, si aggiungono **nuovi agenti** (es. backtesting, testing strategie quant). "Cambiare completamente l'approccio".

---

## Call 2 — Pomeriggio · Progettazione architettura custom (agents.canvas)

> Lavoro diretto sulla canvas `wiki/build/architecture/agents.canvas`. Legenda colori: **arancione = agent**, **azzurro = state** (memoria breve termine), **verde = tool/script Python**, **viola = DB**.

### Layer Analisti
- Figure individuate: **Fondamentali** (financials: bilanci, P/E, ecc.), **Market**, **Sentiment**, **Technical** (analisi dal grafico).
- Aggregazione: il **sentiment** si aggrega al **market**; il **technical** si aggrega ai **fondamentali**. Se possibile dividerli in **4**; altrimenti **2 agenti**, ognuno con 2 moduli interni (market+sentiment / fondamentale+technical).
- Etichettati sulla canvas come **"Analyst Research"** e **"Analyst Technical"**.
- Bias: per natura il settore analisti è **bullish** (raramente, dopo aver speso tempo su un'analisi, si conclude "vendi"). Serve un contrappeso bearish.

### Head of Analyst → poi rimosso a favore del Risk Analyst
- I due branch di analisti fanno un **loop di conversazione**, scrivono uno **research state** condiviso e convergono su una conclusione = **strategia di investimento**.
- Inizialmente previsto un **Head of Analyst** (capo che modera, come il moderatore bull/bear) per scindere il bias bullish.
- **Decisione finale**: invertire/eliminare l'head. Il flusso diventa `research_state → Risk Analyst`. Se il risk analyst approva → si va **direttamente al trade**, **senza head** (filtro ridondante). La parte sinistra (analisti) è la **tesi bullish**; il **Risk Analyst è l'antitesi bearish** che cerca di smontare ogni tesi. "Quando acqua e fuoco si mettono d'accordo, è pronto" — se una strategia mette d'accordo due posizioni opposte è davvero buona (anche per ridurre il rischio reale, sono soldi veri).

### Research State (tesi di investimento completa)
- La conclusione degli analisti **non è solo un'idea**: è una **tesi di investimento completa** = buy / hold / sell **+ target price di entrata + target price di uscita + stop loss + sizing**, con i dati a supporto (perché funziona / perché potrebbe non funzionare) e il piano operativo.
- Versionato: la prima research state chiamata **"versione 1 / alpha"** (`research_state_alpha`), con esiti `approved` o `declined` + razionale.
- È come una **presentazione di equity research** istituzionale: in banca più persone specializzate (equity research, analisi finanziaria, DCF…) per economia di scala/scopo producono lo stesso output di un singolo, ma di qualità migliore e in meno tempo. → ha senso dividere le figure pur arrivando allo stesso risultato.

### Risk Analyst (guardrail deterministici + bear)
- Fa rispettare lo **Statuto / guardrail**. Esempi di guardrail: non più del 30% su un singolo continente; VaR max di portafoglio del 10%; diversificazione (geografica, asset class, settore, duration per i bond) — es. se ho già 10 titoli healthcare non ne aggiungo un altro.
- **Insight chiave**: se i guardrail sono **misurabili numericamente**, **non serve un agent** che fa i calcoli (gli agent sono bravi nel reasoning, **non nei calcoli** — quelli li fanno bene le funzioni Python). Tradurre lo Statuto da **testuale** a una **scheda/Excel** di parametri e misurarli deterministicamente (approve/decline in fila).
- Ma il Risk Analyst deve **anche** incorporare la componente **bearish/negativista** (come il bear). Soglia di approvazione **~60-70%** (non 100%, sennò il bear puro non approva mai): se supera la soglia → avanti.
- Può **rimandare indietro con razionale**: es. "buona idea, ma il **target price è troppo alto**" → abbassando il target (aspettando che scenda un po') deterministicamente può rientrare nel VaR. (Es. su VaR 10.000€: target 50$ vs 30$ cambiano quantità e probabilità.)

### Trader = funzione Python deterministica (NON agent)
- Il **Trade** non è un agent: è una **funzione Python deterministica/algoritmica** (in verde) che **estrae** la proposta dallo state ed **esegue**.
- La scelta del **miglior prezzo** tra broker si risolve **deterministicamente** (al trader arriva un solo prezzo, sempre il migliore). Niente agente per la conversione decision→transazione: una funzione estrae i campi e li trasforma in trade.

### Portfolio Manager (CEO / orchestratore)
- All'inizio è **l'umano** (= loro stessi) che fa override manuale. Concettualmente è anche l'**agente orchestratore** = "il GOAT / Jarvis", con **potere decisionale ed esecutivo**.
- Deve avere in pancia lo **stato attuale del portafoglio** con **tutte le metriche** (rendicontazione), ricevuto in forma **sintetizzata** via uno **state periodical synthesis**.
- Si attiva in **2 casi**: (a) un **alert** (target di prezzo), (b) la **periodical synthesis** (a intervalli fissi). Deve restare per lo più libero (non sempre impiegato), attivarsi e orchestrare: chiamare gli agenti, far ragionare, far fare il trade, scrivere nel DB. Può fare **override** (es. una news contro l'idea in portafoglio → cancella la posizione senza passare dall'origination).
- Metafora **tavolo circolare**: tutti gli agenti sono a un tavolo, tutti si rifanno al portfolio manager (capo del tavolo, orchestratore con tool verso tutti). Decide lui quando "ho informazioni sufficienti" → finalizzare.
- Distinzione vs noi: il portfolio manager è il CEO/esecutore; **noi siamo il board** (lo "licenziamo" se va male).

### Il "Desk" (origination) + Desk di monitoring (evaluation)
- Il **desk** (= team analisti + loop) è il workflow di **origination** delle idee; il PM lo chiama **come un tool**.
- Metafora **"TV state" (TG24)**: uno schermo / telegiornale economico che mostra le cose più rilevanti (news, variazioni di prezzo) — l'unica finestra sul mondo esterno per gli agenti "in un garage senza finestre"; il PM ci manda le comunicazioni. (Poi riconsiderato: la TV dovrebbe mostrare il **DB**, dove c'è tutto.)
- **Pezzo mancante identificato — agente di evaluation/monitoring**: oltre a originare idee, serve **monitorare le posizioni esistenti** in continuo e **rifare il processo del desk** se le news cambiano la tesi. Esempio: comprata Ferrari (target 400), esce "Ferrari-luce", -20% → il target resta 400 ma nessuno rivaluta le prospettive. Rischio: avere **due posizioni di segno opposto** sullo stesso titolo. → desk di **origination** (sotto) + desk di **controllo/monitoring** (sopra) che guardano portafoglio, news e target. Il market analyst research nel desk svolge anche questo ruolo di monitoraggio continuo.

### Investment State (gate di completezza)
- L'**investment_state** (blu) è un **filtro**: **non si può fare un trade finché l'investment_state non è completo** → garantisce che tutte le informazioni siano raccolte prima di una transazione (il PM deve passare per **tutti gli analisti**, non può fare trade solo su una news anomala).
- Si **resetta automaticamente** quando il blocco **trade** rileva una transazione (vede lo state pieno → estrae il trade → resetta).

### DB (rendicontazione + dati live + costituzione + log)
Ispirato pesantemente alla dashboard **Streamlit di SFC** ("SFC.streamlit.app"), fatta da **Edoardo Birondi** (detto "Sbirri/Sbirox"), open source, in SFC da ~2 anni (ex offerta IT da Azimut Monaco). Obiettivo: una **replica custom di Yahoo Finance** specifica per loro. Contenuti del DB:

**1. Rendicontazione portafoglio**
- **Liquidità corrente / investita** (la base: quanti soldi liquidi e quanti investiti).
- **Distribuzione portafoglio con più filtri**: geografica, asset class, **settore**, **duration** (per i bond). Realisticamente una **grande tabella** (ogni riga = azione, ogni colonna = caratteristica). Modello mentale a **oggetti** (ogni azione = oggetto con proprietà; le proprietà possono contenere altri oggetti).
- **P/L e metriche di performance** del portafoglio (come sta andando).

**2. Cose che si aggiornano di continuo**
- **Prezzi di mercato**, **calendario economico**, **news**, **indicatori macro**, **insider trading** (institutional positions — pubblicate in ritardo), **tassi di cambio** (importantissimi: non opereranno solo in EUR; legati ad aspettative banche centrali, curva tassi, inflazione).

**3. Costituzione / Statuto** — al **centro di tutto** (sia rendicontazione sia dati live), base di tutto il sistema.

**4. Log** — includono **states, reports, transactions**. Si salva **tutto lo storico**; i tool chiedono al DB solo le info che servono.

**Retention / clustering**: a lungo termine la memoria cresce troppo → niente troncamento secco, ma **clusterizzare + riassumere + cancellare progressivamente** tenendo un riassunto. Ipotesi: 5 anni giornaliero, 5-10 settimanale, 10-30 mensile. Hardware: hard disk esterni (es. 20TB ~500€, 1TB ~75€). Molti dati vecchi (prezzi, news) sono comunque recuperabili online (Yahoo Finance, Reuters — quest'ultimo ora a pagamento).

### Extractors (set + adaptive) e Market Alert
- **Extractors set** = i **primi tool** a disposizione degli agenti. Estraggono tutte le info di mercato e le mandano **sia al DB sia agli agenti** (salvate in entrambe le direzioni).
- **Adaptive extractor**: frequenza **adattiva** in base alla **vicinanza al target**. Posizione entro il 30% dal target → frequenza alta (modalità rischio); posizione lontana → daily. Serve a risparmiare potenza di calcolo e a rispettare i **rate limit** delle API (Yahoo Finance ecc. bloccano troppe richieste).
- **Market Alert agent**: riceve dagli adaptive extractor; unico tool = **calendar tool** che scrive eventi nel **calendario economico**. Es: se da una news si legge "Ferrari elettrica esce il giorno X", aggiunge la data al calendario → diventa un **alert** (come le trimestrali: alla corrispondenza data/ora scatta l'alert).

### Attivazione del sistema, news e mercati efficienti
- **Alert** = solo **numerico/prezzo** (target). Per le **news** c'è il problema che le **API funzionano solo a richiesta** (non fanno push): non si può essere notificati automaticamente all'uscita di una news.
- **Risoluzione via teoria dei mercati efficienti**: i prezzi riflettono le informazioni. Se succede qualcosa (anche un evento estremo), il **portafoglio si muove** → l'agente che monitora il portafoglio vede il **prezzo anomalo**, va a cercarne la spiegazione (chiama news vecchie, tassi di cambio…) e si attiva. Facendo **long-term**, non serve reazione istantanea alle news (l'implicazione è a 3-6 mesi, non a domani; in caso si compra una **put** di copertura, non si liquida medio).
- Il **Risk Analyst** ben prompted, vedendo un prezzo anomalo, **autonomamente** va a cercare le news/spiegazioni → lo **switch** si dà nel **system prompt** (rendere ogni agente quanto più autonomo possibile è "il vero lavoro che dà valore").

### Portafoglio iniziale già investito
- Per evitare il problema dell'avvio "a portafoglio vuoto" (niente movimenti di prezzo che attivino il sistema), **partire con un portafoglio già investito**: il loro obiettivo è **mantenere/ribilanciare**, non costruire da zero.
- Es. con 100 (10 liquidi), investire nelle **top 10 / magnifiche 7** in proporzione (10 ciascuna). L'**universo investibile** si dà come **lista** (es. tutti i sottostanti dell'S&P / all-world ETF), non come titoli effettivamente investiti.
- Alternativa più semplice: dare un **ETF all-world** (BlackRock/Vanguard) come strumento, fornendo la **lista dei sottostanti** per le analisi (il prezzo dell'ETF incorpora i 500 sottostanti).
- Il PM poi **ribilancia in autonomia** (può vendere e comprare anche nello stesso momento, non singolarmente): "il nostro portafoglio è questo; dopo le analisi dovremmo vendere questo di tot e comprare questo di tot".

### Benchmark
- Una gestione attiva ha **sempre un benchmark** (principio del fondo attivo, da "Atrezzi") = "un numero da superare". Candidati: **S&P 500**, FTSE MIB, **FTSE All-World** (Vanguard/BlackRock).
- Orientamento: tenere **S&P** (US, utile) + un benchmark **60/40 Vanguard all-world** (riferimento già presente su `trading-agent.lucamanca.synology.me`). Col 10% di liquidità saranno ~**50/40** o **55/35** + 10% cash (un po' meno investiti del benchmark, ma puntano a **selezione attiva** migliore).
- **Idea**: **selezione attiva dei titoli dell'S&P** — universo ridotto a 500 (solo US, pubbliche, trasparenti, in inglese), prendere il **percentile migliore** e battere l'indice. "L'unico modo in cui potremmo battere l'S&P".
- Dati: S&P **+29%** ultimi 12 mesi, **+10% YTD** (al 2026-05-29). Per battere serve >30% (sul singolo periodo). Target "soddisfacente": almeno 10% (battere il benchmark).

### LLM: OpenRouter + DeepSeek V4 Pro (con confronto costi)
- Useranno **OpenRouter** = "il router dei modelli", intermediario verso tutti i provider (Anthropic, Google, Qwen, ecc.) → massima agilità per cambiare modello.
- **Confronto costi** sul report NVIDIA reale: **163.000 token input + 20.000 token output** (~183k totali). Prezzi per **milione di token**:

| Modello | Input ($/M) | Output ($/M) | Costo report NVDA |
|---|---|---|---|
| **DeepSeek V4 Pro** (il più usato su OpenRouter) | ~0,40 | ~0,87 | **~$0,09** |
| Claude Sonnet 4.6 | 3 | 15 | ~10× DeepSeek |
| Claude Opus (4.8, uscito ieri) | 10 | 50 | — |
| GPT-5 (latest) | 5 | 30 | — |
| DeepSeek (provider US, alt.) | 1,3 | 2,6 | comunque < Sonnet ma ~3× DeepSeek base |

- **Decisione**: usare **DeepSeek V4 Pro**. I modelli cinesi costano ~10× meno (niente GPU Nvidia per il ban export USA → innovazione forzata sull'efficienza; open source, eseguibili in locale su GPU Nvidia senza cedere dati). Sulla privacy dati: "me ne sbatto" (alla Zuckerberg). C'è anche **DeepSeek V4 Flash** (il più usato della settimana). (Opus 4.8 non usabile senza premium.)
- Nota didattica GPU vs CPU: CPU = calcoli in sequenza; GPU = calcoli in parallelo (nate per il rendering video, perfette per le reti neurali = miliardi di neuroni in parallelo). Nvidia da gaming a leader AI; competitor AMD (Ryzen). Tutte concentrate a San Francisco.

### Principio efficienza agenti (no limite per costo)
- **Non limitare il numero di agenti per costo**: tarare il **massimo risultato col minor costo** evitando il **context rot**.
- **Context rot**: oltre una soglia di contesto riempito (~50-60%, talvolta 30%) le performance calano **drasticamente** e il system prompt comincia a "sfarfallare". Benchmark **"needle in a haystack"**: come gli umani, gli LLM ricordano meglio inizio e fine, non un dettaglio a pagina 85. → dare a ogni agente **solo le info che servono**, non troppe né ridondanti (sennò inventa) né troppo poche.
- Pattern preferito: **~4 agenti** = 3 **specializzati** che compilano gli state + 1 **orchestratore** che legge lo state e **chiama gli altri** secondo necessità (più volte quello delle news se servono più news, meno quello tecnico). "Non è importante quanti agenti hai, ma ottimizzare le info che gli metti dentro" e **definire i ruoli in modo inequivocabile**.
- Agenti **asincroni**: ognuno con i suoi timer, parte su evento o quando chiamato da agenti a valle.
- I costi si possono testare anche **per singolo agente** con LangSmith (tracing/observability, anche metriche non standard).

### Note varie
- **News analyst con indicatori numerici**: dargli dati tangibili (es. **non-farm payrolls**) oltre al reasoning, con spiegazione **oggettiva e vaga** delle possibili implicazioni (per non condizionarlo con opinioni personali). "L'AI è come un figlio (con steroidi: dentro ha tutta la conoscenza, va solo tirata fuori): istruiscila bene, ma non troppo da influenzarla." Da testare se aiuta o intralcia il reasoning.
- **Analisi tecnica** (Salvatore la reputa in parte "fuffa"): ha senso **usata bene** — minimi/massimi a 52 settimane, range, drawdown, volumi, capire cosa è successo il giorno di uno sforamento. Serve ad avere "il quadro" (come una dashboard vs dati grezzi), **non** a fare trading con "candele" alla guru di Dubai. Posizione **ibrida** col sentiment (legge tweet/posizioni delle persone). Il sentiment **non ha indicatori propri** (al massimo indici di paura) → vanno inventati.
- **Fondamentali**: non sono "pochi". Es. esistono **5 tipi di P/E**; Salvatore usa il confronto **trailing vs current** (capire se è sceso per prezzo o per EPS). Si può dare un **tool** per calcolarli e lasciar decidere all'agente come combinarli.
- **Factor investing / regressioni / strumenti statistici**: utili ma "un'altra parte della finanza", richiedono competenze che non hanno e non studiano in finanza → per ora fuori scope.
- **Sogno fine-tuning**: un dataset di **tutte le decisioni + ragionamenti di Salvatore** per fare fine-tuning di un modello che si comporti come lui ("continuous fine-tuning" = vera AGI). Per ora idea.
- **Canale Telegram "sala segnali"**: per Luca (e Salvatore può aggiungersi) con calendario economico, riassunti news, prezzi, trade fatti, variazioni di prezzo importanti (orario/giornaliero). Plaggabile alla dashboard con alert interattivi (anche su telefono).
- **Incidente operativo**: durante la call la canvas (e parte del vault) ha avuto un disastro di sync iCloud/Obsidian su Salvatore; recuperata via GitHub/zip/OneDrive. La `agents.canvas` è stata lavorata pesantemente e va custodita. (Dettaglio operativo, non conoscenza di progetto.)

---

## Action items emersi

- **Salvatore**: convertire il file **market driver** (4 macro-categorie) in TXT e arricchirlo; preparare il documento **indicatori di valuation** (con l'associazione); riclassificare/arricchire i fondamentali (es. tipi di P/E).
- **Luca**: riscrivere il **grafo** (agenti/edge/state/tool) ispirandosi a TradingAgents; implementare **Extractors set + Adaptive extractor + Market Alert + calendar tool**; configurare **OpenRouter + DeepSeek V4 Pro**; progettare il **DB** (rendicontazione + dati live + costituzione + log); valutare il **canale Telegram**; studiare i corsi completi LangGraph e LangSmith.
- **Insieme**: finalizzare la `agents.canvas`; decidere se gli analisti sono 2 o 4; verificare a sviluppo se l'investment_state e l'architettura sono sufficienti ("vedersi più spesso per finire la lavagna").
</content>
</invoke>
