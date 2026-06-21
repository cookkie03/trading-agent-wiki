---
title: "Indicatori per Analisi Macroeconomica"
type: synthesis
tags:
  - strategy
  - market-structure
  - quant
created: 2026-06-05
updated: 2026-06-20
status: active
area: strategy
confidence: high
raw_source_path: "raw/archived/I Driver di Mercato (definitivo).md"
related:
  - "[[system/modules/quant-backtesting]]"
  - "[[strategy/questions-for-salvatore]]"
  - "[[strategy/index]]"
  - "[[system/modules/data-layer]]"
---

# Indicatori per Analisi Macroeconomica

> Guida completa agli indicatori macroeconomici e di mercato per l'analisi di equity, fixed income e cross-asset.
> Fonte originale: `I Driver di Mercato (definitivo).md` (ingestito e archiviato in `raw/archived/I Driver di Mercato (definitivo).md`).

---

## Indice delle categorie

| # | Categoria | Indicatori principali |
|---|-----------|----------------------|
| 1 | Crescita Economica | PIL, Consumi, PMI, Beni Durevoli |
| 2 | Inflazione | CPI, Core CPI, PPI, PCE |
| 3 | Mercato del Lavoro | NFP, Disoccupazione, Salari |
| 4 | Politica Monetaria | Tassi, FOMC, Dot Plot |
| 5 | Liquidità | M2, QE/QT, Reverse repo |
| 6 | Mercato Immobiliare | Costruzioni, Permessi, Vendite |
| 7 | Mercati Obbligazionari | Curva Rendimenti, TIPS, Term Premium |
| 8 | Condizioni del Credito | Spread IG/HY, Financial Conditions |
| 9 | Valute e Materie Prime | DXY, FX, Petrolio, Metalli |
| 10 | Volatilità e Rischio | VIX, Indice MOVE |
| 11 | Flussi e Posizionamento | Flussi ETF, CFTC Positioning |
| 12 | Driver Azionari | EPS, Revisioni Utili, Guidance |

---

## 1. Crescita Economica

### PIL — La Misura Più Ampia dell'Attività Economica

Il PIL misura il valore monetario totale di beni e servizi prodotti in un paese in un dato periodo. È il metro di giudizio più ampio del ciclo economico.

Pubblicato trimestralmente (stima flash, seconda stima, revisione finale), è monitorato da banche centrali, governi e investitori.

Formula: C (Consumi) + I (Investimenti) + G (Spesa pubblica) + NX (Esportazioni nette)

Negli USA i consumi privati rappresentano circa il 70% del PIL. Per questo retail sales, lavoro e salari sono così osservati.

PIL solido conferma l'espansione. Due trimestri negativi consecutivi = recessione tecnica. Il contesto macro determina tutto.

#### Scenario: PIL Sopra Trend — Rialzista
Economia in espansione sopra il potenziale: ricavi aziendali in crescita, equity outperform, spread creditizi in compressione. Le banche centrali rimangono accomodanti finché l'inflazione è sotto controllo.
Implicazioni: Equity positivo, spread creditizi in calo, USD in rafforzamento.

#### Scenario: PIL Surriscaldato — Rischio Inflazione e Tassi
Surriscaldamento: inflazione in crescita, banche centrali costrette ad alzare i tassi aggressivamente, rendimenti obbligazionari in rialzo, titoli growth perdono valore, credito si inasprisce.

Nuance fondamentale: non è il numero del PIL in sé, ma il PIL in relazione all'inflazione che determina il regime macro.

Domanda chiave: la crescita del PIL arriva CON o SENZA inflazione? Questa risposta determina l'intero regime di asset allocation.

---

### Vendite al Dettaglio e Consumi Privati — Il Polso del Consumatore

#### Retail Sales
Pubblicato mensilmente dal Census Bureau. Misura la spesa dei consumatori al punto vendita: stazioni di servizio, elettronica, abbigliamento, ristorazione, grande distribuzione.

Letture principali:
- Headline: include tutto, anche le auto
- Ex-Auto: depura il componente più volatile
- Control Group (ex-auto, carburante, edilizia): alimenta direttamente il calcolo del PIL

Le variazioni mensili contano più di quelle annuali nell'analisi in tempo reale.

Segnale: Retail sales forti + mercato del lavoro solido = inflazione da domanda. Fed rimane restrittiva. Rendimenti salgono.

#### Personal Spending
Parte del report BEA su redditi e spesa personale. Copre un universo più ampio delle retail sales includendo i servizi: sanità, alloggio, servizi finanziari, svago.

I servizi sono oggi il principale driver di inflazione, e il più persistente. Il reddito personale rilasciato contestualmente rivela se i consumi sono finanziati da stipendi o da debito/risparmio.

Dinamica reddito vs spesa:
- Spesa > Reddito = finanziata da debito o risparmio
- Segnale di fiducia nel breve, ma insostenibile nel medio
- Savings rate in calo = consumi a rischio

Il deflatore PCE è derivato da questo report. È il principale indice d'inflazione monitorato dalla Fed.

Segnale: Consumi finanziati da risparmio in calo = rialzista di breve, segnale d'allarme di medio. Monitorare il savings rate.

---

### Produzione Industriale e Ordini di Beni Durevoli

#### Produzione Industriale
Misura la produzione reale di manifattura, miniere e utilities. Pubblicata mensilmente dalla Federal Reserve insieme al tasso di utilizzo della capacità produttiva.

Utilizzo della capacità:
- Sopra 80%: potenziali colli di bottiglia, inflazionistico
- Sotto 75%: slack significativo, disinflazionistico, rischio recessione

