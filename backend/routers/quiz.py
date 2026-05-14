from fastapi import APIRouter, HTTPException
from models.schemas import QuizRequest, QuizResponse, QuizQuestion
from services.vectordb import retrieve_chunks
from agents.langgraph_agents import run_agent

router = APIRouter(prefix="/quiz", tags=["Quiz"])

# In-memory pending store (swap for Redis/DB in production)
_pending_quiz: dict[str, dict] = {}


@router.post("", response_model=QuizResponse)
def generate_quiz(req: QuizRequest):
    """
    HUMAN-IN-THE-LOOP (Golden Feature):
    - First call (approved=None)  → returns awaiting_approval=True, no quiz yet
    - Second call (approved=True) → returns the actual quiz
    - Second call (approved=False)→ cancels the request
    """
    # ── Step 1: Gate ──────────────────────────────────────────────
    if req.approved is None:
        # Store intent and ask for human confirmation
        _pending_quiz[req.document_id] = {
            "num_questions": req.num_questions,
        }
        return QuizResponse(
            questions=[],
            document_id=req.document_id,
            awaiting_approval=True,
        )

    # ── Step 2: Human rejected ────────────────────────────────────
    if req.approved is False:
        _pending_quiz.pop(req.document_id, None)
        raise HTTPException(status_code=200, detail="Quiz generation cancelled by user.")

    # ── Step 3: Human approved → generate ─────────────────────────
    pending = _pending_quiz.pop(req.document_id, None)
    num_q = pending["num_questions"] if pending else req.num_questions

    chunks = retrieve_chunks(req.document_id, "key concepts important facts", top_k=10)
    if not chunks:
        raise HTTPException(status_code=404, detail="Document not found.")

    try:
        state = run_agent("quiz", chunks, num_questions=num_q)
    except Exception as exc:
        message = str(exc).lower()
        if "quota" in message or "rate" in message or "429" in message:
            raise HTTPException(
                status_code=503,
                detail="AI provider quota or rate limit was exceeded. Please try again later or use a Gemini project with available quota.",
            )
        raise HTTPException(status_code=500, detail=f"Quiz generation failed: {exc}")

    raw_questions = state.get("quiz_questions") or []

    questions = [
        QuizQuestion(
            question=q.get("question", ""),
            options=q.get("options", []),
            answer=q.get("answer", ""),
        )
        for q in raw_questions
    ]

    return QuizResponse(
        questions=questions,
        document_id=req.document_id,
        awaiting_approval=False,
    )