#!/usr/bin/env python3
"""Generate comprehensive paper listing markdown for each General/ topic."""

import json, re
from pathlib import Path
from collections import defaultdict

VAULT = Path(__file__).resolve().parents[2]
ASSIGNMENTS = VAULT / "General" / "scripts" / "assignments.json"
OUTPUT_DIR = VAULT / "General" / "scripts" / "listings"

# Subtopic grouping: map secondary tags to readable subtopic names
SUBTOPIC_MAP = {
    1: {  # Foundation Models
        "Vision Transformers": {"transformer", "vision-transformer", "vision", "attention", "architecture"},
        "Self-Supervised Learning": {"self-supervised", "self-supervised-learning", "masked-image-modeling", "contrastive-learning", "representation-learning", "SSL"},
        "Large Language Models": {"LLM", "llm", "language-model", "llm-training", "post-training"},
        "Efficient Training & Inference": {"efficient-inference", "efficiency", "PEFT", "LoRA", "quantization", "pruning", "model-compression", "distillation", "optimization"},
        "Alignment & Adaptation": {"alignment", "fine-tuning", "pre-training", "transfer-learning", "domain-adaptation"},
        "Theory & Interpretability": {"interpretability", "mechanistic-interpretability", "theory", "bayesian-inference", "scaling"},
    },
    2: {  # Vision-Language Models
        "Contrastive Alignment": {"contrastive-learning", "open-vocabulary", "vision-language"},
        "Visual Grounding": {"visual-grounding", "referring-expression", "phrase-grounding", "region-language"},
        "Visual Question Answering": {"VQA", "visual-question-answering"},
        "Hallucination": {"hallucination"},
        "Prompt Learning": {"prompt-learning", "prompt-tuning"},
        "Image-Text Understanding": {"image-captioning", "image-text"},
    },
    3: {  # Reasoning & Planning
        "Chain-of-Thought": {"chain-of-thought", "reasoning"},
        "Agentic Reasoning": {"planning", "search"},
        "Program-Aided": {"code-reasoning", "program-synthesis"},
        "Visual Reasoning": {"visual-reasoning", "spatial-reasoning"},
        "Mathematical Reasoning": {"mathematical-reasoning"},
        "Test-Time Scaling": {"test-time-compute", "test-time-scaling", "slow-thinking"},
    },
    4: {  # Reinforcement Learning
        "RL for LLM Reasoning": {"RLHF", "GRPO", "RLVR", "preference-optimization", "DPO", "reward-model", "reward-modeling"},
        "Model-Based RL & World Models": {"model-based-RL", "world-model"},
        "Policy Optimization": {"policy-optimization", "PPO", "actor-critic"},
        "Exploration & Curiosity": {"exploration", "curiosity"},
        "Visual & Multimodal RL": {"visual-reasoning", "multimodal"},
        "General RL": {"reinforcement-learning", "RL", "offline-RL", "Q-learning", "inverse-RL", "value-function"},
    },
    5: {  # Computer Vision & 3D
        "Object Detection": {"object-detection", "open-set", "zero-shot-detection"},
        "Segmentation": {"segmentation", "semantic-segmentation", "instance-segmentation", "panoptic"},
        "3D Understanding": {"3D", "3D-understanding", "3D-reconstruction", "point-cloud", "depth-estimation", "monocular", "articulated-objects", "scene-understanding", "scene-graph"},
        "Few-Shot & Zero-Shot": {"few-shot-learning", "few-shot", "one-shot", "zero-shot"},
        "Domain Adaptation": {"domain-adaptation", "unsupervised-domain-adaptation", "transfer-learning"},
        "Vision Architectures": {"vision-transformer", "dense-prediction", "feature-extraction"},
    },
    6: {  # Video & Temporal
        "Video Understanding": {"video-understanding", "video-reasoning", "action-recognition", "video-captioning"},
        "Video Generation": {"video-generation", "video-editing"},
        "Motion Generation": {"motion-generation", "human-motion", "optical-flow"},
        "Spatio-Temporal": {"spatio-temporal", "temporal", "diffusion-transformer"},
    },
    7: {  # Robotics & Embodied AI
        "Vision-Language-Action (VLA)": {"VLA"},
        "World Action Models (WAM)": {"WAM", "world-model"},
        "Manipulation": {"manipulation", "grasping", "teleoperation"},
        "Navigation": {"navigation", "autonomous-driving"},
        "Embodied AI": {"embodied-AI", "sim-to-real", "humanoid", "quadruped"},
        "Imitation Learning": {"imitation-learning"},
    },
    8: {  # Benchmarks & Surveys
        "Surveys": {"survey"},
        "Benchmarks": {"benchmark"},
        "Datasets": {"dataset"},
        "Evaluation": {"evaluation"},
    },
    9: {  # Multimodal LLMs
        "Multimodal Architectures": {"multi-modal", "multimodal", "MLLM"},
        "Instruction Tuning": {"instruction-tuning", "visual-instruction"},
        "Audio-Visual": {"audio-visual", "omni-modal"},
        "Any-to-Any Generation": {"any-to-any", "image-text"},
    },
    10: {  # Agents & Tool Use
        "LLM Agents": {"agent", "agents", "agentic-ai", "agentic"},
        "Tool Use": {"tool-use", "function-calling"},
        "Multi-Agent": {"multi-agent"},
        "Code Generation": {"code-generation"},
        "Skill Libraries": {"skill-library"},
    },
    11: {  # Self-Evolving AI
        "Self-Training & Bootstrapping": {"self-training", "bootstrapping", "self-rewarding"},
        "Self-Improvement": {"self-improvement", "self-evolving", "self-play"},
        "Curriculum Learning": {"curriculum-learning", "auto-curriculum"},
        "Meta-Learning": {"meta-learning"},
        "Evolutionary Methods": {"evolutionary", "neuroevolution"},
        "Continual Learning": {"continual-learning", "lifelong-learning"},
    },
    12: {  # Diffusion & Generation
        "Diffusion Models": {"diffusion", "denoising", "score-matching"},
        "Flow Matching": {"flow-matching"},
        "Image Generation": {"image-generation", "text-to-image", "image-synthesis", "generative-model", "generative"},
        "Image Editing": {"image-editing", "inpainting", "style-transfer", "super-resolution"},
    },
}


