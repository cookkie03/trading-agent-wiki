---
title: Frontend Module
type: build
tags:
  - frontend-module
  - architecture
  - software
created: 2026-06-23T00:00:00.000Z
updated: 2026-11-12
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
