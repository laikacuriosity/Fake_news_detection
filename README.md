# **`Fake News Detection using Langchain and Lang Graph`** : Aletheia

An AI-assisted fake news and claim verification tool. Submit an article (and optionally an image), and Aletheia runs it through a multi-agent pipeline ; a style-based classifier, live web search, a curated trusted-source knowledge base, reverse image matching, and an LLM aggregator to return a verdict backed by evidence and source credibility scoring.

## How it works

```
Article + (optional) Image
        │
        ▼
┌───────────────────────────────────────────┐
│           LangGraph orchestration          │
│                                             │
│  Text Verifier ──▶ Image Verifier          │
│       │                  │                 │
│       ▼                  ▼                 │
│  Fact-Check Retriever (live search + RAG)  │
│       │                                    │
│       ▼                                    │
│  Source Credibility Scorer                 │
│       │                                    │
│       ▼                                    │
│  Aggregator (LLM, structured JSON output)  │
└───────────────────────────────────────────┘
        │
        ▼
Verdict + Confidence + Reasoning + Evidence
```

- **Text verifier** — a HuggingFace transformer classifier (style-based signal, logged for reference, not treated as the final verdict)
- **Image verifier** — perceptual hashing (`imagehash`) against a self-built corpus of known/fact-checked images
- **Fact-check retriever** — combines live DuckDuckGo search with a ChromaDB vector store of trusted fact-checking sources (FactCheck.org, Full Fact, TruthOrFiction, and manually ingested entries)
- **Source credibility scorer** — ranks evidence by domain reputation and corpus provenance
- **Aggregator** — a local LLM (via Ollama) that reasons over all gathered evidence and returns a structured verdict: `FAKE`, `REAL`, or `UNVERIFIED`

Everything runs on free, open-source tooling.

## Stack

| Layer | Tech |
|---|---|
| Backend | FastAPI |
| Orchestration | LangGraph |
| Classifier | HuggingFace Transformers (`roberta-fake-news-classification`) |
| Evidence search | `ddgs` (DuckDuckGo, free) |
| Trusted-source RAG | ChromaDB + `sentence-transformers` |
| Image matching | `imagehash` (perceptual hashing) |
| LLM reasoning | Ollama (local, free: `llama3.1`) |
| Frontend | Single-file HTML/CSS/JS |

## Project structure

```
fake_news_detection/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── .env                    # not committed, create one to hold your 'GOOGLE_API_KEY'
│   ├── api/
│   │   └── verify.py
│   ├── services/
│   │   ├── classifier.py
│   │   ├── retriever.py
│   │   ├── llm.py               # aggregator node
│   │   ├── image_search.py
│   │   ├── agent.py            # entry point
│   │   ├── agents.py            # LangGraph agent nodes
│   │   ├── graph.py             # graph definition
│   │   └── graph_state.py
│   └── rag/
│       └── ingest.py
├── frontend/
│   └── index.html
└── README.md
```

## Setup

**1. Install backend dependencies**

```bash
cd backend
pip install -r requirements.txt --break-system-packages
```

**2. Install and run Ollama (local LLM, free)**
- Go to ollama.com/download
- Click Download for Windows
- Run the downloaded .exe installer like any normal Windows program

```bash
ollama pull llama3.1
ollama serve
```

**3. Run the backend in another terminal**

```bash
uvicorn app:app --reload
```

**4. Open the frontend**

Open `frontend/index.html` directly in a browser, or serve it:

```bash
cd frontend
python -m http.server 5500
```

Then visit `http://localhost:5500`.

## API reference

| Endpoint | Method | Description |
|---|---|---|
| `/verify` | POST | Submit `{ "article": "...", "image_url": "..." }`, returns verdict, confidence, reasoning, evidence, and credibility scores |
| `/rag/ingest-feeds` | POST | Pull recent entries from configured trusted-source RSS feeds into ChromaDB |
| `/rag/ingest-manual` | POST | Add a single fact-check document manually |
| `/rag/query` | GET | Debug: query the trusted-source vector store directly (`?q=...`) |

## Example request

```json
POST /verify
{
  "article": "NASA confirms aliens landed yesterday.",
  "image_url": null
}
```

```json
{
  "final_verdict": "FAKE",
  "confidence": 0.95,
  "reasoning": "Trusted fact-checking sources confirm NASA has made no such announcement...",
  "live_evidence": [...],
  "trusted_evidence": [...],
  "source_credibility": [...],
  "image_verification": null
}
```

## Status

- [x] Text classification + live search evidence
- [x] Reverse image matching (perceptual hash against known-image corpus)
- [x] ChromaDB RAG over trusted fact-check sources
- [x] LangGraph multi-agent orchestration
- [x] Frontend dashboard
- [ ] Parallel agent execution (currently sequential)
- [ ] Scheduled RSS ingestion job
- [ ] Kaggle-based reference corpus for style/similarity matching

## Disclaimer

This is a research and demonstration project. It is not a substitute for professional fact-checking, and verdicts should not be treated as authoritative.
