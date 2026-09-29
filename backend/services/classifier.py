import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_NAME = "hamzab/roberta-fake-news-classification"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# Use actual config labels instead of hardcoded
id2label = model.config.id2label

def classify(text: str, title: str = ""):
    # 7. Fix classifier input formatting: <title> TITLE <content> CONTENT <end>
    if title:
        formatted_text = f"<title> {title} <content> {text} <end>"
    else:
        formatted_text = f"<title> Unknown <content> {text} <end>"

    # 6. Add long-document chunking
    tokens = tokenizer(formatted_text, add_special_tokens=True, return_tensors="pt")
    input_ids = tokens["input_ids"][0]
    attention_mask = tokens["attention_mask"][0]
    
    max_len = 512
    chunks_probs = []
    
    # Process in chunks of 512
    for i in range(0, len(input_ids), max_len):
        chunk_input_ids = input_ids[i:i+max_len].unsqueeze(0)
        chunk_attention_mask = attention_mask[i:i+max_len].unsqueeze(0)
        
        with torch.no_grad():
            outputs = model(input_ids=chunk_input_ids, attention_mask=chunk_attention_mask)
            
        probs = torch.softmax(outputs.logits, dim=1)[0]
        chunks_probs.append(probs)
        
    # Aggregate chunks (average pooling over probabilities)
    if not chunks_probs:
        return {"label": "UNVERIFIED", "confidence": 0.0}
        
    avg_probs = torch.stack(chunks_probs).mean(dim=0)
    confidence, prediction_idx = torch.max(avg_probs, dim=0)
    
    return {
        "label": id2label[prediction_idx.item()],
        "confidence": float(confidence.item())
    }