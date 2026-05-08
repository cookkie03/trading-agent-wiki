# Trading System

Trading System significa individuare un approccio al mercato completato di tutti i dettagli.

### **PROGETTAZIONE**

Pianifichiamo: 

- **Orizzonte temporale** di riferimento (lungo termine o breve termine)
- **Capitale allocato**
- **Rischio allocato RR**: in base alla gestione operativa
- **L’Entry placement**: entry ed exit della mia strategia.
- Tutti i **Setup**: solo avendo bene in mente tutti Setup che sto seguendo ed applicando potrò valutarne l’efficienza in fase finale.
- **Contesto** nel quale applicare la mia strategia: considerando strategie simili che hanno avuto o avrebbero avuto successo in determinati contesti nel passato, quella che voglio applicare oggi in quale situazione funziona? Quando la volatilità è alta? Funziona nei periodi Ranging? O di Trending? Funziona meglio sulle cripto? Altcoin? Bitcoin? E così via.
- **Gestione del drawdown**: identifica la perdita massima del mio capitale. Devo calcolare una serie di possibili perdite per capire qual è il mio massimo rischio di perdita. Quanto è aggressivo il mio trading?

### **BACK TEST** – test sui dati storici per verificare l’efficienza

Individuata una strategia o una serie di strategie, dobbiamo immedesimarci nel contesto in cui possiamo testare quella determinata strategia, ovvero **valutare se ha funzionato in altri scenari simili**, oltre al singolo momento.
**Manca la componente emotiva.**

> All’inizio bisogna semplificare
> 

Utilizzare lo **storico** di un asset (importanti gli ultimi 6 mesi circa per il medio-breve termine) per la messa alla prova di una strategia.

La **strategia ci convince** di più quando: 

- il **profitto netto è buono su un intervallo di tempo ampio** (circa 50 o 100 campioni)
- **l’intervallo di campioni è consistente** (più situazioni selezionate hanno avuto esito positivo e più è affidabile la strategia)
- il **drawdown massimo è il minore possibile** (diventa più sostenibile a lungo termine)
- la **frequenza di operazioni necessarie è compatibile con l’impegno** che voglio allocare al trading.

### **TEST** – test in real time, il Trading System è attivo ma a capitale ridotto

Entra in gioco la **componente emotiva.**
Fare è un **passaggio graduale** per capire se sono in grado effettivamente di gestire il Trading System; partire con poco capitale a rischio e amentarlo gradualmente fino al pieno regime.

Valutazione, ed **incremento graduale** del capitale rischiato fino ad arrivare a regime.

- Esempio: **Parto da X%** del **rischio nominale Y**
- Ogni periodo (W? M?) di risultati soddisfacenti, **incremento di uno step di Z%**
- Arrivato **al 100%, la fase di test termina** e la strategia è in prod.
- X, Y, Z variabili in base a “rischiosità” del TS e risultati

### **MESSA IN ATTO**

Fase in cui è necessario **controllare maggiormente il risk management**, anche modificando i parametri del Trading System quando serve.

**Gestire il rischio in itinere** con il Trading System in produzione è possibile tramite due metodi:

1. **Rischio fisso**: definisco un rischio per ogni posizione. Anche questo può essere modificato: se il Setup è particolarmente performante posso allocare più R.
2. **Lottizzazione** del capitale: si adatta bene con Trading System a lungo termine. Il TS va a lavorare su un lotto del mio capitale e non sulla totalità.
    - Ottimo per trade swing/trend follower
    - Capitale diviso in lotti, **il TS lavora su un lotto**
    - In base ai risultati dei trade,**il size si modifica da solo**

### Revisione di una Strategia

**Su quali elementi mi concentro?**

1. Bisogna individuare pattern di errori, su quali siano **stop loss fisiologici** per la strategia e quali invece derivanti da **errori discrezionali.**
2. Impostare un **calendario di revisione della strategia**, per vedere cosa ha funzionato e cosa no e si applicano le modalità di modifica su cosa è andato storto.

**Ogni quanto cambio elementi della strategia?**

Questo dipende dal **time frame operativo**, tendenzialmente si aspetta il completamento di un ciclo di operazioni sufficiente ad evidenziare o meno l’evoluzione del winrate:

- Sempre prendendo in considerazione 100 operazioni, uno swing trader magari impiegherà 6 mesi alla loro esecuzione, uno scalper magari solo un mese e mezzo.
- Passato il periodo predefinito, si può avere una visione più chiara su quali elementi hanno mantenuto il winrate positivo e su quali invece lo hanno penalizzato.

**Sanzioni legate alla violazione di determinati parametri della strategia** (esposizione ridotta, non entrare a mercato, donazione profitti)

---

**Gestire le serie di perdite ([Loss Management](Position%20Sizing%207e601b2c68ba45eaaa15f56670b8ca38.md))**

- Il rischio/capitale allocato va dinamicamente modificato in base ai risultati del TS
- **Evitare “Compounding Losses”**, ma ridurre il rischio dopo una serie di N perdite
    - E’ psicologicamente provante
    - Perdita di efficacia TS?
    - Dopo N perdite, **riduco il rischio** di X% per ogni ulteriore serie di Y perdite
- Lottizzazione capitale: **L’esposizione riduce da sola in caso di perdite**

**Gestire le serie di profitti ([Win Management](Position%20Sizing%207e601b2c68ba45eaaa15f56670b8ca38.md))**

- **Compounding Wins:** dopo serie di profitti, si può incrementare il rischio
    - Occhio all’euforia ed alla sovraesposizione
    - Dopo N profitti, **incremento il rischio** di X% per ogni ulteriore serie di Y profitti, fino ad un massimo di Z
- Lottizzazione del Capitale:
    - Imposizione di una **soglia**, sopra la quale il capitale in eccesso viene versato **in un altro lotto**
    - Rischio, altrimenti, che la prima Loss mangi buona parte dei profitti. (Regolarizzazione Equity Line)

---

**Sospensione di un TS**

- Qualora un TS inizi a perdere di efficacia, si può valutare la sua **sospensione** (predeterminata). Criteri di sospensione:
    - **Rendimento medio** ultimi X campioni negativo
        - Calo repentino win rate a parità R/R medio
        - Calo repentino R/R medio a parità di win rate
        - Lotto capitale ridotto a % inferiore a soglia
    - **Drawdown** massimo ultimi X campioni > soglia
    - Serie eccessivamente lunga di **perdite**
    - **Frequenza** di operatività drasticamente calata

**Loss Analysis**

- Studiare le cause di cattive performance di un TS ben funzionante, e capire dove si può migliorare
    - **Modifica SL placement?** (se spesso scatta SL “involontariamente”)
    - **Modifica TP placement?** (se spesso manca il TP di poco)
    - Introduzione **Trailing Stop o Esclusione rischio**? (se i risultati sono irregolari)
    - Esclusione di alcuni **setup** mal performanti?

- Prima di mettere in produzione un TS, valutarne le performance ed introdurlo in maniera graduale
- In base al proprio tempo a disposizione e alle proprie predisposizioni, valutare **quanti TS tenere attivi**, ed i loro parametri
- **Valutare sempre** un TS anche mentre è in produzione ed eventualmente modificarlo/sospenderlo
- Adattarsi alle condizioni del Mercato, provando sempre **nuovi TS**
- Indispensabile un **Trading Journal** per loggare i risultati dei propri trades e valutare di conseguenza