from fastapi import APIRouter, HTTPException
from models.schemas import SummaryRequest, SummaryResponse
from services.vectordb import retrieve_chunks
from agents.langgraph_agents import run_agent

router = APIRouter(prefix="/summary", tags=["Summary"])


@router.post("", response_model=SummaryResponse)
def summarize_document(req: SummaryRequest):
    """
    Summarizer Agent: generates concise / detailed / bullet-point summary.
    """
    # Retrieve a broad sample of the document (high top_k)
    chunks = retrieve_chunks(req.document_id, "main topics summary overview", top_k=10)
    if not chunks:
        raise HTTPException(status_code=404, detail="Document not found.")

    state = run_agent("summarize", chunks, style=req.style)

    return SummaryResponse(
        summary=state["result"],
        document_id=req.document_id,
    )