Resta un barometro affidabile del ciclo e un leading indicator degli utili nei settori ciclici: industriali, materiali, energia.

PMI manifatturiero e produzione industriale tendono a confermarsi. L'IP fornisce la conferma hard data dei segnali survey del PMI.

Segnale: IP in calo per 2+ mesi + PMI in discesa = evidenza convergente di rallentamento ciclico.

#### Ordini di Beni Durevoli
Traccia gli ordini presso i produttori per beni con vita utile superiore a 3 anni: aeromobili, macchinari, computer, apparecchiature militari.

Il dato chiave è "beni strumentali non-difesa ex-aeromobili" (proxy capex): misura le intenzioni di investimento delle imprese e alimenta direttamente il PIL.

Catena leading indicator:
- Ordini oggi → produzione domani
- Produzione → occupazione → redditi → consumi
- Lag di trasmissione: 6-12 mesi

Attenzione: gli ordini Boeing creano oscillazioni mensili enormi. Leggere sempre il dato ex-trasporti per il segnale pulito.

Segnale: Capex core in rialzo = management ottimista sui ricavi futuri. Calo sostenuto = imprese in attesa, vento contrario al PIL nei prossimi 2-3 trimestri.

---

### PMI e ISM — I Leading Indicator Preferiti dai Mercati

I Purchasing Managers' Index (PMI) e i sondaggi ISM interrogano i responsabili acquisti sulle condizioni di business: nuovi ordini, produzione, occupazione, scorte, tempi di consegna.

PMI Composito = Manifatturiero + Servizi (ponderato)
ISM Manifatturiero e ISM Servizi sono le versioni di riferimento per gli USA.

Pubblicati nei primi giorni lavorativi di ogni mese. Sono i primissimi dati macro del nuovo ciclo e spesso muovono i mercati prima di qualsiasi dato su PIL o occupazione.

Sotto-componenti chiave:
- Nuovi Ordini: il segnale di domanda più forward-looking
- Occupazione: anticipa il report NFP di circa 1 mese
- Prezzi Pagati: leading indicator di PPI e CPI
- Arretrati vs Scorte: segnale di squilibrio domanda/offerta

Il PMI anticipa tipicamente il PIL di 1-2 trimestri. I mercati riprezzano i cambi di direzione del PMI settimane prima che appaiano nei dati ufficiali.

#### Soglia del 50
Sopra 50 = espansione: economia in accelerazione, nuovi ordini in crescita, occupazione in espansione, prezzi in aumento.
Sotto 50 = contrazione: produzione in calo, ordini in discesa, licenziamenti in corso, scorte in aumento.

Segnale: La direzione conta più del livello. Un PMI a 48 in risalita è più rialzista di un PMI a 52 in discesa.

Il PMI muove spesso i mercati più del PIL perché arriva 4-6 settimane prima.

---

## 2. Inflazione

### CPI e Core CPI — Il Dato che Muove Davvero i Mercati

#### CPI — Indice dei Prezzi al Consumo
Il principale indicatore di inflazione. Pubblicato mensilmente dal BLS. È forse il dato più market-moving in assoluto: genera spesso movimenti intraday dell'1-3% sugli indici azionari e di 15-30 bps sui rendimenti Treasury a 2 anni.

Componenti principali:
- Alloggio/Affitti (OER): ~33% — il componente più persistente
- Energia: ~7% — molto volatile, distorce il dato headline
- Alimentari: ~14%
- Sanitario, trasporti, abbigliamento

La variazione mensile è più seguita per il momentum; quella annuale per la magnitudine.

Meccanismo della sorpresa: l'impatto dipende dallo scarto vs le aspettative di consenso. Un miss di 0.1pp può muovere i mercati quanto 0.3pp se inatteso.

Segnale: CPI sopra consenso + mercato del lavoro solido = Fed alza ancora. Rendimenti salgono. Growth equity perde valore.

#### Core CPI — Senza Energia e Alimentari
Il Core CPI depura i due componenti più volatili per rivelare le tendenze inflazionistiche strutturali. Le banche centrali perseguono questo — i picchi di energia e cibo sono shock d'offerta fuori dal controllo della politica monetaria.

Un Core CPI persistentemente elevato è il segnale chiave che l'inflazione si è "radicata" nell'economia.

Sotto-componenti chiave:
- Affitti (OER): dominante, lento, con 12-18 mesi di ritardo rispetto ai prezzi reali
- SuperCore (Servizi ex-alloggio): la metrica più citata da Powell, riflette il trasferimento del costo del lavoro sui prezzi
- Beni core: spesso disinflazionistici post-normalizzazione supply chain

Monitorare il SuperCore: se i servizi rimangono inflazionistici, nessun miglioramento delle catene di fornitura riporterà il core al 2%.

Segnale: Core persistentemente sopra il 3% per 3+ mesi = inflazione duratura. La Fed non può ignorarla. Asset rischiosi soffrono.

---

### PPI e PCE — Costi alla Produzione e la Metrica Preferita dalla Fed

#### PPI — Indice dei Prezzi alla Produzione
Il PPI misura le variazioni di prezzo dal lato dei produttori: i costi sostenuti dalle imprese manifatturiere, agricole e dei servizi.

Come leading indicator del CPI: quando i costi di produzione aumentano, le aziende li trasferiscono sui consumatori con un ritardo di 1-3 mesi.

Letture principali:
- Domanda Finale PPI: headline, il più seguito
- Beni Intermedi PPI: pressioni a monte della filiera
- Servizi Core PPI: alimenta direttamente il PCE

