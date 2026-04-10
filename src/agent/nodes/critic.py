"""Critic node.

Reviews the drafted answer for accuracy, completeness, citation quality, and
compliance with policy.  Stores a critique summary in ``AgentState.critique``
and can trigger a re-draft loop or HITL escalation.
"""

from __future__ import annotations

from langchain_openai import ChatOpenAI
from langgraph.graph import END
from src.agent.state import AgentState
from src.agent.utils import format_docs

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

CRITIC_PROMPT = """You are a compliance answer evaluator.

You will be given:
1. A user question
2. The source policy chunks retrieved to answer it
3. A draft answer generated from those chunks

Your job is to evaluate whether the draft answer is:
- Faithful: only states things that are supported by the source chunks
- Complete: addresses the user question fully
- Cited: references the correct source material

Scoring guide:
0.0 - 0.3: Answer is wrong, hallucinated, or completely misses the question
0.4 - 0.6: Answer is partially correct but missing key information or has unsupported claims
0.7 - 0.9: Answer is mostly correct, grounded in sources, minor gaps acceptable
1.0: Answer is complete, fully faithful to sources, and directly answers the question

User question: {query}

Source chunks:
{source_chunks}

Draft answer:
{answer}

Respond with ONLY a decimal number between 0.00 and 1.00.
Your score:"""



def critique_answer(state: dict) -> dict:
    """Evaluate the current draft answer and return a critique.

    Args:
        state: Current ``AgentState`` dict containing ``answer`` and
               ``retrieved_docs``.

    Returns:
        Partial state update with ``critique`` string and optionally
        ``needs_hitl`` flag.
    """
    # TODO: build critique prompt from answer + source docs
    # TODO: call LLM, extract structured critique (score, reasoning, flag)
    # TODO: return {"critique": <str>, "needs_hitl": bool}
    query = state["query"]
    answer = state["answer"]
    docs = format_docs(state["retrieved_docs"])
    
    response = llm.invoke(CRITIC_PROMPT.format(query=query, answer=answer, source_chunks=docs)).content.strip().lower()
    
    try:
        critique_score = float(response)
    except ValueError:
        print(f"Warning: Critic node got non-numeric response '{critique_answer}', defaulting score to 0.0")
        critique_score = 0.0
    
    if critique_score < 0.0 or critique_score > 1.0:
        print(f"Warning: Critique score {critique_score} out of bounds, defaulting to 0.0")
        critique_score = 0.0
    
    return {"critique_score": critique_score, "retry_count": state.get("retry_count", 0) + 1}
