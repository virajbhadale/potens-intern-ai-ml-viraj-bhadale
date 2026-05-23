# Potens AI/ML Internship Take-Home — Multilingual RAG System

## Overview

This project is a document-grounded multilingual Retrieval-Augmented Generation (RAG) system built for the Potens AI/ML Internship take-home assignment.

The system supports:
- semantic retrieval over multiple research papers
- grounded answer generation with citations
- multilingual question answering
- contradiction analysis between documents
- hallucination prevention through retrieval validation

The project uses:
- FastAPI for backend APIs
- Streamlit for frontend UI
- ChromaDB as vector database
- HuggingFace embeddings
- Groq LLM inference

---

# Features

## 1. Document Question Answering

Users can ask questions about the ingested research papers.

The system:
- retrieves relevant chunks
- generates grounded answers
- returns citations with:
  - source file
  - page number
  - chunk ID
  - snippet

---

## 2. Multilingual Support

Queries in other languages are automatically:
1. detected
2. translated to English
3. processed through RAG
4. translated back to the original language

Example:
- Hindi
- French
- Spanish

---

## 3. Contradiction Analysis

The `/contradict` endpoint compares two documents on a topic and determines:
- whether they conflict
- what they agree on
- concise reasoning

The system uses document-scoped retrieval to avoid unsupported cross-document reasoning.

---

## 4. Hallucination Prevention

The system explicitly refuses unsupported questions when retrieval confidence is low.

This prevents silent hallucinations.

Example refusal:
> "The provided documents do not contain enough information to answer this confidently."

---

# Architecture

```text
Streamlit UI
↓
FastAPI Backend
↓
RAG Pipeline
↓
ChromaDB Vector Store
↓
Groq LLM
```

---

# Documents Used

The system was tested on research papers related to:
- LLM hallucinations
- retrieval-augmented generation
- speculative RAG
- chain-of-agents systems
- context-aware generation

Documents:
- llm_hallucination.pdf
- sufficient_context.pdf
- speculative_rag.pdf
- chain_of_agents.pdf
- preference_gap.pdf
- ad_auctions_rag.pdf

---

# Chunking Strategy

The system uses RecursiveCharacterTextSplitter.

Configuration:
- chunk size: 1000
- chunk overlap: 200

Reasoning:
- large enough to preserve semantic meaning
- overlap preserves contextual continuity across chunk boundaries
- improves retrieval grounding quality

Each chunk stores metadata:
- source document
- page number
- chunk ID

---

# Embedding Model

Model:
`sentence-transformers/all-MiniLM-L6-v2`

Reasoning:
- lightweight
- fast inference
- good semantic retrieval quality
- suitable for 24-hour prototype constraints

---

# Retrieval Strategy

The system uses:
- semantic vector retrieval
- metadata-aware filtering
- distance-threshold filtering

Document-scoped retrieval is used for contradiction analysis to ensure comparisons are grounded only in requested documents.

Weak retrievals are rejected to reduce hallucination risk.

---

# API Endpoints

## POST `/ask`

Question answering endpoint.

### Example Request

```json
{
  "query": "What causes hallucinations in LLMs?"
}
```

---

## POST `/contradict`

Document comparison endpoint.

### Example Request

```json
{
  "doc1": "llm_hallucination.pdf",
  "doc2": "sufficient_context.pdf",
  "topic": "hallucination mitigation"
}
```

---

# How to Run

## 1. Clone Repository

```bash
git clone <repo_url>
cd potens-intern-ai-ml-viraj
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

---

## 3. Activate Environment

### Windows

```bash
.\venv\Scripts\activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Add Environment Variables

Create `.env`

```env
GROQ_API_KEY=your_api_key
```

---

## 6. Run Ingestion

```bash
python test_embeddings.py
```

This:
- loads documents
- chunks them
- creates embeddings
- stores vectors in ChromaDB

---

## 7. Start FastAPI Backend

```bash
uvicorn app.main:app --reload
```

---

## 8. Start Streamlit UI

Open new terminal:

```bash
streamlit run ui/streamlit_app.py
```

---

# Example Queries

## English

```text
What are hallucinations in large language models?
```

---

## Hindi

```text
एलएलएम में hallucination क्या है?
```

---

## Unsupported Query

```text
Who won FIFA World Cup 2018?
```

Expected:
system refusal due to insufficient document grounding.

---

# What Works

- document ingestion
- chunking
- semantic retrieval
- multilingual question answering
- contradiction analysis
- hallucination prevention
- FastAPI backend
- Streamlit UI

---

# Limitations

- contradiction analysis depends on retrieval quality
- translation pipeline may slightly alter nuanced meaning
- no reranker currently implemented
- no evaluation benchmark dataset included

---

# Future Improvements

- reranking layer
- confidence scoring
- human-in-the-loop approval
- streaming responses
- hybrid BM25 + vector retrieval
- evaluation benchmark suite

---

# AI Use Log

## Tools Used

### ChatGPT
- Used for:
  - architecture planning
  - debugging
  - code generation assistance
  - retrieval strategy refinement
  - README drafting

Approximate usage:
- ~250-400 prompts

---

### GitHub Copilot
- Used for:
  - autocomplete
  - boilerplate generation

Approximate usage:
- moderate

---

# Submission Notes

This project was intentionally scoped for a focused 24-hour implementation prioritizing:
- grounded retrieval
- explainability
- robustness
- end-to-end functionality
- hallucination prevention
