"""graph_query.py — graph helpers for paper-curate.

CLI commands (one per Mode/sub-step):

    unassigned                        # Mode A Step 1: KH papers not in any General/ file
    neighbors <arxiv_id>              # Mode A Step 2: vote of neighbors' topics
    same-community <arxiv_id> <topic> # Mode A Step 3: papers in topic sharing a graph community
    audit-coverage                    # Mode B: coverage + centrality + orphans
    sprawl                            # Mode C: SPRAWL candidates
    star <topic_file>                 # Mode D [!star]: top-5 by restricted degree
    recent <topic_file> [n=5]         # Mode D [!tip]: newest arxiv IDs in topic
    bridges <topic_file>              # Mode D [!success]: cross-community bridges
    data-quality                      # Mode E: weak notes / empty frontmatter
    stale-stars                       # Mode E: which topics' [!star] blocks have drifted
    split                             # Mode E: SPLIT (community spans multiple topics)
    validate-tags                     # Mode E: drift check — routing table vs alphaxiv-summary-extract master

All commands assume cwd = vault root and read graphify-out/graph.json + General/ + _KnowledgeHub_/.
All output goes to stdout — no file writes anywhere.
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict

GRAPH_PATH = "graphify-out/graph.json"
GEN_DIR = "General"
KH_DIR = "_KnowledgeHub_"
ARXIV_PATTERN = re.compile(r"\[\[(\d{4}\.\d{4,5})")


def _load_graph() -> dict:
    """Load and return the graphify graph JSON from GRAPH_PATH."""
    return json.load(open(GRAPH_PATH))


def _edges(g: dict) -> list:
    """Return the graph's edge list (stored under the 'links' or 'edges' key)."""
    return g.get("links") or g.get("edges") or []


def _node_to_paper(g: dict) -> dict:
    """Map node_id → arxiv_id (for KH paper-nodes only)."""
    out = {}
    for n in g.get("nodes", []):
        sf = n.get("source_file") or ""
        if "_KnowledgeHub_/" in sf:
            out[n["id"]] = sf.split("_KnowledgeHub_/")[-1].replace(".md", "")
    return out


def _topic_assignments() -> dict:
    """Scan General/ for [[arxiv_id]] wikilinks → {arxiv_id: [topic_files]}."""
    out = defaultdict(set)
    if not os.path.isdir(GEN_DIR):
        return out
    for f in sorted(os.listdir(GEN_DIR)):
        if not f.endswith(".md") or f == "00_Index.md":
            continue
        try:
            for ax in ARXIV_PATTERN.findall(open(os.path.join(GEN_DIR, f)).read()):
                out[ax].add(f)
        except Exception:
            continue
    return out


def _topic_node_set(g: dict, topic_file: str) -> set:
    """Set of node IDs belonging to a General/ topic (its source_file or wikilinked KH papers)."""
    try:
        wikilinked = set(ARXIV_PATTERN.findall(open(topic_file).read()))
    except Exception:
        return set()
    topic_relpath = f"General/{os.path.basename(topic_file)}"
    out = set()
    for n in g.get("nodes", []):
        if n.get("source_file") == topic_relpath:
            out.add(n["id"])
            continue
        sf = n.get("source_file") or ""
        if "_KnowledgeHub_/" in sf:
            ax = sf.split("_KnowledgeHub_/")[-1].replace(".md", "")
            if ax in wikilinked:
                out.add(n["id"])
    return out


def _communities(g: dict) -> dict:
    """{community_id: [node_ids]}."""
    groups = defaultdict(list)
    for n in g.get("nodes", []):
        cid = n.get("community")
        if cid is not None:
            groups[cid].append(n["id"])
    return groups


def _cohesion(g: dict, groups: dict) -> dict:
    """{community_id: cohesion_float} — internal-density per community."""
    node_cid = {n["id"]: n.get("community") for n in g.get("nodes", [])}
    intra = Counter()
    for e in _edges(g):
        cs = node_cid.get(e["source"])
        if cs is not None and cs == node_cid.get(e["target"]):
            intra[cs] += 1
    out = {}
    for cid, members in groups.items():
        size = len(members)
        out[cid] = intra[cid] / (size * (size - 1) / 2) if size >= 2 else 0.0
    return out


# ───── Mode A Step 1 ─────────────────────────────────────────────────────