Insight margini: quando il PPI cresce molto più velocemente del CPI, le aziende non riescono a trasferire i costi. Questo comprime i margini e anticipa revisioni negative agli EPS anche quando il fatturato regge.

Il PPI è un doppio indicatore: segnale anticipatore sia per l'inflazione che per la redditività aziendale.

Segnale: PPI accelera sopra il CPI = rischio compressione margini. Revisioni negative agli utili attese nei prossimi 1-2 trimestri.

#### PCE — Spesa per Consumi Personali
Il metro d'inflazione ufficialmente preferito dalla Federal Reserve. A differenza del CPI, il PCE usa pesi variabili che tengono conto della sostituzione nei consumi. Quando la carne bovina diventa cara, i consumatori si spostano sul pollo: il PCE cattura questa variazione.

Questo rende il PCE strutturalmente inferiore al CPI di 0.2-0.5 punti percentuali, ma più rappresentativo.

Target formale della Fed: 2% in termini di PCE, non di CPI. Il Core PCE al 2% è la destinazione.

Pubblicato nel report BEA su Redditi e Spesa Personale. I mercati ricevono simultaneamente il quadro d'inflazione e di domanda.

Core PCE annualizzato a 3 mesi: più tempestivo dello YoY. È la metrica di tendenza preferita dalla Fed.

Segnale: Core PCE sopra 2.5% in modo sostenuto = Fed hawkish. Focalizzarsi sull'annualizzato a 3 mesi, non solo YoY.

---

### Aspettative di Inflazione — Il Segnale Più Forward-Looking

#### Breakeven di Inflazione
Derivato dallo spread tra rendimenti nominali dei Treasury e rendimenti dei TIPS della stessa scadenza.

Breakeven 10 anni = Rendimento nominale 10Y - Rendimento TIPS 10Y

Rappresenta la previsione implicita del mercato sul CPI medio nei prossimi dieci anni. È un segnale real-money: gli investitori ci mettono capitale dietro la propria visione.

Range normale: 2.0-2.5%
Livelli di attenzione:
- Sopra 3%: mercato teme perdita di credibilità della Fed
- Sotto 1.5%: preoccupazioni deflazionistiche dominanti

I breakeven reagiscono rapidamente alle variazioni del prezzo del petrolio, agli shock geopolitici e alla comunicazione della Fed.

Segnale: Breakeven in rialzo + rendimenti reali in calo = trade reflazionistico, rialzista per materie prime, EM, value.

#### Tasso Forward 5Y5Y
Misura le aspettative di inflazione per un periodo di 5 anni che inizia fra 5 anni. È il tasso "far forward" che depura il rumore di breve termine legato a energia e shock di offerta.

Le aspettative di breve termine fluttuano con il prezzo delle materie prime. Il 5y5y è un segnale più puro di quanto il mercato ritenga che la banca centrale raggiungerà il suo obiettivo di lungo periodo.

Presidenti della Fed e della BCE citano regolarmente il 5y5y come verifica della credibilità nelle conferenze stampa. Un movimento sostenuto sopra il 2.5% viene trattato come un'emergenza di politica monetaria.

Il 5y5y è anche un input nelle valutazioni degli asset rischiosi: un'ancora di inflazione stabile supporta premi al rischio più bassi e multipli azionari più elevati.

Segnale: 5y5y sopra 2.5% per mesi = mercato prezza inflazione strutturale. La Fed deve dare priorità alla credibilità sulla crescita.

#### Aspettative da Sondaggi
Fonti principali: Università del Michigan (UoM) aspettative a 1 anno e 5-10 anni, Conference Board, SPF (Survey of Professional Forecasters).

Le aspettative possono essere autoavveranti:
- Lavoratori che si aspettano inflazione al 5% chiedono aumenti del 5%
- Le aziende anticipano crescita dei costi e prezzano di conseguenza
- Questo può cristallizzare la stessa inflazione che si temeva

La Fed monitora esplicitamente le aspettative a 5-10 anni della UoM come segnale di de-ancoraggio. Se salgono stabilmente sopra il 3%, scatta una risposta più aggressiva.

Divergenza da monitorare: quando le aspettative dai sondaggi e quelle di mercato divergono, segnala asimmetria informativa.

Segnale: Aspettative dei consumatori elevate = la Fed deve agire aggressivamente per ristabilire la credibilità. Rischio stile Volcker.

---

## 3. Mercato del Lavoro

### NFP, Tasso di Disoccupazione e Salari Medi Orari

#### NFP — Non-Farm Payrolls
Pubblicato il primo venerdì di ogni mese dal BLS. L'NFP è il dato USA più atteso: rivaleggia con il CPI per impatto immediato sui mercati.

Misura i posti di lavoro netti creati o persi nell'economia non agricola.

Oltre il dato headline:
- Revisioni: spesso contano quanto il dato corrente
- Full-time vs part-time: qualità della creazione di occupazione
- Tasso di partecipazione: lo slack "nascosto" nel mercato del lavoro
- Ore settimanali medie: leading indicator sull'utilizzo della forza lavoro

NFP costantemente sopra +200k con disoccupazione bassa = mercato del lavoro troppo teso per la Fed.

Segnale: NFP ben sopra il livello neutro (~100-150k) + salari caldi = Fed rimane restrittiva. Rendimenti breve termine elevati.

#### Tasso di Disoccupazione (U3/U6)
U3: il tasso headline. Disoccupati che cercano attivamente lavoro come percentuale della forza lavoro.
U6: la misura più ampia. Aggiunge i part-time per ragioni economiche e i lavoratori scoraggiati.

