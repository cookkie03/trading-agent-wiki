#!/bin/bash
# Script per aggiornare e unire i grafi di trading-agent (codice) e trading-agent-wiki (wiki)

WIKI_DIR="/Users/luca/Library/CloudStorage/OneDrive-Personale/trading-agent-wiki"
CODE_DIR="/Users/luca/Desktop/trading-agent"

echo "=== 1. Aggiornamento del Grafo del Wiki ==="
cd "$WIKI_DIR"

# Ripristina il grafo specifico del wiki prima dell'aggiornamento per evitare accumulo di nodi di codice
if [ -f graphify-out/wiki-graph.json ]; then
  mv graphify-out/graph.json graphify-out/merged-graph.json 2>/dev/null
  mv graphify-out/wiki-graph.json graphify-out/graph.json
fi

graphify update . --force

# Salva il grafo aggiornato del wiki separatamente
mv graphify-out/graph.json graphify-out/wiki-graph.json
if [ -f graphify-out/merged-graph.json ]; then
  mv graphify-out/merged-graph.json graphify-out/graph.json
fi

echo "=== 2. Aggiornamento del Grafo del Codice ==="
cd "$CODE_DIR"
graphify update .

echo "=== 3. Fusione dei Grafi (Merge) ==="
cd "$WIKI_DIR"
graphify merge-graphs \
  "$CODE_DIR/graphify-out/graph.json" \
  "$WIKI_DIR/graphify-out/wiki-graph.json" \
  --out "$WIKI_DIR/graphify-out/graph.json"

echo "=== 4. Ricalcolo delle Comunità (Clustering) ==="
graphify cluster-only .

echo "=== Grafo Unificato Aggiornato con Successo! ==="
