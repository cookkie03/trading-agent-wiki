---
title: "Agents — Portfolio Manager, Desk analisti, Risk Analyst"
type: build
tags:
  - build
  - multi-agent
  - architecture
created: 2026-05-13
updated: 2026-06-20
status: active
priority: high
area: software
related:
  - "[[system/architecture]]"
  - "[[system/modules/data-layer]]"
  - "[[system/modules/execution]]"
  - "[[system/modules/quant-backtesting]]"
  - "[[prior-art/tradingagents/code-wiki]]"
  - "[[prior-art/tradingagents/paper]]"
---

# Agents — Portfolio Manager, Desk analisti, Risk Analyst

> **Stato attuale della pagina (2026-06-23)**: questa è la **spec concettuale** del layer agenti. Le note su Datapizza, branch o file Python precedenti restano utili come **storia / reference design**, ma non descrivono automaticamente il codice attuale del progetto.

> **Direzione invariata**: PM orchestratore, desk specializzati, Risk come gate e agenti fortemente tool-centrici. Il problema aperto non è più “se esiste codice”, ma **quale architettura agente costruire sopra il nuovo harness reale**.

^01280b

Il cuore di ragionamento del sistema: gli agenti LLM che producono la tesi di investimento (`research_state`) e la sottopongono al gate del rischio. Mappa il gruppo **desk (workflow)** di `[[architettura.canvas]]` più il nodo **Portfolio Manager**. La conversione finale in trade è deterministica e vive in [[system/modules/execution]].

Topologia (canvas):
```
Portfolio Manager (agente orchestratore / CEO)
  │  ◄── attivato da: alert numerico | periodical synthesis
  │  (tavolo circolare: tool verso tutti, decide quando "ho info sufficienti")
  ├─► Analyst Research   (Market + Sentiment)   ┐
  ├─► Analyst Technical  (Technical + Fondamentali) ┘→ loop conversazione → research_state
  │                                                        │
  │                                                        ▼
  └─► Risk Analyst (antitesi bear + guardrail da Statuto) → approve (~60-70%) / decline+razionale
                                                           │
                                                           ▼  (se approve)
                                            Investment State → Trade  →  [[system/modules/execution]]
```

---

## Riferimenti di codice (repo esterni)