Regola di Sahm — segnale di recessione affidabile:
Quando la media a 3 mesi del tasso di disoccupazione sale di 0.5pp rispetto al minimo degli ultimi 12 mesi, storicamente la recessione è già iniziata. Si è attivata prima di ogni recessione USA dal 1970 senza falsi positivi.

Doppio mandato della Fed: non può semplicemente tollerare la crescita della disoccupazione per combattere l'inflazione. Quando l'U3 inizia a salire significativamente, il calcolo si sposta verso il taglio dei tassi.

Tasso naturale (NAIRU): circa 4-4.5%. Al di sotto il mercato del lavoro è considerato teso.

Segnale: Regola di Sahm attivata = segnale di recessione quasi certo. La Fed inverte rotta. Duration e difensivi outperformano.

#### Salari Medi Orari
Misura la crescita salariale annua nell'economia USA. È il collegamento più diretto e persistente tra le condizioni del mercato del lavoro e l'inflazione dei servizi.

Rischio spirale salari-prezzi: crescita salariale sopra il 4-4.5% costringe le aziende ad aumentare i prezzi per difendere i margini o ad accettare la compressione degli stessi.

Tracker salariali più precisi:
- Atlanta Fed Wage Tracker: segue gli stessi individui nel tempo; chi cambia lavoro supera chi resta di 2-3pp
- Employment Cost Index (ECI): trimestrale, copre salari + benefici
- Unit Labour Costs: salari corretti per produttività, il vero driver d'inflazione

La produttività è determinante: salari al 4% + produttività al 2% = solo 2% di pressione reale sui costi unitari.

Segnale: Crescita salariale > 4% + produttività piatta = inflazione dei servizi persistente. Il pezzo più difficile da raffreddare.

---

## 4. Politica Monetaria

### Decisioni sui Tassi, FOMC e Dot Plot

#### Decisioni sui Tassi di Riferimento
Il tasso sui federal funds (Fed), il tasso sui depositi (BCE) e il bank rate (BoE) sono le ancore globali della struttura dei tassi. Ogni classe di attivo è prezzata rispetto a questi tassi.

Canali di trasmissione:
- Attualizzazione: tassi più alti → valore attuale dei cash flow futuri più basso → titoli growth perdono molto valore
- Credito bancario: i tassi si trasmettono a mutui, credito corporate e prestiti al consumo
- Valuta: i differenziali di tasso guidano i flussi di capitali e i cambi FX
- Carry trade: i gap tra tassi generano posizioni su EM e G10

I mercati prezzano la decisione in anticipo tramite i futures sui Fed Funds e gli OIS swap. È la componente di sorpresa a generare la volatilità effettiva. Anche una decisione invariata può essere hawkish se il mercato si aspettava un taglio.

Segnale: Non è mai il tasso in sé, ma il divario tra ciò che era prezzato e ciò che è stato consegnato a muovere i mercati.

#### Comunicati FOMC e Verbali
Il comunicato FOMC accompagna ciascuna delle 8 riunioni annuali. I verbali vengono pubblicati 3 settimane dopo. Entrambi vengono analizzati parola per parola dai desk di tassi di tutto il mondo.

Segnali hawkish:
- "L'inflazione rimane elevata"
- "Impegno al target del 2%"
- "Politica restrittiva per qualche tempo"

Segnali dovish:
- "Il mercato del lavoro si sta raffreddando"
- "L'inflazione si sta avvicinando al target"
- "I rischi sono bilanciati"

La conferenza stampa del Presidente segue immediatamente: il tono e le risposte a braccio spesso contano più delle dichiarazioni preparate.

Un cambio di linguaggio da hawkish a neutrale equivale a un movimento di 50-75 bps sui rendimenti a 2 anni.

Segnale: Non leggere solo la decisione. Leggere il comunicato. Poi la conferenza stampa. Il percorso conta più della destinazione.

#### Il Dot Plot
Pubblicato trimestralmente con il Summary of Economic Projections (SEP). Mostra la previsione anonima di ciascun membro del FOMC sul tasso di riferimento nei successivi 3 anni e nel lungo periodo.

Non è un impegno, ma il mercato tratta il punto mediano come un forte segnale di forward guidance.

Dot di lungo periodo (tasso neutrale / R*): il tasso a cui la politica non è né stimolativa né restrittiva. Attualmente stimato intorno al 2.5-3.0%.

I cambi del dot plot tra una riunione e l'altra possono generare movimenti di 40-60 bps sui Treasury a 10 anni e del 5-10% sugli indici azionari.

Asimmetria hawkish/dovish: contare i punti sopra vs sotto la mediana per la distribuzione delle opinioni nel comitato.

Segnale: Dot plot rivisto al rialzo = meno tagli attesi = spike dei rendimenti reali = de-rating dei titoli growth.

---

## 5. Liquidità

### M2, QE/QT e Reverse Repo — L'Idraulica della Liquidità

#### M2 — Offerta di Moneta
M2 = M1 (contante + depositi a vista) + depositi di risparmio + fondi monetari + depositi a termine minori.

Collegamento con la teoria quantitativa: crescita di M2 costantemente superiore alla crescita del PIL nominale implica eccesso di moneta rispetto ai beni, pressione inflazionistica eventuale.

Case study post-2020: espansione di M2 +25% in 12 mesi è stato il segnale anticipatore più chiaro della fiammata inflazionistica del 2021-22, visibile oltre un anno prima del picco del CPI.

Contrazione di M2: il calo YoY del 2022-23 è stato il primo dai tempi della Grande Depressione degli anni 30. Un raro segnale deflazionistico.

