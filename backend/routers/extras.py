import json
from fastapi import APIRouter, HTTPException
from models.schemas import TopicsResponse, CompareRequest, CompareResponse
from services.vectordb import retrieve_chunks, retrieve_chunks_multi
from agents.langgraph_agents import run_agent

# ── Topics ────────────────────────────────────────────────────────────────────

topics_router = APIRouter(prefix="/topics", tags=["Topics"])


@topics_router.get("/{document_id}", response_model=TopicsResponse)
def extract_topics(document_id: str):
    """Extract key topics / concepts from the document."""
    chunks = retrieve_chunks(document_id, "topics concepts subjects themes", top_k=10)
    if not chunks:
        raise HTTPException(status_code=404, detail="Document not found.")

    try:
        state = run_agent("topics", chunks)
    except Exception as exc:
        message = str(exc).lower()
        if "quota" in message or "rate" in message or "429" in message:
            raise HTTPException(
                status_code=503,
                detail="AI provider quota or rate limit was exceeded. Please try again later or use a Gemini project with available quota.",
            )
        raise HTTPException(status_code=500, detail=f"Topics extraction failed: {exc}")

    try:
        topics = json.loads(state["result"])
    except Exception:
        topics = [state["result"]]

    return TopicsResponse(topics=topics, document_id=document_id)


# ── Compare ───────────────────────────────────────────────────────────────────

compare_router = APIRouter(prefix="/compare", tags=["Compare"])


@compare_router.post("", response_model=CompareResponse)
def compare_documents(req: CompareRequest):
    """
    Research Agent: Compare two documents semantically.
    Retrieves relevant chunks from both and finds connections/differences.
    """
    query = f"main content themes overview {req.aspect}"
    chunks = retrieve_chunks_multi(
        [req.document_id_1, req.document_id_2], query, top_k=8
    )
    if not chunks:
        raise HTTPException(status_code=404, detail="One or both documents not found.")

    try:
        state = run_agent("compare", chunks, style=req.aspect)
    except Exception as exc:
        message = str(exc).lower()
        if "quota" in message or "rate" in message or "429" in message:
            raise HTTPException(
                status_code=503,
                detail="AI provider quota or rate limit was exceeded. Please try again later or use a Gemini project with available quota.",
            )
        raise HTTPException(status_code=500, detail=f"Comparison failed: {exc}")

    return CompareResponse(
        comparison=state["result"],
        document_id_1=req.document_id_1,
        document_id_2=req.document_id_2,
    )