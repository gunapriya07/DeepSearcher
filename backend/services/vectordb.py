from pinecone import Pinecone, ServerlessSpec
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from core.config import settings
from typing import List

# ---------- Initialise clients ----------

pc = Pinecone(api_key=settings.pinecone_api_key)

embeddings_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-2",
    google_api_key=settings.google_api_key,
)


def _get_or_create_index():
    """Return the Pinecone index, creating it if it doesn't exist."""
    existing = [i.name for i in pc.list_indexes()]
    if settings.pinecone_index_name not in existing:
        pc.create_index(
            name=settings.pinecone_index_name,
            dimension=768,             # Gemini embedding-001 dimension
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
    return pc.Index(settings.pinecone_index_name)


index = _get_or_create_index()


# ---------- Public helpers ----------

def embed_and_store(document_id: str, chunks: List[str]) -> int:
    """Embed all chunks and upsert into Pinecone with document_id namespace."""
    vectors = []
    for i, chunk in enumerate(chunks):
        embedding = embeddings_model.embed_query(chunk, output_dimensionality=768)
        vectors.append({
            "id": f"{document_id}_{i}",
            "values": embedding,
            "metadata": {
                "document_id": document_id,
                "chunk_index": i,
                "text": chunk,
            },
        })

    # Upsert in batches of 100
    batch_size = 100
    for start in range(0, len(vectors), batch_size):
        index.upsert(vectors=vectors[start: start + batch_size])

    return len(vectors)


def retrieve_chunks(document_id: str, query: str, top_k: int = 5) -> List[str]:
    """Embed the query and fetch top_k relevant chunks for a given document."""
    query_embedding = embeddings_model.embed_query(query, output_dimensionality=768)
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        filter={"document_id": {"$eq": document_id}},
        include_metadata=True,
    )
    return [match["metadata"]["text"] for match in results["matches"]]


def retrieve_chunks_multi(document_ids: List[str], query: str, top_k: int = 5) -> List[str]:
    """Retrieve chunks across multiple documents (for comparison / research agent)."""
    query_embedding = embeddings_model.embed_query(query, output_dimensionality=768)
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        filter={"document_id": {"$in": document_ids}},
        include_metadata=True,
    )
    return [match["metadata"]["text"] for match in results["matches"]]


def delete_document(document_id: str):
    """Remove all vectors belonging to a document."""
    index.delete(filter={"document_id": {"$eq": document_id}})


def ping_pinecone() -> str:
    try:
        index.describe_index_stats()
        return "ok"
    except Exception as e:
        return f"error: {e}"