# Topic-File Formatting Reference

Read this when creating or restructuring a General/ topic overview file. Covers paper ordering, callout types, wikilink format, sub-topic groups, ASCII evolution graphs, and anti-patterns.

### Paper Ordering

Within each sub-topic bullet list, sort wikilinks by **arxiv ID descending** (newest first). This surfaces the latest research immediately. The arxiv ID encodes the submission date (YYMM.NNNNN), so descending order = reverse chronological.

### Callout Types & Their Purpose

Each callout type serves a specific role in the topic overview. Using them consistently helps readers quickly find what they need.

| Callout | Syntax | Purpose | Frequency | Content Rules |
|---------|--------|---------|-----------|---------------|
| **Overview** | `> [!abstract] Overview` | Sets the scene for the entire topic — what it covers, why it matters, and how it connects to the rest of the vault | 1 per file (at top) | 2-3 sentences. Explain scope, evolution arc, and key threads. |
| **Key Papers** | `> [!star] Key Papers` | Highlights the 2-3 most impactful papers in a sub-topic — the ones a newcomer should read first | After each sub-topic group | Each entry: `- [[ID\|Name]] — 1-sentence justification`. Focus on impact (paradigm shift, SOTA, foundational) not content summary. |
| **Practical Insight** | `> [!tip] {Title}` | Synthesizes the section's papers into actionable guidance — the "so what?" for a practitioner | 1 per major `##` section (at end) | 2-3 sentences. Bridge from research to practice. Include concrete recommendations, trade-offs, or decision frameworks. |
| **Ideal Recipe** | `> [!success] {Title}` | Documents a proven, validated approach or recipe that emerged from multiple papers | Rare (0-1 per file) | Use `==highlights==` for key components. Only for well-established patterns with empirical backing. |

**When to update callouts:**
- `[!star]`: Update when a new paper is more impactful than an existing starred paper. Signs: it sets a new SOTA, introduces a paradigm shift, or is from a top group and addresses a key limitation of previously starred work.
- `[!tip]`: Update when new papers collectively shift the practical takeaway. If the old tip says "use X" but 3 recent papers show "Y is better", update it.
- `[!success]`: Update when the proven recipe changes (new component, better backbone, validated alternative).

### Wikilink Format

```
[[2602.15922|DreamZero]]
```
- Use the paper's alias from KH frontmatter as display text
- Arxiv ID without version suffix

### Sub-topic Groups

Each sub-topic group follows this pattern:
```
**{Descriptive Name}** — {1-2 sentence explanation of what these papers share}
- [[ID|Paper1]], [[ID|Paper2]], [[ID|Paper3]]
```

Rules:
- Name should be descriptive and specific (not "Other" or "Miscellaneous")
- Description explains the shared theme or approach
- Papers comma-separated on a single bullet line, sorted by ID descending
- When a sub-topic exceeds ~15 papers, split into two more specific sub-topics

### Evolution Graph Diagrams

Plain-text ASCII/Unicode box diagrams in a fenced `text` block — **not mermaid**. All 12 `General/` files were converted off mermaid (which Obsidian renders inconsistently and which invited hex-color/legend clutter); this is the current and only canonical format.

````
```text
Phase Name

╔══════════════╗
║ *Landmark (2022) ║───────► Follow-on (2023)
╚══════════════╝
       │
       ▼
┌─────────────┐
│ Other (2023) │───────► Cross-Phase Target (2024)   [Other Phase, below]
└─────────────┘


Other Phase

┌─────────────────┐
│ Cross-Phase Target (2024) │
└─────────────────┘

Legend: ╔═╗ double border + "*" prefix = landmark/foundational paper.
```
````

- Each phase is a **plain Title-Case header** (e.g. `Contrastive Alignment`, `WAMs`) — no brackets, no ALL-CAPS, no `==wrapping==`, no letter-codes (`A:`, `B:`) on nodes.
- **Unicode box-drawing only** (`┌─┐│└┘├┬┴╔═╗║╚╝`) — never ASCII `+---+` boxes.
- Node text is `Name (Year)`, plain text, no wikilinks (wikilinks live in the reference table below, not the diagram).
- **Double border (`╔═╗`) + a single leading `*`** marks a landmark/foundational node — the one paper in that phase a newcomer should recognize. Single border (`┌─┐`) for everything else. Use sparingly: not every phase needs one, and not every paper in a phase gets one.
- Cross-phase edges (an arrow pointing to a node that lives in a *different* phase block below) get a bracket hint after the target name: `───────► Target (Year)   [Phase Name, below]`.
- Exactly **one legend line** at the end of the block: `Legend: ╔═╗ double border + "*" prefix = landmark/foundational paper.` — do not restate per-node colors, hex codes, or "originally highlighted in mermaid as..." backstory; the legend explains the diagram's own symbols only.
- Update the graph when a new paper represents a significant evolution milestone — but only when it's genuinely phase-defining (the narrative's own next chapter), not merely the newest paper by date. A diagram whose newest node is a year or two behind the file's body content is normal (the diagram is a curated historical narrative, not an exhaustive feed) as long as no undiagrammed body section represents an actual missed phase of that file's own story.

### Evolution Reference Table

After the evolution graph diagram, add a **trend paragraph** (1-2 sentences explaining the evolutionary phases), then a **3-column reference table**:

```
The field evolved through N phases: **phase name** (years), **phase name** (years), ...

| Year | Paper | Contribution |
|------|-------|-------------|
| 2022 | [[2212.06817\|RT-1]] | Transformer policy on 130K real demos; proved Transformers work for robot control |
| 2024 | [[2410.24164\|π0]] | Flow matching action expert + VLM for dexterous manipulation |
```

- **Year**: extracted from the diagram node label `Name (Year)`
- **Paper**: wikilink with escaped pipe (`\|`) inside table cells
- **Contribution**: one sentence explaining what this paper introduced or proved
- Rows sorted chronologically (oldest first — this is the one place ascending order is used, because the table tells a story of progression)

### What NOT to Do

- No "Other" or "Miscellaneous" catch-all groups — every paper belongs somewhere specific
- No truncated summaries with "..." — just wikilinks grouped by method
- No flat paper dumps — every paper goes in a named sub-topic with a description
- No content duplication — summaries live in KnowledgeHub, General/ just groups and contextualizes
- No `[!star]` without explanation — always include em-dash + 1-sentence justification
- No papers sorted randomly — always sort by arxiv ID descending within each sub-topic
- General/ files should be standalone — do not cross-reference deep-dive folders
- No wikilinks inside evolution-graph diagram nodes — use plain text in nodes, put wikilinks in the reference table below
- No mermaid — evolution graphs are plain-text Unicode box diagrams (see Evolution Graph Diagrams above), not `mermaid` code blocks

