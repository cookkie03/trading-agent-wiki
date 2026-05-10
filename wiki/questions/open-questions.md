---
title: "Open Questions"
type: question
tags:
  - question
  - research
created: 2026-04-30
updated: 2026-04-30
status: active
related:
  - "[[questions/questions]]"
  - "[[ops/dashboard]]"
confidence: high
area: research
---

# Open Questions

Registro dei gap aperti del progetto.

## Uso

Ogni volta che emerge una domanda non banale, aggiungerla qui o creare una pagina dedicata e linkarla da qui.

## Domande

### Strategia e Mercato
- Crypto o equity come mercato iniziale? *(orientamento: crypto/Binance, non chiuso definitivamente)*
- Il primo MVP deve essere una dashboard intelligente o un agente autonomo? *(orientamento: dashboard/augmentation first)*
- Quali metriche possono dare un criterio razionale alle crypto oltre alla pura analisi tecnica?

### Architettura e Moduli
- Qual è il set minimo di moduli necessario per un primo sistema utile?
- **Includere il modulo TA?** Rischio: TA mal calibrata può corrompere l'output del Prediction Module DL. Come valutare il net effect?
- **Frequenza ottimale di invocazione dell'LLM Trader?** I moduli richiedono da secondi a un'ora. Qual è il time period minimo sensato?
- Il modulo "Sentiment degli analisti" (idea di King) è realizzabile? Richiede un approccio completamente diverso dal factor investing.

### Dati e Quantificazione
- Come quantificare in modo affidabile le news come fattori numerici? La metodologia (media empirica degli ultimi N casi) funziona per eventi rari?
- Quanti dati storici sono necessari per rendere affidabile il Factor Investigation Agent?

### Apprendimento
- Fine-tuning periodico o tentativo di continuous learning? Il continuous learning in real-time è ancora irrisolto nella comunità scientifica.
- Come passare dai log delle operazioni a un vero meccanismo di auto-miglioramento?

### Infrastruttura
- Quando ha senso passare a un exchange decentralizzato anonimo (no KYC) rispetto a Binance?
