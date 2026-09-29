import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

NLI_MODEL_NAME = "cross-encoder/nli-deberta-v3-small"

# Lazy loading to avoid overhead when importing
nli_tokenizer = None
nli_model = None

def load_nli_model():
    global nli_tokenizer, nli_model
    if nli_model is None:
        nli_tokenizer = AutoTokenizer.from_pretrained(NLI_MODEL_NAME)
        nli_model = AutoModelForSequenceClassification.from_pretrained(NLI_MODEL_NAME)
        nli_model.eval()

def detect_stance(claim: str, evidence_text: str) -> dict:
    """
    Detects if the evidence SUPPORTS, CONTRADICTS, or is NEUTRAL to the claim.
    Returns:
    { "stance": "SUPPORTS" | "CONTRADICTS" | "NEUTRAL", "confidence": float }
    """
    load_nli_model()
    
    # Format: premise is evidence, hypothesis is claim
    inputs = nli_tokenizer(evidence_text, claim, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = nli_model(**inputs)
        
    probs = torch.softmax(outputs.logits, dim=1)
    
    # For cross-encoder/nli-deberta-v3-small, the labels are typically:
    # 0: contradiction, 1: entailment, 2: neutral
    # But let's check standard mapping. Usually: 0: contradiction, 1: entailment, 2: neutral.
    # Actually for nli-deberta-v3-small: id2label: {0: 'contradiction', 1: 'entailment', 2: 'neutral'}
    
    contradiction_prob = probs[0][0].item()
    entailment_prob = probs[0][1].item()
    neutral_prob = probs[0][2].item()
    
    max_prob = max(contradiction_prob, entailment_prob, neutral_prob)
    
    if max_prob == entailment_prob:
        return {"stance": "SUPPORTS", "confidence": entailment_prob}
    elif max_prob == contradiction_prob:
        return {"stance": "CONTRADICTS", "confidence": contradiction_prob}
    else:
        return {"stance": "NEUTRAL", "confidence": neutral_prob}

