from ddgs import DDGS
from urllib.parse import urlparse

def search_news_for_claims(claims):
    """
    Given a list of claims, generate targeted queries and retrieve results.
    """
    results = []
    seen_urls = set()
    
    with DDGS() as ddgs:
        for claim_obj in claims:
            claim_text = claim_obj.get("text", "")
            if not claim_text:
                continue
                
            queries = [
                claim_text,
                f"{claim_text} fact check"
            ]
            
            for query in queries:
                try:
                    for r in ddgs.text(query, max_results=3):
                        url = r.get("href")
                        if url not in seen_urls:
                            seen_urls.add(url)
                            
                            domain = ""
                            try:
                                domain = urlparse(url).netloc.replace("www.", "")
                            except:
                                pass
                                
                            results.append({
                                "title": r.get("title"),
                                "url": url,
                                "domain": domain,
                                "snippet": r.get("body"),
                                "claim_id": claim_obj.get("claim_id")
                            })
                except Exception as e:
                    print(f"Web search failed for query '{query}': {e}")
                    
    return results

def search_news(query):
    # Fallback for simple queries
    results = []
    with DDGS() as ddgs:
        try:
            for r in ddgs.text(query, max_results=5):
                results.append({
                    "title": r.get("title"),
                    "url": r.get("href"),
                    "snippet": r.get("body")
                })
        except Exception:
            pass
    return results