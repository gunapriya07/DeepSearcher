from fastapi import APIRouter
from models.schemas import HealthResponse
from services.vectordb import ping_pinecone
from langchain_google_genai import ChatGoogleGenerativeAI
from core.config import settings

router = APIRouter(prefix="/health", tags=["Health"])


def ping_gemini() -> str:
    try:
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=settings.google_api_key,
        )
        llm.invoke("ping")
        return "ok"
    except Exception as e:
        return f"error: {e}"


@router.get("", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="ok",
        pinecone=ping_pinecone(),
        gemini=ping_gemini(),
    )