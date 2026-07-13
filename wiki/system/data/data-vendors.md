---
title: "Data Vendors & Coverage Policy"
type: build
tags:
  - infrastructure
  - architecture
  - roadmap
created: 2026-07-13
updated: 2026-07-13
status: active
related:
  - "[[system/data/data-sources-tool-map]]"
  - "[[system/tools/tools-inventory]]"
  - "[[artifacts/tool-catalog.base]]"
  - "[[artifacts/project-board]]"
confidence: medium
area: software
---

# Data Vendors & Coverage Policy

Questa pagina separa la scelta di una **capacità** dalla scelta del suo provider. Il catalogo parte da OpenBB per esplorare copertura e integrazioni, ma il sistema mantiene wrapper interni e fallback: nessun agente o specifica dipende direttamente da un vendor.

## Politica emersa dai commenti

1. **OpenBB-first per catalogazione e ricerca**: mappare ciò che l'aggregatore già espone prima di inventare tool paralleli.
2. **Broker-first per dati di conto e, quando disponibili, prezzi real-time via WebSocket**: Alpaca/IBKR sono fonti naturali di posizioni, cash, ordini e quote live; non sono l'unica fonte possibile.
3. **Multi-vendor per copertura e fallback**: per ogni capacità servono provider candidati, limiti, costo, freshness, licenza, chiave dedup e test con risposta finta.
4. **Persistenza con provenienza**: il dato estratto, calcolato o dedotto conserva fonte, data di raccolta, data di riferimento e politica di retention. Documenti pesanti possono stare in object/raw storage con metadata e derivati indicizzati; non si presume che ogni PDF debba essere duplicato in una tabella relazionale.

## Capacità da valutare

| Capacità | Primaria da valutare | Fallback/candidati | Decisione ancora aperta |
| --- | --- | --- | --- |
| Quote e OHLCV | broker WebSocket / OpenBB | yfinance, Twelve Data, Alpha Vantage | fonte MVP e limiti di freshness |
| Fondamentali e rapporti | OpenBB | provider broker, Alpha Vantage, yfinance | qualità, copertura e calendario di refresh |
| Macro | FRED via wrapper/OpenBB | fonti calendario macro | schema di normalizzazione |
| News e sentiment | OpenBB + fonti specializzate | broker/news vendor, StockTwits, Reddit, X | fonti consentite e metodo di aggregazione |
| Calendario | OpenBB / provider dedicati | broker, fonti macro | priorità e affidabilità eventi |
| Opzioni | IBKR / OpenBB se coperto | Tradier e altri candidati | fuori MVP |

La vista operativa è [[artifacts/tool-catalog.base]]; [[system/tools/tools-inventory]] definisce cosa espone il sistema, non quale SDK deve usare.

