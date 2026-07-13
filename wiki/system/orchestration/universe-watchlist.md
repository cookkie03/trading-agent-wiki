---
title: "Universo investibile, Watchlist dinamica, Gerarchia agenti"
type: build
tags:
  - architecture
  - multi-agent
  - software
created: 2026-06-08
updated: 2026-07-13
status: active
priority: high
area: software
related:
  - "[[system/agents/agents]]"
  - "[[system/orchestration/parallelism-design]]"
  - "[[strategy/metrics/benchmark]]"
  - "[[system/data/data-layer]]"
  - "[[system/_reference/canvas-code-mapping]]"
confidence: high
---

# Universo investibile, Watchlist dinamica, Gerarchia agenti

> **Design attivo:** universo, watchlist e portafoglio sono insiemi distinti. Il benchmark dinamico è esplicitamente **Post-MVP**; questa pagina non attesta implementazioni nel repository esterno.

## Modello a tre insiemi concentrici

```
UNIVERSO   = tutti i tradable del broker, conosciuti + riconciliati periodicamente   (catalogo, righe economiche)
   ⊇  WATCHLIST = sottoinsieme DINAMICO sotto analisi, gestito dagli agent             (working set, analisi costosa)
        ⊇  PORTFOLIO = asset posseduti                                                  (gestione uscite)
BENCHMARK  = opzionale Post-MVP; per l'MVP non guida il processo decisionale
```

L'efficienza: ingestione/deep-dive costosi solo su **watchlist + portfolio + triggerati**; il resto dell'universo è catalogo a costo ~0. Una news/alert su un asset fuori watchlist può farlo **entrare** (dinamicità).

## Universo + riconciliazione
- Il catalogo del broker definisce il perimetro tradable e marca inattivi gli asset non più offerti.
- Un seed di mercato può inizializzare l'universo, ma non è hardcoded né sostituisce il catalogo broker.
- La riconciliazione ha una cadenza configurabile e separata dal deep-dive agentico.

## Watchlist dinamica (membership ibrida)
- **Seed** iniziale = paniere di mercato ∩ broker-tradable.
- **Entra**: candidati deterministici (screening/alert/news); una fonte rilevante può proporre l'ingresso in watchlist.
- La scheda ticker è il hub DB-first: screening, ultima valutazione, membership e date alimentano i trigger.

## Benchmark — Post-MVP

L'MVP opera senza benchmark dinamico. La futura versione potrà confrontare rendimento e alpha con indici configurabili o con una soglia fissa; prima andranno decisi frequenza di calcolo, visibilità al PM e uso effettivo nel processo decisionale.

## Gerarchia agenti (tre livelli)
```
DIRETTORE (Portfolio Manager, uno) — decide cosa analizzare, gestisce watchlist,
   fa fan-out parallelo, decisione di portafoglio + Statuto di portafoglio
      ▼
VALUTATORE (uno per titolo, in parallelo) = brain per-ticker (analyze_symbol)
   coordina i desk → tesi del titolo
      ▼
DESK: Market · Sentiment · Technical · Fondamentali
+ RISK ANALYST = ruolo DISTINTO su DUE livelli:
   - singolo titolo: bear + Statuto del titolo (dentro l'Evaluator)
   - portafoglio: `admit_within_statute` (riserva 10% cassa, VaR totale, settore)
     + giudizio finale del Risk sull'intero book (estendibile)
```
Il Risk Analyst resta una figura distinta. Il suo posizionamento definitivo — desk pari, gate finale o combinazione a due livelli — resta una decisione condivisa da chiudere in board.

## Parallelismo
I Valutatori possono lavorare in parallelo per ticker, entro limiti configurabili e con esecuzione degli ordini seriale. I subgraph LangGraph per ticker restano il pattern di isolamento; la scelta concreta di concorrenza appartiene al repository esterno.

## Riferimento da studiare
**"hermes agent"** (full Python) — segnalato da Luca come riferimento per principi di autonomia/dinamicità/versatilità degli agent generalisti. Da verificare e approfondire (non assunto).
