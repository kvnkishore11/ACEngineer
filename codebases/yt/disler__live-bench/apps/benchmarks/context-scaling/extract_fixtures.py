# /// script
# requires-python = ">=3.12"
# dependencies = ["datasets>=2.0", "huggingface_hub>=0.20"]
# ///
"""Extract GraphWalks fixtures for the context-scaling benchmark.

Generates 2 synthetic small samples (ctx_200, ctx_500) and pulls 7 real samples
from huggingface.co/datasets/openai/graphwalks (ctx_1k through ctx_64k).
Saves all 9 to fixtures.json.

The synthetic samples use the same prompt format as real GraphWalks: directed
graph edge lists with truncated MD5 hash node IDs, 4-shot preamble, and
"parents" problem type. Generated deterministically with seed=42.

Usage: uv run apps/benchmarks/context-scaling/extract_fixtures.py
"""

from __future__ import annotations

import hashlib
import json
import random
import sys
from pathlib import Path

OUTPUT_PATH = Path(__file__).resolve().parent / "fixtures.json"


# ── Synthetic GraphWalks generation ──────────────────────────────

# Preamble extracted verbatim from the real OpenAI GraphWalks dataset.
# The real dataset uses this exact preamble for every sample.
_GRAPHWALKS_PREAMBLE = """\

You will be given a graph as a list of directed edges. All nodes are at least degree 1. You will also get a description of an operation to perform on the graph.
Your job is to execute the operation on the graph and return the set of nodes that the operation results in. If asked for a breadth-first search (BFS), only return the nodes that are both reachable and exactly at that depth (not nodes at intermediate depths), and do not return the starting node. If asked for the parents of a node, only return the nodes that have an edge leading to the given node, do not return the given node itself.

Here is an example:
<begin example>

The graph has the following edges:
uvwx -> alke
abcd -> uvwx
abcd -> efgh
efgh -> uvwx

Example 1:
Operation:
Perform a BFS from node abcd with depth 1.
Final Answer: [uvwx, efgh]

Example 2:
Operation:
Perform a BFS from node alke with depth 1.
Final Answer: []

Example 3:
Operation:
Find the parents of node uvwx.
Final Answer: [abcd, efgh]

Example 4:
Operation:
Find the parents of node abcd.
Final Answer: []

<end example>
Here is the graph to operate on:
The graph has the following edges:
"""

_GRAPHWALKS_SUFFIX = """

You should reason through the operation step by step, and then return the set of nodes that the operation results in. Return your final answer as a list of nodes in the very last line of your response. For example, if the operation returns the set of nodes [node1, node2, node3], your response should be:
Final Answer: [node1, node2, node3]
If the operation returns the empty set, your response should be:
Final Answer: []
"""


def make_node_id(seed_str: str) -> str:
    """Generate a 10-char hex node ID from a seed string, matching GraphWalks format."""
    return hashlib.md5(seed_str.encode()).hexdigest()[:10]


def generate_synthetic(
    label: str,
    target_tokens: int,
    num_nodes: int,
    num_edges: int,
    rng: random.Random,
) -> dict:
    """Generate a synthetic GraphWalks-style sample with a 'parents' query.

    Creates a random directed graph, picks a target node that has at least
    1 parent, and asks: "Find the parents of node <target>."
    Uses the exact same preamble/suffix format as the real dataset.
    """
    # Generate node IDs (10-char truncated MD5, same as real dataset)
    nodes = [make_node_id(f"node_{label}_{i}") for i in range(num_nodes)]

    # Generate random directed edges (allow self-loops and duplicates like real data)
    edges: list[tuple[str, str]] = []
    for _ in range(num_edges):
        src = rng.choice(nodes)
        dst = rng.choice(nodes)
        edges.append((src, dst))

    # Pick a target node that has at least 1 parent (incoming edge from a *different* node)
    parent_map: dict[str, set[str]] = {}
    for src, dst in edges:
        if src != dst:  # self-loops don't count as parents
            parent_map.setdefault(dst, set()).add(src)

    nodes_with_parents = [n for n in parent_map if len(parent_map[n]) > 0]
    if not nodes_with_parents:
        # Fallback: add an edge to ensure at least one parent
        edges.append((nodes[0], nodes[1]))
        parent_map.setdefault(nodes[1], set()).add(nodes[0])
        nodes_with_parents = [nodes[1]]

    target = rng.choice(nodes_with_parents)

    # Compute ground truth: all nodes with a directed edge TO the target (excluding self)
    answer_nodes = sorted(parent_map[target])

    # Build edge list string (same format as real data: "src -> dst")
    edge_lines = "\n".join(f"{src} -> {dst}" for src, dst in edges)

    # Build prompt matching the exact real GraphWalks format
    prompt = (
        _GRAPHWALKS_PREAMBLE
        + edge_lines
        + f"\n\n\nOperation:\nFind the parents of node {target}.\n"
        + _GRAPHWALKS_SUFFIX
    )

    return {
        "key": label,
        "target_tokens": target_tokens,
        "prompt_chars": len(prompt),
        "problem_type": "parents",
        "synthetic": True,
        "prompt": prompt,
        "answer_nodes": answer_nodes,
    }


