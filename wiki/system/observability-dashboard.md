---
title: "Dashboard di osservabilità"
type: build
tags:
  - architecture
  - software
  - ux
  - streamlit
  - nas
  - deploy
created: 2026-06-08
updated: 2026-06-13
status: active
priority: high
area: software
related:
  - "[[system/universe-watchlist]]"
  - "[[system/modules/data-layer]]"
  - "[[prior-art/libraries/sfc-portfolio-tracker]]"
confidence: high
---

# Dashboard di osservabilità (read-only)

> ✅ **Implementata e in produzione** (2026-06-13). Streamlit app multi-pagina, dark theme SFC, accessibile su `https://trading.lucamanca.synology.me`.

## Stato

| Componente | Stato | Note |
|------------|-------|------|
| Dashboard Streamlit | ✅ Running | `http://100.74.207.0:8501` → 200 |
| Trading-agent daemon | ✅ Running | PaperBroker, primo ciclo in corso |
| DB SQLite | ✅ Popolato | 55 ticker, 2 posizioni, NAV $100k |
| Reverse proxy NAS | ✅ Configurato | `trading.lucamanca.synology.me` → `100.74.207.0:8501` |

## Architettura

```
Browser → https://trading.lucamanca.synology.me:443
            ↓
       Synology NAS (reverse proxy)
            ↓
       http://100.74.207.0:8501 (Debian/TailScale)
            ↓
       Streamlit → tradingagents/dashboard/app.py
            ↓
       SQLite DB → ~/.tradingagents/trading_agent.db
```

## URL

**Dashboard**: `https://trading.lucamanca.synology.me`

## Avvio / Gestione

```bash
# Trading-agent daemon
uv run python -m tradingagents.cli start
uv run python -m tradingagents.cli status
uv run python -m tradingagents.cli stop
tail -f ~/.tradingagents/agent.log

# Streamlit dashboard
uv run streamlit run tradingagents/dashboard/app.py \
    --server.headless=true \
    --server.port=8501 \
    --server.address=0.0.0.0
```

## Pagine dashboard
1. **📊 Dashboard** — KPI (NAV, Sharpe, Max DD, Calmar, vol), grafico NAV vs SPY, drawdown, ultimi trade
2. **📋 Watchlist** — tabella watchlist con score/direction, dettaglio ticker con candlestick + decision log
3. **🧠 Decisioni** — decision log con filtri, opinioni per-agente, payload research state
4. **💹 Trades** — tabella trade con filtri, metriche TP/SL
5. **📈 Ticker** — analisi singolo simbolo, candlestick, news
6. **⚙️ Sistema** — stato DB, posizioni, log daemon

## Troubleshooting

### Dashboard non raggiungibile dal browser
1. Verifica Streamlit: `curl -I http://localhost:8501` → 200
2. Verifica reverse proxy NAS: log del NAS
3. Se caricamento infinito: WebSocket bloccato → verificare che il proxy supporti WS upgrade

### Dashboard bianca / errore
- Controllare log: `journalctl -u trading-agent-dashboard` o output del processo
- Verificare che il DB esista: `ls -la ~/.tradingagents/trading_agent.db`
