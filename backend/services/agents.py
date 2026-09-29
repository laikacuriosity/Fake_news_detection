from services.classifier import classify
from services.retriever import search_news, search_news_for_claims
from services.image_search import reverse_image_search
from rag.ingest import query_trusted_sources
from services.claim_extraction import extract_claims
from services.stance_detection import detect_stance
from urllib.parse import urlparse

# Multi-factor credibility mapping (Phase 1, #5)
CREDIBLE_DOMAINS = {
    "reuters.com": 0.95, "apnews.com": 0.95, "factcheck.org": 0.9,
    "fullfact.org": 0.9, "bbc.com": 0.85, "who.int": 0.9,
    "pib.gov.in": 0.85, "wikipedia.org": 0.6,
    "snopes.com": 0.9
}

def _get_domain(url: str) -> str:
    try:
        domain = urlparse(url).netloc.lower()
        if domain.startswith("www."):
            domain = domain[4:]
        return domain
    except:
        return ""

def claim_extractor_node(state):
    """Extracts factual claims from the article."""
    try:
        claims = extract_claims(state["article"])
        return {"claims": claims}
    except Exception as e:
        return {"claims": [], "warnings": [f"Claim extraction failed: {str(e)}"]}

def text_verifier_node(state):
    """Style-based classifier."""
    try:
        result = classify(state["article"], title=state.get("title", ""))
        return {"style_check": result}
    except Exception as e:
        return {"style_check": {"label": "UNVERIFIED", "confidence": 0.0}, "warnings": [f"Classifier failed: {str(e)}"]}

def image_verifier_node(state):
    """Reverse image search via perceptual hash."""
    if not state.get("image_url"):
        return {"image_result": None}
    try:
        result = reverse_image_search(state["image_url"])
        return {"image_result": result}
    except Exception as e:
        return {"image_result": None, "warnings": [f"Image verification failed: {str(e)}"]}

def fact_check_retriever_node(state):
    """Gathers evidence from live web + trusted RAG corpus based on claims."""
    claims = state.get("claims", [])
    
    if claims:
        live = search_news_for_claims(claims)
        
        # Combine claims for RAG or query individually
        trusted = []
        for c in claims:
            try:
                res = query_trusted_sources(c.get("text", ""))
                for r in res:
                    r["claim_id"] = c.get("claim_id")
                trusted.extend(res)
            except Exception:
                pass
    else:
        # Fallback to older logic but handle failures gracefully
        query = state["article"][:200]
        try:
            live = search_news(query)
        except Exception:
            live = []
            
        try:
            trusted = query_trusted_sources(query)
        except Exception:
            trusted = []

    return {"live_evidence": live, "trusted_evidence": trusted}

def stance_detection_node(state):
    """Calculates stance (SUPPORTS/CONTRADICTS/NEUTRAL) for each claim and evidence."""
    claims = state.get("claims", [])
    live_ev = state.get("live_evidence", [])
    trusted_ev = state.get("trusted_evidence", [])
    
    all_evidence = live_ev + trusted_ev
    stance_results = []
    
    try:
        if not claims:
            # Fallback if no claims: just use the first 200 chars as claim
            main_claim = state["article"][:200]
            for ev in all_evidence:
                stance = detect_stance(main_claim, ev.get("snippet", ""))
                stance_results.append({
                    "evidence_url": ev.get("url"),
                    "stance": stance["stance"],
                    "stance_confidence": stance["confidence"]
                })
        else:
            for c in claims:
                claim_text = c.get("text", "")
                claim_id = c.get("claim_id")
                
                # Filter evidence for this claim (if we tracked claim_id)
                relevant_ev = [ev for ev in all_evidence if ev.get("claim_id") == claim_id or "claim_id" not in ev]
                # Limit to top 5 to avoid long processing
                for ev in relevant_ev[:5]:
                    snippet = ev.get("snippet", "")
                    if not snippet:
                        continue
                    stance = detect_stance(claim_text, snippet)
                    stance_results.append({
                        "claim_id": claim_id,
                        "evidence_url": ev.get("url"),
                        "stance": stance["stance"],
                        "stance_confidence": stance["confidence"]
                    })
                    
        return {"stance_analysis": stance_results}
    except Exception as e:
        return {"stance_analysis": [], "warnings": [f"Stance detection failed: {str(e)}"]}

def source_credibility_node(state):
    """Scores source credibility safely."""
    scored = []

    for item in (state.get("trusted_evidence") or []):
        url = item.get("url", "")
        domain = _get_domain(url)
        domain_score = CREDIBLE_DOMAINS.get(domain, 0.75)  # RAG floor
        
        scored.append({
            "url": url,
            "title": item.get("title"),
            "domain": domain,
            "credibility_score": max(domain_score, 0.75),
            "origin": "trusted_corpus"
        })

    for item in (state.get("live_evidence") or []):
        url = item.get("url", "")
        domain = _get_domain(url)
        domain_score = CREDIBLE_DOMAINS.get(domain, 0.4)
        
        scored.append({
            "url": url,
            "title": item.get("title"),
            "domain": domain,
            "credibility_score": domain_score,
            "origin": "live_search"
        })

    scored.sort(key=lambda x: -x["credibility_score"])
    
    # Deduplicate by URL
    seen = set()
    deduped = []
    for s in scored:
        if s["url"] not in seen:
            seen.add(s["url"])
            deduped.append(s)
            
    return {"source_credibility": deduped}