- **Prompt Builder + LLM JSON strict**: [[prior-art/libraries/rizzo-trading-agent]] — utile come riferimento per l'engine che assembla il contesto e per il prompt builder; per la parte di prompt engineering e pattern agentici va confrontato con [[prior-art/tradingagents/code-wiki]].
- **LLM → views ([[_meta/glossario#Black-Litterman|Black-Litterman]])**: [[prior-art/libraries/cvx-portfolio-optimizer]] — `api/baml_src/GenerateViews.baml`: pattern "fattori per asset → views con confidence → Idzorek alpha". L'LLM produce opinioni, la matematica decide i pesi entro i vincoli.
- **Tool ispirazione**: sezione "Data Retrieval Tools and Utilities" di [[prior-art/tradingagents/code-wiki]] (Fundamental Data, News/Insider Transactions tools).

---

## Portfolio Manager — agente orchestratore (CEO)

Il PM è un **agente LLM** con potere decisionale ed esecutivo (il "CEO" / "GOAT" del tavolo circolare): ha tool verso tutti gli agenti, li chiama come tool, e decide quando *"ho informazioni sufficienti"*. 

- **Trigger di attivazione**: Le casistiche di attivazione (elenco di riferimento in [[system/modules/data-layer]]) sono: (a) **alert** numerico/prezzo (target/calendario); (b) **periodical synthesis** (state sintetico a intervalli fissi, rendicontazione + market); (c) **`next_check_date` scaduto** di un investimento precedente → il Dynamic Temporal Checkpoint richiama il PM per rivalutare quella posizione *(input di Luca 2026-06-04)*; (d) news anomale / soglia di variazione (alternative ancora da decidere). Per il resto resta libero e orchestra: chiama agenti → li fa ragionare → genera trade → scrive nel DB.
- **Override**: news contro l'idea → cancella/ribalta la posizione.
- **Istruzione "nel dubbio, chiedi sempre"** (input di Luca 2026-06-04): essendo il decisore finale, il system prompt del PM deve imporgli di **non risolvere mai un dubbio da solo** — in caso di incertezza, *anche minima*, **interroga di nuovo i desk** per più informazioni, **sempre**, prima di chiudere la tesi. Default verso l'approfondimento; i tetti anti-loop ([[system/parallelism-design]]) sono solo rete di sicurezza, e l'**astensione (no-trade)** è preferibile a un trade su basi incerte.
- **Desk di origination** (i due desk analisti) chiamati dal PM come tool. Serve anche un **desk di monitoring/evaluation** che sorveglia le posizioni esistenti e rifà il processo quando le news cambiano la tesi (evita target obsoleti o posizioni di segno opposto sullo stesso titolo). **Punto di partenza per il design**: prendere dalla dashboard SFC il lato osservabilità/reporting, non la logica di decisione.
- **Orchestrazione multi-ticker** (come il PM analizza N ticker in parallelo senza mescolare gli state) e **criteri di "info sufficienti"** (quando decidere di fare/non fare un trade, evitando loop infiniti): alternative di design in **[[system/parallelism-design]]**.

### Autonomia totale: nessun input umano oltre l'accensione (input di Luca 2026-06-04)
Il sistema **non deve richiedere alcun intervento umano** se non l'**accensione del software**. All'avvio il programma fa partire **da solo** i timer della *periodical synthesis* e il *meccanismo di alert*; da lì in poi il PM si auto-attiva sui trigger sopra e opera senza supervisione. L'override umano resta come *possibilità* nelle prime fasi (finché il sistema non è affidabile), non come *requisito* operativo. → decisione in [[system/decision-log]].

### Attivazione e mercati efficienti
Le **API funzionano solo a richiesta** (no push news). Risoluzione via **teoria dei mercati efficienti**: i prezzi riflettono le informazioni → un **prezzo anomalo** attiva il monitoring, che poi cerca la spiegazione (news, tassi). Coerente col mid-term: non serve reazione istantanea. L'autonomia va poi tradotta in prompt, tool policy e trigger, non lasciata come slogan astratto.


---

## Desk analisti

Due desk (decisione consolidata dal canvas, chiude il dubbio "2 vs 4 agenti"):

| Desk | Agenti interni | Funzione |
|------|----------------|----------|
| **Analyst Research** | **Market** + **Sentiment** | Contesto di mercato/macro; sentiment news/social (indicatori da definire, aggrega su Market). |
| **Analyst Technical** | **Technical** + **Fondamentali (financials)** | Segnali tecnici/quantitativi → [[system/modules/quant-backtesting]]; financials e ratio (es. P/E trailing vs current), aggrega sul Technical. |

I due desk saranno in grado anche di conversare tra di loro oltre che con il PM in un **loop di conversazione** e convergono su un `research_state`.

### `research_state` = tesi di investimento completa
Non solo l'idea, ma: `buy/hold/sell` + **target price entrata + uscita + stop loss + sizing** + pro/contro + livello di **convinzione**. Versionato (`alpha`/v1), esiti `approved`/`declined`. **Schema dettagliato e contratto dei campi → [[system/state-schemas]]** (tutti i campi obbligatori; `position_sizing` incluso, vedi [[system/position-sizing]]).

> **[[_meta/glossario#Conviction Level|Conviction level]]** assegnato dal **Portfolio Manager** date le info degli analisti (decisione 2026-06-02). Fa parte del più ampio [[system/rating-scoring]] (conviction sul trade · scoring del lavoro degli agenti · rating asset per il disinvestimento).

>  **Aggregazione `direction` + `conviction`**
> (deciso 2026-06-04): ogni desk lascia nello state la **propria proposta** (`suggested_direction` + `suggested_conviction`); il **PM raccoglie tutte le opinioni e decide** quella finale — l'aggregazione vive nel nodo PM, non in un nodo desk separato. In prospettiva i **pesi** con cui il PM fida ciascun desk vengono dalla hit-rate storica calcolata dal backtesting → [[system/learning-feedback-loop]] §4. Vedi schema in [[system/state-schemas]].

> **Head of Analyst eliminato**: il moderatore anti-bias era ridondante. Gli analisti sono la tesi bullish, il Risk Analyst è l'antitesi bearish.

---

## Risk Analyst — gate bear + guardrail da Statuto

Posizionato come **gate unico** tra il `research_state` e il Trade. Resta comunque aperta una decisione di design: quanto il Risk Analyst debba stare come desk pari agli altri nella fase esplorativa e quanto invece come gate finale separato.

- Gli analisti sono per natura **bullish**; il Risk Analyst è l'**antitesi bearish** che cerca di smontare ogni tesi. *"Quando acqua e fuoco si mettono d'accordo, la strategia è davvero buona."*
- Riceve il `research_state` e dà **`approved` / `declined` + razionale**. Se approva → si va **direttamente** a Investment State → Trade.
- **Soglia ~60-70%** (non 100%: un bear puro non approverebbe mai).
- Può **rimandare indietro con razionale**: es. *target price troppo alto* → abbassandolo la posizione rientra nel [[_meta/glossario#VaR (Value at Risk)|VaR]] (con VaR 10.000€, target 50$ vs 30$ cambiano quantità e probabilità di realizzo).

### Guardrail deterministici vs reasoning
**Insight chiave**: se un guardrail è **misurabile numericamente**, non serve un agente — gli agenti sono bravi nel **reasoning, non nei calcoli**. → tradurre lo **Statuto da testuale a scheda di parametri** e misurarlo **deterministicamente** (check Python approve/decline). Esempi: max % su singola area/continente; **VaR di portafoglio max ~10%**; diversificazione per geografia/asset class/settore/duration (es. niente nuova posizione healthcare se già esposti). La componente **bearish/qualitativa** resta affidata al reasoning dell'agente.

### Lo Statuto del Fondo (institutional-grade)
Insieme generico e rigoroso di regole deterministiche in Python puro (nessun LLM), per emulare gli statuti di rischio istituzionali ed eliminare bias. Regole cardine:
1. **Riserva di Liquidità 10%**: almeno il 10% del portafoglio sempre disinvestito in cash puro (riserva strategica, non intaccabile nelle allocazioni ordinarie).
2. **Meccanismo di Disinvestimento**: nuova opportunità ad altissima convinzione con portafoglio al 90% → modulo deterministico che valuta se disinvestire (parziale/totale) da un asset esistente, calcolando la forza relativa dei segnali.
3. **Leva su Strong Signals**: leva permessa **solo** su `Strong Buy`/`Strong Sell` validati (vedi sotto).

### Gestione Leva con Opzioni (Call/Put)
Leva asimmetrica per mitigare rischio di liquidità/margine. **Dove vive la logica**: il livello di **convinzione** (`Strong Buy`/`Strong Sell`) è un campo dello `research_state` prodotto dagli analisti e **validato dal Risk Analyst**; l'acquisto effettivo delle opzioni è eseguito dalla funzione Trade deterministica ([[system/modules/execution]]).
- **Nessuna leva diretta a debito** (margini gravosi).
- `Strong Buy` validato → opzioni **Call**; `Strong Sell` validato → opzioni **Put**; segnali standard (`Buy`/`Sell`/`Hold`) → equity spot senza leva.
- La rilevazione/validazione del segnale `Strong` è un **task di sistema**, assegnato in fase di mappatura del grafo al nodo più coerente (probabilmente aggregazione analisti → Risk Analyst).

### LLM Token Cost Estimator
Ogni chiamata LLM (via **OpenRouter**) ha un costo in token. Trattamento economico: i costi token (convertiti in $/€) sono **equiparati alle commissioni del broker**. Ogni trade proposto sottrae dal profitto atteso sia le commissioni broker sia il costo token del ciclo (**net performance**). Prospettiva avanzata: auto-finanziamento (preleva parte dei profitti per ricaricare i crediti OpenRouter).

---

## Filosofia degli Agenti

*Consolidata dalla lettura di TradingAgents (2026-05-19) e dal brainstorming del 2026-05-27.*

**Pochi agenti LLM con tool potenti** (contro la proliferazione di agenti di TradingAgents). Due macro-fasi logiche supportate da moduli deterministici:
1. **Ricerca / Analisi**: analisi finanziaria core (fondamentale, macro, settore), rating operativi (`Buy`/`Sell`/`Hold`). I vecchi *Bull/Bear Analyst* sono **eliminati** (2026-05-26): il loro lavoro è incorporato nella vista strategica di analisi finanziaria.
2. **Esecuzione**: ricevono state + proposta, valutano la fattibilità entro i limiti di rischio deterministici, inviano le proposte (vedi [[system/modules/execution]]).

**Efficienza ≠ numero di agenti (context rot)**: non limitare gli agenti per costo, ma massimo risultato col minor costo evitando il **context rot** (degrado oltre ~50-60% di contesto riempito). Pattern preferito: **~4 agenti** = specializzati che compilano gli state + 1 orchestratore. Dare a ogni agente **solo** le info che servono. Agenti **asincroni**, ruoli definiti inequivocabilmente nel system prompt.

**Tool-centric design**: dare quanta più completezza informativa con la minor latenza. Esporre **tool parametrici di calcolo** che l'agente invoca on-demand (non solo un set fisso pre-calcolato). Per ogni tool ereditato dal fork TradingAgents: tenere, potenziare o riscrivere.

> **Tool obbligatorio — iniezione dello stato del portafoglio** (input di Luca 2026-06-04): tra i tool deve esserci quello che **inietta lo stato corrente del portafoglio** (rendicontazione: liquidità, posizioni, distribuzione, P/L) nel contesto dell'agente che ragiona. Senza la foto aggiornata di "dove siamo investiti e con quanta cassa", nessuna decisione di sizing/disinvestimento è sensata. Legge dall'area *rendicontazione* del DB → [[system/modules/data-layer]].

> **Autonomia informativa: real-time tool first, write-through sul DB** (input di Luca 2026-06-05): mentre ragiona su un `investment_state`, l'agente deve essere **estremamente autonomo nel chiamare informazioni aggiornate** — anche **più volte**, per *essere sicuro* del dato e per **verificare aggiornamenti** durante il ragionamento. Regola di precedenza: l'agente prova **prima il tool specifico che estrae l'info in real time** (non il DB), proprio per garantirsi la freschezza nel momento della decisione. Il tool **consegna il dato all'agente *e* manda una copia al DB** (pattern *write-through*): così il **DB resta il centro unico delle informazioni** senza che l'agente debba accontentarsi di un dato potenzialmente vecchio. Si sposa con l'istruzione *"nel dubbio, chiedi sempre"* e con l'autonomia totale. **Riconciliazione con il DB-first** (no contraddizione): vedi nota sotto e in [[system/modules/data-layer]].
>
> - **Dato live / decision-critical** (prezzo corrente, ultima news, quote opzioni): **real-time tool first** → copia in DB. La freschezza vale il costo (token/API trattati come commissioni).
> - **Dato storico / immutabile** (barre passate, bilanci depositati): vale ancora il **check-presenza DB-first** ([[system/modules/data-layer]]) — inutile ri-scaricare ciò che non cambia.
> - Restano attivi i guardrail dell'**adaptive extractor** (frequenza/rate-limit) come rete contro chiamate eccessive.

---

## State Management e Schemas

Obiettivo: **pochi schema potenti e dettagliati**, non tanti frammentati. Pattern da TradingAgents:
- **TypedDict** per gli state di workflow (propagati tra i nodi del grafo).
- **Pydantic** per gli output strutturati LLM (field descriptions come istruzioni).
- **Fallback a free-text** quando lo structured output fallisce (previene interruzioni del pipeline).
- **Investment State = gate di completezza**: nessun trade finché lo state non è completo (forza il passaggio per tutti i desk); reset automatico quando il blocco trade rileva la transazione.

---

## Orchestrazione e Tracciamento

- **Storico recente**: una build precedente aveva migrato il grafo verso Datapizza AI e dismesso il blocco LangChain/LangGraph/LangSmith.
- **Stato attuale del progetto**: il framework concreto del nuovo build va considerato **decisione ancora aperta**, non dato acquisito. Questa pagina descrive il comportamento atteso degli agenti; la scelta definitiva del framework vive in [[system/stack]] e in board.

### Provider LLM: OpenRouter con DeepSeek V4 Pro
**OpenRouter** come router unico verso tutti i provider (agilità). **[[_meta/glossario#DeepSeek|DeepSeek V4 Pro]]** modello principale: sul report NVDA reale (163k input + 20k output token) costa **~$0,09**, contro ~10× di Claude Sonnet 4.6. Vedi [[system/decision-log]] e [[system/stack]].
Nota emersa dai commenti di Luca: resta sul tavolo un assetto **multi-modello**, con un modello frontier per il PM e modelli più economici per i desk. Decisione ancora aperta.

---

## Dipendenze

- Legge da: DB centrale (rendicontazione, dati live, log) → [[system/modules/data-layer]]
- Produce: `research_state` → gate Risk Analyst → Investment State → [[system/modules/execution]]
- Segnali quant per il desk Technical da [[system/modules/quant-backtesting]]

---

## TODO / Decisioni aperte

- Schema finale di `research_state` / `investment_state` → **bozza in [[system/state-schemas]]** (da raffinare).
- Formula di **position sizing** → **[[system/position-sizing]]**.
- **Orchestrazione multi-ticker** + criteri "info sufficienti" + max iterazioni → **[[system/parallelism-design]]**.
- Sistema di **rating/scoring** (conviction, agenti, asset) → **[[system/rating-scoring]]**.
- **Loop di valutazione/apprendimento** (reportistica "cosa va male", scoring agenti, ponderazione pesi, feedback post-trade) → **[[system/learning-feedback-loop]]**. Aperto: punto di aggancio della ponderazione pesi (input PM vs nodo aggregazione) — tensione con "conviction dal PM".
- Integrare i **Dynamic Temporal Checkpoints** nello state (`next_check_date`).
- Dove vive l'aggregazione/validazione del segnale `Strong`.
- ~~**Comportamento di ogni singolo agente del desk**~~ → **impianto approvato (2026-06-06)**, dettaglio in **[[system/agent-behaviors]]**: per Market/Sentiment/Technical/Fondamentali sono definiti input · tool (dall'inventario) · output nello state · stile di ragionamento · criterio di stop. Decisi i 3 snodi: news/sentiment spartiti **per tipo di informazione** (Market=catalizzatori, Sentiment=mood multi-fonte incl. social/Reddit); **tutti contribuiscono alla direzione** (ognuno la sua parte, ma può esprimersi su tutto); **stop = auto-stop + il PM può richiamare**. Sotto-lavoro aperto: enumerare le **fonti/tool di sentiment** (famiglia D di [[system/tools-inventory]]). Resta da scrivere il system prompt che realizza tutto questo (Prompt Builder).
- ~~**Selezione dei tool da costruire per gli agenti**~~ → **impianto approvato (2026-06-06)**, inventario in **[[system/tools-inventory]]**: 9 famiglie (A prezzi · B indicatori · C fondamentali · D news/sentiment · E macro · F calendario · G portafoglio · H opzioni · I guardrail=non-tool), ognuna con 5 etichette (cosa · live/storico · write-through · agente · vendor) + 2 regole trasversali (parametrici mai hardcoded · write-through del dato live). Risolti: portfolio auto+richiamabile, `compute_indicator` parametrico. Restano aperti solo i **vendor** (live MVP + opzioni), a implementazione. Strettamente legato al "comportamento per-agente" qui sotto.
- Valutare l'architettura **debate** del Risk (quanti agenti, quali prospettive).
- Design del **desk di monitoring/evaluation** (partire da SFC Streamlit).
- ~~Ruolo del nodo `mantainer`~~ → **confermato** (technical → rendicontazione, vedi [[system/modules/data-layer]]).
- Regole dello **Statuto**: capire quali info dargli e in quale forma (template/wireframe) — vedi [[system/decision-log]].

*Vedi [[system/decision-log]] per le decisioni aperte e [[system/architecture]] per la vista d'insieme.*

---
## Commenti recuperati da iCloud (2026-07-01)

> Commenti Obsidian `%%...%%` presenti nella vecchia copia iCloud (`7054827`) e reinseriti senza sovrascrivere il contenuto corrente.

%%questa parte e topologia è molto rappresentativa, vale la pena valorizzarla%%

%%ha senso ispriarsi a [[rizzo-trading-agent]] per l'engine che inietta i prompt e come prompt builder, ma come knowledge e engineering dei prompt vale la pena riferirsi al codice della repo di  [[code-wiki]]%%

%%????? non ho capito%%

%% non ho capito quest'ultima frase%%

%%da capire se implementare%%

%% da definire meglio, perché nella mia idea personale e in quella di salvatore, all'inizio il risk analyst aveva lo stesso ruolo degli altri analyst desks e si posizionava in quell'ottica li, ma anche come viene descritta di seguito è una buona idea, valutare%%

%%obsoleto, ora siamo a datapizza AI come framewrok, langchain ecosystem dismesso%%

%% anche se alla fine, per quanto riguarda il PM, utilizzerei comunque un modello claude di frontiera, tenendo Deep seek per gli altri agent%%

