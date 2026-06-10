#!/usr/bin/env python3
"""Costruisce wiki-graph.json dalle pagine wiki/ del vault — estrazione DETERMINISTICA.

Niente LLM, niente servizi esterni. Sfrutta la struttura gia' curata a mano:
  - frontmatter YAML (type, tags, area, status, related)
  - wikilink [[pagina]] / [[pagina#sez|alias]] nel corpo
  - riferimenti a codice in backtick (`tradingagents/...py`, `foo.py`)

I riferimenti al codice vengono risolti contro i file .py reali del repo del
codice, cosi' gli edge wiki->codice puntano a nodi che esisteranno nel grafo
del codice dopo il merge (vedi merge_unified.py).

Uso:
  build_wiki_graph.py [--wiki-root DIR] [--code-root DIR] [--out FILE]

Default: --wiki-root = repo git che contiene questo script;
         --code-root = sibling "trading-agent";
         --out       = <wiki-root>/graphify-out/wiki-graph.json
Richiede l'interprete Python con graphify installato.
"""
import os, re, json, sys, argparse
from pathlib import Path

# directory di tooling/rumore da escludere (allineate a .graphifyignore)
SKIP_PREFIXES = (
    ".obsidian/", "raw/", "graphify-out/", ".git/", "node_modules/",
    ".agents/", ".claude/", ".trunk/", ".cursor/", ".kilo/", ".codex/",
    ".cliner/", ".copilot/", ".windsurf/", ".aider/", ".claw/", ".traes/",
)


def md_pages(root: Path):
    pages = []
    for p in root.rglob("*.md"):
        rel = p.relative_to(root).as_posix()
        if rel.startswith(SKIP_PREFIXES):
            continue
        pages.append(rel)
    return sorted(pages)


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def page_id(rel: str) -> str:
    parts = rel[:-3].split("/")  # drop .md
    if len(parts) == 1:
        return norm(parts[0])
    return norm(parts[-2] + "_" + parts[-1])


def page_label(rel: str) -> str:
    return rel[:-3].split("/")[-1]


WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
CODEREF_RE = re.compile(r"`(tradingagents/[\w./]+|[\w]+/[\w./]+\.py|\w+\.py)`")


def parse_frontmatter(text: str):
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_raw, body = text[3:end], text[end + 4:]
    fm, cur_key = {}, None
    for line in fm_raw.splitlines():
        if re.match(r"^\s*-\s+", line) and cur_key:
            val = line.strip()[1:].strip().strip('"').strip("'")
            fm.setdefault(cur_key, [])
            if isinstance(fm[cur_key], list):
                fm[cur_key].append(val)
        else:
            m = re.match(r"^([a-zA-Z_]+):\s*(.*)$", line)
            if m:
                cur_key = m.group(1)
                v = m.group(2).strip().strip('"').strip("'")
                fm[cur_key] = v if v else []
    return fm, body