def assign_subtopic(paper, topic_num):
    """Assign a paper to a subtopic within its topic."""
    tag_set = set(paper["tags"])
    subtopics = SUBTOPIC_MAP.get(topic_num, {})

    for subtopic_name, subtopic_tags in subtopics.items():
        if tag_set & subtopic_tags:
            return subtopic_name

    return "Other"


def generate_listing(topic_num, papers):
    """Generate markdown listing for a topic."""
    # Group by subtopic
    groups = defaultdict(list)
    for paper in papers:
        subtopic = assign_subtopic(paper, topic_num)
        groups[subtopic].append(paper)

    lines = []
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Complete Paper Listing")
    lines.append("")

    # Sort subtopics, put "Other" last
    sorted_subtopics = sorted(groups.keys(), key=lambda x: (x == "Other", x))

    for subtopic in sorted_subtopics:
        sub_papers = sorted(groups[subtopic], key=lambda x: x["id"])
        lines.append(f"### {subtopic} ({len(sub_papers)})")
        lines.append("")
        lines.append("| Paper | Year | Summary |")
        lines.append("| --- | --- | --- |")
        for p in sub_papers:
            alias = p["alias"].replace("|", "\\|")
            summary = p["summary"].replace("|", "\\|")
            lines.append(f"| [[{p['id']}\\|{alias}]] | {p['year']} | {summary} |")
        lines.append("")

    return "\n".join(lines)


def main():
    with open(ASSIGNMENTS) as f:
        assignments = json.load(f)

    OUTPUT_DIR.mkdir(exist_ok=True)

    for topic_num_str, papers in assignments.items():
        topic_num = int(topic_num_str)
        listing = generate_listing(topic_num, papers)
        out_file = OUTPUT_DIR / f"topic_{topic_num:02d}.md"
        out_file.write_text(listing, encoding="utf-8")
        print(f"Topic {topic_num:2d}: {len(papers):3d} papers -> {out_file.name}")


if __name__ == "__main__":
    main()
