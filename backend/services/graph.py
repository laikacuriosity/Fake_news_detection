from langgraph.graph import StateGraph, END
from services.graph_state import VerificationState
from services.agents import (
    text_verifier_node,
    image_verifier_node,
    fact_check_retriever_node,
    source_credibility_node,
)
from services.llm import aggregator_node

def build_verification_graph():
    graph = StateGraph(VerificationState)

    graph.add_node("text_verifier", text_verifier_node)
    graph.add_node("image_verifier", image_verifier_node)
    graph.add_node("fact_check_retriever", fact_check_retriever_node)
    graph.add_node("source_credibility", source_credibility_node)
    graph.add_node("aggregator", aggregator_node)

    # entry: run text verifier, image verifier, and evidence retrieval in parallel
    graph.set_entry_point("text_verifier")
    graph.add_edge("text_verifier", "image_verifier")
    graph.add_edge("image_verifier", "fact_check_retriever")

    # credibility scoring runs after evidence is gathered
    graph.add_edge("fact_check_retriever", "source_credibility")

    # aggregator runs last, once everything is available
    graph.add_edge("source_credibility", "aggregator")
    graph.add_edge("aggregator", END)

    return graph.compile()

verification_graph = build_verification_graph()