from fastapi import APIRouter, HTTPException
from models.schemas import AskRequest, AskResponse
from services.vectordb import retrieve_chunks
from agents.langgraph_agents import run_agent

router = APIRouter(prefix="/ask", tags=["QA"])


@router.post("", response_model=AskResponse)
def ask_question(req: AskRequest):
    """
    PHASE 6-7: Retrieve relevant chunks → Generate answer via LLM.
    Hallucination prevention: LLM answers ONLY from retrieved context.
    """
    chunks = retrieve_chunks(req.document_id, req.question, top_k=5)
    if not chunks:
        raise HTTPException(status_code=404, detail="No relevant content found. Check document_id.")

    try:
        state = run_agent("qa", chunks, question=req.question)
    except Exception as exc:
        message = str(exc).lower()
        if "quota" in message or "rate" in message or "429" in message:
            raise HTTPException(
                status_code=503,
                detail="AI provider quota or rate limit was exceeded. Please try again later or use a Gemini project with available quota.",
            )
        raise HTTPException(status_code=500, detail=f"Question answering failed: {exc}")

    return AskResponse(
        answer=state["result"],
        citations=state["citations"] or [],
        document_id=req.document_id,
    )