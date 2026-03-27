---
name: knowledgehub-query
description: Read _KnowledgeHub_ paper notes and answer questions about them. Use this whenever the user references @_KnowledgeHub_, provides a list of arxiv IDs or URLs, and wants to compare, summarize, categorize, or analyze papers. Also trigger when the user says "from my notes", "from the knowledge hub", or "what do my notes say about". Runs a script to extract and print all matching note content, then synthesizes the answer from the structured summaries.
---

# KnowledgeHub Query

When the user asks about specific papers by providing arxiv IDs or URLs, run the extraction script to load their note content, then answer from what the notes say.

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
