"""Evaluation test cases.

Defines a curated set of golden question-answer pairs used across RAGAS
and LLM-judge evaluations.  Each entry contains a query, expected answer
snippet, and the policy sections that should be cited.
"""

from __future__ import annotations

from datasets import Dataset

# ---------------------------------------------------------------------------
# Golden evaluation dataset
# Each dict has keys: query, ground_truth, expected_sources
# ---------------------------------------------------------------------------

GOLDEN_CASES: list[dict] = [
    {
        "query": "What types of natural disasters qualify an employee for weather and safety leave?",
        "ground_truth": "Weather and safety leave covers hurricanes, tornadoes, floods, wildfires, earthquakes, landslides, and snowstorms, as well as building-specific emergencies such as fire or power outage.",
        "expected_sources": ["emergencybenefits.pdf"],
        "route": "retriever",
    },
    {
        "query": "What is the maximum number of days used to compute an advance payment during evacuation?",
        "ground_truth": "The selected time period for computing an advance payment may not exceed 30 days.",
        "expected_sources": ["emergencybenefits.pdf"],
        "route": "retriever",
    },
    {
        "query": "Can an employee care for a family member while teleworking?",
        "ground_truth": "No. An employee may not care for a family member while engaged in the performance of official duties, even during telework.",
        "expected_sources": ["elder_care_handbook-05062025.pdf"],
        "route": "retriever",
    },
    {
        "query": "How much sick leave can a federal employee use per year to care for a family member with a serious health condition?",
        "ground_truth": "An employee is entitled to use up to 12 weeks (480 hours) of sick leave each leave year to provide care for a family member with a serious health condition.",
        "expected_sources": ["elder_care_handbook-05062025.pdf"],
        "route": "retriever",
    },
    {
        "query": "Are telework employees eligible for weather and safety leave when the office is closed?",
        "ground_truth": "Generally no. Telework program participants and remote workers are ineligible for weather and safety leave when a closure is announced, unless a regulatory exception applies such as unexpected weather or unsafe telework site.",
        "expected_sources": [
            "12-23-2025-opm-2025-dismissal-and-closure-procedures.pdf"
        ],
        "route": "retriever",
    },
    {
        "query": "How do the elder care and emergency leave policies differ on telework obligations during emergencies?",
        "ground_truth": "The elder care policy allows situational telework flexibility but prohibits caregiving during official duties. The emergency leave policy mandates telework employees continue working during closures without weather and safety leave, creating a conflict for employees needing to balance caregiving and work during emergencies.",
        "expected_sources": [
            "elder_care_handbook-05062025.pdf",
            "12-23-2025-opm-2025-dismissal-and-closure-procedures.pdf",
        ],
        "route": "conflict",
    },
    {
        "query": "I have a complicated personal situation affecting my work attendance",
        "ground_truth": None,
        "expected_sources": [],
        "route": "hitl",
    },
    {
        "query": "What is the company stock option vesting schedule?",
        "ground_truth": None,
        "expected_sources": [],
        "route": "retriever",
    },
]

# Dataset for RAGAS eval — only cases with ground truth
EVAL_DATASET = Dataset.from_list(
    [case for case in GOLDEN_CASES if case["ground_truth"] is not None]
)

# Router test cases — all cases including HITL
ROUTER_TEST_CASES = GOLDEN_CASES
