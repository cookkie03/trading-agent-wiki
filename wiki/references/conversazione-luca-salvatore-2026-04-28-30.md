---
title: "Conversazione progettuale Luca-Salvatore (2026-04-28 / 2026-04-30)"
type: source
tags:
  - source
  - ingest
  - strategy
raw_source_path: "raw/archived/conversazione-luca-salvatore-2026-04-28-30/"
created: 2026-04-30
updated: 2026-04-30
confidence: medium
status: reviewed
related:
  - "[[build/system-map]]"
  - "[[ops/current-state]]"
  - "[[theory/modular-trading-agent-architecture]]"
  - "[[theory/trader-workflow-automation]]"
  - "[[questions/open-questions]]"
---

# Conversazione progettuale Luca-Salvatore (2026-04-28 / 2026-04-30)

Bundle di audio, trascrizioni e appunti relativi alle prime discussioni sul progetto `trading-agent`.

## Contesto

La conversazione ruota attorno a:

- architettura del sistema
- mercato target iniziale
- livello di autonomia desiderato
- modularità e possibilità di estensione
- rapporto tra ricerca, backtesting, news, sentiment e operatività

Sono state escluse le parti strettamente personali e scollegate dal progetto.

## Key takeaways

- L'idea centrale è costruire un sistema che replichi e aumenti il workflow di un trader, non solo un bot che prende ordini in automatico.
- La modularità è stata indicata come requisito fondamentale: l'architettura deve permettere di aggiungere, sostituire e ripesare moduli nel tempo.
- È emerso un confronto forte tra `crypto` ed `equity` come mercato iniziale.
- `Equity` appare più spiegabile economicamente, ma più complesso da modellare.
- `Crypto` appare più semplice lato accesso ai dati e infrastruttura, ma più debole lato razionalità economica e valutazione.
- Il progetto dovrebbe includere strumenti di supporto come backtesting, raccolta news, analisi dei pattern passati, stime di costo, gestione leva, portfolio management e monitoraggio delle operazioni.
- È stata proposta anche una dashboard operativa che aiuti a trasformare idee di strategia in test e valutazioni più velocemente.
- Prima del coding serio serve ricerca: capire se esistono metriche o approcci affidabili, soprattutto per le crypto.

## Tensioni progettuali emerse

### 1. Agente autonomo vs. piattaforma di augmentazione

Una tensione centrale è se il progetto debba partire come:

- agente continuo/autonomo che riceve periodicamente contesto e usa tool
- piattaforma o dashboard che aumenta il lavoro umano di un trader

La conversazione suggerisce che la seconda strada possa essere una fase iniziale più realistica e utile.

### 2. Crypto vs. equity

La discussione non chiude la scelta:

- `crypto` è più accessibile, più semplice sul piano operativo, ma più difficile da giustificare economicamente
- `equity` è più spiegabile e potenzialmente più ricca per analisi causale/sentiment, ma molto più complessa

### 3. Modello numerico vs. modello di sentiment

È emersa una distinzione importante:

- predire il prezzo puntuale può essere poco realistico
- capire direzione e sentiment di mercato può essere più interessante

## Moduli e capacità nominati

- news scraping
- individuazione di volumi anomali o opportunità
- backtesting automatico
- analisi tecnica o equivalente
- gestione stop loss / take profit
- gestione leva
- stime costi e commissioni
- portfolio management
- logging completo delle operazioni e dei prompt
- sistema di pesi o auto-miglioramento dei moduli
- memoria o prompt periodico dell'agente
- pattern matching con situazioni passate

## Impatto sul progetto

Questa conversazione definisce il primo spazio di progettazione del vault:

- cosa deve fare il sistema
- quali tradeoff vanno affrontati
- dove servono ricerca e validazione
- perché la modularità deve essere una priorità di primo livello