La velocità di circolazione conta: crescita M2 in accelerazione + velocità in aumento = effetto moltiplicatore inflazionistico.

Segnale: Crescita M2 significativamente sopra il PIL nominale = segnale di inflazione con 12-18 mesi di anticipo.

#### Quantitative Easing e Tightening
QE (Allentamento Quantitativo): la banca centrale acquista obbligazioni e MBS, iniettando riserve nel sistema bancario. Comprime i rendimenti a lungo termine, favorisce il ribilanciamento verso asset più rischiosi e supporta la capacità di credito delle banche.

QT (Inasprimento Quantitativo): i titoli in scadenza non vengono reinvestiti (passivo) o vengono venduti attivamente. Le riserve si riducono, la liquidità bancaria si contrae e i rendimenti a lungo termine subiscono una pressione al rialzo.

Il bilancio Fed ha raggiunto il picco di ~9 trilioni nel 2022. Il QT ne ha ridotto più di 1.5 trilioni.

Asimmetria fondamentale: il QT funziona lentamente fino a quando non smette di farlo. Lo stress sul mercato repo del settembre 2019 ha costretto la Fed a invertire rotta quando le riserve sono scese troppo.

Segnale: Rialzi dei tassi + QT simultanei = doppio inasprimento. Le condizioni finanziarie si contraggono più velocemente dei modelli.

#### Reverse Repo e Liquidita di Sistema
Reverse Repo Overnight (ON RRP): strumento con cui la Fed drena le riserve in eccesso. Banche e fondi monetari parcheggiano liquidità overnight presso la Fed.

Saldi RRP elevati (oltre 2 trilioni nel 2022-23) = liquidità in eccesso enorme nel sistema.

Soglia critica: quando l'RRP si avvicina a zero, l'ulteriore drenaggio di riserve impatta direttamente le riserve bancarie, più dirompente, storicamente coincide con stress del mercato repo.

Trinità della Liquidità da monitorare ogni settimana:
- Bilancio Fed: in contrazione = drenaggio
- TGA (Treasury General Account): i prelievi iniettano liquidità, le ricostruzioni la drenano
- RRP: in calo = liquidità che fluisce verso i mercati

Liquidità netta = Bilancio Fed - TGA - RRP

Segnale: Liquidità netta in calo = vento contrario per gli asset rischiosi anche se i tassi sono invariati. Monitorare settimanalmente.

---

## 6. Mercato Immobiliare

### Nuove Costruzioni, Permessi Edilizi e Vendite di Case

#### Nuove Costruzioni e Permessi Edilizi
Le nuove costruzioni (Housing Starts) misurano i cantieri residenziali avviati nel mese. I permessi edilizi (Building Permits) sono la controparte forward-looking: vengono rilasciati prima che inizi qualsiasi lavoro.

L'immobiliare è il settore più sensibile ai tassi d'interesse nell'intera economia. Quando la Fed alza i tassi, i costi dei mutui salgono nel giro di settimane.

Catena di trasmissione della politica monetaria:
- Permessi anticipano i cantieri di 1-2 mesi
- Cantieri anticipano l'occupazione edilizia di 3-4 mesi
- Occupazione edilizia anticipa l'inflazione dei servizi
- L'inflazione dei servizi alimenta il Core CPI con 18 mesi di ritardo

Il crollo del settore nel 2022 (cantieri in calo del 30%) è stato uno dei primi segnali visibili che i rialzi della Fed si stavano trasmettendo all'economia reale.

Segnale: Permessi in crollo = freno al PIL nei prossimi 6-9 mesi + futura disinflazione sugli affitti, ma solo 12-18 mesi dopo.

#### Vendite di Case e Indici dei Prezzi
Vendite di Nuove Case: forward-looking (contratti firmati, non rogiti), direttamente legate all'attività dei costruttori e alla sensibilità ai tassi in tempo reale.

Vendite di Case Esistenti: il grosso del mercato (~5-6 milioni di unità/anno). Un "effetto lock-in" critico è emerso post-2022: i proprietari con mutui al 3% sono bloccati, vendere e riacquistare al 7%+ è proibitivo. Questo vincola l'offerta e mantiene i prezzi elevati anche quando la domanda si indebolisce.

Indice Case-Shiller: misura l'apprezzamento dei prezzi nelle principali 20 aree metropolitane. Alimenta il calcolo dell'OER con un ritardo di 12-18 mesi, rendendolo essenziale per prevedere la futura componente affitti del CPI.

Formula dell'accessibilità: REDDITO / (PREZZO CASA x TASSO MUTUO)

Segnale: Effetto lock-in = offerta strutturalmente bassa = prezzi elevati = componente affitti del CPI persistente a lungo.

---

## 7. Mercati Obbligazionari

### Curva dei Rendimenti, Rendimenti Reali (TIPS) e Term Premium

#### Curva dei Rendimenti — Spread 2Y-10Y
La curva dei rendimenti rappresenta i tassi Treasury su tutte le scadenze. Lo spread 2Y-10Y è il segmento più monitorato, normalmente positivo.

Forme della curva:
- Normale (ripida): crescita attesa, politica accomodante
- Piatta: incertezza, inasprimento monetario
- Invertita (2Y > 10Y): ha previsto ogni recessione USA dal 1955 con 12-18 mesi di anticipo

L'inversione del 2022-23 è stata la più profonda in 40 anni (oltre -100 bps).

Da monitorare anche: spread 3M-10Y (modello di probabilità di recessione della Fed di New York). Quando si inverte e poi inizia a irripidirsi in rialzo, l'inizio della recessione è tipicamente vicino.

