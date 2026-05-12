# Trading Journal

- Necessità di **valutazione costante** di ogni TS (anche in backtest) per:
    - Capire dove **allocare più o meno capitale** a rischio
    - Capire se **escluderne** alcuni o **includerne** nuovi
- Per fare ciò occorre:
    - Uno **standard**
        - Dimensionamento del trade in funzione di **size e stop loss**, tenendo come parametro il **capitale a rischio nominale R**
            - P/L già in termini relativi, quindi **confrontabili**
            - Ottimo per trades con Rischio e profitto predefiniti (**setup**)
            - R/R: **Rapporto tra rendimento e rischio**
            - Profitto medio e drawdown espressi **in funzione di R**
        - Per i trades senza SL predefinito (es. trend-follower), dimensionare con **capitale impiegato e % su lotto**
            - P/L relativo a lotto
            - R/R sconosciuto
    - Un **log** delle operazioni e dei risultati che rispetti lo standard, rendendoli oggettivi, valutabili e confrontabili (dati da valutare)
        - Occorre annotare più info possibili su ogni posizione:
            - **Strategia e Setup** sul quale si è operato
            - **Bias** sui diversi TF, analizzando il trend
            - Propria **situazione emotiva**: confidenza con l’apertura di posizione, dare un punteggio da -5 a +5; di fronte ad una situazione critica, abbiamo agito d’impulso o ci siamo attenuti alla strategia iniziale, anche accettando un errore?
        - Dato **cumulativo** per TS
            - R/R, Max DD, Win rate, ...
        - **Panoramica** sul portafoglio
            - Allocazione Capitale sui diversi TS, asset (piramidazione del rischio)
            - Equity Line da regolarizzare, evitare oscillamenti
        - Loggare, a parte, anche i **trades non eseguiti**, con opportune motivazioni, simulandone i risultati
        - Valutare opportune mosse inclusive
        - In ottica migliorativa, loggare ipotetiche **variazioni** di un setup o trade reale (diversi SL/TP, …)
        - Inserire in un foglio una serie di log di operazioni correttive eseguite sulla strategia (in/out di diversi TS, riallocazioni capitale, modifica rischio ed esposizione, …)
    - Elementi che dovrebbero avere tutti
        1. **Data**: il posizionamento di un operazione per dare un ordine cronologico al diario e per dividere l’anno di trading in funzione delle nostre necessità, di revisione o ribilanciamento.
        2. **Sessione operativa e orario:** ricordiamoci che siamo ancora i fratelli minori dei mercati regolamentati, da dove provengono i grandi soldi, non sarà perciò difficile notare, in concomitanza delle aperture, aumenti di volatilità.
        3. **Asset**: Ogni asset su cui conduciamo delle operazioni dovrebbe avere una trade list personale, in quanto ognuno ha delle caratteristiche a sé stanti e alle quali la nostra strategia dovrebbe essere adattata.
        4. **Direzionalità**: La facile sintesi della direzionalità preferita può essere utile nell’individuazione di bias emotivi, dipende molto anche dalla tipologia di strategia, se si cercano i minimi di mercato per eseguire swing rialzisti, è chiaro che la direzionalità sarà spesso Long e viceversa; in una strategia equilibrata, il rapporto tra long e short dovrebbe essere equilibrato.
        5. **Prezzo di entrata/uscita**: Importante per poter avere un visione a posteriori dei vari livelli in cui l’asset è stato scambiato.
        6. **Link trade TW**: Fondamentale per avere una visione immediata delle condizioni in cui è stata svolta l’operazione.
        7. **RR pianificato:** abbiamo detto che questo valore deve essere predeterminato, se gli RR effettivi corrispondono a quelli pianificati vuol dire che si sta seguendo la strategia, mentre se gli effettivi sono minori o maggiori a quelli pianificati, forse dal punto di vista emotivo (fear and greed) si potrebbe applicare qualche miglioramento
        8. **Gestione operativa pianificata**: rende spesso una strategia profittevole, leggere [qui](https://thecryptogateway.it/gestione-operativa/)
        9. **Punti checklist:** quali? quanti? questo è un elemento cruciale nella fase di backtest e ci permette di avere dati sull’efficacia della nostra checklist
        10. **Esito del trade:** come è andato effettivamente il trade? ha seguito la nostra analisi? è andato a stop? a che % è arrivato dal take profit prima di invertire e tornarmi contro? Queste, e molte altre, sono tutte domanda che è solito porsi il trader che vuol portare la sua strategia sempre ad uno step successivo, e che spesso lo rendono profittevole indipendentemente dalle variazioni nelle logiche di mercato
        11. **Note con spunti di miglioramento:** in questa sezione vanno inserite sia le indicazioni operative legate a determinati aspetti migliorabili, derivati da errori o da supposizioni che bisogna testare, ma è anche utile avere traccia delle proprie condizioni emotive legate al trade: avere una visione a posteriori delle condizioni emotive in cui si opera permette un grande salto qualitativo dal punto di vista delle gestione emotiva.
    
    [Esempio TJ Base (a checklist)](Esempio%20TJ%20Base%20(a%20checklist)%20d07ff53b4b534f31b42906851597ee7a.csv)
    
- Analisi del TJ
    
    Chiederesi (ad esempio per il calcolo di RR e WR):
    
    - **Quante operazioni a Stop/Profit**: su una base di 100 operazioni (gestite rigorosamente con i criteri prestabiliti), si può ottenere un Winrate piuttosto affidabile.
        - Su 100 operazioni 50 sono andate a target e 50 a stop loss il mio winrate sarà del 50%, in un operatività che sia mediamente distribuita avrò 5 operazioni su 10 a target e 5 a stop.
    - Meglio utilizzare un **RR predeterminato o le PRZ ottimizzano il rendimento**? Sempre considerando 100 operazioni, avendo segnato correttamente i dati dei target, sarà la statistica a dirci se ci conviene tenere un RR fisso ad esempio 1/3 o se il prezzo mi garantisce rendimenti migliori alla chiusura di determinate strutture.
        - Su 100 operazioni, di 50 andate a Tp 1/3, 30 hanno continuato il percorso fino alla zona successiva con rendimento medio 1/5
        - La considerazione da trarre, potrebbe essere quella di scaricare parziale a 1/3 e lasciar correre il restante fino alla zona successiva con potenziale chiusura definitiva a 1/5
    - **Perché sono andate a SL**? Era troppo stretto, potevo selezionare una zona migliore, il prezzo è andato a cacciare una zona con molta liquidità. Esistono tante risposte, più sono dettagliate, più aiutanonell’individuazione di errori.
        - Su 100 operazioni delle 50 andate a SL, 10 potevano essere chiuse a BE dato che avevano dato un’iniziale escursione positiva, altre 10 operazioni sono andate a target dopo aver preso liquidità sotto una zona ovvia.