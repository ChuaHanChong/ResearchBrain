---
description: Refresh the graphify concept graph over `_KnowledgeHub_/`. Incremental — re-extracts only changed files.
---

# /kh-graph-sync

Use the **research-assistant agent** to refresh `graphify-out/graph.json` so it reflects the current state of `_KnowledgeHub_/`.

## 1. Run the skill

Invoke `Skill(skill="graphify", args="./_KnowledgeHub_ --update --no-viz")`. The skill handles the whole pipeline (detect changes → check cache → extract uncached → merge → cluster → label → report).

## 2. Bash fallback (only if the skill is unavailable)

```bash
graphify ./_KnowledgeHub_ --update --no-viz
```

## 3. Report

After completion, the agent prints:

- Nodes / edges / communities before → after
- Top 5 god nodes by degree
- Top 3 surprising connections from the report
