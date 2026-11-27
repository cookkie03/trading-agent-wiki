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

## Ufficio — 2026-11-22

**Cosa è.** La seconda pagina del cockpit, unita su `feat/cockpit-frontend` (ex `docs/agent-restart`) con i merge `b75a6db` (frontend) e `de6cb4b` (backend) e la correzione `6f75f78`. Scelte di Luca: panoramica più chat, più chat per agente, chiamate ai tool in blocchi espandibili, e la possibilità di scrivere agli agenti, assegnare task e vedere costi e token. Nessuna pausa degli agenti, nessun backend del Bridge, nessuna Evaluation.

**Pagine.** `/ufficio` è la panoramica: una tessera per agente con avatar, ruolo, stato (al lavoro, in attesa, inattivo), task e ticker correnti, ultima attività, costo e token di oggi; sotto, costi e token per Oggi, 7 giorni e 30 giorni; a destra, le conversazioni recenti. `/ufficio/:agent` è la vista dell'agente: agenti e chat dell'agente a sinistra, conversazione e composer al centro, chiamate ai tool dal vivo a destra. Su telefono (390 px) la panoramica diventa una lista e la vista agente ha un selettore di chat e le schede Chat e Tool.

**Contratto del Runtime.** Nuove letture `GET /v1/read/agents`, `chat_topics?agent=`, `tool_calls?agent=&cycle=&after=&limit=`, `usage?agent=&from=&to=`. Eventi SSE `chat.message`, `tool.called`, `agent.status`, scritti nella stessa transazione SQLite e pubblicati al commit, senza polling. Le chiamate ai tool hanno durata ed esito; quando la retention ne svuota il contenuto il flag `compacted` lo dichiara. `/v1/read/chat` con `limit` restituisce gli ultimi messaggi in ordine cronologico.

**Fonti oneste.** Ogni lettura della pagina è reale, ricostruita da letture reali con una nota visibile, oppure dichiarata non disponibile. Le fixture di sviluppo si attivano solo con `COCKPIT_OFFICE_FIXTURES=1` sul server Vite e non entrano nella build.

**Limiti noti.** Una chiamata ai tool compare solo quando è finita: lo stato "in corso" (`tool.started`) non è ancora emesso dal Runtime. Critique 34/40 e audit 18/20, senza P0 o P1, eseguiti in un solo contesto perché i subagenti non erano disponibili.

## Migrazione a shadcn Base UI (`@base-ui/react`) e Blocchi Ufficiali — 2026-11-24

**Cosa è.** Migrazione e modernizzazione completa del frontend (`frontend/`) adottando lo standard ufficiale **shadcn-ui con Base UI (`@base-ui/react`)**, eliminando ogni residuo di Radix UI (`0` import, pacchetto `radix-ui` disinstallato).

**Componenti, Blocchi e Architettura.**
- Tutte le primitive Radix riscritte con le controparti `@base-ui/react`: `Button`, `Separator`, `Tooltip`, `Dialog`, `Sheet`, `AlertDialog`, `Popover`, `DropdownMenu` (Menu), `ScrollArea`, `Toggle`, `ToggleGroup`, `Tabs`, `PanelTabs`, `Checkbox`, `Avatar`.
- Pulizia totale delle dipendenze: rimosso `cmdk` e il componente Command non utilizzato, eliminando `@radix-ui/react-dialog` e `@radix-ui/primitive` anche dall'albero transitivo (`0` pacchetti Radix nel lockfile).
- Controlli del Terminale rifiniti: selettore timeframe convertito a `ToggleGroup` Base UI, schede mobile adeguate a `TabsContent` con gestione accessibilità da tastiera (`Space`/`Enter`), e menu a tendina conformi al contratto `MenuGroupContext`.
- Animazioni applicative migrate a **Motion** (`motion/react` v14) con token e curve fisiche da `DESIGN.md` (`cubic-bezier(0.32, 0.72, 0, 1)`): apertura fluida Bridge via `AnimatePresence`, crescita animata delle barre di esposizione e PnL in Portafoglio, e transizioni morbide nelle chiamate tool in Ufficio, con rispetto della preferenza `prefers-reduced-motion`.
- Installati e integrati i componenti ufficiali dal registry shadcn `base-nova`: `Card`, `Badge`, `Table`, `Input`, `Textarea`, `Label`, `Alert`, `Skeleton`.
- Introdotto il blocco ufficiale **Sidebar** (`SidebarProvider`, `Sidebar`, `SidebarMenu`, `SidebarMenuButton`, `SidebarInset`, `SidebarTrigger`) per `AppShell` e navigazione Desktop/Mobile.
- Riprogettate tutte le viste dell'applicazione: Terminale (`chart-panel`, `activity-panel`, `watchlist`, `orders-dock`), Ufficio (`overview`, `pm-seat`, `proposals`, `conversation`, `desk`), e Portafoglio (`summary`, `positions`, `operations`, `risk`, `allocation`, `performance`) con blocchi `Card`, `Badge`, `Table`, `Alert` e `Skeleton`.
- Sostituite tutte le tabelle HTML grezze con shadcn `Table` (`TableHeader`, `TableBody`, `TableFooter`, `TableHead`, `TableRow`, `TableCell`).
- Eliminati tutti i controlli form nativi (`<input>`, `<textarea>`, `<checkbox>`) a favore di `Input`, `Textarea`, `Checkbox` di shadcn.
- Eliminato ogni residuo di `asChild` a favore della prop nativa `render`.
- **Palette unificata su scala di grigi**: rimossi colori casuali o sfondi ad-hoc; gerarchia visiva sobria ed elegante basata su grigi neutri, con colore riservato solo a semantiche di mercato (`up`/`down`), rischio (`destructive`/`warn`) e accento di fuoco. Iconografia unificata su `lucide-react`.
- `components.json` configurato su stile `base-nova` con base `@base-ui/react`.
- Audit tecnico Impeccable (live browser CDP + scansione statica) verificato con score **19/20 (0 P0/P1)**.
- Build locale e GitHub CI completamente verdi (`Frontend build` + `Backend tests`).

