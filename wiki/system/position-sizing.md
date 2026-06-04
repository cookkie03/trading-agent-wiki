---
title: "Position Sizing — dimensionamento delle posizioni"
type: build
tags:
  - build
  - strategy
  - execution
created: 2026-06-03
updated: 2026-06-03
status: draft
priority: high
area: software
related:
  - "[[system/state-schemas]]"
  - "[[system/modules/execution]]"
  - "[[system/modules/agents]]"
  - "[[system/rating-scoring]]"
confidence: medium
---

# Position Sizing

> Come si decide **quanto** comprare/vendere. È il secondo deliverable concordato con Luca, subito dopo lo [[system/state-schemas]]. Il `position_sizing` è un campo dello state da cui la funzione Trade deterministica estrae l'ordine.

---

## Principio cardine (deciso)

**Sempre relativo al portafoglio, mai valori assoluti** (Luca, call 2026-06-02). Non «compra 1000€ di AAPL» ma «alloca il 4% del portafoglio su AAPL». Questo rende il sizing:
- indipendente dalla dimensione del capitale (scala da [[_meta/glossario#Paper Trading / Testnet|paper trading]] a reale);
- coerente con lo Statuto (riserva 10% cash, % max per asset/settore);
- testabile in backtest senza riscrivere nulla.

---

## Idea concordata: sizing scalato per conviction

Far dipendere la dimensione dal **`conviction_level`** dello state (Luca: *«l'idea di farlo dipendere da un [[_meta/glossario#Conviction Level|conviction level]] è molto valida»*). Logica di massima:

```
size_% = base_weight × conviction_multiplier
         (poi cappato dai vincoli di Statuto: max % per titolo/settore, riserva 10% cash)
```

- `base_weight`: peso "neutro" di una posizione tipica (es. 1/N dell'universo target).
- `conviction_multiplier`: cresce con la convinzione (es. Hold→0, Buy→1×, Strong Buy→1.5× + sblocco leva via opzioni).
- **Cap deterministici** applicati dopo: lo Statuto taglia qualsiasi size che violi [[_meta/glossario#VaR (Value at Risk)|VaR]], % max per area/settore, riserva cash. Vedi guardrail in [[system/modules/agents]].

---

## Kelly Criterion (richiesto da Luca — spiegazione)

> Luca: *«cos'è il [[_meta/glossario#Kelly Criterion|Kelly]] criterion? Aggiungilo alla wiki»*.

Il **Kelly Criterion** è una formula matematica che dice **quale frazione del capitale puntare** su una scommessa per **massimizzare la crescita del capitale nel lungo periodo**, dato che conosci (o stimi) probabilità di vincita e rapporto vincita/perdita.

Formula base (scommessa binaria):
```
f* = p − q/b
```
- `f*` = frazione ottima del capitale da puntare
- `p` = probabilità di vincere
- `q = 1 − p` = probabilità di perdere
- `b` = rapporto vincita/perdita (quanto guadagni per unità rischiata)

**Esempio**: se hai il 60% di probabilità di vincere (`p=0.6`) e guadagni quanto rischi (`b=1`): `f* = 0.6 − 0.4/1 = 0.20` → punta il 20% del capitale.

**Perché ci interessa**: lega la **dimensione della posizione alla qualità del segnale** (probabilità + payoff), esattamente la logica «più convinzione → più size» che vogliamo. Il `conviction_level` e lo storico win-rate degli agenti ([[system/rating-scoring]]) sono i candidati naturali per stimare `p` e `b`.

**Cautele (importanti, da considerare nel design)**:
- Kelly puro è **molto aggressivo**: in pratica si usa **frazionario** (es. *half-Kelly*, metà del valore) perché stimare male `p` porta a sovraesposizione e [[_meta/glossario#Drawdown|drawdown]] pesanti.
- Richiede **stime affidabili** di `p` e `b` — che all'inizio non avremo (no storico). → Kelly è un **obiettivo evolutivo**, non per la prima alpha: si parte con sizing % fisso scalato per conviction, si introduce Kelly frazionario quando c'è storico sufficiente per stimare le probabilità.

---

## Approccio incrementale (coerente con la filosofia di progetto)

Allineato al principio di Luca *«prima un software con un'idea base, poi mano a mano aggiungere pezzi»*:

1. **v0 (prima alpha)**: sizing % fisso (es. peso uguale 1/N), cap da Statuto. Semplice, parte subito.
2. **v1**: sizing scalato per `conviction_level` (multiplier discreto).
3. **v2**: sizing volatility-adjusted (size inversamente proporzionale alla volatilità del titolo, es. via [[_meta/glossario#ATR (Average True Range)|ATR]] — più volatile = posizione più piccola a parità di rischio).
4. **v3**: Kelly frazionario, quando lo storico permette di stimare `p` e `b` per agente/strategia.

---

## Punti aperti

- Valore esatto di `base_weight` e dei moltiplicatori per livello di convinzione.
- Se e quando introdurre il volatility-adjustment (lega al VaR → da capire con Salvatore, vedi [[strategy/questions-for-salvatore]]).
- Interazione sizing ↔ leva via opzioni: il sizing di un'opzione è diverso da quello dell'equity spot (vedi [[system/modules/execution]]).

---

*Il campo vive in [[system/state-schemas]]; lo consuma la funzione Trade in [[system/modules/execution]]; i cap derivano dallo Statuto in [[system/modules/agents]].*
