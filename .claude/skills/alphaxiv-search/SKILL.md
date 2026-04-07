---
name: alphaxiv-search
description: "Search and retrieve AI research papers using the alphaxiv MCP tools. Use whenever the user mentions finding papers, searching for research, looking up a paper by URL or arxiv ID, asking questions about a paper's content, exploring a paper's code repository, doing a literature review, or comparing papers. Also trigger when the user says 'search alphaxiv', 'find papers on', 'what papers exist about', 'look up this paper', or provides an arxiv URL/ID and wants it explained. This skill is the go-to guide for constructing effective search queries and combining multiple MCP tools for comprehensive research."
---

# AlphaXiv MCP Search Guide

Reference guide for using the 6 alphaxiv MCP tools to search, retrieve, and analyze AI research papers.

**Endpoint:** `https://api.alphaxiv.org/mcp/v1`

## When to Use

- User wants to **find papers** on a topic, research question, or method name
- User wants to **read a paper** — fetch its full content or structured report by URL/ID
- User wants to **ask questions** about a paper (datasets, methods, hyperparameters, loss functions, results)
- User wants to **explore code** — browse a paper's GitHub repository
- User wants a **literature review** — comprehensive discovery across a research area
- User wants to **compare papers** — find related work and analyze differences
- User mentions an arxiv URL/ID and wants it explained or summarized
- You need to search for papers on any AI/ML topic

## Tools

### 1. `mcp__alphaxiv__embedding_similarity_search`

Search by semantic/conceptual similarity using embeddings.

**Parameter:**
- `query` (string, required): A detailed, multi-sentence search description (2-3 sentences) covering the research area from multiple angles.

**Returns:** Up to 25 papers ranked by similarity and popularity with title, visit count, likes, publication date, organizations, authors, abstract preview, and arXiv ID.

**Example queries:**
- "Research on transformer architectures using self-attention mechanisms for sequence modeling. Papers covering attention-based neural networks, positional encodings, and their applications to natural language processing tasks like translation and text generation."
- "Methods for improving reasoning capabilities in large language models through chain-of-thought prompting and self-reflection. Include work on verification and iterative refinement of generated reasoning traces."

**Tips:** Use 2-3 detailed sentences. Include key concepts, methods, applications, and related terms. Single keywords are too vague.

---

### 2. `mcp__alphaxiv__full_text_papers_search`

Search the alphaXiv database by keyword, method names, benchmarks, or author names.

**Parameter:**
- `query` (string, required): Plain keywords separated by spaces. Do NOT include quotation marks in the query string. For keyword/topic searches keep it short (3-4 terms).

**Returns:** Up to 25 papers with title, publication date, abstract preview, arXiv ID, and matching text snippets.

**Example queries:**
- Method: `LoRA low-rank adaptation`
- Author: `Yann LeCun`
- Benchmark: `GSM8K math reasoning benchmark`
- Topic: `GRPO reinforcement learning VLA`

**Tips:** Use short keyword phrases, not full sentences. No quotation marks.

---

### 3. `mcp__alphaxiv__agentic_paper_retrieval`

Agentic retrieval tool performing multi-turn searches for comprehensive coverage (beta). Intended to replace previous search tools.

**Parameter:**
- `query` (string, required): The research question or topic to find papers for. Can be a natural language question or topic description.

**Returns:** Papers ordered by relevance with title, visit count, likes, publication date, organizations, authors, abstract preview, and arXiv ID.

**Example queries:**
- "What are the latest approaches to reducing hallucination in large language models?"
- "Papers that use retrieval-augmented generation for question answering"
- "How do recent papers approach multi-modal alignment between vision and language models?"

**Tips:** Use natural language questions. This tool autonomously refines its search across multiple turns.

---

### 4. `mcp__alphaxiv__get_paper_content`

Retrieve paper content as text. Returns AI-generated structured report by default, or full extracted text.

**Parameters:**
- `url` (string URL, required): arXiv or alphaXiv URL
- `fullText` (boolean, optional): If true, return the full extracted text instead of the intermediate report. Defaults to false.

**Returns:** Structured AI-generated report (default) or raw extracted text page-by-page.

**Example URLs:**
- `https://arxiv.org/abs/2307.12307`
- `https://arxiv.org/pdf/1706.03762`
- `https://alphaxiv.org/overview/2512.16649`

**Tips:** Use the report (default) for quick understanding. Use `fullText: true` when you need equations, tables, or specific sections.

---

### 5. `mcp__alphaxiv__answer_pdf_queries`

Answer specific questions about PDF content using advanced AI analysis. Works with arXiv, alphaXiv, Semantic Scholar, or direct PDF URLs.

**Parameters:**
- `url` (string URL, required): PDF or abstract page URL
- `query` (string, required): A brief description of what information you're looking for in this paper

**Returns:** Natural language answer based on full PDF text analysis.

**Example queries:**
- "What datasets were used for training?"
- "What are the main hyperparameters used in the experiments?"
- "How does the attention mechanism work?"
- "What is the loss function and how is it computed?"
- "What are the limitations discussed by the authors?"

**Tips:** Ask specific, focused questions. One question per call for best results.

---

### 6. `mcp__alphaxiv__read_files_from_github_repository`

Read file and directory contents from paper GitHub repositories with efficient parallel fetching.

**Parameters:**
- `githubUrl` (string URL, required): Repository URL (e.g., `https://github.com/owner/repo`)
- `path` (string, required): The path to the file or directory. Use `/` to get the entire repository structure and top-level files.

**Returns:** File contents for single files. List with parallel-fetched contents for directories. Complete file tree plus top-level files for `/`.

**Example usage:**
- Repository overview: `githubUrl: "https://github.com/openai/gpt-2"`, `path: "/"`
- Read a file: `githubUrl: "https://github.com/openai/gpt-2"`, `path: "src/model.py"`
- List directory: `githubUrl: "https://github.com/openai/gpt-2"`, `path: "src/utils"`

**Tips:** Start with `path: "/"` to understand repo structure, then drill into specific files.

---

## Common Use Cases

### Literature Review
1. Use `embedding_similarity_search`, `full_text_papers_search`, and `agentic_paper_retrieval` **in parallel** to discover relevant papers
2. Re-run `embedding_similarity_search` and `full_text_papers_search` with **varied queries** to fill gaps and ensure comprehensive coverage
3. Use `answer_pdf_queries` to extract key information from each paper
4. Synthesize findings across papers

### Code Analysis
1. Use `embedding_similarity_search` or `full_text_papers_search` to find the paper
2. Extract GitHub URL from results
3. Use `read_files_from_github_repository` to explore code

### Comprehensive Paper Search
1. Use `embedding_similarity_search` for conceptual/semantic matches
2. Use `full_text_papers_search` for exact keyword matches
3. Use `agentic_paper_retrieval` for autonomous multi-turn retrieval
4. Run all three **in parallel** for maximum coverage

### Deep Research
1. Use all three search tools **in parallel** to find relevant papers
2. Re-run `embedding_similarity_search` and `full_text_papers_search` with **different queries** for holistic coverage
3. Use `get_paper_content` to read specific papers in full
4. Use `read_files_from_github_repository` to verify implementations
