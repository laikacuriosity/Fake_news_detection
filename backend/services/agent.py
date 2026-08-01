from services.graph import verification_graph

def verify_news(article, image_url=None):
    initial_state = {
        "article": article,
        "image_url": image_url,
    }

    result = verification_graph.invoke(initial_state)

    return {
        "final_verdict": result.get("final_verdict"),
        "confidence": result.get("confidence"),
        "reasoning": result.get("reasoning"),
        "live_evidence": result.get("live_evidence"),
        "trusted_evidence": result.get("trusted_evidence"),
        "source_credibility": result.get("source_credibility"),
        "image_verification": result.get("image_result"),
        "_debug_style_classifier": result.get("style_check"),
    }