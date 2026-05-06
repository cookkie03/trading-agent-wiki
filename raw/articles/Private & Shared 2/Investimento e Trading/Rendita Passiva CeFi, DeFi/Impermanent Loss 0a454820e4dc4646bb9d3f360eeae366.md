# Impermanent Loss:

**Definizione**: **la perdita che potremmo subire fornendo liquidità rispetto al semplice hold**. Il prezzo dei singoli token nel periodo di detenzione (da quando facciamo stake a unstake del token LP) impatta la quantità di token che avremmo avuto nel wallet se avessimo holdato gli stessi token.

**Esempio**: Se 1 **ETH** valesse 4000$ e noi avessimo 4000$, volendo fare da LP nel pool **ETH/USDC**, andremmo a depositare 0,5 ETH e 2000 USDC per mantenere la proporzione 50:50 nel valore dei token.Se ETH dovesse salire a 8000$, ritirando la nostra liquidità, però, dovendo manetere la proporzione 50:50, avremmo 5650$ (0,34 ETH e 2828 USDC): il pool è stato modificato, diminuendo il numero di ETH (ora di maggior valore) e aumentando gli USDC (restato invariato). Nel caso di hold avremmo ottenuto 6000$ (0,5 ETH e 2000 USDC). In questo caso l’impermanent loss sarebbe al 5.7%. Abbiamo comunque guadagnato, ma non come se non avessimo aderito al pool.

**L’impermanent** **loss** **non è permanente finché non preleviamo i fondi**: se ETH dovesse scendere di valore, il pool si modificherebbe e il numero di ETH andrebbe aumentando. Invece, in caso di prelievo dopo importanti variazioni di prezzo di un asset, le **coin** tornerebbero nelle nostre mani e l’impermanent loss diverrebbe invece definitivo.

Come **eliminare** l’impermanent loss?

Una soluzione valida arriva dai pool di token uguali, come **Luna**–**bLuna** (un sintetico ancorato al suo prezzo), annullando l’impermanent loss.

Altrettanto buona è la scelta di pool su **stablecoin**. Un esempio? Sul 3pool su [Curve](https://thecryptogateway.it/curve/), si possono mettere **DAI**/**USDT**/**USDC**. Avendo il valore ancorato a 1$, è molto difficile subire perdite degne di nota: una delle coin dovrebbe perdere il peg e subire forti variazioni, evento alquanto improbabile.

Non esistono altre soluzioni, se non quella di tenere monitorato l’andamento e prelevare gli LP token nel caso vada avviandosi una fase molto rialzista di una delle coin del pool.