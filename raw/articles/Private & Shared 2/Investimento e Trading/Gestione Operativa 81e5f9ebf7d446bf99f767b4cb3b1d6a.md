# Gestione Operativa

Parametri che ci permettono di **ottimizzare i risultati in maniera intelligente**:

- **Parziali**
    
    suddividere **la chiusura della nostra posizione** su diversi livelli di prezzo, prelevando parte del profitto e lasciando correre il guadagno per la restante porzione. 
    
    Tendenzialmente, i parziali si posizionano diversi punti di profitto, quando lungo il percorso dall’entry al target, ci sono **zone intermedie di probabile reazione**; possono essere predefinti rigidamente (TP messi con order llimit) o impostati accompagnando l’asset nella price action
    
- **Break-Even (BE)**
    
    Posizionare lo Stop Loss al livello di Entry, considerando anche le fees dell’operazione (quindi leggermente più in alto). 
    
    Tendenzialmente un asset che rispetta le strutture, permette questa operazione confermata la direzionalità, ma attenzione a manipolazioni e stop hunt.
    
- **Stop Profit (SP)**
    
    Posizionare il **check point** al di sotto del quale **non accettiamo di ridurre il nostro guadagno**. Alazando lo stop, ci si copre dietro la struttura dell’asset, ma attenzione perché ciò che può sembrare un inversione di trend, potrebbe essere una zona di accumulazione.
    
- **Fees**
    
    Nel trading spot le fees sono solo di apertura e chiusura operazione, mentre utilizzando strumenti derivati vanno considerate anche le fees di gestione dell’operazione. Inserirle nel TJ
    

Tipologie di gestione operativa:

- **Gestione Statica**
    
    Ogni trade, dall’inizio alla fine, segue un percorso immutabile. Sono **prestabiliti il prezzo di ingresso e d’uscita**, si entra con la totalità dell’esposizione prevista e a target si chiude l’intera operazione;
    
    Molto utilizzata nelle fasi iniziali di applicazione della strategia e utile per il trader che ha **poco tempo per stare a grafico.**
    
- **Gestione Dinamica**
    
    Si adatta alle risposte del mercato
    
    - Introduzione di **profitti parziali** posizionati a RR fissi o in zone di potenziale inversione
    - **Azzeramento del rischio** mettendo stop a BE nel momento in cui si crea la prima rottura strutturale
    - Utilizzando il **Trailing Stop,** proteggendoci dietro la struttura, trovando cos’ il rendimento ottimo per ogni movimento intercettato, uscendo da mercato solo nel momento in cui il prezzo risponde negativamente alla nostra analisi (previa dimostrazione statistica).
- **Gestione Ibrida**
    
    Usatat da trader esperti con **molto tempo** a disposzione
    
    Ogni qual volta che il prezzo arriva in **zone identificate** come potenzialmente reattive, **valutiamo la reazione del prezzo**, attendendo chiusure nei time frame di riferimento e decidendo se e quanto scaricare e come muovere lo SL. (Utilizzare gli alert)