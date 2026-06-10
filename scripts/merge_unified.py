#!/usr/bin/env python3
"""Merge code-graph + wiki-graph in un grafo unificato con VERI edge wiki->codice.

`graphify merge-graphs` prefissa ogni nodo con '<repo>::' e fa solo nx.compose:
NON crea edge cross-repo, quindi gli stub di codice citati dalla wiki restano
isolati. Questo script invece:
  - prefissa il code graph con 'trading-agent::'
  - prefissa SOLO i nodi wiki reali (document/concept/tag) con 'trading-agent-wiki::'
  - rimappa gli edge wiki->code-stub verso il nodo reale 'trading-agent::{local_id}'
  - scarta gli stub di codice (gia' presenti nel code graph) e gli edge orfani
Risultato: archi reali pagina-wiki -> file/simbolo di codice => le discrepanze
emergono direttamente dal grafo.

Uso:
  merge_unified.py --code-graph FILE --wiki-graph FILE --out FILE \
                   [--code-tag NAME] [--wiki-tag NAME]
"""
import json, sys, argparse
from pathlib import Path


def load(p: Path):
    d = json.loads(p.read_text(encoding="utf-8"))
    links = d.get("links", d.get("edges", []))
    return d, d.get("nodes", []), links


def merge(code_graph: Path, wiki_graph: Path, out_path: Path,
          code_tag: str, wiki_tag: str):
    code_doc, code_nodes, code_links = load(code_graph)
    wiki_doc, wiki_nodes, wiki_links = load(wiki_graph)

    out_nodes, out_links = [], []

    # 1. code graph -> prefisso code_tag
    code_local_ids = set()
    for n in code_nodes:
        lid = n["id"]
        code_local_ids.add(lid)
        nn = dict(n)
        nn["id"] = f"{code_tag}::{lid}"
        nn["repo"] = code_tag
        nn.setdefault("local_id", lid)
        out_nodes.append(nn)
    for e in code_links:
        ee = dict(e)
        ee["source"] = f"{code_tag}::{e['source']}"
        ee["target"] = f"{code_tag}::{e['target']}"
        out_links.append(ee)

    # 2. nodi wiki: separa stub-codice (rimappabili) dai nodi wiki reali
    def remap_to_code(local_id):
        return f"{code_tag}::{local_id}" if local_id in code_local_ids else None

    wiki_real_ids, stub_to_code = set(), {}
    for n in wiki_nodes:
        if n.get("file_type") == "code" or n.get("_stub"):
            mapped = remap_to_code(n["id"])
            if mapped:
                stub_to_code[n["id"]] = mapped
            # stub non risolto -> scartato (ref a codice inesistente)
        else:
            wiki_real_ids.add(n["id"])

    for n in wiki_nodes:
        if n["id"] in wiki_real_ids:
            nn = dict(n)
            nn.pop("_stub", None)
            nn["id"] = f"{wiki_tag}::{n['id']}"
            nn["repo"] = wiki_tag
            nn.setdefault("local_id", n["id"])
            out_nodes.append(nn)

    # 3. edge wiki: rimappa gli endpoint
    def map_endpoint(eid):
        if eid in wiki_real_ids:
            return f"{wiki_tag}::{eid}"
        if eid in stub_to_code:
            return stub_to_code[eid]
        return None

    cross = 0
    for e in wiki_links:
        s, t = map_endpoint(e["source"]), map_endpoint(e["target"])
        if s is None or t is None:
            continue
        ee = dict(e)
        ee["source"], ee["target"] = s, t
        out_links.append(ee)
        if s.startswith(wiki_tag + "::") and t.startswith(code_tag + "::"):
            cross += 1

    merged = {
        "directed": False,
        "multigraph": code_doc.get("multigraph", False),
        "graph": {},
        "nodes": out_nodes,
        "links": out_links,
        "hyperedges": list(code_doc.get("hyperedges", [])),
        "built_at_commit": code_doc.get("built_at_commit"),
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")

    n_code = sum(1 for n in out_nodes if n["repo"] == code_tag)
    n_wiki = sum(1 for n in out_nodes if n["repo"] == wiki_tag)
    print(f"[merge_unified] {len(out_nodes)} nodi ({n_code} codice + {n_wiki} wiki), "
          f"{len(out_links)} edge | cross-repo wiki->codice: {cross}")
    print(f"[merge_unified] -> {out_path}")


def main():
    here = Path(__file__).resolve()
    wiki_root = here.parent.parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--code-graph", default="")
    ap.add_argument("--wiki-graph", default=str(wiki_root / "graphify-out" / "wiki-graph.json"))
    ap.add_argument("--out", default=str(wiki_root / "graphify-out" / "graph.json"))
    ap.add_argument("--code-tag", default="trading-agent")
    ap.add_argument("--wiki-tag", default="trading-agent-wiki")
    args = ap.parse_args()

    code_graph = Path(args.code_graph).resolve() if args.code_graph \
        else (wiki_root.parent / "trading-agent" / "graphify-out" / "graph.json")
    wiki_graph = Path(args.wiki_graph).resolve()
    out_path = Path(args.out).resolve()

    if not wiki_graph.is_file():
        print(f"[merge_unified] ERRORE: wiki-graph mancante: {wiki_graph}", file=sys.stderr)
        sys.exit(1)
    if not code_graph.is_file():
        print(f"[merge_unified] ERRORE: code-graph mancante: {code_graph}", file=sys.stderr)
        sys.exit(1)

    merge(code_graph, wiki_graph, out_path, args.code_tag, args.wiki_tag)


if __name__ == "__main__":
    main()
