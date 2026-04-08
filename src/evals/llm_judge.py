"""LLM-as-judge evaluation module.

Uses a powerful LLM (e.g. GPT-4o) as an impartial judge to score agent
responses on dimensions such as correctness, citation quality, tone, and
policy adherence.  Scores are returned as structured JSON.
"""

from __future__ import annotations

# TODO: from langchain_openai import ChatOpenAI
# TODO: from langchain_core.prompts import ChatPromptTemplate
# TODO: from pydantic import BaseModel


class JudgeScore:
    """Structured output schema for a single LLM-judge evaluation."""

    # TODO: convert to Pydantic BaseModel
    # Fields: correctness (int 1-5), citation_quality (int 1-5),
    #         policy_adherence (int 1-5), reasoning (str)
    pass


def judge_response(query: str, answer: str, context: list[str]) -> dict:
    """Ask an LLM to rate the answer given the query and source context.

    Args:
        query:   The original user question.
        answer:  The agent's drafted answer.
        context: List of retrieved policy snippet strings.

    Returns:
        dict: ``JudgeScore``-shaped dict with numeric scores and reasoning.
    """
    # TODO: build structured judge prompt
    # TODO: call ChatOpenAI with with_structured_output(JudgeScore)
    # TODO: return score.model_dump()
    pass


def batch_judge(test_cases: list[dict]) -> list[dict]:
    """Run ``judge_response`` over a list of test case dicts.

    Args:
        test_cases: List of dicts with keys ``query``, ``answer``, ``context``.

    Returns:
        List of score dicts.
    """
    # TODO: return [judge_response(**tc) for tc in test_cases]
    pass
