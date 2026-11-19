---
title: "MVP — spiegazione e valutazione OpenBB"
type: artifact
tags: [architecture, infrastructure, roadmap]
created: 2026-10-31
updated: 2026-10-31
status: active
confidence: high
area: software
---

# MVP — spiegazione e valutazione OpenBB

Owner: 🛠 Luca (software); aggiornamento della pagina affidato alla chat dedicata. Stato: incarico autorizzato, implementazione e verifiche da registrare.

## Obiettivo

Spiegare OpenBB a Luca, capacità, limiti e alternative con adapter diretti. Riesaminare OpenBB-first; vendor agnostic confermato.

## Proprietà dei file

Solo `docs/research/openbb-assessment.md`.

## Criteri di completamento

Ricerca ufficiale datata, distinta dai requisiti wiki, raccomandazione comprensibile; nessuna implementazione o nuova dipendenza.

Coordinamento: [[artifacts/mvp-parallel-work-2026-10-31]]. Nessun ordine, commit o push richiesto. Credenziali locali, mai in chat.

## Evidenze — 2026-10-31

- **Ricerca completata:** fonti ufficiali OpenBB consultate su ODP/Platform, installazione V5, provider, configurazione, errori, provider selection/fallback, licenza e prezzi Workspace. Dettaglio e URL in `trading-agent/docs/research/openbb-assessment.md`.
- **Repository verificato:** il codice contiene il contratto e l’adapter broker Alpaca read-only; `src/trading_agent/data/` e `src/trading_agent/storage/` sono ancora scaffolding. Nessuna integrazione OpenBB è stata installata o eseguita.
- **Distinzione confermata:** OpenBB/ODP è un toolkit di integrazione, non il fornitore del dato. Provider, chiavi, limiti, termini e copertura restano sottostanti e provider-specifici.
- **Fallback chiarito:** il provider selection documentato da OpenBB sceglie un provider configurato/idoneo per credenziali; non equivale a retry resiliente dopo timeout, rate limit, risposta vuota o dato stale. La policy di fallback resta del progetto.
- **Proposta tecnica delegata:** adottare un approccio ibrido: OpenBB-first per catalogazione e valutazione; OpenBB dietro adapter nostro solo per capability che dimostrino un vantaggio; SDK diretti per broker, live/decision-critical e casi con requisiti stretti. Vendor agnostic, modelli normalizzati, provenienza, dedup, persistenza e rimozione senza impatto sugli agenti restano invariati.
- **Nessuna decisione finale registrata:** la proposta richiede valutazione di una capability rappresentativa prima di aggiungere la dipendenza OpenBB. Cache esclusa dallo scope corrente.

### Limiti

Non sono state installate dipendenze, configurate chiavi o chiamate API provider. La documentazione ufficiale non dimostra la copertura per simbolo/periodo né i costi dei provider sottostanti; questi richiedono test e verifica separati. Il vecchio passaggio del piano operativo che prescriveva OpenBB + fallback automatico + cache è trattato come riferimento storico, superato dal riesame corrente.
