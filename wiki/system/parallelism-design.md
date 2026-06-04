---
title: "Parallelismo & Orchestrazione multi-ticker"
type: build
tags:
  - build
  - architecture
  - multi-agent
created: 2026-06-03
updated: 2026-06-04
status: draft
priority: high
area: software
related:
  - "[[system/modules/agents]]"
  - "[[system/state-schemas]]"
  - "[[system/architecture]]"
  - "[[system/rating-scoring]]"
confidence: low
---

# Parallelismo & Orchestrazione multi-ticker

> Come fa il Portfolio Manager a far analizzare **più ticker** senza che gli state si mescolino e senza saturare il contesto degli agenti. Tema aperto importante (Luca: *«ci sono diverse alternative da valutare, anche con Salvatore»*). Qui le due idee di Luca + alternative aggiunte. Da decidere in fase di engineering del grafo.

---

## Il problema

Il PM orchestratore deve poter valutare N ticker (es. tutto l'universo S&P investibile). Ogni ticker ha il suo `research_state` ([[system/state-schemas]]). Vincoli:
- **isolamento**: lo state di AAPL non deve contaminare quello di MSFT;
- **context rot**: non si può mettere tutto nello stesso contesto di un agente (degrado oltre ~50-60%);
- **rate limit**: gli extractor non possono essere chiamati in parallelo senza coordinamento (vedi [[system/modules/data-layer]]);
- **costo token**: ogni ciclo agente costa (equiparato a commissione).

---

## Alternativa A — Layer di "valutatori" per ticker (idea di Luca)

Inserire un **layer intermedio** tra PM e desk analisti.

```
Portfolio Manager
  ├─► Valutatore(AAPL)  ─► desk analisti (thread separato) ─► research_state(AAPL)
  ├─► Valutatore(MSFT)  ─► desk analisti (thread separato) ─► research_state(MSFT)
  └─► Valutatore(...)   ─► ...
```

- Il PM chiama **quanti valutatori vuole**, uno per ticker da analizzare.
- Ogni valutatore esegue i desk analisti in un **thread separato** → isolamento naturale degli state, parallelismo reale.
- **Pro**: scala bene, ogni ticker ha contesto pulito, parallelizzabile.
- **Contro**: costo token moltiplicato per N; serve un meccanismo per decidere *quali* ticker valutare (non tutti, ogni volta).
- **In LangGraph**: pattern *map* / [[_meta/glossario#Subgraph (LangGraph)|subgraph]] per-ticker con state isolato (checkpointing per-ticker, già previsto nello stack).

---

## Alternativa B — Scheda ticker auto-aggiornante nel DB (idea di Luca)

Un **DB sempre aggiornato** dove ogni ticker ha la sua **scheda/page** con tutte le info utili e la sua **valutazione corrente**, che si auto-aggiorna.

- Il PM non "ricalcola" tutto al volo: **legge la scheda** già pronta.
- **Pro**: latenza bassissima in lettura, info centralizzate, niente ricalcolo ridondante. Coerente con la filosofia DB-first.
- **Contro grosso (Luca: «difficile»)**: gli agenti devono **distinguere le info vecchie/obsolete/non più valide e cancellarle** quando ne arrivano di nuove che le confutano. Gestione della *staleness* e delle contraddizioni è un problema non banale (legato a `publication_date`/`reference_date` e al RAG news).
- **Mitigazioni proposte**: ogni fatto nella scheda ha una data e una *confidence*; un processo (mantainer/quant) marca come stale ciò che supera una soglia temporale o è contraddetto da un fatto più recente; gli agenti leggono solo fatti "freschi".

---

## Alternative aggiunte (proposte da valutare)

### C — Ibrido A+B (consigliata come direzione)
Scheda ticker nel DB (B) come **cache/stato persistente**, ma quando il PM decide di approfondire un ticker lancia un **valutatore** (A) che aggiorna la scheda. Il deep-dive a thread separato si attiva solo su trigger (alert o periodical synthesis), il resto del tempo le schede vivono di aggiornamenti incrementali leggeri (extractor + mantainer). Unisce latenza bassa (lettura scheda) e isolamento (thread on-demand).

### D — Coda di priorità invece di "tutti i ticker"
Il PM non valuta N ticker in parallelo ma mantiene una **coda prioritizzata**: i ticker entrano in coda quando un alert li segnala (prezzo anomalo, news, trimestrale imminente) o quando lo `next_check_date` scade. Si processano i primi K per ciclo. Risolve il "quali ticker valutare" e tiene sotto controllo costo/rate-limit. Combinabile con A o C.

### E — Due livelli di profondità (screening → deep dive)
Uno **screening** economico e veloce (modello piccolo / calcolo deterministico) gira su tutto l'universo e produce solo un punteggio grezzo; solo i ticker che superano una soglia ricevono il **deep dive** dei desk (costoso). Pattern *[[_meta/glossario#Quick Thinker + Deep Thinker|Quick Thinker]] + Deep Thinker* (vedi [[_meta/glossario]]). Riduce drasticamente il costo.

---

## Subgraph: uso granulare (direzione decisa 2026-06-03)

Luca: *«ottima la divisione in sub-grafi, utilizziamoli in maniera granulare anche per collegare parti diverse del sistema»*. → I **subgraph diventano un pattern strutturale di base**, non solo per il fan-out multi-ticker:
- ogni **desk** (Research, Technical) è un subgraph con il proprio state isolato;
- ogni **ticker** in analisi è un subgraph (parallelismo + isolamento);
- aree funzionali distinte (origination, monitoring, execution-prep) si collegano tra loro come subgraph componibili.

Vantaggio: ogni parte ha contesto pulito (anti context-rot), è testabile in isolamento e restituisce al grafo padre solo il risultato sintetico. Differenza pratica in LangGraph:
- **Nodi nello stesso grafo**: unico state globale. Semplice ma, sul multi-ticker, mescola gli state e gonfia il contesto.
- **Subgraph (grafo annidato)**: sotto-grafo con state isolato → da preferire per collegare parti diverse del sistema e per il fan-out (pattern *map*).

---

## Collegato: criteri di "informazioni sufficienti" del PM

Il PM è un agente che decide autonomamente quando *«ho info sufficienti»* per fare/non fare un trade. Serve evitare che giri in loop all'infinito chiamando tool (Luca: *«è necessario valutare quando si può dire di voler fare un trade o meno»*). Idee da discutere con Salvatore:
- **Soglia di convinzione minima**: trade solo se `conviction_level` supera X e il Risk Analyst approva (~60-70%).
- **Budget di iterazioni/token per ciclo**: tetto massimo di chiamate agli analisti; oltre il tetto, decide con ciò che ha o passa (no trade).
- **Stabilità della tesi**: se due interrogazioni successive degli analisti non cambiano la tesi → informazione satura, si decide.
- **Completezza dello state**: il gate di completezza ([[system/state-schemas]]) è già un criterio minimo necessario.

### Bias "nel dubbio, chiedi sempre" (istruzione di system prompt — input di Luca 2026-06-04)
Siccome **il PM è il decisore finale**, il suo system prompt deve istruirlo a **non decidere mai su un'indecisione o un dubbio**: ogni volta che è incerto — *anche sulle piccolezze* — deve **interrogare di nuovo i desk** per ulteriori informazioni, **sempre**, prima di chiudere la tesi. Default verso l'**approfondimento**, non verso il "decido con quel che ho".

Equilibrio con l'anti-loop: i tetti sopra (budget iterazioni, stabilità tesi) sono una **rete di sicurezza per non andare all'infinito**, *non* una scusa per decidere su informazione parziale. Ordine di priorità: **prima chiarisci il dubbio chiedendo ai desk**, e solo quando il dubbio è *davvero* irrisolvibile entro il budget → allora decidi con ciò che hai o **scegli il no-trade** (l'astensione è sempre un'opzione lecita e preferibile a un trade su basi incerte). → istruzione da formalizzare nel system prompt, vedi [[system/modules/agents]].

---

*Tracciato in [[artifacts/project-board]] come decisione da prendere con Salvatore. Vedi [[system/modules/agents]] per il ruolo del PM.*
