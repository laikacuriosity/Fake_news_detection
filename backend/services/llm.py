import ollama
import json

def aggregator_node(state):
    image_context = ""
    img = state.get("image_result")
    if img and img.get("total_matches", 0) > 0:
        image_context = f"\nImage check: matches {img['total_matches']} known prior image(s): {img['matches']}"

    credibility_context = ""
    if state.get("source_credibility"):
        top_sources = state["source_credibility"][:5]
        credibility_context = f"\nSource credibility ranking (higher = more trustworthy): {top_sources}"

    prompt = f"""You are a professional fact checker. Respond ONLY with valid JSON, no other text.

Trusted source evidence (weigh most heavily): {state.get("trusted_evidence")}
General web evidence (secondary): {state.get("live_evidence")}
{credibility_context}
{image_context}

Article to verify: {state["article"]}

Respond with exactly this JSON structure:
{{
  "verdict": "FAKE" or "REAL" or "UNVERIFIED",
  "confidence": a number between 0 and 1,
  "reasoning": "2-3 sentence explanation"
}}

Prioritize higher-credibility sources. If evidence is empty or all sources are low-credibility, use "UNVERIFIED" rather than guessing."""

    response = ollama.chat(
        model="llama3.1",
        messages=[{"role": "user", "content": prompt}],
        format="json"
    )

    try:
        parsed = json.loads(response["message"]["content"])
        return {
            "final_verdict": parsed.get("verdict", "UNVERIFIED"),
            "confidence": parsed.get("confidence", 0.5),
            "reasoning": parsed.get("reasoning", "")
        }
    except (json.JSONDecodeError, KeyError):
        return {
            "final_verdict": "UNVERIFIED",
            "confidence": 0.0,
            "reasoning": "Could not parse model output."
        }