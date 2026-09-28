import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    HINDSIGHT_API_KEY: str = ""
    HINDSIGHT_BASE_URL: str = "https://api.hindsight.vectorize.io"
    HINDSIGHT_BANK_ID: str = "product-engineering-memory"
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    DATABASE_URL: str = "sqlite:///./decision_memory.db"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
