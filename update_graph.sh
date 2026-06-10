#!/usr/bin/env bash
# Aggiorna e unisce i grafi di trading-agent (codice) e trading-agent-wiki (wiki)
# in un unico knowledge graph in trading-agent-wiki/graphify-out/graph.json.
#
# Portabile: nessun path hardcoded. Auto-rileva i due repo come fratelli e
# l'interprete Python con graphify installato. Idempotente.
#
# Pipeline:
#   1. grafo CODICE   : graphify update (AST, no LLM)
#   2. grafo WIKI     : scripts/build_wiki_graph.py (estrazione deterministica, no LLM)
#   3. MERGE unificato: scripts/merge_unified.py (veri edge cross-repo wiki->codice)
#   4. CLUSTERING     : graphify cluster-only
#
# Uso: ./update_graph.sh            (dai due repo fratelli sotto la stessa parent)
set -euo pipefail

# ── Posizioni repo (auto-detect: la wiki e' la parent della cartella scripts/) ──
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WIKI_DIR="$SCRIPT_DIR"
CODE_DIR="${TRADING_AGENT_CODE_DIR:-$(cd "$WIKI_DIR/.." && pwd)/trading-agent}"

if [ ! -d "$CODE_DIR" ]; then
  echo "[update_graph] ERRORE: repo del codice non trovato: $CODE_DIR" >&2
  echo "  Imposta TRADING_AGENT_CODE_DIR oppure metti i due repo come fratelli." >&2
  exit 1
fi

# ── Interprete Python con graphify (riusa la logica dell'hook) ──
GRAPHIFY_PYTHON=""
_PINNED="${GRAPHIFY_PYTHON_BIN:-$HOME/.local/share/uv/tools/graphifyy/bin/python}"
if [ -n "$_PINNED" ] && [ -x "$_PINNED" ] && "$_PINNED" -c "import graphify" 2>/dev/null; then
  GRAPHIFY_PYTHON="$_PINNED"
fi
if [ -z "$GRAPHIFY_PYTHON" ]; then
  if command -v python3 >/dev/null 2>&1 && python3 -c "import graphify" 2>/dev/null; then
    GRAPHIFY_PYTHON="python3"
  elif command -v python >/dev/null 2>&1 && python -c "import graphify" 2>/dev/null; then
    GRAPHIFY_PYTHON="python"
  else
    echo "[update_graph] ERRORE: nessun Python con graphify installato." >&2
    echo "  Installa con: uv tool install graphifyy" >&2
    exit 1
  fi
fi

# Evita ricorsione: l'hook post-commit non deve ripartire durante questo script
export GRAPHIFY_SKIP_HOOK=1
export PYTHONHASHSEED=0

echo "[update_graph] wiki=$WIKI_DIR"
echo "[update_graph] code=$CODE_DIR"
echo "[update_graph] python=$GRAPHIFY_PYTHON"

echo "=== 1. Grafo del CODICE (AST) ==="
( cd "$CODE_DIR" && graphify update . --force )

echo "=== 2. Grafo della WIKI (estrazione deterministica) ==="
"$GRAPHIFY_PYTHON" "$WIKI_DIR/scripts/build_wiki_graph.py" \
  --wiki-root "$WIKI_DIR" \
  --code-root "$CODE_DIR" \
  --out "$WIKI_DIR/graphify-out/wiki-graph.json"

echo "=== 3. Merge unificato (edge cross-repo wiki->codice) ==="
"$GRAPHIFY_PYTHON" "$WIKI_DIR/scripts/merge_unified.py" \
  --code-graph "$CODE_DIR/graphify-out/graph.json" \
  --wiki-graph "$WIKI_DIR/graphify-out/wiki-graph.json" \
  --out "$WIKI_DIR/graphify-out/graph.json"

echo "=== 4. Clustering + report ==="
( cd "$WIKI_DIR" && graphify cluster-only . --graph graphify-out/graph.json --no-viz )

echo "[update_graph] === Grafo unificato aggiornato con successo ==="
