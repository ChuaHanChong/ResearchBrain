---
name: knowledgehub-query
description: "Read _KnowledgeHub_ paper notes and answer questions about them. Use whenever the user references @_KnowledgeHub_, provides arxiv IDs or URLs, or wants to compare, summarize, categorize, or analyze papers from the vault. Also trigger when the user says 'from my notes', 'from the knowledge hub', 'what do my notes say about', 'compare these papers', 'summarize these papers', or asks about specific papers by ID. This is the go-to skill for answering questions grounded in existing KnowledgeHub content."
---

# KnowledgeHub Query

When the user asks about specific papers by providing arxiv IDs or URLs, run the extraction script to load their note content, then answer from what the notes say.

> **Scope**: this skill handles by-ID extraction. For free-form vault questions without IDs ("what does the vault say about X?"), the agent's Vault Search routing handles the discovery step via `Skill(skill="obsidian:obsidian-cli")` first, then passes the resulting IDs back to this skill.

## Workflow

### Step 1: Run the extraction script

From the vault root, pipe the user's full query into the script:

```bash
python .claude/skills/knowledgehub-query/scripts/extract_markdown.py --notes-dir _KnowledgeHub_ <<'QUERY'
<paste the user's full message here>
QUERY
```

The script extracts all arxiv IDs from the text (handles `https://arxiv.org/abs/2602.15922`, plain `2602.15922`, and `2602.15922v2` forms), finds the matching `_KnowledgeHub_/{id}.md` files, and prints their full content separated by dividers. Any IDs with no matching note are reported to stderr.

### Step 2: Answer from the output

Use the printed note content to answer the user's question. Each note contains:

- **Frontmatter**: `aliases` (short model name), `tags`, `authors`
- **Summary**: one-paragraph overview
- **Problem / Method / Results / Takeaways**: structured sections

Refer to papers by their alias (e.g., "DreamZero"), not their arxiv ID. Ground your answer in what the notes say — don't extrapolate from memory.

### Step 3: Handle missing papers

If any IDs have no matching KH note (reported to stderr), inform the user and offer to fetch the paper using `Skill(skill="alphaxiv-search")` or `Skill(skill="alphaxiv-summary-extract")` to add it to the vault.
