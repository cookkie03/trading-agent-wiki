---
title: "Conversazione Luca & Salvatore (2026-05-27)"
type: source
tags:
  - source
  - architecture
  - risk
  - strategy
  - project-management
raw_source_path: "raw/daily-notes/2026-05-27.md"
created: 2026-05-27
updated: 2026-05-27
confidence: high
status: active
related:
  - "[[build/modules/llm-agent-system]]"
  - "[[build/modules/risk-management]]"
  - "[[build/decision-log]]"
---

# Conversazione Luca & Salvatore (2026-05-27)

Sintesi e strutturazione del brainstorming tenutosi il 27 maggio 2026 tra Luca e Salvatore tramite messaggi chat e una serie di 18 note vocali WhatsApp. La sessione ha consolidato scelte fondamentali sull'architettura degli agenti, la gestione del rischio e della liquidità, la leva con opzioni, la stima dei costi LLM e il modello operativo/monetizzazione.

---

## 1. Architettura del Sistema Agenti

### Macro-suddivisione Ricercatori ed Esecutori (Task Decoupling)
- Viene confermata la decisione di dividere concettualmente i compiti del software in due macro-fasi:
  - **Fase di Ricerca / Analisi (Ricercatori)**: condurre l'analisi finanziaria core (fondamentale e macro), generare segnali operativi e produrre rating di convinzione di mercato (Buy/Sell/Hold, con gradazioni come `Strong`).
  - **Fase di Esecuzione (Esecutori)**: traduzione dei segnali elaborati in ordini di mercato reali. Questo layer necessita di **tool estremamente potenti e specializzati** per la gestione operativa.
- *Nota di Design (Scollegamento dei rating dagli agenti specifici)*: La questione dell'emissione dei segnali (compresi `Strong Buy` e `Strong Sell`) viene esplicitamente **scollegata dalla tipologia rigida di agenti che la eseguiranno**. In fase di modellazione del grafo e del team multi-agente, verranno prima definiti e raccolti in modo granulare tutti i singoli compiti che il software deve svolgere. Solo successivamente verrà configurato il team di agenti più efficiente ed ottimizzato, assegnando ciascun compito (inclusa la rilevazione del livello di convinzione) all'agente o al nodo del grafo più coerente.

