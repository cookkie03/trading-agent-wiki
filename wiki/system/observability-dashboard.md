---
title: "Dashboard di osservabilità (read-only)"
type: build
tags:
  - architecture
  - software
  - ux
created: 2026-06-08
updated: 2026-06-13
status: active
priority: high
area: software
related:
  - "[[system/universe-watchlist]]"
  - "[[system/modules/data-layer]]"
  - "[[prior-art/libraries/sfc-portfolio-tracker]]"
  - "[[strategy/metrics/benchmark]]"
confidence: high
---

# Dashboard di osservabilità (read-only)

> ✅ **Implementata e funzionante** (2026-06-13). Streamlit app multi-pagina, dark theme SFC, legge dal DB SQLite del trading-agent.

## Principio
**Osserva, non controlla.** La dashboard legge dal DB (`~/.tradingagents/trading_agent.db`) in sola lettura. Il daemon resta l'unico a operare.

## Architettura

```
Synology NAS (reverse proxy)
  └─ trading.lucamanca.synology.me
       └─ TailScale 100.74.207.0:8501 (Debian server)
            └─ Streamlit → tradingagents/dashboard/app.py
                 └─ SQLite DB ← ~/.tradingagents/trading_agent.db
```

## File

| File | Scopo |
|------|-------|
| `tradingagents/dashboard/app.py` | Streamlit app multi-pagina |
| `tradingagents/dashboard/db_reader.py` | Lettura DB SQLite |
| `tradingagents/dashboard/metrics.py` | Metriche performance (da SFC) |
| `scripts/trading-agent-dashboard.service` | Systemd unit |

## Pagine dashboard
1. **📊 Dashboard** — KPI (NAV, Sharpe, Max DD, Calmar, vol), grafico NAV vs SPY, drawdown, ultimi trade
2. **📋 Watchlist** — tabella watchlist con score/direction, dettaglio ticker con candlestick + decision log
3. **🧠 Decisioni** — decision log con filtri, opinioni per-agente, payload research state
4. **💹 Trades** — tabella trade con filtri, metriche TP/SL
5. **📈 Ticker** — analisi singolo simbolo con candlestick + volume, decisioni, news
6. **⚙️ Sistema** — stato DB, statistiche, log daemon

## Avvio

```bash
# Daemon trading-agent
cd /home/hermes/workspace/trading-agent
uv run python -m tradingagents.cli start

# Dashboard Streamlit (già attiva su :8501)
uv run streamlit run tradingagents/dashboard/app.py --server.headless=true --server.port=8501 --server.address=0.0.0.0
```

## Systemd service (richiede sudo)

```bash
sudo cp scripts/trading-agent-dashboard.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable trading-agent-dashboard
sudo systemctl start trading-agent-dashboard
```

## Istruzioni NAS Synology (reverse proxy)

Il NAS Synology (TailScale `100.122.3.77`) fa reverse proxy per `trading.lucamanca.synology.me`.

**Pannello Synology → Application Portal → Reverse Proxy:**

| Campo | Valore |
|-------|--------|
| Source hostname | `trading.lucamanca.synology.me` |
| Source protocol | HTTPS |
| Source port | 443 |
| Destination hostname | `100.74.207.0` (Debian TailScale IP) |
| Destination protocol | HTTP |
| Destination port | `8501` |

Se il NAS usa **Nginx Proxy Manager** o **Traefik**, equivalente:
- Backend: `http://100.74.207.0:8501`
- Host: `trading.lucamanca.synology.me`

## Configurazione .env necessaria

```bash
# /home/hermes/workspace/trading-agent/.env
OPENROUTER_API_KEY=sk-or-...        # Da openrouter.ai → Keys
ALPACA_API_KEY=PK...                 # Da app.alpaca.markets
ALPACA_SECRET_KEY=...                # Da app.alpaca.markets
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=lsv2_pt_...        # Da smith.langchain.com
```

## Stato
✅ Dashboard implementata e testata
⏳ Reverse proxy NAS da configurare
⏳ API key OpenRouter da inserire nel .env
⏳ Primo run del daemon per popolare il DB