## AI Fund Design System e pagine disegnate ex ante — 2026-11-27

- **Design system**: `frontend/src/ds` (shadcn/ui vanilla su Base UI `base-vega`, blocchi AI Fund) e `docs/design-system/` nel repository `ai-fund` (ex `trading-agent`), unito su `main` con la PR #37. Regole, glossario inglese e contenuto delle pagine in `DECISIONS.md`.
- **Metodo (Luca, 2026-11-27)**: le pagine le disegna Luca insieme all'agente, non il contrario. Intervista a round (`grilling`), poi disegno nel canvas Design «AI Fund Pages» (artifact privato), validazione, solo dopo la pagina successiva. Ogni informazione mostrata oggi resta visibile o va dietro un dettaglio su richiesta (Tabs, Sheet, Dialog, Popover).
- **Conti**: il software non sa se un conto è paper o live; mostra il nome dato da Luca (→ [[system/foundation/decision-log]]).
- **Popover = azioni rapide**: liste selezionabili per cambiare (mercati, account), pulsanti per aprire link, modificare sul posto, accettare. Motivo obbligatorio, anteprima o capitale → Dialog.
- **Home (decisa, da disegnare e validare)**: `/` apre la Home, l'Assistente passa a `/assistant`. Compito: come va il fondo. Cifra principale **Total value** (posizioni a valore di mercato + cassa, in USD, qualsiasi classe di strumento) con piccola curva e selettore 1D/1W/1M. Sezioni: StatCard (Unrealized P&L, Cash vs reserve, Open risk) · **Needs you** (contatori del Briefing, 3 proposte più vecchie con Approve/Decide in stile outline, elementi per gravità Critical/Review/Info, View all) · Activity con la fila degli agenti al lavoro. AccountSwitcher in sidebar, MarketClock in top bar, pannello «Sistema» nel Popover della freshness.
- **Backend da aggiungere per la Home**: `open_risk` aggregato in `portfolio_summary`; route unica per il feed attività.
- **Assistant**: il nome «Bridge» è dismesso; agente e pagina si chiamano Assistant.
- **Deciso anche**: Q20 azioni dell'Assistant da confermare nella card Briefing di «Needs you»; Q26 Runtime irraggiungibile = tutto disattivato tranne la navigazione; Q27 Home vuota; Q28 Skeleton per sezione. Q25 Halt = Approve disattivato, Decide attivo (rimandare e rifiutare non mandano ordini).
- **Q29**: «Needs you» diventa una sola lista inbox, la più urgente in cima, con Tabs e conteggi (All · To approve · To confirm · Alerts) e due azioni per riga; sostituisce card + Briefing.
- **Scroll**: scorre solo il contenuto della pagina (e i componenti interni scorrevoli); sidebar e top bar restano ferme, sul telefono anche la barra delle tab.
- **Home telefono (P1–P7)**: stesso ordine del desktop in colonna; cifre in una card a righe; «Needs you» con tap che apre un Drawer con dettaglio e azioni; icona Assistant nella top bar mobile; orologio di mercato nel Popover della freshness.
- **Bozza viva**: il canvas mostra la bozza della pagina in corso (Home), aggiornata a ogni round; niente pagina «Today».

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