Zona di pericolo: inversione > 6 mesi seguita da rapido irripidimento è il segnale storico più affidabile di recessione imminente.

Segnale: Inversione poi rapido irripidimento = recessione imminente. Il dis-irripidimento spesso segna l'inizio, non la fine.

#### Rendimenti Reali — TIPS
I rendimenti TIPS rappresentano il tasso di rendimento reale privo di rischio dopo aver depurato la componente inflazionistica. Misurano il vero costo opportunità del capitale.

Rendimento Reale = Rendimento Nominale - Breakeven di Inflazione

I titoli growth sono così sensibili perché sono asset a lunga duration: la maggior parte del loro valore risiede in cash flow lontani nel futuro. Rendimenti reali più alti aumentano il tasso di sconto, comprimendo il valore attuale.

Case study: il crollo del NASDAQ nel 2022 (-35%) ha coinciso con la salita del TIPS a 10 anni da -1.0% a +1.5%, uno spostamento di 250 bps nel tasso di sconto reale.

L'oro non paga cedole, quindi il suo rendimento implicito è il negativo del tasso reale. Rendimenti reali in rialzo → oro cala.

Segnale: TIPS a 10Y sopra il 2% = tasso reale altamente restrittivo. Titoli growth e oro sotto massima pressione di valutazione.

#### Term Premium
Il term premium è il rendimento aggiuntivo che gli investitori esigono per detenere un'obbligazione a lungo termine: compensazione per l'incertezza sui tassi, il rischio di inflazione e l'illiquidità dell'impegno a lungo termine.

Stimato da modelli (il modello ACM della Fed di New York è il più citato).

Contesto storico: per gran parte del 2012-2021, il term premium è stato negativo. Il QE lo ha artificialmente compresso. Il suo ritorno in territorio positivo nel 2023 (+100 bps) ha guidato gran parte del rialzo dei rendimenti a lungo termine.

Canale del rischio fiscale: quando i deficit pubblici e l'emissione di debito preoccupano i mercati, il term premium sale.

Segnale: Term premium elevato = correlazione bond-equity diventa positiva. Il classico portafoglio 60/40 perde la sua copertura.

---

## 8. Condizioni del Credito

### Spread Creditizi e Financial Conditions Index

#### Spread Creditizi — IG e High Yield
Gli spread creditizi misurano il premio di rendimento richiesto per detenere obbligazioni corporate rispetto ai Treasury. Sono il barometro in tempo reale del rischio di default percepito e della propensione al rischio aggregata.

Investment Grade (BBB- e superiori): tipicamente 50-200 bps.
High Yield / Junk (BB e inferiori): tipicamente 300-700 bps in mercati normali, oltre 1000 in crisi.

Segnali:
- Spread in compressione = risk-on, condizioni creditizie facili
- Spread in allargamento = stress in costruzione, spesso anticipa i ribassi azionari di 4-8 settimane
- HY anticipa IG: lo stress si manifesta sempre prima sulla carta di qualità inferiore

Strumenti chiave: CDX IG e CDX HY (USA), iTraxx Main e iTraxx Xover (Europa) per il pricing CDS.

Contano sia i livelli che la velocità del movimento. Un allargamento di 50 bps in una settimana è più allarmante di 100 bps in sei mesi.

Segnale: Spread HY sopra 600 bps = elevato rischio di recessione/default. Mercati che prezzano stress corporate significativo.

#### Financial Conditions Index (FCI)
Un indice composito che aggrega la tensione o l'allentamento nell'intero sistema finanziario: prezzi azionari, spread creditizi, livelli valutari, tassi a breve e lungo termine, standard di prestito bancario.

Principali fornitori: Goldman Sachs FCI, Chicago Fed NFCI, Bloomberg FCI.

Perché il FCI conta più del solo tasso di riferimento: la politica monetaria non si trasmette attraverso i tassi in isolamento. Opera attraverso l'intero sistema finanziario. Un rally azionario può "annullare" mesi di inasprimento Fed.

La Fed guarda attentamente il FCI: quando le condizioni si allentano troppo nonostante i rialzi, è necessario un ulteriore inasprimento. Quando si contraggono bruscamente, fornisce la copertura per un cambio di politica.

Interpretazione NFCI: sotto zero = accomodante, sopra zero = restrittivo, sopra +1.0 = tensione acuta.

Segnale: FCI allentato durante un ciclo di rialzi = condizioni facili che minano la politica. La Fed risponderà verbalmente o con ulteriori rialzi.

---

## 9. Valute e Materie Prime

### DXY, Tassi FX, Petrolio e Metalli Industriali

#### DXY — Indice del Dollaro
Il DXY misura la forza del dollaro USA rispetto a un paniere di 6 valute (EUR ~57%, JPY ~14%, GBP ~12%).

Il rafforzamento del dollaro ha implicazioni globali:
- Il debito denominato in dollari diventa più costoso per i mutuatari EM
- Le materie prime quotate in dollari scendono in termini locali
- Le multinazionali americane subiscono venti contrari sui ricavi esteri

Il DXY è guidato da differenziali di tasso relativi, propensione al rischio e dinamiche delle partite correnti.

Segnale: DXY sopra 105-110 = freno significativo per azionario EM, materie prime e propensione al rischio globale.

#### Tassi FX e Dinamiche Cross-Valutarie
EUR/USD è la coppia valutaria più liquida al mondo.

