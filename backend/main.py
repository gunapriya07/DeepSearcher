from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.upload import router as upload_router
from routers.ask import router as ask_router
from routers.summary import router as summary_router
from routers.quiz import router as quiz_router
from routers.extras import topics_router, compare_router
from routers.health import router as health_router

app = FastAPI(
    title="DeepSearcher API",
    description="Production-grade Multi-Agent RAG system — AI Research Assistant for Students & Professionals",
    version="1.0.0",
)

# ── CORS (allow Streamlit / React frontend) ───────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(upload_router)
app.include_router(ask_router)
app.include_router(summary_router)
app.include_router(quiz_router)
app.include_router(topics_router)
app.include_router(compare_router)
app.include_router(health_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "DeepSearcher API is running ",
        "docs": "/docs",
        "endpoints": [
            "POST /upload",
            "POST /ask",
            "POST /summary",
            "POST /quiz",
            "GET  /topics/{document_id}",
            "POST /compare",
            "GET  /health",
        ],
    }