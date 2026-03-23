#!/usr/bin/env python3
"""Assign every KnowledgeHub paper to exactly one General/ topic."""

import os, re, json, sys
from pathlib import Path

VAULT = Path(__file__).resolve().parents[2]
KH_DIR = VAULT / "_KnowledgeHub_"
OUT_FILE = VAULT / "General" / "scripts" / "assignments.json"

# Priority-ordered tag→topic mapping.
# First matching rule wins. Order matters: more specific tags first.
TAG_RULES = [
    # Topic 07: Robotics (must come before VLA/WAM get caught by RL or VLM)
    (7, {"VLA", "WAM", "manipulation", "embodied-AI", "navigation",
         "autonomous-driving", "imitation-learning", "teleoperation",
         "sim-to-real", "grasping", "humanoid", "quadruped",
         "trajectory-prediction"}),
    # Topic 06: Video & Temporal
    (6, {"video-understanding", "video-generation", "motion-generation",
         "human-motion", "temporal", "diffusion-transformer", "video-reasoning",
         "video-editing", "action-recognition", "video-captioning",
         "spatio-temporal", "optical-flow"}),
    # Topic 12: Diffusion & Generation (before foundation models catch "diffusion")
    (12, {"diffusion", "image-generation", "generative", "flow-matching",
          "text-to-image", "image-editing", "inpainting", "super-resolution",
          "style-transfer", "image-synthesis", "generative-model",
          "score-matching", "denoising"}),
    # Topic 11: Self-Evolving AI
    (11, {"self-evolving", "self-improvement", "self-play",
          "curriculum-learning", "meta-learning", "auto-curriculum",
          "self-training", "bootstrapping", "self-rewarding",
          "evolutionary", "neuroevolution"}),
    # Topic 10: Agents & Tool Use
    (10, {"agent", "tool-use", "multi-agent", "agentic-ai", "agents",
          "code-generation", "web-agent", "skill-library",
          "function-calling", "agentic"}),
    # Topic 04: Reinforcement Learning
    (4, {"reinforcement-learning", "RL", "policy-optimization",
         "RLHF", "GRPO", "reward-model", "reward-modeling",
         "offline-RL", "exploration", "curiosity",
         "PPO", "DPO", "actor-critic", "value-function",
         "inverse-RL", "model-based-RL", "Q-learning",
         "RLVR", "preference-optimization"}),
    # Topic 03: Reasoning & Planning
    (3, {"reasoning", "chain-of-thought", "planning", "tool-use",
         "test-time-compute", "test-time-scaling", "mathematical-reasoning",
         "commonsense-reasoning", "logical-reasoning", "program-synthesis",
         "code-reasoning", "visual-reasoning", "spatial-reasoning",
         "llm-reasoning", "slow-thinking", "search"}),
    # Topic 09: Multimodal LLMs (before VLM catches them)
    (9, {"multi-modal", "multimodal", "MLLM", "instruction-tuning",
         "visual-instruction", "image-text", "audio-visual",
         "omni-modal", "any-to-any"}),
    # Topic 02: Vision-Language Models
    (2, {"vision-language", "visual-grounding", "contrastive-learning",
         "open-vocabulary", "VLM", "referring-expression",
         "image-captioning", "VQA", "visual-question-answering",
         "phrase-grounding", "region-language", "hallucination",
         "prompt-learning"}),
    # Topic 05: Computer Vision & 3D
    (5, {"computer-vision", "3D", "3D-understanding", "3D-reconstruction",
         "object-detection", "segmentation", "depth-estimation",
         "few-shot-learning", "few-shot", "domain-adaptation",
         "image-classification", "semantic-segmentation",
         "instance-segmentation", "panoptic", "point-cloud",
         "scene-understanding", "scene-graph", "monocular",
         "articulated-objects", "vision-transformer", "vision",
         "image-recognition", "feature-extraction", "dense-prediction",
         "weakly-supervised", "crowded-scene", "crowd-analysis",
         "one-shot", "zero-shot-detection", "open-set",
         "transfer-learning", "unsupervised-domain-adaptation",
         "data-augmentation", "dataset-pruning", "knowledge-distillation",
         "model-merging"}),
    # Topic 08: Benchmarks & Surveys
    (8, {"benchmark", "dataset", "evaluation", "survey"}),
    # Topic 01: Foundation Models (catch-all for transformer/LLM/SSL)
    (1, {"transformer", "LLM", "llm", "foundation-model",
         "pre-training", "fine-tuning", "efficient-inference",
         "alignment", "architecture", "self-supervised",
         "self-supervised-learning", "representation-learning",
         "scaling", "tokenization", "attention", "efficiency",
         "PEFT", "LoRA", "adapter", "prompt-tuning",
         "language-model", "masked-image-modeling",
         "contrastive-learning", "SSL",
         "optimization", "training", "inference",
         "interpretability", "mechanistic-interpretability",
         "theory", "bayesian-inference",
         "continual-learning", "lifelong-learning",
         "knowledge-editing", "model-compression",
         "quantization", "pruning", "distillation",
         "llm-training", "post-training"}),
]

