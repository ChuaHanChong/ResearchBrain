---
name: alphaxiv-search
description: "Search and retrieve AI research papers using the alphaxiv MCP tools. Use whenever the user mentions finding papers, searching for research, looking up a paper by URL or arxiv ID, asking questions about a paper's content, exploring a paper's code repository, doing a literature review, or comparing papers. Also trigger when the user says 'search alphaxiv', 'find papers on', 'what papers exist about', 'look up this paper', or provides an arxiv URL/ID and wants it explained. This skill is the go-to guide for constructing effective search queries and combining multiple MCP tools for comprehensive research."
---

# AlphaXiv MCP Search Guide

> Tool descriptions, parameter tables, and examples below are copied from the official docs at https://www.alphaxiv.org/docs/mcp. Re-check that page if a call starts failing with "No such tool available" - the server's tool set has changed before.

## When to Use

- User wants to **find papers** on a topic, research question, or method name
- User wants to **read a paper** — fetch its full content or structured report by URL/ID
- User wants to **ask questions** about a paper (datasets, methods, hyperparameters, loss functions, results)
- User wants to **explore code** — browse a paper's GitHub repository
- User wants a **literature review** — comprehensive discovery across a research area
- User wants to **compare papers** — find related work and analyze differences
- User mentions an arxiv URL/ID and wants it explained or summarized
- You need to search for papers on any AI/ML topic

## Research Tools

### 1. `mcp__alphaxiv__discover_papers`

"Discovers and ranks multiple candidate papers for a research topic." Combines keyword search, embedding search, and optional multi-round follow-up searches.

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `keywords` | string[] | Yes | "3-4 concise keyword terms for exact-name, acronym, method, benchmark, author, or title matching" |
| `question` | string | Yes | "A detailed semantic description of the papers that would best answer the user's request" |
| `difficulty` | number (1-10) | Yes | "A 1-10 estimate of how much retrieval effort this request warrants. Higher values take longer but trigger multi-round follow-up searches" |
| `published_after` | string (YYYY-MM-DD) | No | Filter to papers published on or after this date |
| `published_before` | string (YYYY-MM-DD) | No | Filter to papers published on or before this date |
| `prioritize` | `"default"` \| `"historical"` \| `"recency"` | No | Sort results by relevance, publication history, or newest first |

**Returns:** "Ranked list of 5-15 papers, ordered by the requested priority, with: title, publication date, contributing organizations, abstract preview, and arXiv ID."

**Limitations:** "Counts against your assistant quota."

**Example calls:**
1. `keywords: ["hallucination", "LLM", "factuality"]`, `question: "Recent approaches to reducing hallucination in large language models, covering retrieval grounding, decoding-time interventions, and post-hoc verification."`, `difficulty: 5`
2. `keywords: ["RAG", "retrieval-augmented generation", "question answering"]`, `question: "Papers that use retrieval-augmented generation for open-domain question answering, including dense retrievers and reader-generator architectures."`, `difficulty: 3`
3. `keywords: ["vision-language", "multimodal alignment", "VLM"]`, `question: "How recent papers approach multi-modal alignment between vision and language models, including contrastive training, projection layers, and instruction tuning."`, `difficulty: 8`

### 2. `mcp__alphaxiv__get_paper_content`

"Get the content of an arXiv/alphaXiv paper as text. By default returns a structured AI-generated intermediate report optimized for LLM consumption. If no report is available, automatically falls back to the full extracted text. Use the fullText option to skip the report and get the raw extracted text directly."

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `url` | string (URL) | Yes | "An arXiv or alphaXiv URL (e.g., 'https://arxiv.org/abs/2307.12307', 'https://arxiv.org/pdf/2401.12345', 'https://www.alphaxiv.org/overview/2307.12307')" |
| `fullText` | boolean | No | "If true, return the full extracted text instead of the intermediate report. Defaults to false. Useful when you need raw paper content or the report is insufficient." |

