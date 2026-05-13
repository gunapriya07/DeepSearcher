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

    state = run_agent("qa", chunks, question=req.question)

    return AskResponse(
        answer=state["result"],
        citations=state["citations"] or [],
        document_id=req.document_id,
    )