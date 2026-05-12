# Hot Cache — Trading Agent

> Contesto di sessione recente. Aggiornare a fine sessione. Tenere entro 300 righe.

## Sessione Corrente
- **Data**: 2026-05-10
- **Agent**: Claude Sonnet 4.6
- **Operazioni**: (1) Integrazione trascrizioni alta fedeltà videochiamata 04-30. (2) Creazione board personali Luca e Salvatore con focus separati. (3) Ingest trascrizione completa videochiamata 05-06 — molti contenuti nuovi rispetto alla versione precedente.

## Pagine toccate
- [[sources/videochiamata-luca-salvatore-2026-04-30]] — arricchita con trascrizioni alta fedeltà
- [[sources/videochiamata-luca-salvatore-2026-05-06]] — riscritta con trascrizione completa (molto più lunga della versione precedente)
- [[concepts/modular-trading-agent-architecture]] — aggiunto principio deterministico e correlazione cripto
- [[decisions/decision-log]] — aggiunte decisioni aperte importanti (trading singolo vs portfolio, multi-asset)
- [[questions/open-questions]] — arricchite con nuove domande critiche
- [[artifacts/luca-board]] — aggiunto modulo analisi documenti in corso, decisioni tecniche
- [[artifacts/salvatore-board]] — aggiornata con tutte le nuove idee della call 05-06

## Stato attuale del progetto
- Fase: **Design** — nessun codice ancora
- Luca ha iniziato il **modulo analisi documenti** (primo modulo concreto)
- **Decisione critica aperta**: trading singolo vs portfolio bilanciato — da chiudere prima di costruire
- **Framing aggiornato**: il progetto è un "AI Investment Fund / Factory", non solo un trading bot
- Exchange: Binance (crypto), ma Salvatore propone di partire da asset tradizionali

## Pending ingest
- Le trascrizioni in `raw/audio/` possono essere archiviate in `raw/archived/`

## Note sessione critiche
- Il **principio deterministico** è un vincolo architetturale: LLM solo per ragionamento, tutto il resto Python. Anche i backtest costano token.
- **Modelli cinesi (DeepSeek)**: costano 1/20 degli americani. Google Cloud + modelli open source = infrastruttura ottimale.
- Salvatore ha proposto regole del portafoglio stile fondo professionale (nessuna asset class >5%, vendi a +100% profitto, cash-out periodico). Da formalizzare come "statuto del fondo".
- La correlazione tra cripto richiede un modulo di allocazione dinamica nel basket.
