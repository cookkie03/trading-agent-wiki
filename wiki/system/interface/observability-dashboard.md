---
title: Cockpit operativo e osservabilità
type: build
tags:
  - dashboard-design
  - architecture
  - software
created: 2026-06-08T00:00:00.000Z
updated: 2026-07-13T00:00:00.000Z
status: active
priority: high
area: software
related:
  - '[[system/orchestration/universe-watchlist]]'
  - '[[system/data/data-layer]]'
  - '[[prior-art/libraries/sfc-portfolio-tracker]]'
confidence: high
---

# Cockpit operativo e osservabilità

> [!important] Promemoria prima di riprendere la UI
> Prima di riprendere design o implementazione della dashboard del Trading Agent su GitHub, **chiedere a Giuseppe (vedi lista contatti)** un confronto e un aiuto sulla UI.

Pagina di **spec**, non di stato del repository esterno. L'obiettivo è fornire un cockpit completo per osservare e governare il sistema, mantenendo la logica di dominio nel backend; vedi anche [[system/interface/frontend-module]].

## Principi architetturali

Il cockpit legge e modifica risorse tramite API e contratti applicativi espliciti. Non chiama vendor direttamente e non implementa nel frontend logica di trading, calcoli risk/quant o regole di strategia. Le azioni operative sono mediate dal backend e sottoposte a validazione, autorizzazioni e audit.

## Superfici funzionali

1. **Overview e osservabilità:** portfolio snapshot, liquidità, posizioni, watchlist, stato agenti/workflow, decisioni, trigger, trades, health, freshness, trace e audit.
2. **Configurazione e personalizzazione:** parametri applicativi, preferenze utente, profili, strategie, limiti, pianificazioni e state modificabili.
3. **Provider e integrazioni:** catalogo provider, capability, stato connessione, configurazione, priorità e fallback; gestione credenziali tramite secret store sicuro.
4. **Controllo operativo:** avvio/arresto/pausa dei workflow autorizzati, gestione job, retry, refresh, approvazioni e stato delle operazioni.
5. **Ricerca e analisi:** schede ticker, evidenze, decision log, backtest, metriche, storico e confronto tra strategie.
6. **Audit e versioni:** cronologia delle modifiche, autore, motivazione, diff, esito e ripristino quando supportato.

## Informazioni da esporre

1. portfolio snapshot, liquidità e posizioni;
2. watchlist, ticker e ultimo stato di analisi;
3. decisioni, opinioni, trigger e motivazioni;
4. trade, `exit_reason` e metriche di esito;
5. health del sistema e staleness dei dati;
6. benchmark/alpha solo quando il benchmark sarà introdotto Post-MVP.

## Evoluzione Post-MVP — Configuration & State Agent

L'agente conversazionale non è richiesto per il completamento del cockpit MVP. Nel MVP le modifiche alle risorse sono eseguite attraverso controlli UI strutturati e API applicative.

In una fase Post-MVP, il cockpit potrà includere un agente conversazionale che traduce richieste in linguaggio naturale in modifiche a configurazioni personali, strategie, parametri, state e provider collegati. L'agente opera solo su risorse e azioni esposte da un catalogo allowlist con schemi tipizzati; non modifica codice, file sorgente, prompt di sistema protetti o segreti.

Flusso minimo Post-MVP: interpretazione → identificazione risorse → anteprima/diff → validazione schema e invarianti → conferma proporzionata al rischio → applicazione tramite API → audit trail → eventuale rollback. Le credenziali sono gestite da un secret manager e non vengono restituite al modello.

Le azioni che possono generare ordini o effetti finanziari hanno autorizzazioni, conferme e controlli separati dalla normale gestione della configurazione.

## Evoluzione

React + TypeScript deve riusare contratti API stabili per lettura e scrittura, con service layer disaccoppiato dal framework UI. La struttura visuale e la gerarchia delle schermate restano da definire dopo la discovery UX.
