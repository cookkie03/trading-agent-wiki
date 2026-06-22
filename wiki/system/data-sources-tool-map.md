---
title: "Data Sources & Tool Map"
type: build
tags:
  - infrastructure
  - software
  - architecture
created: 2026-06-23
updated: 2026-06-23
status: active
confidence: medium
area: software
related:
  - "[[system/tools-inventory]]"
  - "[[system/data-providers]]"
  - "[[system/modules/data-layer]]"
  - "[[artifacts/project-board]]"
---

# Data Sources & Tool Map

Pagina di raccordo tra vendor, wrapper e tool. Nasce dai commenti di Luca: manca ancora un posto unico dove definire **fonti dati**, **insieme dei tool disponibili su ogni fonte** e il confine tra extraction, normalization e agent tools.

## Domande a cui deve rispondere

- Quali vendor o librerie coprono prezzi, news, fundamentals, macro, social, options, broker state?
- Quale wrapper interno standardizza ogni fonte?
- Quali tool espone poi il sistema agli agenti o ai moduli deterministici?
- Cosa resta live, cosa va in DB-first, cosa diventa cache o materialized view?

## Direzione proposta

- **Vendor wrapper layer**: un adapter per ogni sorgente esterna, con output normalizzato.
- **Tool layer**: tool stabili che usano i wrapper e nascondono all'agente i dettagli del vendor.
- **Capability layer**: calcoli deterministici composti su dati normalizzati.
- **Storage layer**: repository e tables che preservano dato grezzo, derivati e storico.

## Backlog collegato

- Studiare OpenBB come possibile meta-provider / research platform.
- Studiare FinRL come riferimento per moduli RL o workflow quant sperimentali.
- Continuare il crawl di `optimizer`, `datapizza-ai`, `TradingAgents`, `Rizzo`, `SFC` e altri prior-art.
- Esplicitare per ogni fonte le policy di dedup, retention e freshness.

## Stato

Documento seed. Va consolidato leggendo `[[system/tools-inventory]]`, `[[system/data-providers]]` e i prior-art già presenti in `wiki/prior-art/`.
