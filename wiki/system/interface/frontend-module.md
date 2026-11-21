---
title: Frontend Module
type: build
tags:
  - frontend-module
  - architecture
  - software
created: 2026-06-23T00:00:00.000Z
updated: 2026-11-20
status: active
confidence: medium
area: software
related:
  - '[[system/foundation/codebase-architecture]]'
  - '[[system/interface/observability-dashboard]]'
  - '[[prior-art/libraries/sfc-portfolio-tracker]]'
  - '[[artifacts/project-board]]'
---

# Frontend Module

> [!important] Promemoria per la UI
> Prima di riprendere la progettazione o l'implementazione della UI del Trading Agent su GitHub, **chiedere a Giuseppe (vedi lista contatti)** un confronto e un aiuto sulla UI.

Il frontend è un modulo sostituibile e disaccoppiato dal core. La decisione MVP corrente è **React + TypeScript + Vite/npm**, con backend Python esposto tramite API applicative. La precedente ipotesi Streamlit è superata.

## Boundary e responsabilità

Il frontend è una console operativa completa. Può leggere dati e modificare, attraverso API e servizi applicativi espliciti, le configurazioni, gli state e le risorse che l'utente è autorizzato a gestire. Non incorpora direttamente la logica di dominio né contiene credenziali o segreti.

Le operazioni sono eseguite dal backend tramite contratti tipizzati, validazione server-side, autorizzazioni, audit e gestione degli errori. Le azioni che incidono su capitale o invio ordini mantengono workflow e conferme distinti: la possibilità di configurare il sistema non equivale ad autorizzare automaticamente l'esecuzione di trade.

Il frontend può includere:

- componenti UI, navigazione, viste analitiche e read model;
- editor per configurazioni, strategie, parametri, preferenze e state utente;
- gestione dei provider disponibili, connessioni, capability e stato delle integrazioni;
- controlli operativi per agenti, workflow, job e runtime;
- interazioni con API applicative per applicare modifiche e avviare azioni autorizzate;
- log, trace, audit trail, cronologia modifiche e ripristino delle versioni precedenti.

## Contratti minimi

Il cockpit deve consumare e aggiornare risorse tramite contratti applicativi stabili, non accedere direttamente a repository interni sparsi:

- portfolio snapshot;
- positions;
- cash/liquidity;
- trades e `exit_reason`;
- watchlist/universe;
- benchmark/alpha;
- decision log;
- trigger/events;
- system health;
- last run / daemon status.

Questi contratti possono essere funzioni Python, API locali o query layer, ma devono restare indipendenti dal framework UI.

## MVP corrente

**React + TypeScript + Vite/npm** con backend Python e API applicative. La UI deve essere un cockpit completo e coerente, non una semplice pagina di metriche: deve coprire tutte le funzionalità del sistema, rendere comprensibili stati operativi e fonti, e distinguere dati reali, demo, vuoti, errori e funzionalità non disponibili. Deve inoltre permettere di configurare e governare il sistema senza intervenire sul codice sorgente. La pagina [[system/interface/observability-dashboard]] definisce il dettaglio funzionale.

## Pagine del cockpit — 2026-11-20

Il motore lavora in autonomia al 100%; il cockpit è il posto di lavoro personale dell'ufficio, dove Luca entra come membro («collega jolly») quando vuole, da desktop o da telefono. Sei pagine, un solo design system. L'idea del **collega jolly** pervade tutta la UI: Luca lavora sullo stesso materiale degli agenti, con le stesse letture e scritture via Runtime (React, TypeScript, Vite, Tailwind, shadcn/ui; strumenti standard, niente stack custom):

1. **Assistente** (home): chat in linguaggio naturale con il **Bridge agent**, pari di Luca: legge tutto, parla con ogni agente dell'ufficio e usa gli stessi comandi della UI, con conferma per ciò che tocca capitale. Ora si progetta la UI/UX; l'agente si implementa dopo nel Runtime.
2. **Ufficio**: gli agenti, le loro chat (Luca le legge e ci scrive direttamente, anche senza Bridge) e lo stream dei tool che chiamano.
3. **Terminale**: pagina unica, moderna, alla maniera dei software finanziari professionali, su TradingView lightweight-charts come **ambiente principale del Technical Analyst**: prezzo, volumi, indicatori; niente order book; ordini aperti e pendenti (approvazione per gli account in manuale), agenti attivi sullo strumento, **watchlist condivisa** con gli agenti e modificabile. Ciò che un agente disegna sul grafico (livelli, trend, indicatori) compare qui; ciò che disegna Luca lo leggono gli agenti.
4. **Notizie**: l'ambiente news degli agenti, con gli stessi tool: Luca legge, filtra, seleziona e invia notizie agli agenti.
5. **Portafoglio**: come un'app bancaria desktop: statistiche, investito, allocazione, posizioni, trade, performance; sezione con le **metriche e i vincoli di rischio** che il portafoglio deve rispettare.
6. **Configurazioni**: agenti, modelli, prompt, schedule, budget, provider, account broker, DB e retention, salute del Runtime.

