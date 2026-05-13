import os
import aiofiles
from fastapi import APIRouter, UploadFile, File, HTTPException
from core.config import settings
from models.schemas import UploadResponse
from services.parser import extract_text, chunk_text, generate_document_id
from services.vectordb import embed_and_store

router = APIRouter(prefix="/upload", tags=["Upload"])

os.makedirs(settings.upload_dir, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx"}


@router.post("", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    PHASE 1-5: Upload → Parse → Chunk → Embed → Store in Pinecone.
    Returns a document_id used in all subsequent calls.
    """
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Only PDF, TXT, and DOCX files allowed. Got: {ext}")

    document_id = generate_document_id()
    file_path = os.path.join(settings.upload_dir, f"{document_id}{ext}")

    # Save file
    async with aiofiles.open(file_path, "wb") as f:
        content = await file.read()
        await f.write(content)

    # Parse → Chunk → Embed → Store
    try:
        text = extract_text(file_path)
        if not text.strip():
            raise HTTPException(status_code=422, detail="Could not extract text from file.")

        chunks = chunk_text(text)
        num_chunks = embed_and_store(document_id, chunks)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

    return UploadResponse(
        document_id=document_id,
        filename=file.filename,
        num_chunks=num_chunks,
        message="Document uploaded and indexed successfully.",
    )