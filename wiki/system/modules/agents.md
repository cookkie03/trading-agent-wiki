---
title: "Agents — Portfolio Manager, Desk analisti, Risk Analyst"
type: build
tags:
  - build
  - multi-agent
  - architecture
created: 2026-05-13
updated: 2026-05-29
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

Il cuore di ragionamento del sistema: gli agenti LLM che producono la tesi di investimento (`research_state`) e la sottopongono al gate del rischio. Mappa il gruppo **desk (workflow)** di `architettura.canvas` più il nodo **Portfolio Manager**. La conversione finale in trade è deterministica e vive in [[system/modules/execution]].

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

- **Prompt Builder + LLM JSON strict**: [[prior-art/libraries/rizzo-trading-agent]] — `main.py` assembla il contesto multi-sorgente con tag XML (`<indicatori>`, `<news>`, `<sentiment>`, `<forecast>`) iniettato in `system_prompt.txt`; `trading_agent.py` usa Structured Output JSON Schema **strict** (template del nostro contratto decisione→ordine), con regole anti-overtrading e attenzione ai costi.
- **LLM → views (Black-Litterman)**: [[prior-art/libraries/cvx-portfolio-optimizer]] — `api/baml_src/GenerateViews.baml`: pattern "fattori per asset → views con confidence → Idzorek alpha". L'LLM produce opinioni, la matematica decide i pesi entro i vincoli.
- **Tool ispirazione**: sezione "Data Retrieval Tools and Utilities" di [[prior-art/tradingagents/code-wiki]] (Fundamental Data, News/Insider Transactions tools).

---

## Portfolio Manager — agente orchestratore (CEO)

Il PM è un **agente LLM** con potere decisionale ed esecutivo (il "CEO" / "GOAT" del tavolo circolare): ha tool verso tutti gli agenti, li chiama come tool, e decide quando *"ho informazioni sufficienti"*. L'umano interviene solo come **override iniziale** finché il sistema non è affidabile (traiettoria augmentation → autonomy).

- **Si attiva in 2 casi**: (a) un **alert** (solo numerico/prezzo, dal calendario/target via [[system/modules/data-layer]]); (b) la **periodical synthesis** (state sintetico a intervalli fissi con rendicontazione + market). Per il resto resta libero, si attiva e orchestra: chiama agenti → li fa ragionare → genera trade → scrive nel DB.
- **Override**: news contro l'idea → cancella/ribalta la posizione.
- **Desk di origination** (i due desk analisti) chiamati dal PM come tool. Serve anche un **desk di monitoring/evaluation** che sorveglia le posizioni esistenti e rifà il processo quando le news cambiano la tesi (evita target obsoleti o posizioni di segno opposto sullo stesso titolo).

### Attivazione e mercati efficienti
Le **API funzionano solo a richiesta** (no push news). Risoluzione via **teoria dei mercati efficienti**: i prezzi riflettono le informazioni → un **prezzo anomalo** attiva il monitoring, che poi cerca la spiegazione (news, tassi). Coerente col mid-term: non serve reazione istantanea. Lo **switch di autonomia** si dà nel **system prompt**: "rendere ogni agente quanto più autonomo possibile" è il vero valore aggiunto.

---

## Desk analisti

Due desk (decisione consolidata dal canvas, chiude il dubbio "2 vs 4 agenti"):

| Desk | Agenti interni | Funzione |
|------|----------------|----------|
| **Analyst Research** | **Market** + **Sentiment** | Contesto di mercato/macro; sentiment news/social (indicatori da definire, aggrega su Market). |
| **Analyst Technical** | **Technical** + **Fondamentali (financials)** | Segnali tecnici/quantitativi → [[system/modules/quant-backtesting]]; financials e ratio (es. P/E trailing vs current), aggrega sul Technical. |

I due desk fanno un **loop di conversazione** e convergono su un `research_state`.

### `research_state` = tesi di investimento completa
Non solo l'idea, ma: `buy/hold/sell` + **target price entrata + uscita + stop loss + sizing** + pro/contro + livello di **convinzione**. Versionato (`alpha`/v1), esiti `approved`/`declined`.

> **Head of Analyst eliminato**: il moderatore anti-bias era ridondante. Gli analisti sono la tesi bullish, il Risk Analyst è l'antitesi bearish.

---

## Risk Analyst — gate bear + guardrail da Statuto

Posizionato come **gate unico** tra il `research_state` e il Trade.

- Gli analisti sono per natura **bullish**; il Risk Analyst è l'**antitesi bearish** che cerca di smontare ogni tesi. *"Quando acqua e fuoco si mettono d'accordo, la strategia è davvero buona."*
- Riceve il `research_state` e dà **`approved` / `declined` + razionale**. Se approva → si va **direttamente** a Investment State → Trade.
- **Soglia ~60-70%** (non 100%: un bear puro non approverebbe mai).
- Può **rimandare indietro con razionale**: es. *target price troppo alto* → abbassandolo la posizione rientra nel VaR (con VaR 10.000€, target 50$ vs 30$ cambiano quantità e probabilità di realizzo).

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

---

## State Management e Schemas

Obiettivo: **pochi schema potenti e dettagliati**, non tanti frammentati. Pattern da TradingAgents:
- **TypedDict** per gli state di workflow (propagati tra i nodi del grafo).
- **Pydantic** per gli output strutturati LLM (field descriptions come istruzioni).
- **Fallback a free-text** quando lo structured output fallisce (previene interruzioni del pipeline).
- **Investment State = gate di completezza**: nessun trade finché lo state non è completo (forza il passaggio per tutti i desk); reset automatico quando il blocco trade rileva la transazione.

---

## Orchestrazione e Tracciamento: LangGraph + LangSmith

- **LangGraph** orchestra i workflow multi-agente, **LangChain** definisce nodi/agenti (fork da TradingAgents). `StateGraph` (nodi = agenti, edge = logica condizionale), `ConditionalLogic` per routing dinamico, `Propagator` per inizializzare lo state, checkpointing SQLite per-ticker.
- **LangSmith (UI/CLI)** come interfaccia centrale per debug, logging, monitoring ed **evaluation**: configurare metriche e raffinare i prompt visualmente prima di consolidarli nel codice.

### Provider LLM: OpenRouter + DeepSeek V4 Pro
**OpenRouter** come router unico verso tutti i provider (agilità). **DeepSeek V4 Pro** modello principale: sul report NVDA reale (163k input + 20k output token) costa **~$0,09**, contro ~10× di Claude Sonnet 4.6. Vedi [[system/decision-log]] e [[system/stack]].

---

## Dipendenze

- Legge da: DB centrale (rendicontazione, dati live, log) → [[system/modules/data-layer]]
- Produce: `research_state` → gate Risk Analyst → Investment State → [[system/modules/execution]]
- Segnali quant per il desk Technical da [[system/modules/quant-backtesting]]

---

## TODO / Decisioni aperte

- Integrare i **Dynamic Temporal Checkpoints** nello `research_state` (l'AI definisce il prossimo check temporale).
- Dove vive l'aggregazione/validazione del segnale `Strong`.
- Valutare l'architettura **debate** del Risk (quanti agenti, quali prospettive, se mantenerla efficientata).
- Schema finale di `research_state` / `investment_state` (TypedDict + Pydantic).
- Design del **desk di monitoring/evaluation** delle posizioni esistenti.
- Ruolo esatto del nodo **`mantainer`** nel grafo.

*Vedi [[system/decision-log]] per le decisioni aperte e [[system/architecture]] per la vista d'insieme.*
