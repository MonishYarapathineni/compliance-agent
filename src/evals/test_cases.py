"""Evaluation test cases.

Defines a curated set of golden question-answer pairs used across RAGAS
and LLM-judge evaluations.  Each entry contains a query, expected answer
snippet, and the policy sections that should be cited.
"""

from __future__ import annotations

# TODO: from datasets import Dataset

# ---------------------------------------------------------------------------
# Golden evaluation dataset
# Each dict has keys: query, ground_truth, expected_sources
# ---------------------------------------------------------------------------

GOLDEN_CASES: list[dict] = [
    # TODO: populate with realistic compliance Q&A pairs, e.g.:
    # {
    #     "query": "What is the maximum expense claim allowed per diem?",
    #     "ground_truth": "...",
    #     "expected_sources": ["expense-policy-v3.pdf#section-4"],
    # },
]

# TODO: EVAL_DATASET = Dataset.from_list(GOLDEN_CASES)
EVAL_DATASET = None
