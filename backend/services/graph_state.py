from typing import TypedDict, Optional, List, Dict, Any

class VerificationState(TypedDict):
    article: str
    image_url: Optional[str]

    # populated by agents
    style_check: Optional[Dict[str, Any]]
    live_evidence: Optional[List[Dict]]
    trusted_evidence: Optional[List[Dict]]
    source_credibility: Optional[List[Dict]]
    image_result: Optional[Dict[str, Any]]

    # final output
    final_verdict: Optional[str]
    confidence: Optional[float]
    reasoning: Optional[str]