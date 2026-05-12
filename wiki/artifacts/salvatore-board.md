---
kanban-plugin: basic
---

## 💡 Idee di mercato

- [ ] **Strategia Sentiment degli Analisti** — capire il *perché* del consenso bullish/bearish: identificare il pattern di metriche che lo genera → il bot lo replica e trada prima della folla. Idea originale, molto diversa dal factor investing classico
- [ ] **Stop loss istituzionali a domino** — sfruttare le soglie psicologiche dove si concentrano gli SL degli istituzionali: quando il prezzo scende sotto, scatta una cascata di vendite prevedibile. Come identificare queste soglie in anticipo?
- [ ] **Quantificazione eventi rari** — come gestire eventi mai visti prima (prima riunione di un nuovo presidente BCE)? Usare la categoria più vicina o trattarli come unknown?
- [ ] **Analisi dei paper di finanza** — ci sono paper accademici su factor investing crypto? Salvatore potrebbe raccogliere paper rilevanti e ingestarli nel wiki per costruire la base teorica dei fattori


## 🔴 Da portare al progetto (priorità alta)

- [ ] **Raccogliere e validare indicatori di analisi tecnica** — quelli che usi/conosci: medie mobili, Fibonacci, supporti/resistenze, volumetrica. Appuntarli come note raw in Obsidian, l'agente li struttura (da call 05-06)
- [ ] **Lista di fattori candidati per il modello** — per ogni fattore: categoria (macro / aziendale / ratio / evento), come è misurabile numericamente, su quale strumento/mercato impatta. Es: tasso BCE, fatturato trimestrale, dimissioni CEO, prezzo petrolio
- [ ] **Descrivere la giornata tipo di un trader** — cosa guarda, in quale ordine, quali decisioni prende e su quali basi. Serve per capire cosa il bot deve replicare esattamente
- [ ] **Valutare AlphaArena dal punto di vista trading** — le 5 LLM testate su Bitcoin hanno tradato in modo sensato economicamente? Hanno rispettato logiche di mercato reale o hanno fatto scelte casuali?
- [ ] **Valutare NeuroEspresso dal punto di vista trading** — l'approccio multi-agente (economista, analista, trader separati) ha senso dal punto di vista di come funziona davvero una trading room?
- [ ] **Raccogliere casi reali eventi → impatto prezzi** — esempi concreti: "quando è successo X, il prezzo di Y ha fatto Z". Questo è il dataset grezzo per la factor quantification


## 🟡 In corso

- [ ] **Definire cosa replica il bot nel mondo reale** — qual è esattamente il workflow di un trader che questo sistema deve automatizzare? Chi è il trader "tipo" che stiamo costruendo?
- [ ] **Raccolta di meccanismi di mercato da portare nel progetto** — ogni volta che osservi qualcosa nel mercato reale che potrebbe essere modellato, portalo nel vault come nota raw


## 🟠 Decisioni economiche da prendere

- [ ] **Trading singolo vs Portfolio bilanciato** — questa è LA decisione più importante ora. Trading singolo è semplice da valutare (SL/TP). Portfolio bilanciato è più robusto ma richiede metriche diverse e orizzonte temporale più lungo. Qual è più adatto come primo sistema?
- [ ] **Multi-asset o solo cripto come punto di partenza?** — Salvatore ha già espresso preferenza per asset tradizionali (equity/ETF) come base più solida. Cripto come side. Da confermare ufficialmente
- [ ] **Regole del portafoglio — scrivere lo statuto** — partendo dall'esperienza di Starting Finance: max 5% per asset class, vendi a +100% di profitto, cash-out periodico. Portare queste regole formalmente al progetto
- [ ] **Cash-out strategy: quale %?** — regola da stabilire a priori: quanti profitti vengono estratti periodicamente vs reinvestiti?
- [ ] **Crypto vs Equity definitivo** — dai fondamentali: quale mercato ha più razionalità per un sistema quantitativo? Crypto più accessibile ma rumoroso; equity più storia e logica fondamentale
- [ ] **Strategia Sentiment degli Analisti: vale la pena?** — edge reale o troppo difficile da modellare? Studio di fattibilità economica prima che Luca valuti la parte tecnica
- [ ] **Frequenza di trading ottimale** — intraday? Giornaliero? Settimanale? Quale time frame ha storicamente più segnale vs rumore per un sistema quantitativo?


## 🟡 In corso

- [ ] **Definire cosa replica il bot nel mondo reale** — qual è esattamente il workflow di un trader che questo sistema automatizza?
- [ ] **Raccolta meccanismi di mercato** — ogni osservazione sul mercato reale che potrebbe essere modellata va come nota raw nel vault


## ✅ Fatto

- [x] Presentazione del concetto di **factor investing** — fattori macro, aziendali, ratio, eventi: ognuno ha un coefficiente calcolabile su serie storiche
- [x] Descrizione dei **meccanismi di esecuzione** — limit orders, cascata stop loss, effetto domino istituzionali, soglie psicologiche
- [x] Presentazione di **FinAgent, AlphaArena, NeuroEspresso** come benchmark di riferimento del settore
- [x] Proposta **strategia Sentiment degli Analisti** — idea originale su come battere il mercato anticipando il consenso
- [x] Allineamento su **analisi tecnica come serie di segnali numerici** in Python, non come visione del grafico (call 05-06)
- [x] Introduzione al concetto di **trading con leva** e perché è necessario per rendimenti significativi
- [x] Proposta **portfolio bilanciato con regole anti-bias** stile fondo professionale (max 5% per asset class, +100% → vendi, cash-out periodico)
- [x] Proposta di partire da **asset tradizionali** con cripto come side — più metodologie consolidate
- [x] Introduzione alla **correlazione intra-crypto** e all'allocazione dinamica nel basket (call 05-06)
- [x] Framing del progetto come **AI Investment Fund / Factory** — non solo trading bot


%% kanban:settings
```
{"kanban-plugin":"basic","list-collapse":[false,false,false,false,false]}
```
%%
