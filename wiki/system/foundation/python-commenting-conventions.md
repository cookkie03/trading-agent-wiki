---
title: Convenzioni per i commenti Python
type: build
tags:
  - architecture
  - software
  - codebase-design
created: 2026-10-31
updated: 2026-10-31
status: active
confidence: high
area: software
related:
  - '[[system/foundation/codebase-architecture]]'
  - '[[system/foundation/decision-log]]'
  - '[[system/foundation/implementation-status]]'
---

# Convenzioni per i commenti Python

> Decisione di sviluppo approvata da Luca il 2026-10-31. Si applica ai nuovi moduli Python e alle modifiche sostanziali ai moduli esistenti.

## Principio

Adottiamo un metodo pragmatico ispirato ai commenti di antirez in Redis e nei progetti di strutture dati:

> Il codice spiega il **cosa**; il commento spiega il **perché**, le invarianti e i vincoli che il codice da solo non rende evidenti.

I commenti non devono compensare nomi scarsi, funzioni troppo grandi o una struttura confusa. Prima si migliora il codice; poi si commenta ciò che resta non ovvio.

## Ordine di priorità

1. Codice autoesplicativo: nomi, tipi e funzioni piccole.
2. Docstring brevi per l'interfaccia pubblica.
3. Commenti inline per motivazioni, invarianti e vincoli esterni.
4. Test per il comportamento verificabile.
5. Wiki, documentazione e decision log per architettura, trade-off e storia del progetto.

## Tipi di commento da usare

### Docstring di interfaccia

Le funzioni, classi e `Protocol` pubblici documentano solo ciò che il chiamante deve sapere e la firma non esprime:

- risultato e semantica dei dati;
- limiti, ordinamento o finestre restituite;
- errori e differenza tra errore e risultato vuoto;
- effetti collaterali;
- invarianti e precondizioni.

```python
def get_orders(self, query: OrderQuery | None = None) -> tuple[Order, ...]:
    """Restituisce una finestra limitata, dal più recente.

    Gli errori del broker non diventano un risultato vuoto e le gambe
    annidate degli ordini restano parte del risultato.
    """
```

Non documentare riga per riga un corpo già leggibile.

### Commenti di motivazione

Spiegano perché una soluzione apparentemente più semplice sarebbe sbagliata o pericolosa:

```python
# Non convertiamo Decimal in float: la perdita di precisione può propagarsi
# nei valori di portafoglio e nei controlli di rischio.
```

Questo è il formato inline principale del progetto.

### Commenti sulle invarianti

Rendono esplicito ciò che deve restare vero in ogni esecuzione:

```python
# Il modello contiene dati normalizzati del progetto; nessun tipo dello SDK
# deve attraversare questo seam.
```

Sono particolarmente importanti in modelli condivisi, `Protocol`, repository, risk gate e stato degli agenti.

### Commenti sugli algoritmi e sulle ratio economiche

Si introducono quando diventano operative le feature quantitative, soprattutto per ratio economiche, metriche di rischio, indicatori e backtest. Devono chiarire:

- definizione di dominio adottata;
- motivo della scelta rispetto alle alternative;
- unità e periodo di riferimento;
- trattamento di zeri, valori mancanti, segni e dati non comparabili;
- eventuali bias temporali o assunzioni del backtest.

```python
# Usiamo il rendimento semplice, non il log-return: questa metrica alimenta
# lo scoring MVP e deve restare coerente con il protocollo di backtest.
```

Per una ratio economica, il commento non deve limitarsi a espandere l'acronimo: deve proteggere la semantica finanziaria del calcolo. La definizione ufficiale e le decisioni condivise restano nella wiki; il codice documenta il vincolo locale che serve a non implementarla in modo ambiguo.

### Commenti temporali o storici

Si usano solo quando un vincolo esterno attuale spiega una scelta apparentemente strana: versione di uno SDK, compatibilità, workaround o migrazione incompleta. Devono descrivere il vincolo verificabile e, se utile, la condizione per rimuoverlo; non devono diventare un diario personale.

```python
# La versione supportata dello SDK non espone un timeout pubblico; lo
# configuriamo qui e teniamo il coupling confinato all'adapter.
```

Evitare date, nomi e cronache se non servono a capire il comportamento attuale. La storia della decisione va nel decision log o nella ricerca tecnica.

## Dove mettere cosa

| Informazione | Destinazione |
|---|---|
| Contratto d'uso di una funzione pubblica | Docstring |
| Motivazione, invariante o vincolo locale | Commento vicino al codice |
| Comportamento verificabile | Test |
| Decisione architetturale | Wiki / `docs/architecture.md` |
| Trade-off difficile da invertire | Decision log o ADR |
| Lavoro futuro concreto | Project board; TODO solo se localizzato nel codice |
| Storia di un bug risolto | Di norma non nel codice |

## Regole pratiche

- Non commentare codice ovvio.
- Non tradurre in italiano la riga successiva.
- Non usare commenti per compensare un nome o un'interfaccia debole.
- Scrivere il commento vicino al punto in cui protegge una decisione.
- Eliminare o aggiornare un commento diventato falso dopo un refactoring.
- Preferire due righe precise a un blocco narrativo.
- Commentare esplicitamente i rischi di perdita di precisione, dati mancanti, dati non aggiornati, errori mascherati e confusione tra `nessun dato` e `lettura fallita`.
- Non duplicare nella docstring decisioni già documentate nella wiki: collegare la pagina quando serve contesto.

## Applicazione

Questa convenzione vale da ora per le nuove modifiche Python. L'adeguamento dei file esistenti avviene opportunisticamente quando vengono modificati per una feature o un bugfix; non si apre una riscrittura separata dei commenti senza un beneficio concreto.
