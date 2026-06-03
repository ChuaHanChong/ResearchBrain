#!/usr/bin/env python3
"""kh-graph-sync — additively refresh graphify-out/graph.json from _KnowledgeHub_.

Run under graphify's interpreter (it imports graphify):
    PY=$(cat graphify-out/.graphify_python)
    $PY .claude/skills/kh-graph-sync/scripts/kh_graph_sync.py <subcommand>

Subcommands
    delta      Graph-source diff: which notes have no nodes in graph.json.
               Writes .kh_missing.txt + .chunklist_NN.txt. Prints {"missing","chunks"}.
    finalize   Validate+merge the subagent chunk files, additively merge into graph.json
               (NEVER build_merge), wire frontmatter tags into the tag_* backbone,
               re-cluster, write graph.json + GRAPH_REPORT.md, cache the new notes,
               refresh the manifest, print before->after diff + god nodes + surprises.
    enrich     (periodic) Add semantically_similar_to edges (TF-IDF kNN) + concept_*
               hub nodes for named entities spanning >=N papers, then re-cluster.

Why not `graphify --update`: its content-addressed cache is invalidated by bulk note
edits, and its generic extraction/merge corrupts this vault (wrong IDs, no tag wiring,
destructive dedup). See SKILL.md.
"""
import sys, json, re, glob
import os.path as osp
from pathlib import Path
from collections import defaultdict

OUT = Path("graphify-out")
KH = Path("_KnowledgeHub_")
GRAPH = OUT / "graph.json"
CHUNK_SIZE = 22

# enrichment params
SIM_K, SIM_THRESH = 5, 0.22
CONCEPT_MIN_PAPERS = 3


# ---------- shared helpers ----------
def _load_graph():
    g = json.loads(GRAPH.read_text())
    return g, g.get("links", g.get("edges", []))


def _edges_of(g):
    return g.get("links", g.get("edges", []))


def _arx(path_or_name):
    return Path(path_or_name).name.replace(".md", "").replace(".", "_")


def _auto_labels(G, communities, id2label):
    deg = dict(G.degree())

    def clean(lbl):
        head = re.split(r"[:(]", str(lbl))[0].strip()
        return " ".join(head.split()[:5]) or "Concept Cluster"

    labels = {}
    for cid, members in communities.items():
        best = max(members, key=lambda m: (0 if str(m).startswith(("tag_", "concept_")) else 1, deg.get(m, 0)))
        labels[cid] = clean(id2label.get(best, f"Community {cid}"))
    return labels


def _rebuild(extraction, total_files):
    """build_from_json -> cluster -> report -> to_json. Returns (G, communities)."""
    from graphify.build import build_from_json
    from graphify.cluster import cluster, score_all
    from graphify.analyze import god_nodes, surprising_connections, suggest_questions
    from graphify.report import generate
    from graphify.export import to_json

    G = build_from_json(extraction)
    communities = cluster(G)
    cohesion = score_all(G, communities)
    gods = god_nodes(G)
    surprises = surprising_connections(G, communities)
    id2label = {n["id"]: n.get("label", n["id"]) for n in extraction["nodes"]}
    labels = _auto_labels(G, communities, id2label)
    questions = suggest_questions(G, communities, labels)
    det = {"total_files": total_files, "total_words": 0, "files": {"document": []}, "skipped_sensitive": []}
    (OUT / "GRAPH_REPORT.md").write_text(
        generate(G, communities, cohesion, labels, gods, surprises, det, {"input": 0, "output": 0}, ".", suggested_questions=questions)
    )
    to_json(G, communities, str(GRAPH))
    (OUT / ".graphify_labels.json").write_text(json.dumps({str(k): v for k, v in labels.items()}, ensure_ascii=False))
    return G, communities, gods, surprises


# ---------- delta ----------
def cmd_delta():
    g, _ = _load_graph()
    srcs = {osp.basename(n.get("source_file") or n.get("source") or "") for n in g["nodes"]}
    disk = {osp.basename(p) for p in glob.glob(str(KH / "*.md"))}
    missing = sorted("_KnowledgeHub_/" + m for m in disk if m and m not in srcs)
    # clear stale chunk artifacts from any prior run
    for f in glob.glob(str(OUT / ".chunklist_*.txt")) + glob.glob(str(OUT / ".graphify_chunk_*.json")):
        Path(f).unlink()
    nchunks = 0
    if missing:
        (OUT / ".kh_missing.txt").write_text("\n".join(missing))
        for i in range(0, len(missing), CHUNK_SIZE):
            nchunks += 1
            (OUT / f".chunklist_{nchunks:02d}.txt").write_text("\n".join(missing[i : i + CHUNK_SIZE]))
    else:
        (OUT / ".kh_missing.txt").unlink(missing_ok=True)  # nothing to do; leave no artifacts
    print(json.dumps({"on_disk": len(disk), "in_graph": len(disk & srcs), "missing": len(missing), "chunks": nchunks}))


