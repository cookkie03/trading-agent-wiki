---
title: "TradingAgents: Multi-Agents LLM Financial Trading Framework"
type: source
tags:
  - source
  - architecture
  - multi-agent
  - research
raw_source_path: "raw/articles/TradingAgents.md"
created: 2026-05-12
updated: 2026-05-21
confidence: high
status: reviewed
related:
  - "[[build/system-map]]"
  - "[[references/tradingagents-code-wiki]]"
---

# TradingAgents: Multi-Agents LLM Financial Trading Framework

Paper di ricerca che propone un framework di trading multi-agente ispirato alle società di trading reali.

## Visione Centrale

Il framework supera i limiti dei sistemi a singolo agente o dei sistemi multi-agente che usano solo linguaggio naturale disordinato (effetto "telefono"). Introduce:
1. **Specializzazione dei Ruoli**: Agenti con compiti e tool specifici.
2. **Protocollo di Comunicazione Strutturato**: Gli agenti comunicano tramite **report e documenti strutturati** (diagrammi, tabelle) per preservare l'integrità del dato su orizzonti lunghi.
3. **Dibattito Agentico**: Uso del dibattito (bull vs bear) per far emergere punti di vista critici prima della decisione.

## Ruoli degli Agenti

### 1. Analyst Team
- **Fundamental Analyst**: Valuta bilanci, earnings, insider transactions.
- **Sentiment Analyst**: Analizza social media (Reddit, X) e sentiment score.
- **News Analyst**: Analizza macroeconomia e news aziendali.
- **Technical Analyst**: Calcola e seleziona indicatori tecnici (MACD, RSI).

### 2. Researcher Team
- **Bullish Researchers**: Cercano opportunità e segnali positivi.
- **Bearish Researchers**: Cercano rischi e segnali negativi.
- *Processo*: Debattono per $n$ round; un facilitatore seleziona la prospettiva prevalente.

### 3. Trader Agents
- Sintetizzano i report di analisti e ricercatori.
- Decidono timing e size del trade.

### 4. Risk Management Team
- Monitorano volatilità e liquidità.
- Deliberano da tre prospettive: risk-seeking, neutral, risk-conservative.
- Regolano il piano di trading entro i vincoli di rischio.

### 5. Fund Manager
- Approvazione finale ed esecuzione.

## Key Insights Tecniche

- **ReAct Prompting**: Tutti gli agenti usano il framework Reasoning + Acting.
- **Hybrid Communication**: Report strutturati per il controllo e linguaggio naturale per il dibattito.
- **Backbone LLM Strategico**: 
  - Modelli "Quick-thinking" (GPT-4o-mini) per task semplici, summarization e recupero dati.
  - Modelli "Deep-thinking" (o1-preview) per decision-making e analisi complessa.
- **Superiorità**: Il framework ha superato i baseline (Buy & Hold, MACD, SMA) in Cumulative Return e Sharpe Ratio, mantenendo un Maximum Drawdown contenuto.

## Relazione con il Progetto
- Conferma la validità dell'architettura multi-agente modulare.
- Introduce l'importanza della **comunicazione strutturata** tra moduli (già presente come idea di "DB" nel nostro `system-map`).
- Suggerisce l'uso di **debater** per migliorare la robustezza della decisione del Trader.

## Pattern adottati nel nostro progetto

- **Comunicazione strutturata via JSON** (non chat free-form) tra agenti — evita l'effetto "telefono senza fili"
- **Quick Thinker + Deep Thinker**: modelli economici per raccolta dati, modelli capaci solo per la decisione finale
- **Risk Management upstream** (nostra variante): nel TradingAgents originale il Risk Team valuta *dopo* il Trader; nel nostro design il Risk Analyst agisce *prima*, impostando i paletti

Per i dettagli implementativi del codebase vedere [[references/tradingagents-code-wiki]].
