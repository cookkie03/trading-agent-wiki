---
title: "Dashboard di osservabilità — istruzioni NAS"
type: build
tags:
  - infrastructure
  - nas
  - reverse-proxy
  - streamlit
  - dashboard
  - deploy
created: 2026-06-13
updated: 2026-06-13
status: active
priority: high
area: software
related: []
confidence: high
---
# Trading Agent — Streamlit Dashboard su NAS Synology

> **Stato**: Dashboard implementata e funzionante. Il trading-agent gira su Debian (Hermes). Il reverse proxy va configurato sul NAS Synology per esporre la dashboard su `trading.lucamanca.synology.me`.

---

## 1. Architettura

```
Synology NAS (reverse proxy)         Debian Server (Hermes)
trading.lucamanca.synology.me  ──►  100.74.207.0:8501
       :443 (HTTPS)                    Streamlit Dashboard
                                       └─ legge DB SQLite
                                          ~/.tradingagents/trading_agent.db
```

- **Debian**: Streamlit gira su porta `8501`
- **NAS**: Reverse proxy da `trading.lucamanca.synology.me:443` → `100.74.207.0:8501`
- **DB**: SQLite su `/home/hermes/.tradingagents/trading_agent.db`

---

## 2. Prerequisiti

### 2a. Dashboard su Debian

```bash
# Installa (sudo necessario)
sudo cp scripts/streamlit-dashboard.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable trading-agent-dashboard
sudo systemctl start trading-agent-dashboard

# Oppure manuale (senza sudo)
cd /home/hermes/workspace/trading-agent
uv run streamlit run tradingagents/dashboard/app.py \
    --server.headless=true \
    --server.port=8501 \
    --server.address=0.0.0.0
```

### 2b. Verifica locale

```bash
# Da Debian stesso
curl -I http://localhost:8501  → 200 OK
```

---

## 3. Reverse Proxy NAS — Synology DSM

### Opzione A: Application Portal (consigliato)

1. **DSM → Application Portal → Reverse Proxy**
2. Clicca **Crea**
3. Nome: `trading-agent-dashboard`
4. **Origine**:
   - Protocollo: **HTTPS**
   - Nome host: `trading.lucamanca.synology.me`
   - Porta: `443`
5. **Destinazione**:
   - Protocollo: **HTTP**
   - Nome host: `100.74.207.0` (IP TailScale del Debian)
   - Porta: `8501`
6. Salva

### Opzione B: Nginx Proxy Manager (se installato)

Se hai Nginx Proxy Manager come container:

1. **Hosts → Proxy Hosts → Add Proxy Host**
2. Domain: `trading.lucamanca.synology.me`
3. Forward Hostname: `100.74.207.0`
4. Forward Port: `8501`
5. Scheme: `http`
6. Bloccia sì
7. Salva

### Opzione C: nginx.conf manuale (container/VM nginx)

Se nginx gira in un container nginx-proxy-manager o similare:

```nginx
server {
    listen 443 ssl;
    server_name trading.lucamanca.synology.me;

    ssl_certificate     /path/to/fullchain.pem;
    ssl_certificate_key /path/to/privkey.pem;

    location / {
        proxy_pass http://100.74.207.0:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }
}
```

Ricarica nginx dopo la modifica.

---

## 4. Dashboard Pagine

| Pagina | Descrizione |
|--------|-------------|
| 📊 Dashboard | KPI, NAV vs SPY, drawdown, ultimi trade |
| 📋 Watchlist | Tabella con score, direzione, conviction, dettaglio candlestick |
| 🧠 Decisioni | Decision log, opinioni agenti, payload ricerca |
| 💹 Trades | Tabella trade, filtri, metriche TP/SL |
| 📈 Ticker | Analisi singolo simbolo, candlestick, news |
| ⚙️ Sistema | Stato DB, posizioni, log daemon |

---

## 5. Servizi systemd sul Debian

### Trading Agent daemon

```bash
# Start
uv run python -m tradingagents.cli start

# Status
uv run python -m tradingagents.cli status

# Stop
uv run python -m tradingagents.cli stop

# Log
tail -f ~/.tradingagents/agent.log
```

### Streamlit Dashboard

```bash
# Start (se installato come servizio)
sudo systemctl start trading-agent-dashboard

# Status
sudo systemctl status trading-agent-dashboard

# Stop
sudo systemctl stop trading-agent-dashboard

# Log
sudo journalctl -u trading-agent-dashboard -f
```

---

## 6. Credenziali .env

```toml
OPENROUTER_API_KEY=***        # openrouter.ai → Keys
ALPACA_API_KEY=PK***E        # app.alpaca.markets → Paper API Key
LANGCHAIN_API_KEY=***        # smith.langchain.com
```

Il file è in `/home/hermes/workspace/trading-agent/.env`.

---

## 7. Stato attuale

| Componente | Stato | Note |
|------------|-------|------|
| Dashboard Streamlit | ✅ Su :8501 | Partito, risponde 200 |
| DB SQLite | ✅ 55 ticker, 55 watchlist | NAV $100k |
| Trading agent | ✅ Primo ciclo in corso | PaperBroker, niente Alpaca |
| Reverse proxy NAS | ⏳ Da configurare | Vedi sezione 3 |
