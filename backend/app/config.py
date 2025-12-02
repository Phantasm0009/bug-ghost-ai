import json
from pydantic import field_validator
"""Application configuration."""
from pydantic_settings import BaseSettings
from typing import List, Union, Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/bug_ghost_ai"
    
    # LLM
    LLM_PROVIDER: str = "openai"  # openai or anthropic
    LLM_API_KEY: str
    LLM_MODEL: str = "gpt-4-turbo-preview"
    
    # OAuth - GitHub
    GITHUB_CLIENT_ID: str = "Ov23li1EIr7THAoPMIZk"
    GITHUB_CLIENT_SECRET: str = "80ad95e8234de5dd269444b5b4f1891c39b23f34"
    GITHUB_REDIRECT_URI: str = "http://localhost:8000/api/auth/github/callback"
    
    # Auth/JWT (future use)
    JWT_SECRET: str = "07b28276182c084de6b3d810b4cef400"
    JWT_ALGORITHM: str = "HS256"
    
    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    CORS_ORIGINS: Union[List[str], str] = "*"

    # Accept flexible env formats for CORS_ORIGINS
    # Examples supported:
    # - CORS_ORIGINS="*"
    # - CORS_ORIGINS="http://localhost:3000"
    # - CORS_ORIGINS="http://localhost:3000,https://example.com"
    # - CORS_ORIGINS='["http://localhost:3000", "https://example.com"]'
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if v is None:
            return ["*"]
        if isinstance(v, list):
            return v
        if isinstance(v, str):
            s = v.strip()
            if s in ("", "*"):
                return ["*"]
            # Try JSON array
            try:
                loaded = json.loads(s)
                if isinstance(loaded, list):
                    return loaded
            except Exception:
                pass
            # Comma-separated string fallback
            parts = [p.strip() for p in s.split(",") if p.strip()]
            return parts if parts else ["*"]
        return ["*"]
    
    # Optional: Rate limiting
    MAX_REQUESTS_PER_MINUTE: int = 10
    
    # Sandbox (Docker-in-Docker)
    DOCKER_HOST: Optional[str] = None  # e.g., tcp://dind:2375
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