# Fallback: if no tag matches, assign based on robotics-related title keywords
ROBOTICS_KEYWORDS = {"robot", "manipul", "grasp", "embodied", "vla", "wam"}


def extract_frontmatter(filepath):
    """Extract tags, aliases, title from YAML frontmatter."""
    text = filepath.read_text(encoding="utf-8")
    fm_match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not fm_match:
        return [], [], ""

    fm = fm_match.group(1)
    tags = re.findall(r"^\s+-\s+(.+)$", fm, re.MULTILINE)

    # Extract title
    title_match = re.search(r'^title:\s*"(.+?)"', fm, re.MULTILINE)
    title = title_match.group(1) if title_match else ""

    # Extract first alias
    alias_section = re.search(r"^aliases:\s*\n((?:\s+-\s+.+\n?)*)", fm, re.MULTILINE)
    aliases = []
    if alias_section:
        aliases = re.findall(r"^\s+-\s+(.+)$", alias_section.group(1), re.MULTILINE)

    # Extract year from paper ID
    paper_id = filepath.stem
    year_prefix = paper_id.split(".")[0]
    if len(year_prefix) == 4 and year_prefix.isdigit():
        year = f"20{year_prefix[:2]}"
    else:
        year = "20??"

    # Extract one-line summary
    summary_match = re.search(r">\s*\[!summary\]\s*Summary\n>\s*(.+?)(?:\n|$)", text)
    summary_line = ""
    if summary_match:
        summary_line = summary_match.group(1).strip()
        # Truncate to ~120 chars
        if len(summary_line) > 120:
            summary_line = summary_line[:117] + "..."

    return tags, aliases, title, year, summary_line


def assign_paper(tags, title):
    """Assign a paper to a topic based on its tags."""
    tag_set = set(tags)
    for topic_num, rule_tags in TAG_RULES:
        if tag_set & rule_tags:
            return topic_num

    # Fallback: check title for robotics keywords
    title_lower = title.lower()
    for kw in ROBOTICS_KEYWORDS:
        if kw in title_lower:
            return 7

    return None  # unassigned


def main():
    assignments = {}  # topic_num -> list of (paper_id, alias, title, year, summary)
    unassigned = []

    for md_file in sorted(KH_DIR.glob("*.md")):
        paper_id = md_file.stem
        tags, aliases, title, year, summary = extract_frontmatter(md_file)
        alias = aliases[0] if aliases else paper_id

        topic = assign_paper(tags, title)
        if topic is None:
            unassigned.append((paper_id, alias, title, tags))
            topic = 1  # default to Foundation Models

        if topic not in assignments:
            assignments[topic] = []
        assignments[topic].append({
            "id": paper_id,
            "alias": alias,
            "title": title,
            "year": year,
            "summary": summary,
            "tags": tags,
        })

    # Sort each topic by year then ID
    for topic in assignments:
        assignments[topic].sort(key=lambda x: x["id"])

    # Report
    total = sum(len(v) for v in assignments.values())
    print(f"Total papers: {total}")
    print(f"Unassigned (defaulted to topic 1): {len(unassigned)}")
    print()

    topic_names = {
        1: "Foundation Models",
        2: "Vision-Language Models",
        3: "Reasoning & Planning",
        4: "Reinforcement Learning",
        5: "Computer Vision & 3D",
        6: "Video & Temporal",
        7: "Robotics & Embodied AI",
        8: "Benchmarks & Surveys",
        9: "Multimodal LLMs",
        10: "Agents & Tool Use",
        11: "Self-Evolving AI",
        12: "Diffusion & Generation",
    }

    for topic in sorted(assignments.keys()):
        name = topic_names.get(topic, f"Topic {topic}")
        print(f"  {topic:2d}. {name}: {len(assignments[topic])} papers")

    if unassigned:
        print(f"\nUnassigned papers:")
        for pid, alias, title, tags in unassigned:
            print(f"  {pid} | {alias} | tags: {tags}")

    # Save to JSON
    # Convert to serializable format
    out = {str(k): v for k, v in assignments.items()}
    OUT_FILE.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(f"\nSaved to {OUT_FILE}")


if __name__ == "__main__":
    main()
