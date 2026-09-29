import ollama
import json

def aggregator_node(state):
    # Prepare structured context for LLM
    structured_context = {
        "article": state.get("article", ""),
        "extracted_claims": state.get("claims", []),
        "classifier_signal": state.get("style_check", {}),
        "evidence_stances": state.get("stance_analysis", []),
        "source_credibility": state.get("source_credibility", [])[:5],
        "warnings": state.get("warnings", [])
    }
    
    img = state.get("image_result")
    if img and img.get("total_matches", 0) > 0:
        structured_context["image_check"] = img
        
    prompt = f"""You are a professional fact checker. Respond ONLY with valid JSON, no other text.
Do not invent facts. Base your verdict purely on the structured evidence below.

EVIDENCE BLOCK:
{json.dumps(structured_context, indent=2)}

Your task:
1. Review the classifier_signal.
2. Review the extracted_claims and evidence_stances. Do trusted sources CONTRADICT or SUPPORT the claims?
3. Calculate an overall verdict.
If major claims are CONTRADICTED by high credibility sources, the verdict is FAKE.
If major claims are SUPPORTED by high credibility sources, the verdict is REAL.
If evidence is missing, conflicting without a clear winner, or low credibility, the verdict is UNVERIFIED.

Respond with exactly this JSON structure:
{{
  "verdict": "FAKE" or "REAL" or "UNVERIFIED",
  "confidence": <float between 0 and 1>,
  "reasoning": "2-3 sentence explanation referencing specific evidence and source credibility"
}}
"""
    try:
        response = ollama.chat(
            model="llama3.1",
            messages=[{"role": "user", "content": prompt}],
            format="json"
        )
        parsed = json.loads(response["message"]["content"])
        return {
            "final_verdict": parsed.get("verdict", "UNVERIFIED"),
            "confidence": parsed.get("confidence", 0.5),
            "reasoning": parsed.get("reasoning", "")
        }
    except Exception as e:
        return {
            "final_verdict": "UNVERIFIED",
            "confidence": 0.0,
            "reasoning": f"Aggregation failed: {str(e)}"
        }