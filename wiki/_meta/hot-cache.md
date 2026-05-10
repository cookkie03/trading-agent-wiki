# Hot Cache — Trading Agent

> Contesto di sessione recente. Aggiornare a fine sessione. Tenere entro 300 righe.

## Sessione Corrente
- **Data**: 2026-05-10
- **Agent**: Claude Sonnet 4.6
- **Operazioni**: Integrazione di due trascrizioni ad alta fedeltà della videochiamata 2026-04-30. Le nuove trascrizioni hanno aggiunto dettagli significativi rispetto alla versione precedente (generata da audio con tool meno precisi).

## Pagine toccate
- [[sources/videochiamata-luca-salvatore-2026-04-30]] — riscritta con tutti i dettagli dalle nuove trascrizioni
- [[concepts/modular-trading-agent-architecture]] — aggiornata con: Prompt Builder, needle-in-haystack, Factor Investigation Agent, Prediction Module DL, TA risk, Sentiment degli Analisti, Volume Spike module, Binance, AlphaArena/FinAgent specifici
- [[build/system-map]] — aggiornata con Prompt Builder, Factor Investigation Agent, Prompt Store, Security Module
- [[decisions/decision-log]] — aggiunte 5 decisioni chiuse (from scratch, crypto/Binance, limit order SL/TP, design-first, augmentation→autonomy)
- [[questions/open-questions]] — arricchite con nuove domande (frequenza trade, TA inclusion, sentiment degli analisti, quantificazione news, continuous learning)
- [[ops/backlog]] — aggiornato: completati i task già fatti, aggiunti: analisi FinAgent, AlphaArena, NeuroEspresso, definizione artifact, I/O per modulo

## Pending ingest
- Paper FinAgent (Cornell, 38 pagine) — salvato nella conversazione, da ingestare formalmente come source
- Le nuove trascrizioni in `raw/audio/` possono essere archiviate in `raw/archived/videochiamata-2026-04-30/`

## Stato attuale del progetto
- Fase: **Design** — nessun codice ancora, raccolta conoscenza e progettazione
- Exchange deciso: **Binance** (crypto)
- Architettura decisa: **from scratch**, multi-agente, modulare
- Trade mechanism: **limit order + SL + TP + leva**
- Prossimo passo urgente: analisi dei tre progetti di riferimento (FinAgent, AlphaArena, NeuroEspresso)

## Note sessione
- Le trascrizioni ad alta fedeltà hanno rivelato molto più dettaglio di quanto catturato nella prima versione del source 04-30.
- Il Prompt Builder è un componente architetturale esplicito non presente nelle versioni precedenti.
- L'idea "Sentiment degli Analisti" (Salvatore/King) è una strategia alternativa al factor investing — merita uno studio dedicato.
- Il rischio "TA corrompe Prediction Module" è una tensione progettuale aperta importante.
