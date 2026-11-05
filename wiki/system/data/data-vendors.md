---
title: Data Vendors & Coverage Policy
type: build
tags:
  - data-vendors
  - coverage-policy
  - infrastructure
  - architecture
created: 2026-07-13T00:00:00.000Z
updated: 2026-07-13T00:00:00.000Z
status: active
related:
  - '[[system/data/data-sources-tool-map]]'
  - '[[system/tools/tools-inventory]]'
  - '[[artifacts/tool-catalog.base]]'
  - '[[artifacts/project-board]]'
confidence: medium
area: software
---

# Data Vendors & Coverage Policy

Questa pagina separa la scelta di una **capacità** dalla scelta del suo provider. Il sistema mantiene wrapper interni indipendenti dai vendor; la policy di fallback multi-provider resta da definire.

### Chiarimento di Luca — 2026-11-04

OpenBB SDK è il percorso principale per i dati di mercato, non Yahoo diretto prioritario; Alpaca è la fonte dei dati di portafoglio (conto, posizioni e ordini). OpenBB è un'interfaccia di accesso, distinta dal provider effettivo sottostante, da tracciare nella provenance: non è stata decisa l'esclusività di alcun provider. Adapter diretti restano possibili; selezione e comportamento del fallback sono ancora aperti.

### Decisione implementativa — 2026-10-31

Luca ha scelto di iniziare con un'architettura ibrida: OpenBB è il primo vendor operativo per la raccolta dati, mentre gli adapter diretti restano percorsi reali e sostituibili. Nel repository il seam è `MarketDataProvider`; `OpenBBProvider` normalizza verso i modelli propri e conserva il provider sottostante nella provenance, senza esporre namespace OpenBB al resto del sistema. Questo consente di spostarsi da OpenBB a un adapter diretto senza riscrivere storage, capability o agenti.

**Stato verificato:** OpenBB 4.6.0 è installato nell'ambiente del progetto il 2026-10-31. `OpenBBProvider` implementa OHLCV e fundamentals via yfinance e serie macro via FRED; le prove reali su AAPL e GDP sono riuscite (319 osservazioni GDP). La suite conta 44 test passati e 1 skipped; l'adapter conserva il provider sottostante nella provenance e non espone tipi OpenBB. La ricerca Alpaca come vendor dati è stata completata su fonti ufficiali e salvata in `docs/research/alpaca-data-vendor.md`; `AlpacaMarketDataProvider` implementa OHLCV storico equities con feed esplicito e provenance. News, corporate actions, options e crypto restano capability separate da progettare.

## Policy MVP di freshness e retention — 2026-10-31

Per l'OHLCV storico del primo flusso OpenBB:

- `collected_at` è l'evidenza temporale della raccolta; non equivale a un feed live e non introduce uno SLA universale.
- `publication_date` e `reference_date` restano distinte per evitare look-ahead bias; quando il vendor non pubblica una data separata, il bridge usa rispettivamente `collected_at` e `timestamp` come fallback espliciti.
- `source` partecipa alla deduplicazione: dati uguali provenienti da provider diversi restano osservazioni distinte e tracciabili.
- Il file SQLite MVP non applica retention automatica: nessun dato viene cancellato implicitamente. Una retention futura dovrà distinguere raw payload, dati normalizzati e derivati, con un job esplicito e verificabile.
- Retry, fallback multi-provider, run ID e freshness SLA provider-specifici restano decisioni successive; non vengono dedotti dal provider selection di OpenBB.

Questa è una policy di perimetro MVP, non una garanzia di qualità o disponibilità del vendor.

## Politica emersa dai commenti

1. **OpenBB-first per catalogazione e ricerca**: mappare ciò che l'aggregatore già espone prima di inventare tool paralleli.
2. **Broker-first per dati di conto e, quando disponibili, prezzi real-time via WebSocket**: Alpaca/IBKR sono fonti naturali di posizioni, cash, ordini e quote live; non sono l'unica fonte possibile.
3. **Multi-vendor per copertura e fallback**: per ogni capacità servono provider candidati, limiti, costo, freshness, licenza, chiave dedup e test con risposta finta.
4. **Persistenza con provenienza**: il dato estratto, calcolato o dedotto conserva fonte, data di raccolta, data di riferimento e politica di retention. Documenti pesanti possono stare in object/raw storage con metadata e derivati indicizzati; non si presume che ogni PDF debba essere duplicato in una tabella relazionale.

## Capacità da valutare

| Capacità | Primaria da valutare | Fallback/candidati | Decisione ancora aperta |
| --- | --- | --- | --- |
| Quote e OHLCV | OpenBB come percorso principale | broker WebSocket, yfinance, Twelve Data, Alpha Vantage | provider effettivo, limiti di freshness e policy di fallback |
| Fondamentali e rapporti | OpenBB | provider broker, Alpha Vantage, yfinance | qualità, copertura e calendario di refresh |
| Macro | FRED via wrapper/OpenBB | fonti calendario macro | schema di normalizzazione |
| News e sentiment | OpenBB + fonti specializzate | broker/news vendor, StockTwits, Reddit, X | fonti consentite e metodo di aggregazione |
| Calendario | OpenBB / provider dedicati | broker, fonti macro | priorità e affidabilità eventi |
| Opzioni | IBKR / OpenBB se coperto | Tradier e altri candidati | fuori MVP |

La vista operativa è [[artifacts/tool-catalog.base]]; [[system/tools/tools-inventory]] definisce cosa espone il sistema, non quale SDK deve usare.