def build(wiki_root: Path, code_root: Path, out_path: Path):
    PAGES = md_pages(wiki_root)

    # indice di risoluzione wikilink
    page_by_stem, page_by_rel = {}, {}
    for rel in PAGES:
        stem = rel[:-3].split("/")[-1]
        page_by_stem.setdefault(stem.lower(), rel)
        key = rel[:-3].lower()
        page_by_rel[key] = rel
        if key.startswith("wiki/"):
            page_by_rel[key[len("wiki/"):]] = rel

    def resolve_wikilink(target: str):
        t = target.strip().lower().split("#")[0].strip()
        if not t:
            return None
        if t.endswith((".canvas", ".md")):
            t = t.rsplit(".", 1)[0]
        if t in page_by_rel:
            return page_id(page_by_rel[t])
        stem = t.split("/")[-1]
        if stem in page_by_stem:
            return page_id(page_by_stem[stem])
        return None

    # file di codice reali (per validare i ref)
    code_files = set()
    if code_root.is_dir():
        for p in code_root.rglob("*.py"):
            ap = p.as_posix()
            if "/.git/" in ap or "__pycache__" in ap:
                continue
            code_files.add(p.relative_to(code_root).as_posix())
    code_basenames = {}
    for f in code_files:
        code_basenames.setdefault(os.path.basename(f), f)

    def code_node_id(code_rel: str) -> str:
        parts = code_rel[:-3].split("/")
        if len(parts) == 1:
            return norm(parts[0])
        return norm(parts[-2] + "_" + parts[-1])

    def resolve_coderef(ref: str):
        r = ref.strip()
        if r in code_files:
            return code_node_id(r), r
        if ("tradingagents/" + r) in code_files:
            return code_node_id("tradingagents/" + r), "tradingagents/" + r
        bn = os.path.basename(r)
        if bn in code_basenames:
            return code_node_id(code_basenames[bn]), code_basenames[bn]
        return None

    nodes, edges, seen = [], [], set()

    def add_node(nid, label, ftype, source_file, **extra):
        if nid in seen:
            return
        seen.add(nid)
        n = {"id": nid, "label": label, "file_type": ftype,
             "source_file": source_file, "source_location": None}
        n.update(extra)
        nodes.append(n)

    def add_edge(src, tgt, rel, conf, score, source_file):
        edges.append({"source": src, "target": tgt, "relation": rel,
                      "confidence": conf, "confidence_score": score,
                      "source_file": source_file, "source_location": None, "weight": 1.0})

    stats = dict(wl_ok=0, wl_orphan=0, code_ok=0, code_broken=0)

    for rel in PAGES:
        text = (wiki_root / rel).read_text(encoding="utf-8", errors="ignore")
        fm, body = parse_frontmatter(text)
        pid, label = page_id(rel), page_label(rel)
        add_node(pid, label, "document", rel,
                 area=str(fm.get("area", "")) or None,
                 doc_type=str(fm.get("type", "")) or None,
                 status=str(fm.get("status", "")) or None)

        tags = fm.get("tags", [])
        if isinstance(tags, str):
            tags = [tags] if tags else []
        for tg in tags:
            if not tg:
                continue
            tnid = "tag_" + norm(tg)
            add_node(tnid, "#" + tg, "concept", "_meta/taxonomy.md")
            add_edge(pid, tnid, "references", "EXTRACTED", 1.0, rel)

        related = fm.get("related", [])
        if isinstance(related, str):
            related = [related] if related else []
        for r in related:
            for m in WIKILINK_RE.finditer(r):
                tgt = resolve_wikilink(m.group(1))
                if tgt:
                    add_edge(pid, tgt, "conceptually_related_to", "EXTRACTED", 1.0, rel)
                    stats["wl_ok"] += 1
                else:
                    stats["wl_orphan"] += 1

        body_targets = set()
        for m in WIKILINK_RE.finditer(body):
            raw = m.group(1).split("|")[0]
            tgt = resolve_wikilink(raw)
            if tgt and tgt != pid:
                body_targets.add(tgt)
                stats["wl_ok"] += 1
            elif not tgt:
                stats["wl_orphan"] += 1
        for tgt in body_targets:
            add_edge(pid, tgt, "references", "EXTRACTED", 1.0, rel)

        code_targets = set()
        for m in CODEREF_RE.finditer(body):
            res = resolve_coderef(m.group(1))
            if res:
                code_targets.add(res)
                stats["code_ok"] += 1
            else:
                stats["code_broken"] += 1
        for cid, crel in code_targets:
            add_node(cid, os.path.basename(crel), "code", crel, _stub=True)
            add_edge(pid, cid, "references", "EXTRACTED", 1.0, rel)

    extraction = {"nodes": nodes, "edges": edges, "hyperedges": [],
                  "input_tokens": 0, "output_tokens": 0}

    # build via graphify API
    from graphify.build import build_from_json
    from graphify.cluster import cluster
    from graphify.export import to_json

    G = build_from_json(extraction, directed=False, root=str(wiki_root))
    communities = cluster(G)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    to_json(G, communities, str(out_path), force=True)

    print(f"[build_wiki_graph] pagine={len(PAGES)} nodi={G.number_of_nodes()} "
          f"edge={G.number_of_edges()} community={len(communities)}")
    print(f"[build_wiki_graph] wikilink ok={stats['wl_ok']} orfani={stats['wl_orphan']} | "
          f"ref-codice ok={stats['code_ok']} rotti={stats['code_broken']}")
    print(f"[build_wiki_graph] -> {out_path}")


def main():
    here = Path(__file__).resolve()
    # repo wiki = git toplevel del file (fallback: parent della cartella scripts/)
    default_wiki = here.parent.parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--wiki-root", default=str(default_wiki))
    ap.add_argument("--code-root", default="")
    ap.add_argument("--out", default="")
    args = ap.parse_args()

    wiki_root = Path(args.wiki_root).resolve()
    code_root = Path(args.code_root).resolve() if args.code_root \
        else (wiki_root.parent / "trading-agent")
    out_path = Path(args.out).resolve() if args.out \
        else (wiki_root / "graphify-out" / "wiki-graph.json")

    if not wiki_root.is_dir():
        print(f"[build_wiki_graph] ERRORE: wiki-root inesistente: {wiki_root}", file=sys.stderr)
        sys.exit(1)
    if not code_root.is_dir():
        print(f"[build_wiki_graph] ATTENZIONE: code-root inesistente: {code_root} "
              f"(i ref al codice non saranno risolti)", file=sys.stderr)

    build(wiki_root, code_root, out_path)


if __name__ == "__main__":
    main()
