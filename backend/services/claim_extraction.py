import ollama
import json

def extract_claims(article_text):
    prompt = f"""You are a fact-checking assistant. Extract the most important verifiable factual claims from the following article.
Focus on claims that include dates, numbers, named entities, organizations, or specific events.
Return the output ONLY as a JSON object with this exact structure:
{{
  "claims": [
    {{
      "claim_id": 1,
      "text": "Extracted claim text here",
      "importance": 0.95
    }}
  ]
}}
Do not include any markdown formatting, backticks, or extra text. Only the JSON.

Article:
{article_text}
"""
    try:
        response = ollama.chat(
            model="llama3.1",
            messages=[{"role": "user", "content": prompt}],
            format="json"
        )
        parsed = json.loads(response["message"]["content"])
        if "claims" in parsed:
            return parsed["claims"]
        return []
    except Exception as e:
        print(f"Claim extraction failed: {e}")
        # fallback: return the whole article as one claim or first 200 chars
        return [{"claim_id": 1, "text": article_text[:200], "importance": 1.0}]