Lo JPY è il principale safe haven globale e valuta di finanziamento del carry trade. Un apprezzamento improvviso dello yen genera vendite forzate e simultanee di asset rischiosi globali.

I differenziali di tasso tra la Fed e le altre banche centrali sono il principale driver FX nel breve periodo. Le partite correnti e la crescita relativa contano nel medio-lungo termine.

Segnale: Rapido apprezzamento dello JPY = unwind del carry globale = vendite forzate simultanee su tutti gli asset rischiosi.

#### Petrolio — WTI e Brent
L'energia è il canale più diretto tra le materie prime e l'inflazione headline. Un rialzo di 10 dollari al barile aggiunge circa +0.3pp al CPI headline entro 2-3 mesi attraverso benzina, trasporti e costi degli input industriali.

Il petrolio riflette anche segnali di domanda globale (Brent), le decisioni di offerta dell'OPEC+ e un premio per il rischio geopolitico.

Prezzi elevati comprimono contemporaneamente il potere d'acquisto dei consumatori e i margini aziendali: una forza stagflazionistica.

Segnale: Petrolio sopra 100 dollari in modo sostenuto = rischio stagflazione. Banche centrali di fronte alla peggiore combinazione possibile.

#### Gas Naturale, Metalli e Supply Chain
Gas Naturale (TTF Europa): post-Ucraina, la sicurezza energetica è diventata una variabile geopolitica e macroeconomica. La competitività industriale europea dipende dai prezzi del gas.

Metalli industriali (Rame, Alluminio): il "Dottor Rame" è un proxy della crescita globale in tempo reale. Un calo del rame superiore al 20% ha storicamente segnalato rallentamenti globali.

Oro: proxy dei rendimenti reali, safe haven e strumento di diversificazione delle riserve. Guidato dai tassi reali e dal dollaro.

Segnale: Rame + petrolio in calo simultaneo = rallentamento globale sincronizzato. Attenzione recessione elevata.

---

## 10. Volatilità e Rischio

### VIX e Indice MOVE — I Termometri della Paura dei Mercati

#### VIX — Indice di Volatilità CBOE
Il "Termometro della Paura": misura la volatilità implicita a 30 giorni delle opzioni sull'S&P 500.

Livelli chiave:
- VIX sotto 15: compiacenza, mercati calmi, risk-on
- VIX 15-25: normale incertezza, posizionamento moderato
- VIX 25-35: paura elevata, potenziale stress di mercato
- VIX sopra 40: crisi acuta (Covid 2020: 85, GFC 2008: 80)

Insight contrarian: i picchi estremi del VIX sopra 40 hanno storicamente segnato minimi di mercato nel breve termine. Quando tutti sono al massimo della paura, i venditori marginali sono esauriti. Il trade "compra il picco del VIX" ha un solido track record storico.

Struttura a termine dei futures VIX: contango (normale) vs backwardation (paura acuta di breve termine) distingue lo stress temporaneo da quello strutturale.

Segnale: Picco VIX sopra 40 + rapporto put/call estremo = panico massimo. Storicamente uno dei migliori segnali di ingresso sull'azionario.

#### Indice MOVE — Volatilità Obbligazionaria
L'indice MOVE (Merrill Lynch Option Volatility Estimate) è l'equivalente del VIX per il reddito fisso. Misura la volatilità implicita delle opzioni sui Treasury USA a 2, 5, 10 e 30 anni.

Perché il MOVE è diventato cruciale post-2022:
- La volatilità dei tassi è diventata il principale driver delle correlazioni cross-asset nel ciclo 2022-24
- MOVE elevato = profonda incertezza sul percorso dei tassi = difficoltà nel valorizzare qualsiasi asset
- Quando il MOVE sale, la tradizionale correlazione negativa bond-equity si rompe: entrambi gli asset scendono simultaneamente

Contesto storico 2022-23: il MOVE ha raggiunto i livelli di crisi del 2008, riflettendo il ciclo di rialzi senza precedenti da 0% a 5.25% in soli 18 mesi.

Rapporto MOVE/VIX: quando la volatilità obbligazionaria supera quella azionaria, il rischio macro domina il rischio specifico d'impresa.

Segnale: MOVE sopra 140 = estrema incertezza sui tassi. La costruzione di portafoglio si inceppa. La copertura multi-asset è costosa.

---

## 11. Flussi e Posizionamento

### Flussi ETF/Fondi e CFTC Positioning

#### Flussi ETF e Fondi Comuni
I flussi settimanali in entrata e in uscita da ETF azionari, obbligazionari e su materie prime rivelano il comportamento aggregato degli investitori e la propensione al rischio in tempo quasi reale.

Principali fonti: ICI (Investment Company Institute), EPFR Global, Bloomberg.

Pattern e segnali chiave:
- Afflussi record nell'azionario vicino ai picchi = classico indicatore contrarian
- Afflussi sostenuti negli ETF settoriali = rischio di crowding, possono accelerare i movimenti ma anche invertirsi violentemente
- Deflussi dai fondi obbligazionari durante i cicli di rialzo = pressione di vendita strutturale sulla duration
- Flussi EM: i primi a riflettere i cambiamenti nella propensione al rischio globale

Archivio 13F trimestrale (posizioni azionarie long degli hedge fund): quadro istituzionale dettagliato con 45 giorni di ritardo.

Segnale: Afflussi retail estremi + margin debt elevato = sentiment a picco. Storicamente precede una correzione.

#### CFTC — Commitments of Traders
Pubblicato settimanalmente dalla CFTC. Il report CoT mostra le posizioni aggregate long e short sui futures: S&P 500, Nasdaq, Treasury, valute (EUR, JPY, GBP), materie prime (petrolio, oro, rame).

