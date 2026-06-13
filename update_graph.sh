#!/bin/bash
# Script per aggiornare e unire i grafi di trading-agent (codice) e trading-agent-wiki (wiki)

WIKI_DIR="/Users/luca/Library/Mobile Documents/iCloud~md~obsidian/Documents/trading-agent-wiki"
CODE_DIR="/Users/luca/Desktop/trading-agent"

echo "=== 1. Aggiornamento del Grafo del Wiki ==="
cd "$WIKI_DIR"
graphify update . --force

echo "=== 2. Aggiornamento del Grafo del Codice ==="
cd "$CODE_DIR"
graphify update .

echo "=== 3. Fusione dei Grafi (Merge) ==="
cd "$WIKI_DIR"
graphify merge-graphs \
  "$CODE_DIR/graphify-out/graph.json" \
  "$WIKI_DIR/graphify-out/graph.json" \
  --out "$WIKI_DIR/graphify-out/graph.json"

echo "=== 4. Ricalcolo delle Comunità (Clustering) ==="
graphify cluster-only .

echo "=== Grafo Unificato Aggiornato con Successo! ==="
