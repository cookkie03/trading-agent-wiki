---
title: "Videochiamata Luca-Salvatore (2026-05-06)"
type: source
tags:
  - source
  - ingest
  - architecture
  - analysis
  - strategy
raw_source_path: "raw/audio/Come stai tutto bene?...txt"
created: 2026-05-06
updated: 2026-05-10
confidence: high
status: reviewed
related:
  - "[[references/videochiamata-luca-salvatore-2026-04-30]]"
  - "[[build/system-map]]"
  - "[[build/system-map]]"
  - "[[build/decision-log]]"
---

# Videochiamata Luca-Salvatore (2026-05-06)

Chiamata lunga e densa. Si parte da un allineamento su come l'AI può fare Analisi Tecnica, si apre un dibattito importante su trading singolo vs portfolio bilanciato, si discute multi-asset vs solo cripto, emergono vincoli economici chiave (costo token), e il progetto assume un nuovo framing: **AI Investment Fund**.

---

## 1. Analisi Tecnica — Come la fa l'AI

- L'AI **non può leggere i grafici visivamente** in modo affidabile per fare TA seria. I trader cripto fanno TA guardando grafici e disegnando linee — questo non è direttamente replicabile.
- Approccio corretto: tradurre tutti gli indicatori TA in **funzioni Python** che producono segnali numerici (es. incrocio medie mobili → 1/0, rottura supporto → valore soglia). L'AI ragiona sui numeri, non sui grafici.
- Questo vale anche per la parte fondamentale: price-to-earning, fatturato, ratios → tutti calcolabili deterministicamente. L'LLM fa il ragionamento sui risultati, non i calcoli.

---

## 2. Correlazione tra Cripto — Multi-trade per sessione

- Le cripto sono **altamente correlate**: quando Bitcoin sale del 10%, anche Ethereum, Solana, ecc. salgono di tot.
- Il bot può aprire **più trade in parallelo** in una sessione, distribuendo su più cripto correlate.
- Il modulo di correlazione deve:
  1. Capire che le cripto sono correlate tra loro (dato macro).
  2. Usare le **news specifiche di ogni cripto** per decidere quale privilegiare o shortare all'interno del basket.
  3. Esempio: Bitcoin in trend positivo → si investe in Bitcoin + Ethereum + Solana. Ma se Solana ha una news negativa specifica → si non-investe o si shorta Solana nonostante il trend macro positivo.
- Questo porta a un sistema di **allocazione dinamica** nel basket di cripto, non solo "compro tutto".

---

## 3. Dibattito Centrale — Trading Singolo vs Portfolio Bilanciato

### Trading singolo (approccio corrente)
- Ogni trade ha entry, SL, TP definiti.
- Facile da valutare: SL = fallito, TP = successo.
- Più adatto all'intraday / breve periodo.

### Portfolio bilanciato (alternativa emersa)
- Portafoglio di asset con **ribilanciamento periodico** invece di trade singoli.
- Pro: diversificazione ("le uova non tutte in un paniere"), approccio value investing, orizzonte temporale più lungo.
- Contro: **molto più difficile da valutare** — non c'è un segnale binario chiaro di successo/fallimento come SL/TP.
- Richiede metriche di performance di portafoglio (drawdown, rendimento annuale, Sharpe ratio, ecc.).
- Esempio reale: Starting Finance ha fatto +2M su 10M in 2 anni con un approccio value investing.

### Cash-out strategy
- Da decidere a priori: quale percentuale dei profitti viene estratta periodicamente?
- Es. 10% dei guadagni viene tirato fuori, il restante 90% rimane investito come capitale.
- Questo permette di capitalizzare senza perdere il compounding effect.
- Analogia: partendo da 200€ a testa, se si arriva a 10.000€ a testa, ha senso tirare fuori 1.000€ e continuare con 9.000€ come capitale.

### Regole del portafoglio (stile statuto del fondo)
Ispirato al fondo di Starting Finance dell'università:
- **Nessuna asset class supera il 5% del portafoglio** → diversificazione forzata.
- **Quando una posizione supera il 100% di profitto → si vende** → elimina il bias di affezione.
- Queste regole vanno stabilite **a priori**, scritte come uno statuto, e implementate **deterministicamente** nel Security Module (non ragionamento LLM).
- Obiettivo: eliminare i bias cognitivi dall'esecuzione.

---

## 4. Multi-Asset vs Solo Cripto — Decisione Aperta