Categorie principali:
- Non-commerciali (Speculativi): hedge fund e grandi speculatori, il "fast money"
- Commerciali (Hedgers): produttori e consumatori che coprono esposizioni genuine
- Non-reportable (Piccoli Speculatori): proxy del sentiment retail, spesso sbagliato agli estremi

Applicazione contrarian: quando il posizionamento speculativo è estremamente unilaterale (oltre 2 deviazioni standard), il rischio di crowding è severo. "Chi vuole comprarlo lo ha già comprato", il compratore marginale scompare.

Metodo Z-score: (posizione netta corrente - media 3 anni) / deviazione standard 3 anni. Z > 2.0 = posizionamento affollato.

Segnale: CFTC netto short estremo = setup per short squeeze, acquisto contrarian. Netto long estremo = crowding, fade del movimento.

---

## 12. Driver Azionari

### EPS, Revisioni degli Utili e Guidance del Management

#### EPS — Utile per Azione
Il driver fondamentale del prezzo azionario nel lungo periodo.

Formula: Prezzo Azione = EPS x Multiplo P/E

La crescita degli utili è l'ancora dei rendimenti azionari su qualsiasi ciclo completo. L'espansione/contrazione dei multipli è temporanea; gli EPS si compongono nel tempo.

Earnings season (4 volte l'anno): le società dell'S&P 500 riportano rispetto al consenso degli analisti. Storicamente circa il 70% batte le stime.

Decomposizione degli EPS:
- Crescita dei ricavi (top line)
- Espansione/compressione dei margini
- Buyback (riduce il denominatore)

In un rallentamento: i ricavi rallentano per primi, poi i margini si comprimono, creando un doppio freno. La "recessione degli utili" (2 trimestri di calo EPS YoY) tipicamente segue il rallentamento economico di 2-3 trimestri.

Segnale: Rischio recessione degli utili = calo ricavi + compressione margini simultanei. I multipli P/E si contraggono in parallelo.

#### Revisioni degli Utili
Le revisioni delle stime degli analisti sono più potenti dei livelli assoluti degli EPS nel determinare la performance azionaria nel breve termine. La direzione e il momentum delle revisioni guidano sistematicamente i rendimenti dei titoli.

Ampiezza delle revisioni: la percentuale di titoli con revisioni al rialzo vs al ribasso è un indicatore della salute macro. Ampiezza negativa = recessione degli utili in avvicinamento.

NTM EPS (Next Twelve Months): il benchmark degli utili forward standard. Ma incorpora un bias sistematico di ottimismo: gli analisti storicamente iniziano troppo in alto.

Trappola di valutazione critica: quando le stime NTM scendono mentre i multipli si espandono, si ottiene un "P/E sulla speranza". Il mercato paga di più per meno. Questo è lo scenario ad alto rischio.

NTM EPS anticipa i mercati di circa 1-2 mesi: monitorare le revisioni, non solo i prezzi.

Segnale: Stime NTM in calo + multipli P/E in espansione = il setup azionario più pericoloso. Alto rischio di contrazione dei multipli.

#### Guidance del Management
Le indicazioni del management su ricavi, margini ed EPS futuri possono essere il driver più rilevante e sottovalutato. Definisce il baseline del consenso degli analisti per il trimestre successivo.

Perché la guidance conta oltre i numeri:
- Il management ha la migliore lettura in tempo reale del portafoglio ordini, del potere di prezzo e dei costi
- Una guidance cauta da parte di aziende benchmark invia segnali a tutto il settore
- FedEx = domanda logistica globale, TSMC = ciclo dei semiconduttori, JPMorgan = salute del credito, Walmart = salute del consumatore

Pattern:
- Guidance conservativa + beat = il titolo outperforma
- Guidance aggressiva + lieve beat/miss = punizione severa
- Guidance ritirata = de-rating massimo

Ascoltare il linguaggio sui prezzi nelle conference call: "volumi stabili ma prezzi tagliati per mantenere quota" = compressione dei margini in arrivo.

Segnale: Taglio guidance di un'azienda benchmark = segnale macro più forte del miss sugli EPS. Implicazioni per tutto il settore.

---

## Il Framework Analitico

Nessun indicatore vive in isolamento. Il vantaggio analitico si costruisce leggendo le connessioni.

PIL + CPI + Lavoro + Politica + Liquidità = il regime macro. Tutto il resto è contesto.

### 1. Crescita + Inflazione prima
PIL, PMI e CPI definiscono il regime macro. Il regime determina l'asset allocation.

### 2. La politica segue i dati
Fed e BCE reagiscono a lavoro e inflazione. Imparare ad anticipare la loro prossima mossa.

### 3. La liquidità guida la magnitudine
I tassi danno la direzione; la liquidità determina la dimensione dei movimenti. Monitorare i bilanci.

### 4. Il posizionamento è il catalizzatore
I trade affollati si invertono violentemente. CFTC + flussi = il livello di gestione del rischio.

---

## Note operative per il trading agent

Questi indicatori definiscono il **regime macro** che il desk Analyst Research deve interpretare. Principio (Luca): all'agente si dà *"questa metrica ti indica questo"*, **non** *"usa questa metrica per questo"* — è l'agente a imparare come combinarle. Vedi [[strategy/questions-for-salvatore]] §6.

**Fonte dati**: FRED (gratuito, 800k+ serie storiche) per PIL, tassi, inflazione, occupazione, M2. Alpha Vantage per dati macro US. Vedi [[system/data-providers]] per la mappatura completa.