# ---------- finalize ----------
def _merge_chunks():
    nodes, edges = [], []
    chunks = sorted(glob.glob(str(OUT / ".graphify_chunk_*.json")))
    for c in chunks:
        d = json.loads(Path(c).read_text())
        nodes += d.get("nodes", [])
        edges += d.get("edges", [])
    fix = lambda i: re.sub(r"[^a-z0-9_]+", "_", i.lower())
    remap = {n["id"]: fix(n["id"]) for n in nodes if not re.fullmatch(r"[a-z0-9_]+", n.get("id", ""))}
    for n in nodes:
        n["id"] = remap.get(n["id"], n["id"])
    for e in edges:
        e["source"] = remap.get(e.get("source"), e.get("source"))
        e["target"] = remap.get(e.get("target"), e.get("target"))
    return nodes, edges, len(chunks), len(remap)


def _parse_tags(md):
    m = re.match(r"^---\n(.*?)\n---", md, re.S)
    fm = m.group(1) if m else ""
    blk = re.search(r"^tags:\s*\n((?:[ \t]*-[ \t]*.+\n?)+)", fm, re.M)
    if blk:
        out = []
        for l in blk.group(1).splitlines():
            mm = re.match(r"\s*-\s*(.+?)\s*$", l)
            if mm:
                out.append(mm.group(1).strip().strip("\"'"))
        return out
    inl = re.search(r"^tags:\s*\[(.*?)\]", fm, re.M)
    return [x.strip().strip("\"'") for x in inl.group(1).split(",") if x.strip()] if inl else []


def cmd_finalize():
    if not glob.glob(str(OUT / ".graphify_chunk_*.json")):
        print("ERROR: no .graphify_chunk_*.json found — dispatch extraction subagents first.")
        sys.exit(1)
    import shutil
    shutil.copy(GRAPH, OUT / ".graphify_old.json")
    old = json.loads((OUT / ".graphify_old.json").read_text())
    old_nodes = old["nodes"]
    old_edges = [dict(e) for e in _edges_of(old)]
    old_ids = {n["id"] for n in old_nodes}

    new_nodes, new_edges, nchunks, nfixed = _merge_chunks()
    (OUT / ".graphify_semantic_new.json").write_text(json.dumps({"nodes": new_nodes, "edges": new_edges}))

    # additive node merge (keep existing on collision)
    add = [n for n in new_nodes if n["id"] not in old_ids]
    nodes = old_nodes + add
    id_set = {n["id"] for n in nodes}

    # tag-backbone wiring for the new notes
    def tagid(t):
        return "tag_" + re.sub(r"[^a-z0-9]+", "_", t.strip().lower()).strip("_")

    tag_edges = []
    files = [l for l in (OUT / ".kh_missing.txt").read_text().splitlines() if l.strip()]
    for f in files:
        pid = f"{_arx(f)}_paper"
        for t in _parse_tags(Path(f).read_text()):
            tid = tagid(t)
            if not tid or tid == "tag_":
                continue
            if tid not in id_set:
                nodes.append({"id": tid, "label": t, "file_type": "rationale", "source_file": None,
                              "source_location": None, "source_url": None, "captured_at": None,
                              "author": None, "contributor": None})
                id_set.add(tid)
            tag_edges.append({"source": pid, "target": tid, "relation": "references", "confidence": "EXTRACTED",
                              "confidence_score": 1.0, "source_file": f, "source_location": None, "weight": 1.0})

    # additive edge merge: dedup exact (source,target,relation), drop dangling
    seen, edges = set(), []
    for e in old_edges + new_edges + tag_edges:
        s, t, r = e.get("source"), e.get("target"), e.get("relation")
        if s not in id_set or t not in id_set or (s, t, r) in seen:
            continue
        seen.add((s, t, r))
        edges.append(e)

    extraction = {"nodes": nodes, "edges": edges,
                  "hyperedges": old.get("hyperedges", []) + json.loads((OUT / ".graphify_semantic_new.json").read_text()).get("hyperedges", []),
                  "input_tokens": 0, "output_tokens": 0}
    G, _comm, gods, surprises = _rebuild(extraction, len(files))

    # cache new notes (0.8.28 format) + refresh manifest
    from graphify.cache import save_semantic_cache
    from graphify.detect import detect, save_manifest
    save_semantic_cache(new_nodes, new_edges, [])
    save_manifest(detect(KH)["files"])

    # before -> after
    def stats(gg):
        return len(gg["nodes"]), len(_edges_of(gg)), len({n.get("community") for n in gg["nodes"] if "community" in n})
    on, oe, oc = stats(old)
    ng = json.loads(GRAPH.read_text())
    nn, ne, nc = stats(ng)
    # new-paper connectivity
    new_papers = {f"{_arx(f)}_paper" for f in files}
    linked = sum(1 for p in new_papers if p in G and any(nb in old_ids for nb in G.neighbors(p)))
    print(f"NODES       {on} -> {nn}  (+{nn-on})")
    print(f"EDGES       {oe} -> {ne}  (+{ne-oe})")
    print(f"COMMUNITIES {oc} -> {nc}")
    print(f"new papers connected to >=1 existing node: {linked}/{len(new_papers)}")
    print(f"merged {nchunks} chunks (+{len(add)} nodes, {len(tag_edges)} tag edges, {nfixed} ids sanitized)")
    print("TOP GOD NODES: " + ", ".join(f"{x['label']}({x['degree']})" for x in gods[:5]))
    print("SURPRISES: " + " | ".join(f"{s['source'][:40]} -> {s['target'][:40]}" for s in surprises[:3]))

    for f in (glob.glob(str(OUT / ".graphify_chunk_*.json")) + glob.glob(str(OUT / ".chunklist_*.txt"))
              + [str(OUT / ".graphify_semantic_new.json"), str(OUT / ".kh_missing.txt"), str(OUT / ".graphify_old.json")]):
        Path(f).unlink(missing_ok=True)


