---
title: Antirez / Redis Testing Practices
type: research
tags:
  - testing
  - redis
  - antirez
  - software-quality
created: 2026-10-31
updated: 2026-10-31
status: active
confidence: high
area: software
related:
  - '[[system/foundation/codebase-architecture]]'
  - '[[system/foundation/python-commenting-conventions]]'
---

# Antirez / Redis / DS4 Testing Practices

> Ricerca primaria: pratiche ricavate esclusivamente dai repository ufficiali Redis e DS4 e da testi ufficiali di antirez. Le regole operative per `trading-agent` sono adottate qui come convenzione di lavoro; le scelte di prodotto restano nel decision log.

## Sintesi operativa

Redis combina un harness locale che avvia e manipola processi reali, un percorso contro server esterni, tag di compatibilità/capability e filtri automatici per rendere eseguibili subset coerenti della suite. Il test runner non è soltanto una raccolta di unit test: la suite include unit, integration, modules, Sentinel, cluster e vector-set areas nel repository ufficiale. [Redis `tests/README.md`](https://github.com/redis/redis/blob/unstable/tests/README.md), [Redis `tests/` tree](https://github.com/redis/redis/tree/unstable/tests)

Per questo progetto, la lezione applicabile è mantenere test deterministici e veloci per i contratti, separare esplicitamente i test che richiedono provider/credenziali o risorse reali, e usare marker/configurazioni per escludere solo ciò che l'ambiente non può verificare. Questa è una proposta derivata dalle fonti, non una modifica al codice né una decisione chiusa.

## Pratiche osservate nelle fonti primarie

### DS4 — principi aggiuntivi verificati

DS4 estende la stessa filosofia a un sistema con modello, prompt, tool, stato KV, server HTTP e coding agent:

1. **Integration-first sul percorso reale**: i controlli verificano il comportamento del sistema composto; i test dei componenti restano un livello separato, non il sostituto del percorso end-to-end.
2. **Casi dichiarativi e grading indipendente**: i casi sono dati separati dal runner; ogni caso dichiara provenienza, dominio, suite, budget e tipo di risposta. Il grading interpreta forme equivalenti senza ricostruire l'output usando l'implementazione sotto test.
3. **Stati oltre pass/fail**: pending, passed, failed, skipped, stopped e incomplete distinguono un difetto da un prerequisito assente o da un'esecuzione interrotta.
4. **Diagnosi come artefatto**: trace, log e dump sono strumenti per localizzare il guasto; se contengono dati reali restano privati.
5. **Copertura guidata dal failure mode**: ogni modifica va provata contro il modo realistico in cui può fallire, includendo correttezza e, quando rilevante, performance.
6. **Riproducibilità delle misure**: confronti prestazionali e di qualità usano ambiente, input, modello/dataset e condizioni registrati e invariati.
7. **Smoke test non equivale a QA**: un test rapido dà un segnale iniziale, non autorizza a dichiarare verificato l'intero sistema.

Fonti DS4: [README](https://github.com/antirez/ds4/blob/main/README.md), [TESTING.md](https://github.com/antirez/ds4/blob/main/docs/TESTING.md), [QA_BEFORE_RELEASES.md](https://github.com/antirez/ds4/blob/main/QA_BEFORE_RELEASES.md), [CONTRIBUTING.md](https://github.com/antirez/ds4/blob/main/CONTRIBUTING.md), [ds4_eval.c](https://github.com/antirez/ds4/blob/main/ds4_eval.c), [ds4_eval_cases.c](https://github.com/antirez/ds4/blob/main/ds4_eval_cases.c), [EVAL_DATA.md](https://github.com/antirez/ds4/blob/main/EVAL_DATA.md).

### Regole operative adottate per `trading-agent`

Queste regole devono guidare ogni nuovo o modificato test:

- **Seam pubblico prima del test**: dichiarare quale interfaccia osservabile si sta provando e cosa il test non copre.
- **Expected indipendente**: usare esempi della specifica, fixture note o risultati calcolati da una fonte indipendente; mai costruire l'atteso usando il tipo/metodo restituito dal codice sotto test.
- **Failure mode prima della coverage**: partire dal danno possibile (ordine duplicato, dato vecchio, errore scambiato per vuoto, precisione persa, rollback parziale), non dalla percentuale di righe.
- **Stato esplicito**: distinguere pass, skip per prerequisito, errore di integrazione e incompletezza; non mascherare un'assenza di dati come risultato valido.
- **Fixture e provenienza**: casi realistici, piccoli e tracciabili; per dati esterni conservare provider, versione/periodo, payload minimo e motivazione.
- **Trace solo per diagnosi**: registrare richieste, risposte normalizzate e decisioni di orchestrazione quando servono a riprodurre un guasto; non includere segreti.
- **Smoke separato dalla QA**: i test veloci non sostituiscono contratti, regressioni e integrazioni reali.
- **Performance riproducibile**: misurare solo con input, ambiente e condizioni dichiarati; non introdurre benchmark casuali nei test funzionali.


### 1. Harness locale con risorse reali e harness contro server esterno

La README ufficiale descrive come modalità normale l'avvio e la manipolazione di istanze locali `redis-server`, inclusi controllo dello stato dei processi e ispezione dei log. La stessa suite supporta un server esterno con `--host` e `--port`; in quel modo i test marcati `external:skip` vengono saltati. [Redis `tests/README.md`, lines 4–10](https://github.com/redis/redis/blob/unstable/tests/README.md#L4-L10)

Il wrapper `runtest` alza il limite dei file aperti a 1024 quando necessario, seleziona una versione disponibile di Tcl (`tclsh8.5` fino a `tclsh9.0`) e inoltra gli argomenti a `tests/test_helper.tcl`. Questo rende il bootstrap parte osservabile e ripetibile dell'harness, invece di nasconderlo nella singola suite. [Redis `runtest`](https://github.com/redis/redis/blob/unstable/runtest)

### 2. Tag a più livelli e capability esplicite

Redis consente di applicare tag nel contesto `start_server`, in un contesto `tags` che raggruppa più test, oppure nel singolo test. La README elenca capability come `needs:repl`, `needs:debug`, `needs:config-maxmemory`, `needs:reset` e `needs:save`; i tag descrivono prerequisiti osservabili, non categorie vaghe. [Redis `tests/README.md`, lines 27–49](https://github.com/redis/redis/blob/unstable/tests/README.md#L27-L49)

La suite filtra automaticamente i test incompatibili con l'ambiente: `external:skip` per server esterni, `cluster:skip` in `--cluster-mode` e `largemem:skip` quando non è attivo `--large-memory`. È inoltre documentato il filtro negativo, per esempio `./runtest --host <host> --port <port> --tags -needs:repl`. [Redis `tests/README.md`, lines 51–63](https://github.com/redis/redis/blob/unstable/tests/README.md#L51-L63)

### 3. Modalità di esecuzione come parte del contratto

Le opzioni documentate includono `--singledb`, `--ignore-encoding`, `--ignore-digest`, `--cluster-mode` e `--large-memory`. Non sono semplici dettagli del comando: dichiarano quali assunzioni la suite può fare sull'ambiente e quali verifiche sono intenzionalmente ridotte. [Redis `tests/README.md`, lines 11–21](https://github.com/redis/redis/blob/unstable/tests/README.md#L11-L21)

La struttura del repository separa aree e supporti (`unit`, `integration`, `modules`, `sentinel`, `helpers`, `support`, `assets`), rendendo visibile il confine tra test di comportamento locale, integrazione e infrastruttura di test. [Redis `tests/` tree](https://github.com/redis/redis/tree/unstable/tests)

### 4. Coverage non equivale a stati verificati

Nel testo ufficiale *A new era for software testing*, antirez osserva che coprire tutte le righe non significa coprire tutti gli stati possibili del software. Propone quindi di usare QA manuale/agentica per esplorare combinazioni e comportamenti che una suite tradizionale può non attraversare, inclusi casi sorprendenti, documentazione insufficiente e interfacce poco curate. [antirez, “A new era for software testing”](https://antirez.com/news/168)

Questo punto è una posizione dell'autore, non una misura della suite Redis. La conseguenza pratica per `trading-agent` è trattare coverage e test verdi come segnali necessari ma non sufficienti: servono anche scenari d'integrazione e verifiche orientate all'esperienza del chiamante quando il flusso diventa abbastanza maturo.

## Applicazione proposta a `trading-agent`

| Pratica osservata | Applicazione proposta | Stato |
|---|---|---|
| Harness locale + server esterno | Separare test con fake/mock deterministici da test espliciti contro Alpaca paper o vendor reali | Proposta |
| Tag di capability | Conservare marker come `integration` e introdurre nuovi marker solo per prerequisiti reali (credenziali, rete, provider, risorse) | Proposta |
| Filtri automatici | Il comando di default deve restare sicuro e ripetibile; i test dipendenti dall'ambiente devono essere opt-in o filtrabili senza nascondere un errore del test | Proposta |
| Suite per aree | Mantenere confini leggibili tra contratti di broker/data, storage, integrazione e interfaccia | Proposta; la struttura esiste già nel repository |
| Coverage non sufficiente | Aggiungere scenari end-to-end e regressione solo quando rappresentano stati/contratti non coperti dai test locali | Proposta |

Il repository corrente già configura `pytest` su `tests/`, usa `--strict-markers` e definisce il marker `integration` per controlli read-only contro Alpaca paper. [Repository `pyproject.toml`, lines 23–29](https://github.com/cookkie03/trading-agent/blob/main/pyproject.toml) La suite locale contiene test per broker, data provider, storage e interfaccia; questa verifica descrive lo stato osservato il 2026-10-31 e non sostituisce l'esecuzione dei test. [Repository `tests/`](https://github.com/cookkie03/trading-agent/tree/main/tests)

## Limiti della ricerca

- Le fonti usate sono il repository ufficiale `redis/redis` e il sito ufficiale di antirez; non sono state usate guide o articoli secondari.
- Le pagine Redis citate puntano al branch `unstable`: dettagli del runner e dei tag possono evolvere.
- Il testo di antirez è una fonte normativa/opinionale dell'autore, non una specifica formale del progetto Redis.
- Nessun codice, test o configurazione del repository `trading-agent` è stato modificato per questa nota.

## Fonti primarie

1. [Redis test-suite README](https://github.com/redis/redis/blob/unstable/tests/README.md)
2. [Redis test-suite tree](https://github.com/redis/redis/tree/unstable/tests)
3. [Redis `runtest`](https://github.com/redis/redis/blob/unstable/runtest)
4. [Redis `tests/test_helper.tcl`](https://github.com/redis/redis/blob/unstable/tests/test_helper.tcl)
5. [antirez — “A new era for software testing”](https://antirez.com/news/168)
6. [trading-agent `pyproject.toml`](https://github.com/cookkie03/trading-agent/blob/main/pyproject.toml)
7. [trading-agent `tests/`](https://github.com/cookkie03/trading-agent/tree/main/tests)