L'input di Luca (messaggi, notizie, disegni, watchlist) è un parere che gli agenti pesano e possono contestare; il Risk Gate resta sovrano. Direzione visiva: lo standard di ogni genere eseguito al livello dei migliori prodotti, senza metafore (scelta di Luca dopo due giri di direzioni Impeccable).

**Gap di backend** da chiudere nel Runtime prima delle pagine che li usano: letture e scritture degli ambienti per il frontend (OHLCV, indicatori, news), come fanno gli agenti; annotazioni del grafico condivise; stream delle chiamate ai tool negli eventi; storico equity; vincoli di portafoglio e configurazione modificabili via comandi; più avanti il Bridge agent. lightweight-charts disegna serie ma non ha indicatori né strumenti di disegno integrati: indicatori dal Runtime o dal nostro codice, disegni tramite primitive del grafico.

Questa decisione porta il Bridge agent (prima «Configuration & State Agent», post-MVP) dentro lo scope del cockpit.

## Prima build e rifinitura — 2026-11-21

**Gara tra modelli.** Claude Opus 5.5 e GPT 6.1 Terra hanno eseguito lo stesso handoff di shell e Terminale. Luca ha scelto la build di Opus (branch `claude/cockpit-frontend-opus-54052e`, non ancora unito a `docs/agent-restart`). È un terminale denso e completo: watchlist con autori, disegni firmati sul grafico, coefficienti dell'ordine, agenti sullo strumento, ordini pendenti con Approva e Rifiuta. La build di GPT era povera di dati e generica.

**Giudizio di Luca.** La build è valida e professionale, ma non ancora bella. Serve una rifinitura molto più curata, "Apple-like", senza liquid glass. I difetti riconosciuti:

- tutto è sullo stesso piano, grigio piatto con linee di 1 px: servono livelli (la barra laterale arretra, il contenuto avanza), meno linee e più spazio;
- la tipografia è uniforme: il prezzo deve essere grande e protagonista, le etichette devono arretrare;
- il grafico è rumoroso (etichette sovrapposte, tratteggi ovunque, griglia invadente): servono linee sottili, una griglia appena visibile e il colore solo dove serve;
- manca il movimento: transizioni, hover, pannelli che si aprono con morbidezza;
- i dettagli sono generici: pulsanti, tabelle e badge degli agenti sono quelli di default.

