# DeepSearcher

## Intelligent Document Intelligence & Multi-Agent AI Research Assistant

**DeepSearcher** is a production-grade, multi-agent RAG (Retrieval-Augmented Generation) system that transforms how students, professionals, and researchers analyze, understand, and extract insights from documents. Powered by advanced AI agents orchestrated through LangGraph, it combines intelligent document parsing, semantic vector search, and multi-step reasoning to deliver comprehensive research insights.

---

## [•] Key Features

### [AI] Multi-Agent Intelligence

- **Summarizer Agent**: Generates concise, actionable summaries
- **Q&A Agent**: RAG-powered question answering with source citations
- **Quiz Agent**: Intelligent MCQ generation for knowledge assessment
- **Explainer Agent**: Breaks down complex concepts into understandable parts
- **Research Agent**: Identifies cross-document connections and patterns
- **Citation Agent**: Tracks and validates source references

### [DOC] Document Processing

- **Multi-Format Support**: PDF, Word (.docx), and text files
- **Intelligent Parsing**: Extracts structured content preserving context
- **Vector Indexing**: Semantic embedding via Sentence-Transformers
- **Scalable Storage**: Pinecone vector database for enterprise-grade retrieval

### [UI] User Experience

- **Modern Web UI**: Streamlit-powered intuitive interface
- **Real-time Processing**: Async request handling with streaming responses
- **RESTful API**: Production-ready FastAPI backend
- **Dark Theme**: Professional, eye-friendly design

---

## [ARCH] Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Streamlit)                      │
│            User Interface & Document Upload                  │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/REST
┌────────────────────▼────────────────────────────────────────┐
│                   BACKEND (FastAPI)                          │
│  ├─ /upload    - Document ingestion                         │
│  ├─ /ask       - Query processing                           │
│  ├─ /summary   - Document summarization                     │
│  ├─ /quiz      - Question generation                        │
│  ├─ /topics    - Topic extraction                           │
│  └─ /compare   - Cross-document analysis                    │
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
┌───────▼──┐  ┌─────▼───┐  ┌────▼────────┐
│  Parser  │  │ LangGraph│  │   Vector DB  │
│(PDF/Docx)│  │  Agents  │  │  (Pinecone)  │
└──────────┘  └─────┬────┘  └──────────────┘
                    │
            ┌───────▼────────┐
            │ Google Gemini  │
            │  (LLM Engine)  │
            └────────────────┘
```

---

## [TOOLS] Tech Stack

| Layer                   | Technologies                               |
| ----------------------- | ------------------------------------------ |
| **Frontend**            | Streamlit, Requests                        |
| **Backend**             | FastAPI, Uvicorn                           |
| **AI/ML**               | LangChain, LangGraph, Google Generative AI |
| **Embeddings & Search** | Sentence-Transformers, Pinecone            |
| **Document Processing** | PyPDF, PyMuPDF, python-docx                |
| **Data Validation**     | Pydantic                                   |
| **Infrastructure**      | Docker, Python                             |

---

## [LAUNCH] Quick Start

### Prerequisites

- Python 3.10+
- Google API Key (for Gemini LLM)
- Pinecone API Key

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/DeepSearcher.git
   cd DeepSearcher
   ```

2. **Set up environment variables** (`.env`)

   ```
   GOOGLE_API_KEY=your_google_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   LLM_MODEL=gemini-2.0-flash
   ```

3. **Install backend dependencies**

   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Run backend server**

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **In a new terminal, run frontend**
   ```bash
   cd frontend
   pip install -r requirements.txt
   streamlit run streamlit_app.py
   ```

### Docker Deployment

```bash
docker build -t deepsearcher .
docker run -p 8000:8000 -p 8501:8501 deepsearcher
```

---

## [API] API Endpoints

| Method | Endpoint                | Purpose                          |
| ------ | ----------------------- | -------------------------------- |
| `POST` | `/upload`               | Upload and parse documents       |
| `POST` | `/ask`                  | Query document with AI reasoning |
| `POST` | `/summary`              | Generate document summary        |
| `POST` | `/quiz`                 | Generate assessment questions    |
| `GET`  | `/topics/{document_id}` | Extract key topics               |
| `POST` | `/compare`              | Cross-document analysis          |
| `GET`  | `/health`               | System health check              |

---

## [DIR] Project Structure

```
DeepSearcher/
├── frontend/
│   ├── streamlit_app.py       # Main UI application
│   └── requirements.txt
├── backend/
│   ├── main.py                # FastAPI server
│   ├── requirements.txt
│   ├── agents/
│   │   └── langgraph_agents.py  # Multi-agent orchestration
│   ├── routers/               # API route handlers
│   │   ├── upload.py
│   │   ├── ask.py
│   │   ├── summary.py
│   │   ├── quiz.py
│   │   ├── extras.py
│   │   └── health.py
│   ├── services/              # Business logic
│   │   ├── parser.py          # Document parsing
│   │   └── vectordb.py        # Vector operations
│   ├── models/
│   │   └── schemas.py         # Pydantic schemas
│   ├── tools/                 # Utility functions
│   ├── core/
│   │   └── config.py          # Configuration
│   └── uploads/               # Temporary storage
└── Dockerfile
```

---

## [GOALS] Use Cases

- **Academic Research**: Intelligent summarization and quiz generation for study materials
- **Legal Document Analysis**: Extract key clauses, cross-reference documents
- **Business Intelligence**: Analyze reports, identify trends, compare datasets
- **Knowledge Management**: Auto-index and retrieve insights from knowledge bases
- **Medical Records**: Secure document analysis and pattern extraction

---

## [SEC] Security Considerations

- API keys stored in environment variables (`.env`)
- CORS configured (tighten in production)
- Input validation via Pydantic
- Rate limiting recommended for production
- Document encryption recommended for sensitive data

---

## [PERF] Performance

- **Vector Search**: Sub-100ms latency (Pinecone)
- **Document Parsing**: Handles 50MB+ PDFs
- **Query Response**: 2-5 seconds (depends on document size & model)
- **Concurrent Users**: Async support via FastAPI

---




