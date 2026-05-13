import os
import uuid
import fitz                          # PyMuPDF
from pypdf import PdfReader
from docx import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from core.config import settings


def parse_pdf_pymupdf(file_path: str) -> str:
    """Extract text using PyMuPDF (handles complex PDFs better)."""
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text


def parse_pdf_pypdf(file_path: str) -> str:
    """Extract text using pypdf (lightweight fallback)."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text


def parse_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def parse_docx(file_path: str) -> str:
    """Extract text from DOCX (Word) files."""
    doc = Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text


def extract_text(file_path: str) -> str:
    """Auto-detect file type and extract text."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".docx":
        return parse_docx(file_path)
    elif ext == ".pdf":
        try:
            text = parse_pdf_pymupdf(file_path)
            if len(text.strip()) < 100:           # fallback if PyMuPDF gets nothing
                text = parse_pdf_pypdf(file_path)
            return text
        except Exception:
            return parse_pdf_pypdf(file_path)
    elif ext == ".txt":
        return parse_txt(file_path)
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def chunk_text(text: str) -> list[str]:
    """
    Recursive character text splitter — balances fixed & semantic chunking.
    Returns list of chunk strings.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    return splitter.split_text(text)


def generate_document_id() -> str:
    return str(uuid.uuid4())