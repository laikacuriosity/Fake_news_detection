from services.classifier import classify
from services.retriever import search_news
from services.image_search import reverse_image_search
from rag.ingest import query_trusted_sources

# Basic credibility scoring — expand this list over time
CREDIBLE_DOMAINS = {
    "reuters.com": 0.95, "apnews.com": 0.95, "factcheck.org": 0.9,
    "fullfact.org": 0.9, "bbc.com": 0.85, "who.int": 0.9,
    "pib.gov.in": 0.85, "wikipedia.org": 0.6,
}

def text_verifier_node(state):
    """Agent 1: style-based classifier (logged signal, not a verdict)."""
    result = classify(state["article"])
    return {"style_check": result}

def image_verifier_node(state):
    """Agent 2: reverse image search via perceptual hash."""
    if not state.get("image_url"):
        return {"image_result": None}
    result = reverse_image_search(state["image_url"])
    return {"image_result": result}

def fact_check_retriever_node(state):
    """Agent 3: gathers evidence from live web + trusted RAG corpus."""
    query = state["article"][:200]
    live = search_news(query)
    trusted = query_trusted_sources(query)
    return {"live_evidence": live, "trusted_evidence": trusted}

def source_credibility_node(state):
    scored = []

    # Trusted RAG results start with a high baseline — they came from your curated corpus
    for item in (state.get("trusted_evidence") or []):
        url = item.get("url", "")
        domain_score = next((v for d, v in CREDIBLE_DOMAINS.items() if d in url), 0.75)
        scored.append({
            "url": url,
            "title": item.get("title"),
            "credibility_score": max(domain_score, 0.75),  # RAG membership floor
            "origin": "trusted_corpus"
        })

    # Live web results scored purely by domain reputation
    for item in (state.get("live_evidence") or []):
        url = item.get("url", "")
        domain_score = next((v for d, v in CREDIBLE_DOMAINS.items() if d in url), 0.4)
        scored.append({
            "url": url,
            "title": item.get("title"),
            "credibility_score": domain_score,
            "origin": "live_search"
        })

    scored.sort(key=lambda x: -x["credibility_score"])
    return {"source_credibility": scored}