def cmd_unassigned() -> None:
    """KH papers with no wikilink in any General/ topic file."""
    all_kh = set(f.replace(".md", "") for f in os.listdir(KH_DIR) if f.endswith(".md"))
    assigned = set()
    for gf in os.listdir(GEN_DIR):
        if not gf.endswith(".md") or gf == "00_Index.md":
            continue
        try:
            assigned.update(ARXIV_PATTERN.findall(open(os.path.join(GEN_DIR, gf)).read()))
        except Exception:
            continue
    unassigned = sorted(all_kh - assigned)
    print(f"KH papers: {len(all_kh)}")
    print(f"Assigned: {len(assigned)}")
    print(f"Unassigned: {len(unassigned)}")
    for pid in unassigned:
        print(f"  {pid}")


# ───── Mode A Step 2 ─────────────────────────────────────────────────────


def cmd_neighbors(arxiv_id: str) -> None:
    """For an arxiv ID, vote of which General/ topics its graph neighbors belong to."""
    g = _load_graph()
    n2p = _node_to_paper(g)
    target_sf = f"_KnowledgeHub_/{arxiv_id}.md"
    target_nodes = {n["id"] for n in g.get("nodes", []) if n.get("source_file") == target_sf}
    if not target_nodes:
        print(f"Neighbor topics for {arxiv_id}:")
        print("  (no nodes found in graph — paper may not be indexed yet)")
        return
    assigned = _topic_assignments()
    votes = Counter()
    for e in _edges(g):
        other = (
            e["target"] if e["source"] in target_nodes
            else e["source"] if e["target"] in target_nodes
            else None
        )
        if other is None or other in target_nodes:
            continue
        ax = n2p.get(other)
        if not ax or ax == arxiv_id:
            continue
        for t in assigned.get(ax, []):
            votes[t] += 1
    print(f"Neighbor topics for {arxiv_id}:")
    if not votes:
        print("  (no cross-paper neighbors found)")
    for topic, count in votes.most_common(5):
        print(f"  {count:>3}  {topic}")


# ───── Mode A Step 3 ─────────────────────────────────────────────────────


def cmd_same_community(arxiv_id: str, topic_file: str) -> None:
    """Papers already wikilinked in topic_file that share a graph community with arxiv_id."""
    g = _load_graph()
    target_sf = f"_KnowledgeHub_/{arxiv_id}.md"
    target_communities = {
        n.get("community")
        for n in g.get("nodes", [])
        if n.get("source_file") == target_sf and n.get("community") is not None
    }
    if not target_communities:
        print(f"{arxiv_id} not found in graph (or has no community).")
        return

    try:
        wikilinked = set(ARXIV_PATTERN.findall(open(topic_file).read()))
    except Exception as e:
        print(f"Could not read {topic_file}: {e}")
        return

    same_by_paper = {}  # arxiv_id → label
    for n in g.get("nodes", []):
        if n.get("community") not in target_communities:
            continue
        sf = n.get("source_file") or ""
        if "_KnowledgeHub_/" not in sf:
            continue
        ax = sf.split("_KnowledgeHub_/")[-1].replace(".md", "")
        if ax == arxiv_id or ax not in wikilinked:
            continue
        same_by_paper.setdefault(ax, n.get("label", ax))

    print(f"Papers in {topic_file} sharing a graph community with {arxiv_id}:")
    if not same_by_paper:
        print("  (none — no graph-similar neighbors already in this topic)")
        return
    for ax in sorted(same_by_paper):
        print(f"  [[{ax}|{same_by_paper[ax]}]]")


# ───── Mode B ─────────────────────────────────────────────────────────────


def cmd_audit_coverage() -> None:
    """Coverage table + unassigned-by-centrality + orphan flagging."""
    g = _load_graph()
    all_kh = set(f.replace(".md", "") for f in os.listdir(KH_DIR) if f.endswith(".md"))
    assigned = set()
    per_topic = {}
    for gf in sorted(os.listdir(GEN_DIR)):
        if not gf.endswith(".md") or gf == "00_Index.md":
            continue
        papers = set(ARXIV_PATTERN.findall(open(os.path.join(GEN_DIR, gf)).read()))
        per_topic[gf] = len(papers)
        assigned |= papers
    unassigned = sorted(all_kh - assigned)

    # Cross-paper degree per arxiv ID
    n2p = _node_to_paper(g)
    cross = Counter()
    for e in _edges(g):
        ps, pt = n2p.get(e["source"]), n2p.get(e["target"])
        if ps and pt and ps != pt:
            cross[e["source"]] += 1
            cross[e["target"]] += 1
    paper_degree = Counter()
    for nid, c in cross.items():
        p = n2p.get(nid)
        if p:
            paper_degree[p] += c

    print("Topic coverage:")
    for gf, n in sorted(per_topic.items()):
        print(f"  {gf}: {n}")
    print(f"Total KH: {len(all_kh)}  Assigned: {len(assigned)}  Unassigned: {len(unassigned)}")
    print()
    print("Unassigned (top 10 by graph centrality — high priority to assign):")
    for ax in sorted(unassigned, key=lambda a: -paper_degree.get(a, 0))[:10]:
        print(f"  {ax}  (cross-paper edges: {paper_degree.get(ax, 0)})")
    print()
    orphans = [ax for ax in all_kh if paper_degree.get(ax, 0) == 0]
    print(f"Orphans (0 cross-paper edges): {len(orphans)}")
    suspicious = []
    for ax in orphans:
        for gf, n in per_topic.items():
            if n > 30 and ax in open(os.path.join(GEN_DIR, gf)).read():
                suspicious.append(ax)
                break
    print(f"  of those, in major topics (>30 papers — suspicious, re-tag candidates): {len(suspicious)}")
    for ax in suspicious[:5]:
        print(f"    {ax}")