# ---------- enrich ----------
def cmd_enrich():
    import numpy as np
    from scipy import sparse

    g, links = _load_graph()
    id2 = {n["id"]: n for n in g["nodes"]}
    papers = [n["id"] for n in g["nodes"] if n.get("file_type") == "paper" and n["id"].endswith("_paper")]
    pset = set(papers)

    children = defaultdict(list)
    for e in links:
        s, t, r = e.get("source"), e.get("target"), e.get("relation")
        if r == "rationale_for" and t in pset and s in id2:
            children[t].append(id2[s].get("label", ""))
        if r == "references" and s in pset and isinstance(t, str) and t.startswith("tag_") and t in id2:
            children[s].append(id2[t].get("label", ""))

    STOP = set("the a an of for to in on and or with via using based model models method approach learning "
               "network networks task tasks data new from into is are be we our this that it as by at".split())
    def toks(text):
        out = []
        for w in re.findall(r"[a-zA-Z][a-zA-Z0-9\-]+", text.lower()):
            w = w.strip("-")
            if len(w) >= 3 and w not in STOP:
                out.append(w)
        return out

    docs = {p: toks(id2[p].get("label", "") + " " + " ".join(children.get(p, []))) for p in papers}
    vocab = {}
    for p in papers:
        for w in set(docs[p]):
            vocab.setdefault(w, len(vocab))
    n, V = len(papers), len(vocab)
    rows, cols, vals = [], [], []
    df = np.zeros(V)
    for i, p in enumerate(papers):
        tf = defaultdict(int)
        for w in docs[p]:
            tf[w] += 1
        for w, c in tf.items():
            rows.append(i); cols.append(vocab[w]); vals.append(c); df[vocab[w]] += 1
    idf = np.log((1 + n) / (1 + df)) + 1
    X = sparse.csr_matrix((vals, (rows, cols)), shape=(n, V), dtype=np.float64).multiply(sparse.csr_matrix(idf))
    norms = np.sqrt(np.asarray(X.multiply(X).sum(axis=1)).ravel()); norms[norms == 0] = 1
    X = sparse.diags(1 / norms) @ X.tocsr()
    Sim = (X @ X.T).toarray()
    np.fill_diagonal(Sim, 0.0)

    existing = {(e.get("source"), e.get("target")) for e in links}
    existing |= {(t, s) for s, t in existing}
    sim_edges, pairs = [], set()
    for i, p in enumerate(papers):
        for j in np.argsort(-Sim[i])[:SIM_K]:
            cs = float(Sim[i, j])
            if cs < SIM_THRESH:
                break
            q = papers[j]
            a, b = (p, q) if p < q else (q, p)
            if (a, b) in pairs or (a, b) in existing:
                continue
            pairs.add((a, b))
            score = 0.95 if cs >= 0.6 else 0.85 if cs >= 0.45 else 0.75 if cs >= 0.33 else 0.65
            sim_edges.append({"source": a, "target": b, "relation": "semantically_similar_to", "confidence": "INFERRED",
                              "confidence_score": score, "source_file": None, "source_location": None, "weight": round(cs, 3)})

    # concept hubs: named entities (acronyms / CamelCase) spanning >= N papers
    rat2paper = {e["source"]: e["target"] for e in links if e.get("relation") == "rationale_for" and e.get("target") in pset}
    tag_norms = {nid[4:] for nid in id2 if nid.startswith("tag_")}
    STOP_ENT = {"rl", "ai", "ml", "llm", "llms", "vlm", "vlms", "vla", "vlas", "cnn", "rnn", "lstm", "mlp", "gpu", "cpu",
                "api", "sota", "mdp", "pomdp", "sgd", "adam", "rgb", "iid", "ood", "mse", "kl", "ema", "dof", "nlp",
                "cot", "rag", "gru", "bert", "gpt", "relu", "json", "html", "2d", "3d", "4d", "6d", "vqa", "qa",
                "dataset", "datasets", "benchmark", "method", "model"}
    ACRO = re.compile(r"\b([A-Z][A-Za-z0-9]*[A-Z0-9])\b")
    CAMEL = re.compile(r"\b([A-Z][a-z]+(?:[A-Z][a-z0-9]+)+)\b")
    norm = lambda s: re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")
    ent_papers, disp = defaultdict(set), {}
    def scan(text, paper):
        if not paper:
            return
        for m in ACRO.findall(text) + CAMEL.findall(text):
            if len(m) < 3 or m.lower() in STOP_ENT:
                continue
            nm = norm(m)
            if not nm or nm in tag_norms:
                continue
            ent_papers[nm].add(paper); disp.setdefault(nm, m)
    for nd in g["nodes"]:
        if nd.get("file_type") == "rationale" and nd["id"] in rat2paper:
            scan(nd.get("label", ""), rat2paper[nd["id"]])
        elif nd["id"] in pset:
            scan(nd.get("label", ""), nd["id"])
    cnodes, cedges, ekeys = [], [], {(e.get("source"), e.get("target"), e.get("relation")) for e in links}
    existing_ids = set(id2)
    for ent, ps in ent_papers.items():
        if len(ps) < CONCEPT_MIN_PAPERS:
            continue
        cid = f"concept_{ent}"
        if cid not in existing_ids:
            cnodes.append({"id": cid, "label": disp[ent], "file_type": "concept", "source_file": None,
                           "source_location": None, "source_url": None, "captured_at": None, "author": None, "contributor": None})
            existing_ids.add(cid)
        for p in ps:
            if (p, cid, "references") not in ekeys:
                cedges.append({"source": p, "target": cid, "relation": "references", "confidence": "EXTRACTED",
                               "confidence_score": 1.0, "source_file": None, "source_location": None, "weight": 1.0})
                ekeys.add((p, cid, "references"))

    extraction = {"nodes": g["nodes"] + cnodes, "edges": [dict(e) for e in links] + sim_edges + cedges,
                  "hyperedges": g.get("hyperedges", []), "input_tokens": 0, "output_tokens": 0}
    G, communities, _g, _s = _rebuild(extraction, len(extraction["nodes"]))
    print(f"enrichment: +{len(sim_edges)} similarity edges, +{len(cnodes)} concept hubs (+{len(cedges)} edges)")
    print(f"graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges, {len(communities)} communities")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    OUT.mkdir(exist_ok=True)
    if cmd == "delta":
        cmd_delta()
    elif cmd == "finalize":
        cmd_finalize()
    elif cmd == "enrich":
        cmd_enrich()
    else:
        print(__doc__)
        sys.exit(2)
