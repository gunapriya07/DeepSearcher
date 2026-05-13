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

    state = run_agent("topics", chunks)

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

    state = run_agent("compare", chunks, style=req.aspect)

    return CompareResponse(
        comparison=state["result"],
        document_id_1=req.document_id_1,
        document_id_2=req.document_id_2,
    )