**Riferimenti di rifinitura** (approvati da Luca, sono l'asticella e non un aspetto da copiare):

- Robinhood Legend: terminale professionale con la cura di un'app consumer, il più vicino;
- app Borsa di macOS: come trattare grafico e numeri;
- Linear, redesign recente: densità con calma, livelli e tipografia;
- Raycast e Things 3: dettagli, movimento, materiali;
- Finder e pannelli di Xcode: barra laterale e pannelli.

Il motore del grafico resta TradingView lightweight-charts con lightweight-charts-drawing: la rifinitura cambia lo stile del grafico, non la libreria.

**Stato unico del grafico** (approvato). Quello che si vede sul grafico vive in un oggetto di dati salvato nel Runtime: ticker, timeframe, indicatori, disegni con autore e stato (attivo o barrato), note. Desktop, telefono e agenti leggono e scrivono lo stesso stato tramite comandi ed eventi. La libreria di grafici è solo una vista ed è sostituibile. Gli agenti leggono il grafico come testo compatto, non come immagine.

**Flusso di rifinitura** (Impeccable). Prima la direzione: due o tre varianti dello stesso Terminale reale, servite a Luca sul Mac, tra cui sceglie o mescola. Poi la sessione Opus applica polish, tipografia, layout e animazioni a shell e Terminale, seguiti da critique, audit e aggiornamento di `DESIGN.md`.

**Backend del Terminale.** Già integrato su `docs/agent-restart` (commit `d5beacd` e `0bb0b99`): barre, indicatori, annotazioni condivise, autore delle righe della watchlist, timeframe configurabile in `config/office.toml` (`[market] bar_timeframe`), dev server con dati finti `scripts/dev_cockpit_server.py`.

**Stile scelto: Legend.** Tra tre varianti — A Calma ispirata a Linear, B Legend ispirata a Robinhood Legend e C Borsa ispirata a macOS — Luca ha scelto B Legend. Ha approvato il risultato applicato: «così va bene». Il commit è `3167eac` sul branch `claude/cockpit-frontend-opus-54052e`, non ancora unito.

Il fondo è quasi nero. I moduli sono tessere grafite separate da 10 px. Il prezzo è grande, a 30 px. I controlli sono segmentati, gli avatar degli autori sono pieni e il grafico è senza griglia.

Il layout funziona come VS Code. La watchlist si nasconde con Ctrl/⌘ B, il pannello attività con Ctrl/⌘ Alt B e gli ordini con Ctrl/⌘ J. I pannelli si ridimensionano trascinando lo spazio tra le tessere. Il layout resta salvato nel browser.

I raggi sono concentrici: 12 px per la tessera, 8 px per il controllo, 6 px per l'elemento e 4 px per il tag. I cerchi sono riservati agli avatar e ai pallini di stato. Il sistema completo è descritto in `DESIGN.md` sul branch della build.

## UI design & build workflow

La costruzione della UI è un vero workstream del progetto, non un'attività accessoria di styling. Prima di riprendere il frontend, **chiedere a Giuseppe (vedi lista contatti)** un confronto e un aiuto sulla UI del Trading Agent su GitHub.

### Strumenti di riferimento

- **[21st.dev](https://21st.dev/)** — riferimento primario per esplorare componenti, pattern, template e temi React/shadcn, cercare componenti adatti al cockpit e integrarli nel repository. Preferire componenti con codice sorgente installabile e adattarli al design system del progetto; evitare di copiare componenti senza verificarne accessibilità, responsive behavior, dipendenze e coerenza visiva.
  - Skill ufficiali: [21st-dev/skill](https://github.com/21st-dev/skill).
  - Setup skill: `npx @21st-dev/cli install-skill`.
  - CLI: `npx @21st-dev/cli` (login/API key solo se necessario).
- **[Impeccable](https://github.com/pbakaus/impeccable)** — skill di riferimento per progettazione, implementazione e revisione critica della UI. Usarla per shape/plan prima di implementare, poi per critique/audit/polish e verifica di accessibilità, responsive behavior, gerarchia visiva, tipografia, stati e micro-interazioni.
  - Installazione skill: `npx skills add pbakaus/impeccable --skill impeccable`.
  - Licenza del progetto skill: Apache-2.0.

### Sequenza di lavoro UI

1. Raccogliere il confronto con Giuseppe e definire obiettivi, utenti, casi d'uso e direzione visuale.
2. Esaminare codebase, API e modelli di dominio; definire le superfici del cockpit, le risorse modificabili, i permessi e le priorità informative prima del codice.
3. Usare Impeccable per strutturare la direzione e il piano UX/UI; documentare decisioni e token condivisi.
4. Usare 21st.dev per cercare e selezionare componenti/pattern utili, poi adattarli e integrarli nel progetto React/TypeScript.
5. Costruire il cockpit end-to-end: navigazione e overview, portfolio, watchlist, agent/workflow observability, decision log, trades, system health, gestione provider, configurazioni, strategie, state e controlli operativi; includere stati vuoti/errore/loading e feedback delle operazioni.
6. Verificare desktop e mobile, accessibilità, interazioni, performance, coerenza e stati edge; usare Impeccable per critique/audit/polish e test automatici/manuali.
7. Registrare componenti riusati, dipendenze aggiunte, scelte visuali e limiti. Il codice finale deve restare nel repository, comprensibile e modificabile, senza dipendere da un servizio remoto per renderizzare componenti già installati.

### Evoluzione Post-MVP — Configuration & State Agent

L'agente conversazionale è **esplicitamente fuori dallo scope MVP**. Il cockpit MVP deve poter gestire le risorse configurabili tramite interfacce UI strutturate e API tipizzate; l'interazione in linguaggio naturale sarà una feature Post-MVP.

In una fase successiva, il cockpit potrà includere un agente con cui l'utente interagisce in linguaggio naturale per modificare le risorse di propria competenza, senza modificare il codice sorgente. Ambito previsto:

- configurazioni personali e preferenze operative;
- parametri, profili e strategie selezionabili;
- state utente e state applicativi esplicitamente modificabili;
- provider disponibili, connessioni, capability e priorità/fallback;
- impostazioni degli agenti, workflow e pianificazioni, entro schemi e limiti autorizzati.

Workflow obbligatorio per la fase Post-MVP: interpretare la richiesta, identificare le risorse coinvolte, mostrare un piano/diff comprensibile, validare schema e invarianti, richiedere conferma quando la modifica ha effetti rilevanti, applicare tramite API tipizzate e registrare autore, motivazione, valori precedenti/nuovi, timestamp ed esito. Supportare annullamento o ripristino quando tecnicamente possibile. Non consentire scritture arbitrarie su file, codice, prompt di sistema protetti o segreti. Le credenziali devono essere gestite da un secret manager/credential store e non restituite al modello.

L'agente conversazionale non è un terminale generico né un coding agent: può operare esclusivamente su un catalogo esplicito di azioni e risorse configurabili. Le azioni di trading e quelle finanziariamente rilevanti richiedono autorizzazioni e conferme separate.

21st.dev e Impeccable sono strumenti di supporto al design/build, non vincoli architetturali né sostituti dei contratti API, dei test o della verifica del prodotto.

## Evoluzione futura

Una UI TypeScript futura deve poter riusare gli stessi contratti:

- o tramite API HTTP locale;
- o tramite file/read model esportati;
- o tramite un service layer condiviso.

La scelta tecnica si decide quando la dashboard diventa prodotto, non nel primo harness.
