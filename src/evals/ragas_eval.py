"""RAGAS evaluation module.

Runs the RAGAS evaluation framework against the compliance agent's outputs to
measure retrieval and generation quality metrics: faithfulness, answer
relevancy, context precision, and context recall.
"""

from __future__ import annotations
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_recall
from src.evals.test_cases import EVAL_DATASET
from src.agent.graph import build_graph
from langgraph.checkpoint.memory import MemorySaver
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
import mlflow

def run_ragas_eval(dataset=None) -> dict:
    """Execute RAGAS evaluation over the provided or default dataset.

    Args:
        dataset: Optional ``datasets.Dataset``; falls back to ``EVAL_DATASET``.

    Returns:
        dict: Mapping of metric name -> score.
    """

    app = build_graph(checkpointer=MemorySaver())
    
    queries, answers, contexts, ground_truths = [], [], [], []
    
    for case in EVAL_DATASET:
        # run the agent
        result = app.invoke({
            "query": case["query"],
            "retry_count": 0,
            "needs_hitl": False,
            "routed_to": None,
            "retrieved_docs": None,
            "answer": None,
            "critique": None,
            "critique_score": None,
            "hitl_response": None,
            "messages": []
        }, config={"configurable": {"thread_id": case["query"][:20]}})
        
        # collect outputs
        queries.append(case["query"])
        answers.append(result.get("answer", ""))
        contexts.append([doc.page_content for doc in result.get("retrieved_docs", [])])
        ground_truths.append(case["ground_truth"])
    
    ragas_dataset = build_ragas_dataset(queries, answers, contexts, ground_truths)
    ragas_llm = LangchainLLMWrapper(ChatOpenAI(model="gpt-4o-mini", max_tokens=4096, temperature=0.0))
    ragas_embeddings = LangchainEmbeddingsWrapper(OpenAIEmbeddings())   
    result = evaluate(
        ragas_dataset,
        metrics=[faithfulness, answer_relevancy, context_recall],
        llm=ragas_llm,
        embeddings=ragas_embeddings
        )

    mlflow.set_experiment("compliance-agent-evals")

    with mlflow.start_run(run_name="ragas_eval_v1"):
        mlflow.log_metric("faithfulness", result.to_pandas()["faithfulness"].mean())
        mlflow.log_metric("answer_relevancy", result.to_pandas()["answer_relevancy"].mean())
        mlflow.log_metric("context_recall", result.to_pandas()["context_recall"].mean())
        mlflow.log_param("k", 6)
        mlflow.log_param("chunk_size", 1024)
        mlflow.log_param("model", "gpt-4o-mini")
    return result
    


def build_ragas_dataset(queries: list, answers: list, contexts: list, ground_truths: list) -> object:
    """Construct a RAGAS-compatible ``Dataset`` from raw lists.

    Args:
        queries:       List of user question strings.
        answers:       Corresponding agent answer strings.
        contexts:      List of lists of retrieved context strings.
        ground_truths: List of reference answer strings.

    Returns:
        datasets.Dataset
    """
    return Dataset.from_dict({"question": queries, "answer": answers, "contexts": contexts, "ground_truth": ground_truths})
