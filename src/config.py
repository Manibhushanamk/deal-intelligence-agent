import os
from pydantic import BaseModel, Field

class Config(BaseModel):
    # Hindsight Memory SDK Configuration
    HINDSIGHT_API_KEY: str = Field(default_factory=lambda: os.getenv("HINDSIGHT_API_KEY", "mock_hindsight_api_key"))
    HINDSIGHT_BASE_URL: str = Field(default_factory=lambda: os.getenv("HINDSIGHT_BASE_URL", "https://api.hindsight.vectorize.io"))

    # Neon PostgreSQL Database Configuration
    NEON_DATABASE_URL: str = Field(
        default_factory=lambda: os.getenv("NEON_DATABASE_URL", "postgresql://user:pass@ep-mock-neon.pooler.us-east-2.aws.neon.tech/neondb")
    )

    # Google Workspace API Configuration
    GOOGLE_CLIENT_ID: str = Field(default_factory=lambda: os.getenv("GOOGLE_CLIENT_ID", "mock_google_client_id"))
    GOOGLE_CLIENT_SECRET: str = Field(default_factory=lambda: os.getenv("GOOGLE_CLIENT_SECRET", "mock_google_client_secret"))
    GOOGLE_REFRESH_TOKEN: str = Field(default_factory=lambda: os.getenv("GOOGLE_REFRESH_TOKEN", "mock_google_refresh_token"))

    # LLM / Groq API Configuration
    GROQ_API_KEY: str = Field(default_factory=lambda: os.getenv("GROQ_API_KEY", "mock_groq_api_key"))
    LLM_MODEL: str = Field(default_factory=lambda: os.getenv("LLM_MODEL", "qwen/qwen3-32b"))

config = Config()