**Returns:** "The paper content as text. By default, a structured AI-generated report. With fullText=true, the raw extracted text of the paper page by page."

**Limitations:** Requires arXiv/alphaXiv URLs; falls back to raw text if report unavailable.

**Example calls:**
1. `{"url": "https://arxiv.org/abs/2307.12307"}` — the AI-generated report
2. `{"url": "https://arxiv.org/abs/1706.03762", "fullText": true}` — full raw text
3. `{"url": "https://www.alphaxiv.org/overview/2512.16649"}` — via an alphaXiv URL

### 3. `mcp__alphaxiv__answer_pdf_queries`

"Returns the filtered page-level content of a single PDF that is relevant to one or more queries. Output is XML (`<paper id="..."><page num="N">...</page>...</paper>`) so you can construct citations directly from the returned page text."

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `paper` | string | Yes | "The paper to read, as an ID ('2307.12307'), a URL, or a title. Supports arXiv (arxiv.org/pdf/\*, arxiv.org/abs/\*), alphaXiv (alphaxiv.org/abs/\*), Semantic Scholar abstract pages, and direct PDF URLs." |
| `queries` | string[] | Yes | "One or more brief descriptions of the information you're looking for in the paper. Batch all questions about a paper into a single call." |

**Returns:** "XML containing only the pages relevant to your queries: `<paper id="..."><page num="N">page text</page>...</paper>`. Use the page text directly to construct citations."

**Limitations:** Supports a single PDF per call; batch queries to reduce cost.

**Example calls:**
1. `{"paper": "2307.12307", "queries": ["What datasets were used for training?"]}` — single-aspect query
2. `{"paper": "2307.12307", "queries": ["What datasets were used?", "What are the ablation results?"]}` — batched multiple questions in one call
3. Passing a direct PDF URL instead of an ID also works

### 4. `mcp__alphaxiv__read_files_from_github_repository`

"Reads the contents of files or directories from a paper's GitHub repository. This tool has special behaviors for efficient code exploration: reading '/' returns the complete file tree and all top-level files; reading a directory fetches all files in parallel; reading a file returns its contents."

**Parameters:**

| Name | Type | Required | Description |
|------|------|----------|-------------|
| `githubUrl` | string (URL) | Yes | "The URL of the paper's codebase repository (e.g., https://github.com/owner/repo)" |
| `path` | string | Yes | "The path to the file or directory. Use '/' to get the entire repository structure and top-level files." |

**Returns:** "For files: the file contents as text. For directories: list of files/directories with their contents fetched in parallel. For '/': complete file tree plus all top-level file contents."

**Limitations:** Requires valid GitHub repository URLs from papers.

**Example calls:**
1. Repository overview: `{"githubUrl": "https://github.com/openai/gpt-2", "path": "/"}`
2. Read a specific file: `{"githubUrl": "https://github.com/openai/gpt-2", "path": "src/model.py"}`
3. Read all files in a directory: `{"githubUrl": "https://github.com/openai/gpt-2", "path": "src/utils"}`

## Common Use Cases

### Literature Review
1. Use `discover_papers` to surface relevant candidates for the topic
2. Re-run `discover_papers` with varied `keywords`/`question` or a higher `difficulty` to fill gaps and ensure comprehensive coverage
3. Use `answer_pdf_queries` (batching multiple questions per paper) to extract citation-ready excerpts from each paper
4. Synthesize findings across papers

### Code Analysis
1. If the user already named a specific paper (title or arXiv ID), skip straight to `get_paper_content` - `discover_papers` can miss well-known older papers in favor of newer similar ones.
2. Extract the GitHub URL from results (or from the paper's metadata)
3. Use `read_files_from_github_repository` with `path="/"` for an overview, then drill into specific directories

### Deep Research
1. Use `discover_papers` (possibly multiple framings in parallel) to find sources
2. Use `get_paper_content` to read full text or the AI-generated report
3. Use `answer_pdf_queries` for citation-grade excerpts from specific pages
4. Use `read_files_from_github_repository` to verify implementation claims
