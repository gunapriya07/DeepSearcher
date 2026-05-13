from pydantic import BaseModel
from typing import Optional, List


class AskRequest(BaseModel):
    document_id: str
    question: str


class AskResponse(BaseModel):
    answer: str
    citations: List[str]
    document_id: str


class SummaryRequest(BaseModel):
    document_id: str
    style: Optional[str] = "concise"   # concise | detailed | bullet


class SummaryResponse(BaseModel):
    summary: str
    document_id: str


class QuizRequest(BaseModel):
    document_id: str
    num_questions: int = 5
    approved: Optional[bool] = None    # Human-in-the-loop gate


class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    answer: str


class QuizResponse(BaseModel):
    questions: List[QuizQuestion]
    document_id: str
    awaiting_approval: bool = False


class TopicsResponse(BaseModel):
    topics: List[str]
    document_id: str


class CompareRequest(BaseModel):
    document_id_1: str
    document_id_2: str
    aspect: Optional[str] = "general"


class CompareResponse(BaseModel):
    comparison: str
    document_id_1: str
    document_id_2: str


class UploadResponse(BaseModel):
    document_id: str
    filename: str
    num_chunks: int
    message: str


class HealthResponse(BaseModel):
    status: str
    pinecone: str
    gemini: str