# ───── Mode C ─────────────────────────────────────────────────────────────


def cmd_sprawl(cohesion_threshold: float = 0.3, size_threshold: int = 5, sprawl_threshold: int = 3) -> None:
    """SPRAWL: General/ topics that span many high-cohesion communities (split candidates)."""
    g = _load_graph()
    groups = _communities(g)
    cohesion = _cohesion(g, groups)
    assigned = _topic_assignments()

    topic_cids = defaultdict(set)
    for n in g.get("nodes", []):
        cid = n.get("community")
        if cid is None or len(groups[cid]) < size_threshold:
            continue
        if cohesion[cid] < cohesion_threshold:
            continue
        sf = n.get("source_file") or ""
        if "_KnowledgeHub_/" in sf:
            ax = sf.split("_KnowledgeHub_/")[-1].replace(".md", "")
            for t in assigned.get(ax, []):
                topic_cids[t].add(cid)

    sprawls = [(t, cids) for t, cids in topic_cids.items() if len(cids) > sprawl_threshold]
    if not sprawls:
        print("No SPRAWL candidates — current topic taxonomy looks coherent.")
        return
    print("SPRAWL candidates (consider splitting):")
    for t, cids in sorted(sprawls, key=lambda x: -len(x[1])):
        print(f"  {t}: spans {len(cids)} high-cohesion communities")


# ───── Mode D [!star] ────────────────────────────────────────────────────


def cmd_star(topic_file: str, top_n: int = 5) -> None:
    """Top-N KH papers in topic ranked by topic-restricted degree."""
    g = _load_graph()
    in_topic = _topic_node_set(g, topic_file)
    if not in_topic:
        print(f"No nodes match topic {topic_file}")
        return
    deg = Counter()
    for e in _edges(g):
        if e["source"] in in_topic and e["target"] in in_topic:
            deg[e["source"]] += 1
            deg[e["target"]] += 1
    nodes_by_id = {n["id"]: n for n in g.get("nodes", [])}
    print(f"Top-{top_n} [!star] candidates for {topic_file}:")
    count = 0
    for nid, d in deg.most_common():
        n = nodes_by_id.get(nid)
        if not n or n.get("file_type") != "paper":
            continue
        sf = n.get("source_file", "") or ""
        if "_KnowledgeHub_/" not in sf:
            continue
        ax = sf.split("_KnowledgeHub_/")[-1].replace(".md", "")
        print(f"  [[{ax}|{n.get('label', ax)}]] (degree {d})")
        count += 1
        if count >= top_n:
            break


# ───── Mode D [!tip] ─────────────────────────────────────────────────────


def cmd_recent(topic_file: str, n: int = 5) -> None:
    """N newest arxiv IDs in the topic (lexical sort — arxiv IDs are date-prefixed)."""
    try:
        wikilinked = set(ARXIV_PATTERN.findall(open(topic_file).read()))
    except Exception as e:
        print(f"Could not read {topic_file}: {e}")
        return
    newest = sorted(wikilinked, reverse=True)[:n]
    print(f"Newest {n} papers in {topic_file}:")
    for ax in newest:
        kh_path = f"_KnowledgeHub_/{ax}.md"
        marker = "✓" if os.path.exists(kh_path) else "✗ (KH note missing)"
        print(f"  {ax}  {marker}")


# ───── Mode D [!success] ─────────────────────────────────────────────────


