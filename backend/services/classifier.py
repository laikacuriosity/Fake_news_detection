from services.utils.logger import logger
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from core.device import get_device

MODEL_NAME = "hamzab/roberta-fake-news-classification"
tokenizer = None
model = None
id2label = None

def _load_model():
    global tokenizer, model, id2label
    if model is None:
        device = get_device()
        try:
            tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, local_files_only=True)
            model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, local_files_only=True)
        except Exception:
            tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
        model.to(device)
        model.eval()
        id2label = model.config.id2label

def classify(text: str, title: str = ""):
    _load_model()
    device = get_device()
    # 7. Fix classifier input formatting: <title> TITLE <content> CONTENT <end>
    if title:
        formatted_text = f"<title> {title} <content> {text} <end>"
    else:
        formatted_text = f"<title> Unknown <content> {text} <end>"

    # Add long-document chunking with special token preservation
    encodings = tokenizer(
        formatted_text,
        max_length=512,
        truncation=True,
        return_overflowing_tokens=True,
        stride=128,
        padding=True,
        return_tensors="pt"
    )
    
    input_ids = encodings["input_ids"].to(device)
    attention_mask = encodings["attention_mask"].to(device)
    
    with torch.inference_mode():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        probs = torch.softmax(outputs.logits, dim=1).cpu()
        
    # Aggregate chunks (average pooling over probabilities)
    if probs.shape[0] == 0:
        return {"label": "UNVERIFIED", "confidence": 0.0}
        
    avg_probs = probs.mean(dim=0)
    confidence, prediction_idx = torch.max(avg_probs, dim=0)
    
    return {
        "label": id2label[prediction_idx.item()],
        "confidence": float(confidence.item())
    }