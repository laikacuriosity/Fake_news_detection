# Aletheia Model Evaluation

## Benchmark Approach
Aletheia's V2 architecture requires evaluating the complete verification pipeline, not just the underlying NLP classifier. The verification pipeline should be evaluated on datasets that include evidence, such as **LIAR-PLUS** or **FakeNewsNet**.

## Suggested Metrics
*   **Accuracy:** Overall correct predictions (REAL vs FAKE).
*   **Precision/Recall/F1-score:** To measure performance on the FAKE class specifically.
*   **ROC-AUC:** To measure confidence calibration.
*   **Confusion Matrix:** To track MISLEADING vs FAKE vs UNVERIFIED handling.

## Baseline Comparisons
In future iterations, Aletheia will be benchmarked against these baselines:

| Model | Accuracy | Precision | Recall | F1 |
|-------|----------|-----------|--------|----|
| TF-IDF + Logistic Regression | -- | -- | -- | -- |
| TF-IDF + SVM | -- | -- | -- | -- |
| BERT (Text Only) | -- | -- | -- | -- |
| RoBERTa (Text Only) | -- | -- | -- | -- |
| RoBERTa + Evidence RAG | -- | -- | -- | -- |
| Full Aletheia | -- | -- | -- | -- |

## Ablation Study Results (To be populated)
An ablation study will measure the F1 contribution of each major component in the V2 architecture:

| Component | F1 |
|-----------|----|
| RoBERTa | 0.xx |
| + Web | 0.xx |
| + RAG | 0.xx |
| + NLI (Stance Detection) | 0.xx |
| + Image Similarity | 0.xx |
| + Source Credibility | 0.xx |
| **Full System** | **0.xx** |

## Robustness Testing
Robustness tests should include intentionally difficult examples:
*   **Paraphrasing:** "NASA confirms alien life" vs. "Nasa confrm aliens"
*   **Short Claims:** "Aliens landed on Earth."
*   **Long Articles:** 2,000–5,000 words testing chunking mechanism.
*   **Misleading Headlines:** True event + false headline.
*   **Old News as New:** 2021 event presented as 2026.
