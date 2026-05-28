---
title: "Note Audio Salvatore — Strategie Quant (2026-05)"
type: source
tags:
  - source
  - strategy
  - quant
raw_source_path: "raw/archived/articles/quant strategy/"
created: 2026-05-22
updated: 2026-05-22
confidence: medium
status: active
related:
  - "[[strategy/methods/trend-following]]"
  - "[[strategy/index]]"
  - "[[build/modules/quant-backtesting]]"
---

# Note Audio Salvatore — Strategie Quant (2026-05)

Raccolta di note vocali di Salvatore mentre studia libri di quantitative finance e value investing. Contiene due idee distinte: (1) dual portfolio value+quant e (2) mean reversion / statistical arbitrage.

Fonte: 6 file `.txt` in `raw/articles/quant strategy/` (trascrizioni audio). I file sono duplicati in coppie (stessa trascrizione ripetuta più volte per ragioni tecniche della registrazione).

---

## Idea 1 — Dual Portfolio: Value + Quant

**Contesto**: Salvatore sta leggendo due libri in parallelo, uno su quantitative finance e uno su value investing.

### La proposta

Creare **due portafogli distinti sotto lo stesso budget**, con l'AI che ripartisce i soldi tra i due in base a parametri:

- **Portafoglio Value** (ancora di salvezza): orizzonte temporale ~5 anni. Non segue tanto l'andamento dei prezzi, ma segue idee, settori, trend in cui si crede. Approccio fondamentale.
- **Portafoglio Quant** (strategia attiva): applica strategie quantitative come quelle che Salvatore sta studiando (es. mean reversion). Orizzonte più breve, approccio sistematico.

**Meccanismo**: l'AI (il cervello del fondo) decide come ripartire le risorse tra i due portafogli in base a parametri da definire.

### Nota operativa

Questa è un'idea preliminare, ancora da esplorare. Salvatore ha esplicitamente detto di stare "facendo progressi nel chiarire le idee" e che per completare i due libri ci vorranno almeno due mesi. L'idea del dual portfolio è quindi ancora ad uno stadio embrionale.

---

## Idea 2 — Mean Reversion e Statistical Arbitrage (Stat Arb)

**Contesto**: Salvatore ha trovato questa strategia studiando e la ritiene "una cosa molto carina" e funzionale come punto di partenza, perché semplice e codificabile.

### Definizione

**Mean Reversion**: la tendenza che hanno due titoli correlati a convergere. Se si sovrappongono i grafici di due asset molto correlati (es. Coca-Cola e Pepsi, gold su EUR e gold su USD), dovrebbero muoversi in modo quasi identico. Non sempre è così.

**Statistical Arbitrage (Stat Arb) / Pairs Trading**: si tradia quando lo spread tra i due asset correlati è più ampio del normale. Si entra quando lo spread è abbastanza ampio, aspettandosi che si assottiglierà — perché i due asset sono correlati e tenderanno a tornare alla loro relazione storica.

### Strategia concreta

1. Identificare due asset molto correlati
2. Monitorare continuamente lo spread tra i due prezzi
3. Quando lo spread si allarga oltre una soglia statistica → entrare in posizione (long il sottoperformante, short il sovraperformante)
4. Uscire quando lo spread si assottiglia (convergenza)

### Perché Salvatore la valuta positivamente

- Logica chiara e basata su fondamentali matematici (correlazione statistica)
- Codificabile in modo relativamente semplice
- Applicabile su azioni (non solo crypto)
- Non richiede velocità elevatissima (non è HFT)
- Supera il filtro di Salvatore: non usa derivati, non richiede frequenza incompatibile con costo token

### Limiti identificati da Salvatore

- Serve un articolo di 80 pagine (trovato) da leggere per approfondire
- Da valutare se le correlazioni reggono in regime di stress (il rischio principale della mean reversion è che la correlazione si rompa)
- Tra le strategie che Salvatore ha scartato: quelle che usano derivati, quelle che richiedono troppa velocità

### Applicazione al progetto

Secondo Salvatore questa strategia può essere fatta su stock tradizionali, basta capire le correlazioni. La proposta è di partire da cose semplici e codificabili, poi aggiungere parametri. L'articolo trovato (80 pagine) sarà il prossimo materiale da ingestare.

---

## Note di contesto

- Salvatore dedica circa 1 ora / 40 minuti al giorno a leggere materiale
- Sta studiando mean reversion come potenziale prima strategia codificabile
- L'articolo tecnico `Quantitative Trading Strategies: Alpha, Backtesting & Performance` (Michael Brenndoerfer) è stato trovato nella stessa sessione di ricerca → vedere [[references/quantitative-trading-strategies-brenndoerfer]]
