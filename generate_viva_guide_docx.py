import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_document():
    doc = Document()
    
    # Page setup - Margins 1 inch
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)

    # Document Header / Title
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_inst = title_p.add_run("VINAYAKA MISSION'S RESEARCH FOUNDATION\nAARUPADAI VEEDU INSTITUTE OF TECHNOLOGY (AVIT)\nDEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING\n")
    run_inst.font.name = 'Calibri'
    run_inst.font.size = Pt(12)
    run_inst.font.bold = True
    run_inst.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    sub_p = doc.add_paragraph()
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub_p.paragraph_format.space_after = Pt(12)
    run_sub = sub_p.add_run("35021M81 — MINI PROJECT TECHNICAL BLUEPRINT & VIVA DEFENSE GUIDE (v1.0.0)")
    run_sub.font.name = 'Calibri'
    run_sub.font.size = Pt(10)
    run_sub.font.bold = True
    run_sub.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    # Project Title Banner Table
    banner_table = doc.add_table(rows=1, cols=1)
    banner_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    b_cell = banner_table.cell(0, 0)
    set_cell_background(b_cell, "002B49")
    set_cell_margins(b_cell, top=200, bottom=200, left=250, right=250)
    bp = b_cell.paragraphs[0]
    bp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    bp.paragraph_format.space_before = Pt(4)
    bp.paragraph_format.space_after = Pt(4)
    brun = bp.add_run("SATYASCAN: AUTONOMOUS MULTI-SIGNAL FAKE NEWS VERIFICATION AND TRUTH INTELLIGENCE SYSTEM")
    brun.font.name = 'Calibri'
    brun.font.size = Pt(14)
    brun.font.bold = True
    brun.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # Metadata Card Table
    meta_table = doc.add_table(rows=2, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("PROJECT TEAM MEMBERS", "Sanskar Kumar (3502310567)\nJayasri (3502310530)\nSumit Kumar (3502310573)"),
        ("ACADEMIC SUPERVISOR", "Dr. G. Kavitha, Department of CSE\nAcademic Year: 2026–2027 (Odd Semester)\nStatus: Production Live (Version 1.0.0)")
    ]
    for r_idx, (k, v) in enumerate(meta_data):
        c1 = meta_table.cell(r_idx, 0)
        c2 = meta_table.cell(r_idx, 1)
        set_cell_background(c1, "F2F5F8")
        set_cell_background(c2, "FAFAFA")
        set_cell_margins(c1, 120, 120, 150, 150)
        set_cell_margins(c2, 120, 120, 150, 150)
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(k)
        r1.font.bold = True
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
        
        p2 = c2.paragraphs[0]
        p2.paragraph_format.space_after = Pt(0)
        r2 = p2.add_run(v)
        r2.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    def add_h1(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(18)
        h.paragraph_format.space_after = Pt(6)
        h.paragraph_format.keep_with_next = True
        hrun = h.add_run(text)
        hrun.font.name = 'Calibri'
        hrun.font.size = Pt(15)
        hrun.font.bold = True
        hrun.font.color.rgb = RGBColor(0x00, 0x2B, 0x49)
        return h

    def add_h2(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.keep_with_next = True
        hrun = h.add_run(text)
        hrun.font.name = 'Calibri'
        hrun.font.size = Pt(12.5)
        hrun.font.bold = True
        hrun.font.color.rgb = RGBColor(0x0A, 0x5C, 0x96)
        return h

    def add_h3(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(10)
        h.paragraph_format.space_after = Pt(2)
        h.paragraph_format.keep_with_next = True
        hrun = h.add_run(text)
        hrun.font.name = 'Calibri'
        hrun.font.size = Pt(11)
        hrun.font.bold = True
        hrun.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
        return h

    def add_qna(q_text, a_text):
        qp = doc.add_paragraph()
        qp.paragraph_format.space_before = Pt(10)
        qp.paragraph_format.space_after = Pt(2)
        qp.paragraph_format.keep_with_next = True
        qrun = qp.add_run(q_text)
        qrun.font.bold = True
        qrun.font.color.rgb = RGBColor(0x8B, 0x00, 0x00) # Dark red for Q
        
        # Answer Box
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, "F9FBFD")
        set_cell_margins(cell, 120, 120, 160, 160)
        
        # Left border border color via oxml
        tcPr = cell._tc.get_or_add_tcPr()
        tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="0A5C96"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
        tcPr.append(tcBorders)
        
        ap = cell.paragraphs[0]
        ap.paragraph_format.space_before = Pt(2)
        ap.paragraph_format.space_after = Pt(2)
        arun = ap.add_run(a_text)
        arun.font.size = Pt(10)
        arun.font.color.rgb = RGBColor(0x11, 0x11, 0x11)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # =========================================================================
    # PART 1: 14-POINT MINI-PROJECT BLUEPRINT
    # =========================================================================
    add_h1("PART 1: COMPREHENSIVE 14-POINT MINI-PROJECT BLUEPRINT")

    # Point 1
    add_h2("1. What is the Problem?")
    doc.add_paragraph(
        "Traditional automated fake news detectors treat misinformation purely as a static text-classification problem. "
        "Standard machine learning pipelines (such as TF-IDF, Naive Bayes, or standalone BERT models) analyze lexical surface syntax, "
        "word frequencies, and emotional tone to flag sensationalist words.\n\n"
        "The Epistemic Inversion Vulnerability:\n"
        "Sophisticated disinformation campaigns deliberately adopt calm, formal, academic, and journalistic language, whereas authentic breaking "
        "news dispatches frequently contain urgent, dramatic, or emotional phrasing. As a result, surface text classifiers suffer from severe false "
        "positives on genuine news and fail completely on well-written falsehoods. You cannot determine whether a factual statement is true or false "
        "by inspecting the vocabulary alone; truth requires verification against external authoritative ground-truth evidence."
    )

    # Point 2
    add_h2("2. What is My Solution?")
    doc.add_paragraph(
        "SatyaScan is an autonomous, multi-signal truth intelligence platform powered by an Epistemic Evidence-Grounding Architecture. "
        "Instead of guessing credibility from linguistic style, SatyaScan:\n"
        "• Decomposes submitted news articles into atomic, verifiable factual propositions.\n"
        "• Queries live global internet search streams (DuckDuckGo, Wikipedia, institutional news feeds) and a local ChromaDB vector vault concurrently.\n"
        "• Uses a fine-tuned DeBERTa-v3 Cross-Encoder for Natural Language Inference (NLI) to test whether retrieved evidence Supports, Contradicts, or is Neutral toward the claim.\n"
        "• Weights evidence by institutional domain credibility and synthesizes an explainable intelligence dossier with confidence metrics in under 1.5 seconds."
    )

    # Point 3
    add_h2("3. What is My Objective?")
    doc.add_paragraph(
        "Primary Objective:\n"
        "To architect, train, and deploy an end-to-end, multi-agent automated fact-verification engine that grounds live user submissions against real-world evidence in real time.\n\n"
        "Measurable Secondary Objectives:\n"
        "• Accuracy Target: Achieve >95% classification accuracy on benchmark datasets (achieved 98.4% with DeBERTa-v3 cross-encoder vs 83.2% on legacy TF-IDF).\n"
        "• Sub-Second Latency: Process multi-source retrieval, NLI cross-attention, and verdict synthesis in <1.5 seconds using GPU tensor acceleration (PyTorch CUDA on NVIDIA RTX 3050).\n"
        "• Explainability: Deliver an auditable evidence trail showing exact source citations, domain credibility scores, and sentence-level stance attributions rather than an opaque black-box score.\n"
        "• Multimodal Verification: Provide perceptual hash (pHash) matching for manipulated imagery."
    )

    # Point 4
    add_h2("4. What are the Algorithms, Functions, Methods, and Processing?")
    doc.add_paragraph(
        "Data Processing & NLP:\n"
        "• Claim Decomposition: Entity and qualifier tokenization (extract_claims) via local LLaMA-3.1 with fallback regex heuristic decomposition.\n"
        "• Dense Semantic Embedding: sentence-transformers/all-MiniLM-L6-v2 generating 384-dimensional dense semantic vectors.\n"
        "• Vector Indexing: Hierarchical Navigable Small World (HNSW) cosine similarity search in ChromaDB.\n"
        "• Perceptual Image Hashing: 64-bit Discrete Cosine Transform (DCT) perceptual hashing via imagehash.phash() with Hamming distance thresholding (<= 8).\n\n"
        "Core Neural Inference Models:\n"
        "• Cross-Encoder Stance Inference: cross-encoder/nli-deberta-v3-small evaluating joint cross-attention across premise-hypothesis pairs:\n"
        "  Softmax(Logits) -> [P(Contradiction), P(Entailment), P(Neutral)]\n"
        "• Stylistic Surface Classifier: hamzab/roberta-fake-news-classification running sliding-window chunking (512 tokens with stride 128) for auxiliary sensationalism checks.\n\n"
        "Algorithmic Methods & Functions:\n"
        "• State Machine Orchestration: langgraph.graph.StateGraph managing parallel asynchronous node execution with acyclic synchronization barriers.\n"
        "• REST Microservices: FastAPI ASGI endpoints (POST /verify, GET /health, POST /rag/ingest-manual)."
    )

    # Point 5
    add_h2("5. What is the Full Process with Technical Terms (End-to-End Pipeline)?")
    doc.add_paragraph(
        "The end-to-end processing pipeline executes across seven distinct engineering stages:\n\n"
        "1. Ingestion & Preprocessing: The user submits news text and optional image URL. Text length is validated (<= 10,000 chars), inputs sanitized, and image pHash computed.\n"
        "2. Parallel Agent Fan-Out (LangGraph): LangGraph simultaneously triggers the Claim Extractor (entity/date parsing), RoBERTa Stylistic Classifier (sliding-window tokens), and Image Verifier.\n"
        "3. Multi-Stream Evidence Harvesting: Parallel workers query DuckDuckGo, Wikipedia REST APIs, and ChromaDB vector vault (top-k=5, 384-dim cosine search).\n"
        "4. Relevance Filtering & Epistemic Calibration: Dynamic token overlap filters out unrelated snippets: min_required = min(2, len(claim_words)).\n"
        "5. DeBERTa-v3 Cross-Encoder Stance Inference: Premise-hypothesis pairs are processed through joint cross-attention to produce Softmax probabilities for Entailment, Contradiction, and Neutral.\n"
        "6. Credibility-Weighted Bayesian Aggregator: Stance scores are modulated by domain authority weights (W = Credibility_Score * Stance_Confidence) to synthesize final verdict (REAL / FAKE / UNVERIFIED).\n"
        "7. Output Generation & Client Telemetry: Results are packaged into a structured JSON payload and displayed as an interactive forensic dossier with confidence gauge and cited sources."
    )

    # Point 6 Table
    add_h2("6. Why This Algorithm/Model/Function, and Why Not Others? (Trade-offs & Justification)")
    t6 = doc.add_table(rows=5, cols=4)
    t6.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Component", "Why Chosen?", "What Was Rejected?", "Why Rejected?"]
    for i, h_text in enumerate(headers):
        cell = t6.cell(0, i)
        set_cell_background(cell, "002B49")
        set_cell_margins(cell, 100, 100, 120, 120)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    t6_data = [
        ("Cross-Encoder DeBERTa-v3", 
         "Joint token-level cross-attention across premise & hypothesis. Disentangled attention captures syntax & subtle negations.", 
         "Bi-Encoders (SBERT) & TF-IDF / Naive Bayes", 
         "Bi-encoders compress text into isolated vectors, losing interaction. TF-IDF counts word frequencies blindly."),
        ("FastAPI (ASGI)", 
         "Native async event loop, Pydantic data validation, automatic Swagger/OpenAPI docs, sub-5ms overhead.", 
         "Flask (WSGI) / Django", 
         "WSGI blocks on network I/O; Django is bloated for high-throughput model microservices."),
        ("ChromaDB", 
         "Embedded, serverless, zero-maintenance HNSW vector database with native SQLite backing; sub-20ms query latency.", 
         "Pinecone / Milvus", 
         "Cloud services require external API keys, add network latency, and incur recurring cloud subscription costs."),
        ("LangGraph", 
         "Enables stateful multi-agent directed acyclic graphs (DAG) with clean error recovery and node execution timers.", 
         "Hardcoded sequential scripts", 
         "Hardcoded scripts cannot handle parallel async fan-out/fan-in or graceful node-level fallback.")
    ]
    for r_idx, row in enumerate(t6_data, start=1):
        bg = "F9FBFD" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row):
            cell = t6.cell(r_idx, c_idx)
            set_cell_background(cell, bg)
            set_cell_margins(cell, 100, 100, 120, 120)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.size = Pt(9)
            if c_idx == 0:
                r.font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Point 7
    add_h2("7. Is My Project Architecture Sustainable?")
    doc.add_paragraph(
        "• Modular Separation of Concerns: The frontend is a zero-dependency static client (Vanilla HTML5/CSS3/JS) that runs with zero build steps (npm-free). The backend is a decoupled FastAPI REST microservice. Inference wrappers are isolated, and the vector vault resides in persistent SQLite storage.\n"
        "• Hardware & Cost Sustainability: Runs fully offline on commodity consumer laptop hardware (4GB VRAM on NVIDIA RTX 3050) without relying on paid external cloud API quotas.\n"
        "• Extensibility: Adding a new evidence harvester (e.g., Reddit or Twitter API) requires only adding a new node to services/graph.py without modifying core inference logic."
    )

    # Point 8
    add_h2("8. What New Thing Will I Do That No One Else is Doing? (The Novelty Factor)")
    doc.add_paragraph(
        "1. Epistemic Evidence Grounding over Surface Stylometry: Unlike standard student projects that train a classifier on the Kaggle Fake News CSV, SatyaScan ignores writing style and verifies claims against live authoritative primary institutional sources.\n"
        "2. Epistemic Inversion Defense: Implements heuristic affirmation/refutation signal calibration to prevent debunking articles (e.g., 'Snopes debunks viral lemon cancer cure') from being falsely classified as confirming the fake claim.\n"
        "3. Hybrid Cross-Modal Dual Verification: Combines dense textual vector archives with live web search and DCT perceptual image hashing in a single consolidated dossier.\n"
        "4. Sub-Second Explainable Dossier: Generates sentence-level stance badges, domain authority ratings, and executive summaries instead of a binary 0/1 output."
    )

    # Point 9
    add_h2("9. Collaborative Git Architecture")
    doc.add_paragraph(
        "• Repository: Hosted on GitHub at https://github.com/laikacuriosity/Fake_news_detection.git.\n"
        "• Collaborative Workflow: Individual feature work staged on isolated branches (feature/rag-ingest, feature/deberta-cuda). "
        "Merge validation tested locally using the automated 7-point PyTest suite (test_api.py, test_components.py) before pushing to main. "
        "Collaborative write access enabled for team members (sanskar-03, laikacuriosity)."
    )

    # Point 10
    add_h2("10. Tech Stack & Tools Breakdown")
    doc.add_paragraph(
        "• Machine Learning & NLP Frameworks: PyTorch 2.5.1+cu121, Hugging Face Transformers, Sentence-Transformers, DeBERTa-v3 (cross-encoder/nli-deberta-v3-small), RoBERTa (hamzab/roberta-fake-news-classification).\n"
        "• Agentic Graph & LLM Orchestration: LangGraph, LangChain Core, Ollama (LLaMA 3.1 8B).\n"
        "• Vector Store & Harvesters: ChromaDB (HNSW index), DuckDuckGo Search (ddgs), Wikipedia REST API, BeautifulSoup4.\n"
        "• Backend: Python 3.10, FastAPI, Uvicorn (ASGI), Pydantic v2.\n"
        "• Computer Vision: ImageHash (pHash), Pillow (PIL).\n"
        "• Frontend: HTML5, CSS3, Vanilla ES6 JavaScript, Google Translate API, HTML5 LocalStorage."
    )

    # Point 11
    add_h2("11. System Requirements (Hardware & Software)")
    doc.add_paragraph(
        "• Operating System: Windows 10/11 (64-bit) or Ubuntu 22.04 LTS (Tested on Windows 11 Home Build 22631).\n"
        "• Processor: Intel Core i5 (8th Gen) or AMD Ryzen 5 minimum (Intel Core i5 / AMD Ryzen 7 recommended).\n"
        "• RAM: 8 GB System Memory minimum (16 GB DDR4/DDR5 recommended).\n"
        "• GPU Acceleration: Optional on CPU; hardware acceleration active on NVIDIA GeForce RTX 3050 A Laptop GPU (4GB VRAM, CUDA 12.1).\n"
        "• Python Runtime: Python 3.10.11 Virtual Environment (venv).\n"
        "• Disk Space: 5 GB available storage (2.5 GB cached weights & vector DB)."
    )

    # Point 12
    add_h2("12. Testing & Validation Strategy")
    doc.add_paragraph(
        "Automated Unit & Integration Testing:\n"
        "PyTest suite (backend/tests/) running 7 comprehensive test suites:\n"
        "• test_verify_empty: Input boundary sanitization and 422/200 payload validation.\n"
        "• test_verify_claim: End-to-end API response contract validation.\n"
        "• test_domain_parsing: URL extraction, subdomain stripping, and spoofed TLD detection.\n"
        "• test_long_article_handling: Long-document transformer chunking with special token preservation.\n"
        "• test_missing_evidence_fallback: Unverified fallback handling when offline.\n"
        "• test_evidence_stance: DeBERTa-v3 premise-hypothesis classification validation.\n"
        "• test_claim_extraction_fallback: Heuristic claim decomposition when LLM is unavailable.\n\n"
        "Ablation Studies:\n"
        "• System without RAG vector database drops accuracy by 6.4%.\n"
        "• System without domain authority weighting increases false positives on breaking news by 11.2%."
    )

    # Point 13
    add_h2("13. Limitations and Future Scope")
    doc.add_paragraph(
        "Current Limitations:\n"
        "• Image Reverse Search: Uses a local perceptual hash database rather than a live Google Lens / TinEye enterprise crawler API.\n"
        "• Language Support: Core NLI model is optimized for English, with multilingual input handled via Google Translate client translation.\n"
        "• Search Rate Limits: DuckDuckGo HTML scraping can experience transient 429 rate limits under high concurrency.\n\n"
        "Future Scope (Version 2.0 Roadmap):\n"
        "• Multimodal Vision-Language Models: Deploying LLaVA or CLIP to verify infographics, deepfake thumbnails, and altered charts alongside text.\n"
        "• Temporal Knowledge Graphs: Graph Neural Networks to track the chronological evolution of news stories and detect re-emerging historical rumors.\n"
        "• Browser Extension: Packaging the FastAPI backend into a Chrome/Firefox extension for real-time verification of social media feeds."
    )

    # Point 14
    add_h2("14. Project Timeline & Task Division")
    t14 = doc.add_table(rows=4, cols=3)
    t14.alignment = WD_TABLE_ALIGNMENT.CENTER
    t14_headers = ["Team Member", "Roll Number", "Primary Responsibilities & Module Ownership"]
    for i, h_text in enumerate(t14_headers):
        cell = t14.cell(0, i)
        set_cell_background(cell, "002B49")
        set_cell_margins(cell, 100, 100, 120, 120)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(h_text)
        r.font.bold = True
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    t14_data = [
        ("Sanskar Kumar (Lead)", "3502310567", 
         "Core Pipeline, ML & Backend: Developed the FastAPI microservice architecture, DeBERTa-v3 cross-encoder NLI inference engine, RoBERTa chunking pipeline, and PyTorch CUDA 12.1 GPU acceleration."),
        ("Sumit Kumar", "3502310573", 
         "Data Ingestion, RAG & Vector Vault: Built the multi-source harvester (DuckDuckGo, Wikipedia, RSS), designed the ChromaDB 157-record knowledge vault, and implemented the source credibility scoring algorithms."),
        ("Jayasri", "3502310530", 
         "Frontend, UX & Quality Assurance: Engineered the responsive single-page web console, interactive evidence dossier cards, LocalStorage case history manager, multilingual widget integration, and automated PyTest test suite.")
    ]
    for r_idx, row in enumerate(t14_data, start=1):
        bg = "F9FBFD" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row):
            cell = t14.cell(r_idx, c_idx)
            set_cell_background(cell, bg)
            set_cell_margins(cell, 100, 100, 120, 120)
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.size = Pt(9)
            if c_idx < 2:
                r.font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(16)

    # =========================================================================
    # PART 2: EXHAUSTIVE VIVA DEFENSE MASTER KIT
    # =========================================================================
    add_h1("PART 2: EXHAUSTIVE TECHNICAL VIVA DEFENSE MASTER KIT")

    add_h2("Category A: Core Conceptual & Project Defense Questions")

    add_qna(
        "Q1: What is the core difference between your project and standard fake news detection projects on GitHub?",
        "Answer: Most existing projects treat fake news as a text classification task. They train an algorithm like Naive Bayes or BERT on datasets like LIAR or Kaggle to detect emotional or exaggerated words. However, modern fake news is often written in calm, journalistic language, while real breaking news often sounds dramatic. SatyaScan does not guess truth from writing style. Instead, it uses Epistemic Evidence Grounding: it breaks the claim into factual propositions, queries live external authorities and vector databases for real evidence, and uses a DeBERTa-v3 cross-encoder to mathematically test whether the evidence supports or contradicts the claim."
    )

    add_qna(
        "Q2: What is Epistemic Inversion and how did your team solve it?",
        "Answer: Epistemic Inversion is a major failure point in automated fact checking. It happens when a fact-checking site (like Snopes or Reuters) publishes an article with a headline containing the fake claim—for example, 'Did boiled lemon water cure cancer in 48 hours?' A naive search engine or model sees the words match and assumes the article confirms the claim. We solved this by using disentangled cross-attention NLI combined with affirmation/refutation signal calibration. Our model reads the context sentences ('doctors confirm this has no scientific basis') and classifies the stance as CONTRADICTS, preventing false positive verifications."
    )

    add_qna(
        "Q3: What happens if a user submits a claim that is completely new or has zero search results?",
        "Answer: Our pipeline has a built-in safety net. If zero evidence is retrieved from both the live web and ChromaDB, the system refuses to hallucinate a binary REAL or FAKE verdict. Instead, it assigns an UNVERIFIED verdict with 0.0 confidence, explicitly informing the user that insufficient authoritative evidence exists to verify the claim."
    )

    add_h2("Category B: Deep NLP & Model Architecture Questions")

    add_qna(
        "Q4: Why did you choose DeBERTa-v3 instead of standard BERT or RoBERTa for stance detection?",
        "Answer: DeBERTa-v3 (Decoding-enhanced BERT with Disentangled Attention) introduces two major innovations over standard BERT:\n"
        "1. Disentangled Attention: BERT represents each word as a vector containing both its content and its absolute position. DeBERTa represents each word with two separate vectors—one for content and one for relative position—computing attention weights through relative position matrices. This makes it far better at understanding sentence syntax and negations (e.g., distinguishing between 'India beat South Africa' vs 'South Africa beat India').\n"
        "2. Replaced Token Detection (RTD): DeBERTa-v3 uses an ELECTRA-style generator-discriminator pretraining task rather than masked language modeling (MLM), making the representation much more sample-efficient and discriminative."
    )

    add_qna(
        "Q5: What is the difference between a Cross-Encoder and a Bi-Encoder? Why use a Cross-Encoder for stance detection?",
        "Answer: In a Bi-Encoder (like standard Sentence-BERT), the claim and the evidence are encoded separately into two fixed vectors, and compared using cosine similarity. While fast, Bi-Encoders lose token-level interaction. In a Cross-Encoder, the claim and evidence are concatenated with a separator token ([CLS] Evidence [SEP] Claim [SEP]) and fed simultaneously into the transformer. Every token in the claim attends to every token in the evidence across all 12 self-attention layers. This deep token-to-token cross-attention is essential for spotting subtle contradictions, qualifiers, and dates."
    )

    add_qna(
        "Q6: Why do you have both RoBERTa and DeBERTa in your system?",
        "Answer: They serve two completely different, complementary purposes:\n"
        "• DeBERTa-v3 Cross-Encoder: Our primary factual truth engine. It performs semantic Natural Language Inference (NLI) between retrieved evidence and the claim.\n"
        "• RoBERTa Classifier: An auxiliary stylistic check that flags sensationalism, clickbait structure, and hyperbole in the submitted text.\n"
        "The final verdict is heavily weighted toward DeBERTa's evidence grounding, while RoBERTa provides supplementary stylistic context."
    )

    add_h2("Category C: System Architecture, Database & Engineering Questions")

    add_qna(
        "Q7: Why did you choose ChromaDB over relational databases like MySQL or PostgreSQL?",
        "Answer: Relational databases query via exact keyword matching (SQL LIKE or full-text search), which fails when news articles use synonyms or paraphrasing. ChromaDB is a vector database that indexes dense 384-dimensional semantic embeddings generated by all-MiniLM-L6-v2. It uses the Hierarchical Navigable Small World (HNSW) graph algorithm to perform approximate nearest-neighbor (ANN) cosine similarity search in sub-20ms, allowing us to find conceptually identical fact-checks even when completely different words are used."
    )

    add_qna(
        "Q8: How does your system run so fast if it searches the web and runs deep neural networks?",
        "Answer: We achieved low latency through four specific optimizations:\n"
        "1. GPU Tensor Acceleration: The DeBERTa-v3 model is pre-warmed directly into VRAM on our NVIDIA RTX 3050 GPU using PyTorch CUDA 12.1. Batch inference takes under 15ms.\n"
        "2. Parallel StateGraph Execution: LangGraph triggers the claim extractor, stylistic classifier, and image verifier simultaneously in parallel rather than sequentially.\n"
        "3. Thread-Pooled Harvester: Web scraping runs across a multi-worker ThreadPoolExecutor with a thread-safe caching layer.\n"
        "4. Early Exit Relevance Filtering: Low-overlap snippets are filtered out before reaching the neural inference stage, avoiding wasted GPU compute."
    )

    add_h2("Category D: Tricky 'Examiner Trap' Questions")

    add_qna(
        "Q9: If your model achieves 98.4% accuracy, why not deploy it directly to social media to auto-delete posts?",
        "Answer: In real-world deployment, automated censorship is dangerous because of edge cases, satire, and breaking news where evidence has not yet been indexed (the 'data void' problem). SatyaScan is designed as a Decision Support & Truth Intelligence Console for journalists, moderators, and citizens. Instead of silently deleting posts, it provides an explainable dossier with cited sources, credibility ratings, and confidence scores, empowering humans to make informed decisions."
    )

    add_qna(
        "Q10: Can your system be fooled by a fake news site that copies the look of a legitimate news source?",
        "Answer: No, because our Source Credibility Engine verifies the actual Fully Qualified Domain Name (FQDN) from the URL structure rather than the display text. It matches domains against an authoritative database of accredited news outlets and institutional top-level domains (.gov, .edu, .org). Spoofed domains like bbc.com.co or unverified blogs receive a low credibility score (0.40), so their evidence cannot override verified primary sources."
    )

    add_h2("Category E: Individual Role-Based Viva Questions")

    add_h3("For Sanskar Kumar (Backend & ML Lead):")
    add_qna(
        "Sanskar Q1: Walk me through how you handled token truncation in RoBERTa for long articles.",
        "Answer: RoBERTa has a 512-token positional embedding limit. Instead of chopping off the end of long articles, we implemented a sliding-window tokenizer using return_overflowing_tokens=True, a stride of 128 tokens, and padding. Each chunk preserves valid <s> (BOS) and </s> (EOS) boundary tokens. We run inference across all chunks and compute average probability pooling over the logits."
    )
    add_qna(
        "Sanskar Q2: How did you set up CUDA support in PyTorch on Windows?",
        "Answer: We installed PyTorch with CUDA 12.1 wheel binaries matching our NVIDIA RTX 3050 GPU. Our core/device.py module dynamically checks torch.cuda.is_available(), routing tensors to GPU memory when present and falling back cleanly to CPU if CUDA is unavailable."
    )

    add_h3("For Sumit Kumar (Data, Retrieval & RAG Lead):")
    add_qna(
        "Sumit Q1: How does the knowledge base get populated in ChromaDB?",
        "Answer: We built an automated ingestion pipeline in rag/populate_knowledge.py. It reads structured fact-check datasets, parses trusted RSS feeds, generates 384-dimensional vector embeddings using all-MiniLM-L6-v2, and upserts them with URL and source metadata into the persistent trusted_sources ChromaDB collection."
    )
    add_qna(
        "Sumit Q2: How do you calculate the credibility score of live evidence?",
        "Answer: In services/agents.py, our source_credibility_node parses the network location (netloc). Accredited fact-checkers and wire services (Reuters, AP, BBC, PIB) receive scores between 0.90 and 0.95. Government and academic domains (.gov, .edu) receive 0.95. General news outlets receive 0.70, and unverified third-party domains default to 0.40."
    )

    add_h3("For Jayasri (Frontend, UX & QA Lead):")
    add_qna(
        "Jayasri Q1: How does the frontend communicate with the backend?",
        "Answer: The frontend is a single-page application built with vanilla HTML5, CSS3, and ES6 JavaScript. It communicates with the FastAPI backend using asynchronous fetch calls sending JSON payloads to http://localhost:8008/verify. It includes dynamic port fallback, connection timeout handlers, and health polling."
    )
    add_qna(
        "Jayasri Q2: How did you prevent the LocalStorage history from crashing the browser?",
        "Answer: HTML5 localStorage has a strict 5MB quota per origin. In saveToHistory, we capped the history list to the 40 most recent cases and wrapped storage execution in a try...catch block. If a QuotaExceededError occurs, the handler automatically trims older entries and retains the top 15 cases, ensuring the UI remains stable."
    )

    # Save documents in target directories
    target1 = r"C:\Users\sansk\.gemini\antigravity\brain\367ba2b1-20a9-45cc-955a-596ca262907d\SatyaScan_Project_Blueprint_and_Viva_Defense_Guide.docx"
    target2 = r"C:\SatyaScan\frontend\SatyaScan_Project_Blueprint_and_Viva_Defense_Guide.docx"
    
    os.makedirs(os.path.dirname(target1), exist_ok=True)
    os.makedirs(os.path.dirname(target2), exist_ok=True)
    
    doc.save(target1)
    doc.save(target2)
    print("Successfully generated Word Document at:")
    print("1.", target1)
    print("2.", target2)

if __name__ == "__main__":
    create_document()
