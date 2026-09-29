from typing import TypedDict, Optional, List, Dict, Any

class VerificationState(TypedDict):
    article: str
    image_url: Optional[str]
    title: Optional[str]

    # Extracted claims (from claim_extractor)
    claims: Optional[List[Dict[str, Any]]]

    # populated by agents
    style_check: Optional[Dict[str, Any]]
    live_evidence: Optional[List[Dict]]
    trusted_evidence: Optional[List[Dict]]
    
    # Credibility and stance
    source_credibility: Optional[List[Dict]]
    stance_analysis: Optional[List[Dict]]
    
    image_result: Optional[Dict[str, Any]]
    
    warnings: Optional[List[str]]

    # final output
    final_verdict: Optional[str]
    confidence: Optional[float]
    reasoning: Optional[str]