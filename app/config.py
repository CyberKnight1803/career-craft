import os 
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_DB_URI = os.environ["POSTGRES_DB_URI"] 
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]


settings  = Settings()