# ── HuggingFace extraction ──────────────────────────────────────

HF_TARGETS = [
    {"key": "ctx_1k",  "tokens": 1_024,  "target_chars": 3_584},
    {"key": "ctx_2k",  "tokens": 2_048,  "target_chars": 7_168},
    {"key": "ctx_4k",  "tokens": 4_096,  "target_chars": 14_336},
    {"key": "ctx_8k",  "tokens": 8_192,  "target_chars": 28_672},
    {"key": "ctx_16k", "tokens": 16_384, "target_chars": 57_344},
    {"key": "ctx_32k", "tokens": 32_768, "target_chars": 114_688},
    {"key": "ctx_64k", "tokens": 65_536, "target_chars": 229_376},
]


def extract_from_hf() -> list[dict]:
    """Pull 7 samples from the OpenAI GraphWalks dataset."""
    from datasets import load_dataset

    print("Loading OpenAI GraphWalks dataset from HuggingFace...", file=sys.stderr)
    ds = load_dataset("openai/graphwalks", split="train")
    print(f"  Loaded {len(ds)} samples", file=sys.stderr)

    results = []
    for target in HF_TARGETS:
        # Find closest sample by char count, requiring non-empty answer_nodes
        best_idx = None
        best_dist = float("inf")
        for i in range(len(ds)):
            row = ds[i]
            if not row["answer_nodes"]:  # skip empty answers
                continue
            dist = abs(row["prompt_chars"] - target["target_chars"])
            if dist < best_dist:
                best_dist = dist
                best_idx = i

        if best_idx is None:
            print(f"  WARNING: no sample found for {target['key']}", file=sys.stderr)
            continue

        row = ds[best_idx]
        print(
            f"  {target['key']}: {row['prompt_chars']:>7,} chars "
            f"(target {target['target_chars']:>7,}), "
            f"type={row['problem_type']}, "
            f"answers={len(row['answer_nodes'])} nodes",
            file=sys.stderr,
        )
        results.append({
            "key": target["key"],
            "target_tokens": target["tokens"],
            "prompt_chars": row["prompt_chars"],
            "problem_type": row["problem_type"],
            "synthetic": False,
            "prompt": row["prompt"],
            "answer_nodes": row["answer_nodes"],
        })

    return results


# ── Main ─────────────────────────────────────────────────────────

def main() -> int:
    rng = random.Random(42)

    # Generate synthetic small samples
    print("Generating synthetic samples...", file=sys.stderr)
    synthetics = [
        generate_synthetic("ctx_200", 200, num_nodes=5, num_edges=8, rng=rng),
        generate_synthetic("ctx_500", 500, num_nodes=12, num_edges=20, rng=rng),
    ]
    for s in synthetics:
        print(
            f"  {s['key']}: {s['prompt_chars']} chars, "
            f"answers={len(s['answer_nodes'])} nodes: {s['answer_nodes']}",
            file=sys.stderr,
        )

    # Extract from HuggingFace
    hf_samples = extract_from_hf()

    # Combine and save
    all_fixtures = synthetics + hf_samples
    print(f"\nSaving {len(all_fixtures)} fixtures to {OUTPUT_PATH}", file=sys.stderr)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(all_fixtures, f, indent=2)

    print("Done!", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