### Stack Tecnologico ed Evaluation (LangSmith)
- Luca sta approfondendo lo studio di LangChain/LangGraph. Fa riferimento a diversi corsi: quelli di tipo *Essentials/Quickstart* (della durata di un'ora, già completati) e i corsi completi che durano circa 30-50 ore, che intende completare con calma ma costanza.
- Viene introdotta l'adozione di **LangSmith** e del relativo portale UI/CLI. Questo strumento permetterà di tracciare le invocazioni degli agenti, modificare le catene e configurare metriche di valutazione (evaluation) direttamente tramite l'interfaccia web user-friendly del provider, evitando di dover programmare interamente questi sistemi lato codice in questa fase. Una volta testati e validati sul portale, i flussi potranno essere esportati o integrati nativamente.

---

## 2. Risk Management & Lo Statuto del Fondo

### Lo Statuto Deterministico (Institutional-Grade)
- Il Risk Management non opererà solo con paletti dinamici ciclo per ciclo, ma implementerà a monte uno **"Statuto del Fondo"** a livello deterministico (scritto in Python puro, non delegato a LLM).
- Questo statuto conterrà un insieme generico e strutturato di regole rigide e inviolabili, sul modello degli statuti degli investitori istituzionali reali, con l'obiettivo di eliminare completamente i bias emotivi e operativi del trader.

### Regola della Riserva di Liquidità (10%)
- Come prima regola cardine dello Statuto, viene imposto l'obbligo di mantenere una **riserva di liquidità costante del 10% del portafoglio sempre disinvestita** (in cash puro).
- La liquidità è considerata a tutti gli effetti un asset strategico. Questa riserva garantisce:
  1. La disponibilità immediata di capitale per cogliere occasioni di mercato sottoprezzate (value opportunities).
  2. Una barriera minima di protezione e stabilità del portafoglio.
- Viene riconosciuta l'impossibilità di operare ad alta velocità (HFT) o fare arbitraggio causa limiti hardware e di infrastruttura (impossibile battere operatori professionali 24/7). Il vantaggio del sistema non risiede nella velocità ma nel monitoraggio disciplinato e nel **ribilanciamento del portafoglio** (Value Trading / Wealth Manager autonomo).

### Meccanismo di Vendita e Allocazione della Liquidità
- Viene sollevato un problema finanziario complesso: se il Trader identifica un titolo altamente promettente in cui investire ma il portafoglio è già interamente allocato (salvo il 10% di riserva intangibile), dove recupera la liquidità?
- Il Trader non può semplicemente attingere alla riserva. Deve implementare un **meccanismo deterministico di vendita / disinvestimento parziale**:
  - Valutare la forza del nuovo segnale rispetto alle posizioni già in essere.
  - Decidere da quale asset disinvestire (anche se valutato positivamente) per liberare capitale in favore dell'opportunità migliore.
  - Questo algoritmo di vendita/ribilanciamento rappresenta una delle sfide matematiche e di codice più rilevanti del Modulo C/Risk.

### Leva Finanziaria e Derivati
- L'utilizzo della leva finanziaria a debito diretta è giudicato estremamente rischioso e insostenibile all'inizio, a causa dei severi requisiti di margine e delle elevate quote di capitale che il broker richiede di mantenere bloccate come garanzia.
- **Soluzione alternativa**: Esposizione a leva tramite derivati (opzioni **Call e Put**), sfruttando il fatto che ogni contratto di opzione controlla 100 quote del sottostante con un esborso di premio limitato.
- **Strategia di implementazione**:
  1. *Fase 1*: Avviare il sistema in modalità standard (equity pura, stock-only) senza alcuna leva per verificarne l'efficacia e stabilizzare i modelli.
  2. *Fase 2*: Inserire l'operatività in leva solo in corrispondenza di rating di forte convinzione del sistema, ovvero segnali di tipo **Strong Buy** o **Strong Sell**. In questi casi, il modulo/nodo esecutore preposto potrà scegliere di acquistare opzioni (Call per Strong Buy, Put per Strong Sell) invece di acquistare il titolo sottostante direttamente. L'attribuzione di quale specifico agente debba determinare o validare questa forte convinzione è rimandata alla mappatura delle funzioni nel grafo di LangGraph.

---

## 3. Modello di Business e Monetizzazione

### Filosofia Open Source
- Il codice sorgente del progetto rimarrà ospitato in modalità **open source** su GitHub.
- Questa scelta è di vitale importanza per Luca: avendo deciso di cambiare indirizzo di carriera alla fine della sua laurea triennale senza intraprendere un secondo ciclo triennale, ha la necessità assoluta di costruire un **portfolio progetti solido e visibile** da presentare ai datori di lavoro per dimostrare le proprie competenze pratiche di sviluppo e AI engineering.

### Il Modello "Piero" & Friends Performance Fee
- Nonostante il codice sia pubblico (chi ha le competenze tecniche può installarselo e farlo girare in autonomia), il team monetizzerà offrendo il servizio in modalità gestita:
  - Creazione di un sito web pubblico che mostri in tempo reale le performance reali del wealth manager AI, battezzato ironicamente **"Piero"** (*Piero, il tuo wealth manager personale*).
  - Offerta di gestione fondi rivolta ad una cerchia ristretta di contatti e amici personali ("molto easy"), senza newsletter o promozioni pubbliche sui social per evitare gravosi adempimenti legali e burocratici (es. profilazione MiFID complessa richiesta per i fondi aperti al pubblico).
  - Gestione regolata tramite un **contratto privato firmato con clausole di scarico di responsabilità**, informando chiaramente i partecipanti sulla natura rischiosa degli investimenti.
  - Applicazione di una commissione di performance (*performance fee*) del **1% calcolata esclusivamente sui profitti generati** (non sul totale del portafoglio). Luca specifica: *"se l'investimento passa da 100 a 103 euro guadagnandone 3, la nostra percentuale dell'1% si applica sui 3 euro di rendimento, non sui 103 totali"*.
- L'obiettivo finale di lungo termine è creare una **rendita passiva costante e consistente** anziché puntare a un'exit tradizionale di vendita del software (di cui a Salvatore non interessa). Se le performance storiche dovessero dimostrarsi eccezionali e battere sistematicamente indici come l'S&P 500, non è esclusa la privatizzazione immediata del codice o una proposta di acquisto ad altissime cifre da parte di istituzioni come JPMorgan o Goldman Sachs.

---

## 4. Infrastruttura API LLM & Costi Operativi

### Token Cost Estimator come Commissione
- L'utilizzo degli LLM (tramite il provider **OpenRouter**) comporta costi legati al consumo di token.
- Viene concordata la necessità di progettare un **modulo stimatore dei costi dei token** (calcolo dei token consumati e conversione in dollari/euro).
- Dal punto di vista del Risk Management, il costo dei token LLM deve essere trattato **al pari delle commissioni operative del broker** su ciascun trade. L'impatto economico dell'invocazione degli agenti deve essere integrato nel calcolo del rendimento netto.
- **Auto-finanziamento delle API**: Un obiettivo di automazione avanzata prevede che il sistema sia in grado di prelevare autonomamente parte dei profitti realizzati sul conto trading per ricaricare in automatico il saldo crediti su OpenRouter, mantenendo l'infrastruttura AI autosufficiente.

---

## 5. Frequenza Operativa e Checkpoint Temporali

### Frequenza Swing
- Si conferma un'operatività di tipo swing trading con orizzonti medio-brevi: nessuna transazione ad alta frequenza (HFT), ma neanche una singola operazione al mese. Il target ottimale prevede transazioni in grado di coprire l'operatività settimanale o su archi di 3, 5 giorni.
- **Temporal Checkpoint dinamico**: Sarà lo stesso LLM Trader ad autocontrollarsi e autolimitarsi temporalmente. Nell'output JSON strutturato, oltre ai target di prezzo, l'AI definirà in modo flessibile il prossimo checkpoint temporale per la verifica dello stato (es. *"ricontrolliamo questa posizione domani"* oppure *"prossimo check tra una settimana"*), adattandosi dinamicamente al mutare delle condizioni di mercato.
