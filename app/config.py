import os 
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_DB_URI: str = os.environ["POSTGRES_DB_URI"] 
    OPENAI_API_KEY: str = os.environ["OPENAI_API_KEY"]
    RESUME_PARSER_API_KEY: str = os.environ["RESUME_PARSER_API_KEY"]

    LLM_MODEL: str = "gpt-4o"
    TEMPERATURE: float = 0.0
    MAX_TOKENS: int = 4096
    TIMEOUT: float = 300.0

settings  = Settings()