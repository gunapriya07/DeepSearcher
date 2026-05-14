from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    pinecone_api_key: str
    pinecone_index_name: str = "deepsearcher"
    google_api_key: str
    # LLM model name to use for Google Generative AI (override in .n
    llm_model: str = "gemini-2.0-flash"
    upload_dir: str = "uploads"
    chunk_size: int = 1000
    chunk_overlap: int = 200

    class Config:
        env_file = ".env"


settings = Settings()