def cmd_bridges(topic_file: str, top_n: int = 5) -> None:
    """Topic papers ranked by edges into OTHER communities (recipe-bridge candidates)."""
    g = _load_graph()
    in_topic = _topic_node_set(g, topic_file)
    if not in_topic:
        print(f"No nodes match topic {topic_file}")
        return
    node_cid = {n["id"]: n.get("community") for n in g.get("nodes", [])}
    in_topic_cids = {node_cid[nid] for nid in in_topic if node_cid.get(nid) is not None}

    bridge_count = Counter()
    for e in _edges(g):
        s, t = e["source"], e["target"]
        cs, ct = node_cid.get(s), node_cid.get(t)
        if cs in in_topic_cids and ct is not None and ct not in in_topic_cids:
            bridge_count[s] += 1
        if ct in in_topic_cids and cs is not None and cs not in in_topic_cids:
            bridge_count[t] += 1

    nodes_by_id = {n["id"]: n for n in g.get("nodes", [])}
    print(f"Top-{top_n} bridge papers for {topic_file}:")
    count = 0
    for nid, n_other in bridge_count.most_common():
        n = nodes_by_id.get(nid)
        if not n or n.get("file_type") != "paper":
            continue
        if nid not in in_topic:
            continue
        print(f"  {n.get('label', nid)} → bridges {n_other} other communities")
        count += 1
        if count >= top_n:
            break


# ───── Mode E data-quality ──────────────────────────────────────────────


def cmd_data_quality() -> None:
    """Find KH notes with weak Method sections or empty authors/tags/aliases."""
    issues = []
    for f in sorted(os.listdir(KH_DIR)):
        if not f.endswith(".md"):
            continue
        content = open(os.path.join(KH_DIR, f)).read()
        pid = f.replace(".md", "")
        if "authors: []" in content:
            issues.append(f"  {pid}: empty authors")
        if "tags: []" in content:
            issues.append(f"  {pid}: empty tags")
        if "aliases: []" in content:
            issues.append(f"  {pid}: empty aliases")
        m = re.search(r"## Method\n(.*?)(\n## )", content, re.DOTALL)
        if m and len(m.group(1).strip()) < 50:
            issues.append(f"  {pid}: weak Method section ({len(m.group(1).strip())} chars)")
    print(f"Issues found: {len(issues)}")
    for i in issues:
        print(i)


# ───── Mode E stale-stars ────────────────────────────────────────────────


def cmd_stale_stars() -> None:
    """For each topic, check whether current [!star] papers still match the graph's top-5."""
    g = _load_graph()
    nodes_by_id = {n["id"]: n for n in g.get("nodes", [])}

    for gf in sorted(os.listdir(GEN_DIR)):
        if not gf.endswith(".md") or gf == "00_Index.md":
            continue
        path = os.path.join(GEN_DIR, gf)
        content = open(path).read()
        # Locate any [!star] block — extract arxiv IDs cited within it
        star_blocks = re.findall(r">\s*\[!star\][^\n]*\n(?:>[^\n]*\n)+", content, re.IGNORECASE)
        if not star_blocks:
            continue
        current_stars = set()
        for b in star_blocks:
            current_stars.update(re.findall(r"\[\[(\d{4}\.\d{4,5})", b))

        # Compute graph's top-5 for this topic
        in_topic = _topic_node_set(g, path)
        if not in_topic:
            continue
        deg = Counter()
        for e in _edges(g):
            if e["source"] in in_topic and e["target"] in in_topic:
                deg[e["source"]] += 1
                deg[e["target"]] += 1
        top5_arxiv = []
        for nid, _ in deg.most_common():
            n = nodes_by_id.get(nid)
            if not n or n.get("file_type") != "paper":
                continue
            sf = n.get("source_file", "") or ""
            if "_KnowledgeHub_/" not in sf:
                continue
            top5_arxiv.append(sf.split("_KnowledgeHub_/")[-1].replace(".md", ""))
            if len(top5_arxiv) >= 5:
                break

        graph_top5 = set(top5_arxiv)
        stale = current_stars - graph_top5
        missing = graph_top5 - current_stars
        if stale or missing:
            print(f"  {gf}: {len(stale)} stale, {len(missing)} missing from top-5")
            if missing:
                # Only show what graph thinks SHOULD be starred — actionable
                print(f"    suggest adding: {', '.join(sorted(missing))}")
        else:
            print(f"  {gf}: stable")


# ───── Mode E SPLIT ──────────────────────────────────────────────────────


