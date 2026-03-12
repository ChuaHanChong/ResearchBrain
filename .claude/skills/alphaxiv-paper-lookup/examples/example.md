# alphaxiv-paper-lookup — Usage Examples

## Queries that SHOULD trigger this skill

| Query | Why it triggers |
|-------|----------------|
| `hey can you look up this paper for me: https://arxiv.org/abs/2310.06825` | Direct arxiv URL |
| `i found this really interesting paper on diffusion models, arxiv id is 2209.00796, can you explain what it's doing?` | Explicit arxiv ID + explanation request |
| `summarize 2401.12345 for me` | Bare paper ID |
| `what's the main contribution of https://arxiv.org/pdf/2305.10601.pdf? I'm trying to understand if it's relevant to my research on LLM reasoning` | arxiv PDF URL + content question |
| `paper 2312.00752v2 — what does the methodology section say about their evaluation setup?` | Versioned paper ID + section question |
| `I'm reading through https://alphaxiv.org/overview/2406.04271 but I don't understand the loss function they describe. can you explain it?` | alphaxiv URL |
| `can you give me a quick overview of the paper 'Attention Is All You Need'? the arxiv link is https://arxiv.org/abs/1706.03762` | Named paper + arxiv URL |
| `I have this arxiv paper 2407.01234 that I need to add to my Obsidian vault. can you pull the abstract and key findings so I can write a note on it?` | arxiv ID + note-taking intent |
| `just sent you arxiv.org/abs/2501.09223 — does this paper's approach to retrieval-augmented generation differ from what we've seen before?` | arxiv URL (no https) |
| `2310.11511 what are the limitations they mention` | Bare ID + terse question |

## Queries that should NOT trigger this skill

| Query | Why it doesn't trigger |
|-------|----------------------|
| `I've been reading a lot of papers lately on transformers and I'm trying to understand multi-head attention better. can you explain how it works?` | General concept question, no specific paper |
| `download this PDF for me and convert it to markdown: https://openreview.net/pdf?id=abc123` | Non-arxiv URL (OpenReview) |
| `I want to search for recent papers on chain-of-thought prompting. where should I look?` | Paper search request, not lookup |
| `can you read this research paper I uploaded and tell me what it says? (user attaches a local PDF file)` | Local file, not arxiv |
| `I'm writing a literature review on RLHF. can you help me outline it and suggest what topics to cover?` | Topic-level task, no specific paper |
| `fetch the content from this URL and summarize it: https://proceedings.neurips.cc/paper_files/paper/2023/hash/abc.html` | Non-arxiv URL (NeurIPS proceedings) |
| `what's the difference between BERT and GPT architectures? I keep seeing it referenced in papers but I'm fuzzy on the details` | General ML concept question |
| `can you help me find the arxiv page for the original CLIP paper by OpenAI? I don't have the ID but I know it came out around 2021` | Search request (no ID known yet) |
| `I need to cite a paper in my notes. the format I need is APA. the paper is 'Language Models are Few-Shot Learners' by Brown et al.` | Citation formatting, no arxiv ID |
| `I'm reading the GPT-4 technical report (not on arxiv, it's at openai.com/research/gpt-4) — can you fetch it and summarize the safety evaluations section?` | Explicitly non-arxiv source |

## Key trigger signals

- `arxiv.org/abs/NNNN.NNNNN`
- `arxiv.org/pdf/NNNN.NNNNN`
- `alphaxiv.org/overview/NNNN.NNNNN`
- Bare ID pattern: `YYMM.NNNNN` (e.g. `2401.12345`) or versioned `2312.00752v2`