Salvatore porta una prospettiva forte su questo:
- **Cripto è un mondo a parte**: non correlata con equity, bond, commodity. Reagisce in modo completamente diverso al sentiment. Analizzarla richiede un approccio specializzato.
- **Asset tradizionali** (equity, ETF, bond, commodity): metodologie più consolidate, più dati disponibili in modo strutturato, react al sentiment in modo più prevedibile e studiato.
- **Proposta di Salvatore**: partire da asset tradizionali come base, poi aggiungere cripto come **side project / spin off** separato.
- **CAPM come punto di partenza**: per l'analisi equity, Salvatore suggerisce di partire dal Capital Asset Pricing Model.
- **Regola pratica**: indicatori versatili (es. volumi) funzionano su tutte le asset class; indicatori specifici cripto non si trasferiscono all'equity.
- **Criterio di scelta**: tra multi-asset e solo-cripto, scegliere quello che permette l'approccio più versatile, cioè quello i cui strumenti si trasferiscono meglio ad altri mercati.

### Posizione di Luca
- Tendenza a preferire un approccio versatile/universale.
- "Parti da quello che vuoi tu — qualsiasi informazione mi dai io troverò il modo migliore per gestirla."
- Disponibile a partire da asset tradizionali se Salvatore lo guida con la conoscenza di dominio.

---

## 5. Costo dei Token — Vincolo Architetturale Critico

Emerso durante la discussione: **anche il backtest e il demo costano token**. Questo cambia l'approccio architetturale:

### Principio deterministico
- Tutto ciò che **non richiede ragionamento** va fatto in **Python deterministico** a costo zero di token.
- Esempi: trovare il prezzo minimo tra 8 exchange, calcolare un ratio, applicare una formula, recuperare dati da un'API.
- L'LLM deve fare **solo e unicamente ragionamento** — non calcoli, non data fetching, non operazioni meccaniche.
- Metafora: "tu hai 8 schermi con 8 broker. Invece di un agente che guarda tutti gli 8 schermi (costoso), hai Python che scarica la tabella, estrae il valore che ti serve, lo calcola. L'agente vede solo il risultato."

### Implicazioni
- Minimizzare le chiamate all'LLM è un obiettivo di design, non solo di ottimizzazione.
- I moduli devono essere il più possibile **pre-processing deterministico + una sola chiamata LLM per il ragionamento**.
- Questo vale anche per i test: più i moduli sono deterministici, meno costano da testare.

---

## 6. Modelli e Infrastruttura

### Modelli cinesi (DeepSeek e altri open source)
- Costano **1/20 rispetto ai modelli americani** per le stesse performance "di forza bruta".
- Per questo progetto serve "ragionamento bruto su un compito specifico" — non le capacità più avanzate.
- I modelli cinesi open source si scaricano e si fanno girare su cloud.

### Infrastruttura consigliata
- **Non comprare hardware fisico (GPU)**: inefficiente, costoso, non scalabile, se si rompe sei bloccato.
- **Google Cloud GPU a consumo** + modelli open source scaricati = soluzione ottimale.
- Esiste già un mercato: aziende americane che comprano GPU, scaricano modelli cinesi, li vendono come servizio.
- Modello DIY: Google Cloud → GPU a consumo → scarichi DeepSeek / modelli open → paghi solo quello che usi.

---

## 7. Nuovo Framing — AI Investment Fund / Factory

La conversazione ha fatto emergere un nuovo modo di vedere il progetto:
- Non è "solo un trading bot" — è un **AI Investment Fund** o **AI Investment Factory**.
- Struttura analoga a un fondo professionale: ogni area ha un head agent con un team di agenti sotto.
- Esempio: 3 head agent (Equity Research, Fixed Income, Commodities) → ciascuno con 10 agenti specializzati.
- **Potenzialmente vendibile** a istituzioni (JP Morgan, Goldman Sachs) — sostituisce un trading floor intero.
- Vincolo: prima deve dimostrare di funzionare, poi si scala e si vende.
- Il costo di un agente AI vs un trader umano ($250k/anno): se l'agente è altrettanto efficace, il ROI è enorme.
- Efficienza: prima si costruisce un singolo agente/modulo che funziona bene, poi si scala.

---

## 8. Luca — Primo Passo Concreto

Alla fine della chiamata, Luca dichiara che inizierà subito a lavorare sul **"modulo che analizza i documenti"** — primo modulo concreto del sistema. Da tracciare come in-progress.

---

## 9. Decisioni e Tensioni Emerse

| Tema | Stato |
|------|-------|
| Trading singolo vs portfolio bilanciato | **Aperta** — nessuna scelta definitiva |
| Multi-asset vs solo cripto | **Aperta** — orientamento verso asset tradizionali + cripto come side |
| Cash-out strategy (quale %) | **Aperta** — da stabilire come regola fissa a priori |
| Regole del portafoglio (statuto) | **Aperta** — da scrivere e implementare |
| Frequenza/time frame dei trade | **Aperta** — intraday vs day trading vs swing? |

## 10. Action Items

- **Salvatore**: portare le regole di portafoglio dal fondo Starting Finance come base di lavoro; approfondire quale asset class come punto di partenza.
- **Luca**: cominciare il modulo di analisi documenti; studiare tutta la wiki prima della prossima sessione.
- **Entrambi**: brainstorming con l'AI (conversazione → esporta → ingest nel vault) come metodo di lavoro continuativo.