def cmd_split(cohesion_threshold: float = 0.5, size_threshold: int = 10, off_dom_threshold: float = 0.4) -> None:
    """SPLIT: high-cohesion communities whose papers span multiple General/ topics."""
    g = _load_graph()
    groups = _communities(g)
    cohesion = _cohesion(g, groups)
    assigned = _topic_assignments()

    findings = []
    for cid, members in groups.items():
        if len(members) < size_threshold or cohesion[cid] < cohesion_threshold:
            continue
        topic_counts = Counter()
        for nid in members:
            for n in g.get("nodes", []):
                if n["id"] == nid:
                    sf = n.get("source_file") or ""
                    if "_KnowledgeHub_/" in sf:
                        ax = sf.split("_KnowledgeHub_/")[-1].replace(".md", "")
                        for t in assigned.get(ax, []):
                            topic_counts[t] += 1
                    break
        total = sum(topic_counts.values())
        if total == 0 or len(topic_counts) < 2:
            continue
        dominant, dom_count = topic_counts.most_common(1)[0]
        off_dom = 1 - dom_count / total
        if off_dom >= off_dom_threshold:
            findings.append((cid, len(members), cohesion[cid], dominant, topic_counts))

    if not findings:
        print("No SPLIT mismatches — communities align with topic taxonomy.")
        return
    print("SPLIT mismatches (community spans multiple topics):")
    for cid, size, coh, dom, counts in sorted(findings, key=lambda x: -x[1])[:10]:
        others = ", ".join(f"{t} ({c})" for t, c in counts.most_common()[1:3])
        print(f"  Community {cid} ({size} papers, cohesion {coh:.2f}): mostly {dom}; also {others}")


# ───── Mode E validate-tags ──────────────────────────────────────────────


SKILL_PATH = ".claude/skills/paper-curate/SKILL.md"
ALPHAXIV_PATH = ".claude/skills/alphaxiv-summary-extract/SKILL.md"
TAG_TOKEN = re.compile(r"`([A-Za-z0-9][A-Za-z0-9_-]*?)`")


def _extract_tags_in_table(path: str, header_marker: str) -> set:
    """Pull backtick-quoted tag tokens from the markdown table that follows header_marker.

    Scans only lines starting with `|` (table rows) and skips the header/separator rows.
    """
    text = open(path).read()
    idx = text.find(header_marker)
    if idx < 0:
        return set()
    rest = text[idx:]
    end_match = re.search(r"\n##+\s", rest[len(header_marker):])
    section = rest if not end_match else rest[: len(header_marker) + end_match.start()]

    tags = set()
    for line in section.splitlines():
        if not line.startswith("|"):
            continue
        if set(line.replace("|", "").strip()) <= set("-: "):
            continue  # separator row like |---|---|
        tags.update(TAG_TOKEN.findall(line))
    return tags


def cmd_validate_tags() -> None:
    """Lint: every tag in paper-curate routing table must appear in alphaxiv master vocabulary."""
    master = _extract_tags_in_table(ALPHAXIV_PATH, "Canonical Tag Taxonomy")
    routing = _extract_tags_in_table(SKILL_PATH, "Tag → Topic mapping")

    if not master:
        print(f"ERROR: could not parse master vocabulary from {ALPHAXIV_PATH}")
        sys.exit(2)
    if not routing:
        print(f"ERROR: could not parse routing table from {SKILL_PATH}")
        sys.exit(2)

    unknown_in_routing = routing - master
    unmapped_in_master = master - routing

    print(f"Master vocabulary: {len(master)} tags")
    print(f"Routing table:     {len(routing)} tags")
    print()
    if unknown_in_routing:
        print(f"❌ Unknown tags in routing table (not in master vocabulary):")
        for t in sorted(unknown_in_routing):
            print(f"   {t}")
    else:
        print("✓ All routing tags exist in master vocabulary.")
    print()
    if unmapped_in_master:
        print(f"ℹ Tags in master vocabulary with no topic routing (orthogonal qualifiers — usually fine):")
        for t in sorted(unmapped_in_master):
            print(f"   {t}")

    if unknown_in_routing:
        sys.exit(1)


# ───── Dispatch ──────────────────────────────────────────────────────────

COMMANDS = {
    "unassigned": cmd_unassigned,
    "neighbors": cmd_neighbors,
    "same-community": cmd_same_community,
    "audit-coverage": cmd_audit_coverage,
    "sprawl": cmd_sprawl,
    "star": cmd_star,
    "recent": cmd_recent,
    "bridges": cmd_bridges,
    "data-quality": cmd_data_quality,
    "stale-stars": cmd_stale_stars,
    "split": cmd_split,
    "validate-tags": cmd_validate_tags,
}


def main() -> None:
    """Dispatch the named CLI subcommand to its handler, or print usage and exit 1."""
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    args = sys.argv[2:]
    try:
        COMMANDS[cmd](*args)
    except TypeError as e:
        print(f"usage error in `{cmd}`: {e}\n")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
