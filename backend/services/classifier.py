import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_NAME = "hamzab/roberta-fake-news-classification"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

labels = ["FAKE", "REAL"]   # Adjust if model provides different labels


def classify(text):
    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=512,
        padding=True,
    )

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = torch.softmax(outputs.logits, dim=1)

    confidence, prediction = torch.max(probabilities, dim=1)

    return {
        "label": labels[prediction.item()],
        "confidence": float(confidence.item())
    }