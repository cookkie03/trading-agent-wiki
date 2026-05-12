# Position Sizing

Quantità di asset che andrai ad acquistare/vendere ad ogni trade.

> Il punto di partenza per estrapolare i dati sufficienti a valutare le nostre posizioni, è il **Trading Journal.**
> 

A volte il mercato presenta **inefficienze**: può esserci *Probabilità di successo* (stimabile con il Win Rate) e R/R entrambi elevati.
Situazione a **maggior profitto potenziale**

**Criterio di Kelly:**

f = ( bp – q ) / b = [ p ( b+1 ) – 1 ] / b

- **b** = guadagno in caso di vincita (R/R)
- **p** = probabilità di vincita (Win Rate)
- **q** = probabilità di perdita (1-p)
- **f** = % di capitale ottimale per un asset da utilizzare (R)
    - Tutte le percentuali vanno traformate in decimali, da 0 a 1

**Oltre a Kelly:**

Consderare le componenti del Risk Management

- Gestione di serie di vincite o perdite

Per farlo devo eseguire un adeguamento lineare o esponenziale

**Compounding Wins:**

esempio:

- Ogni win dopo il 3° trade, rischio + 0.5R (Compounding **lineare**)
- W1, W2, W3 = R (+3R)
- W4 = 1.5R
    - L4 = -1.5R
- W5 = 2R
    - L5 = -2R
- Prima Loss = sizing di nuovo R,oppure decremento -0.5R
- **Esponenziale**: **+/-x%** ogni volta

![Immagine 2022-02-05 143149.png](Immagine_2022-02-05_143149.png)

**Cutting Losses:**

- Cutting **Esponenziale** (meglio del linere): Ogni loss dopo la 3°, riduco del 25% il rischio
- L1, L2, L3 = -R
- L4 = -0.75R
    - W4 = +0.75R
- L5 = -0.56R
    - W5 = 0.56R
- Ad ogni Win faccio un **“passo indietro”**

![Immagine 2022-02-05 143504.png](Immagine_2022-02-05_143504.png)

**Risk Management (RM) Dinamico**

- I parametri modulabili sono:
    - Decisione se **Lineare o Esponenziale**
    - **Entità** dei tagli o degli incrementi
    - **Reattività** (dopo quante W/L intervenire)
    - **Sbilanciamento** tra CW e CL
- Questo deve dipendere da:
    - Regolarità dell’**Equity Line e max Drawdown**
        - DD più basso = si può minimizzare il CL
        - DD basso ed EL regolare = si può spingere su CW
    - **Rischiosità** posizione
        - Win Rate basso, R/R alto -> consigliabile RM che impatta poco
        - Win Rate alto, R/R basso -> RM molto presente

> Usare la “**confidenza**” ed il **cuscinetto** guadagnato con serie di vincite per permettersi di rischiare un po’ di più.
**Limare la perdita** dopo averne subite altre
**Contestualizzare** nella strategia (serie di perdite è la normalità?)
>