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

    try:
        state = run_agent("summarize", chunks, style=req.style)
    except Exception as exc:
        message = str(exc).lower()
        if "quota" in message or "rate" in message or "429" in message:
            raise HTTPException(
                status_code=503,
                detail="AI provider quota or rate limit was exceeded. Please try again later or use a Gemini project with available quota.",
            )
        raise HTTPException(status_code=500, detail=f"Summarization failed: {exc}")

    return SummaryResponse(
        summary=state["result"],
        document_id=req.document_id,
    )