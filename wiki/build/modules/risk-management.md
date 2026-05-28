---
title: "Risk Management"
type: build
tags:
  - build
  - software
  - strategy
created: 2026-05-13
updated: 2026-05-27
status: active
priority: low
area: software
related:
  - "[[build/system-map]]"
  - "[[build/modules/llm-agent-system]]"
  - "[[build/decision-log]]"
---

# Risk Management

Il guardiano del rischio. Opera **upstream** del Trader: imposta i paletti dinamici per il ciclo corrente prima che il Trader prenda qualsiasi decisione. Il Trader decide dentro quello spazio, non viene corretto fuori da esso.

---

## Lo Statuto del Fondo (Institutional-Grade)

Il Risk Management non si limita a produrre paletti dinamici, ma applica a monte lo **Statuto del Fondo**:
- **Natura**: Un insieme generico e rigoroso di regole deterministiche scritte in codice Python puro (nessun LLM coinvolto per garantire rigidità matematica).
- **Obiettivo**: Emulare gli statuti di rischio dei grandi investitori istituzionali reali per eliminare bias cognitivi, emotivi e operativi.
- **Regole Cardine**:
  1. **Riserva di Liquidità del 10%**: Il sistema impone deterministicamente di mantenere almeno il **10% del valore del portafoglio sempre disinvestito** in cash puro. Questa quota è considerata riserva strategica per far fronte alla volatilità o per finanziare opportunità eccezionali sottoprezzate, e non può essere intaccata nelle allocazioni ordinarie.
  2. **Meccanismo di Vendita/Disinvestimento**: Se l'agente identifica una nuova opportunità ad altissima convinzione ma il portafoglio è allocato al 90% (massimo consentito dallo statuto), viene attivato un modulo deterministico per valutare se disinvestire parzialmente o totalmente da un asset già in portafoglio, calcolando la forza relativa dei segnali per liberare liquidità.
  3. **Leva su Strong Signals**: L'operatività in leva (esclusivamente tramite acquisto di opzioni Call/Put) è permessa solo su rating `Strong Buy` o `Strong Sell` determinati e validati all'interno del sistema (indipendentemente da quale specifico agente esegua il calcolo della convinzione).

---

## LLM Token Cost Estimator

Ogni chiamata LLM (tramite provider **OpenRouter**) ha un costo variabile in token. Il Risk Management integra un modulo dedicato per il calcolo di questa voce di spesa:
- **Trattamento Economico**: I costi dei token (convertiti da token in dollari/euro in base al modello utilizzato) sono equiparati alle **commissioni di transazione del broker** (come Alpaca o Interactive Brokers).
- **Net Performance**: Ogni trade proposto deve sottrarre dal profitto atteso sia le commissioni del broker sia il costo stimato dei token consumati dagli agenti per quel ciclo decisionale.
- **Auto-finanziamento (Prospettiva)**: In fase avanzata, il sistema preleverà automaticamente parte dei profitti realizzati per ricaricare il saldo crediti su OpenRouter.

---

## Cosa fa

Ogni ciclo, prima del Prompt Builder:

1. Legge lo **stato corrente del portafoglio** (esposizione, liquidità, drawdown corrente, rispetto dello Statuto del 10% cash)
2. Legge lo **stato del mercato** (volatilità, volume, segnali di regime)
3. Calcola il consumo stimato delle API e i costi di elaborazione
4. Calcola e produce un **briefing rischio** da iniettare nel prompt:
   - VaR (perdita max stimata nel periodo)
   - Esposizione massima ammessa per il ciclo corrente (nel rispetto del 90% massimo)
   - Range SL/TP ammissibili (in % del capitale)
   - Costo stimato token LLM allocato per la decisione
   - Go / No-Go per il ciclo (se le condizioni di mercato lo sconsigliano)

---

## Differenza rispetto al Security Module

| | Risk Analyst (upstream) | Security Module (downstream) |
|-|------------------------|------------------------------|
| Quando | Prima del Trader | Dopo la proposta del Trader |
| Cosa fa | Imposta i paletti dinamici | Valida la proposta contro i paletti fissi |
| Natura | Contestuale (cambia ogni ciclo) | Deterministico (regole fisse — statuto del fondo) |
| Implementazione | LLM o algoritmo | Python puro, no LLM |

---

## Decisioni aperte

- **Cash-out strategy**: quale % dei profitti viene estratta periodicamente? Deve essere codificata come regola dello statuto del fondo.
- **Regole specifiche del portafoglio (statuto)**: max esposizione per asset class, regola +100% → vendi e porta a casa, max drawdown tollerato prima di stop definitivo del sistema.
- **Meccanismo di disinvestimento ottimale**: come calcolare deterministicamente quale asset vendere in favore del nuovo acquisto.
- **Regime detection**: in futuro, usare HMM per adattare la metrica di rischio al regime (varianza in bull, CVaR in bear). Post-MVP avanzato.

---

## Dipendenze

- Legge da: `portfolio_state`, `market_data`
- Scrive in: `module_outputs` (briefing rischio per il Prompt Builder)
- Il Prompt Builder lo include come sezione dedicata nel prompt del Trader

---

## Librerie candidate (post-MVP)

- **cvx-portfolio-optimizer** (skfolio): gestisce Black-Litterman, Entropy Pooling, CVaR, regime detection via HMM. Vedere [[references/external/cvx-portfolio-optimizer]].
