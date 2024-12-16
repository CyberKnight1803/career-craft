import os 
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_DB_URI: str = os.environ["POSTGRES_DB_URI"] 
    OPENAI_API_KEY: str = os.environ["OPENAI_API_KEY"]
    RESUME_PARSER_API_KEY: str = os.environ["RESUME_PARSER_API_KEY"]

    LLM_MODEL: str = "gpt-4o"
    TEMPERATURE: float = 0.0
    MAX_TOKENS: int = 4096
    TIMEOUT: float = 300.0

    GCP_SECRET_VERSION: str = os.environ["SECRET_VERSION"]
    GCP_SCOPES: List[str] = [
        "https://www.googleapis.com/auth/documents",
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/gmail.send"
    ]

settings  = Settings()