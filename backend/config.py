from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # App Settings
    app_name: str = "Agentic AI Slack Bot"
    app_env: str = "development"
    secret_key: str = "development-secret-key-change-in-production"
    database_url: str = "sqlite:///./slack_ai_bot.db"
    
    # CORS
    allowed_origins: str = "http://localhost:3000,http://localhost:5173"
    
    # JWT Configuration
    jwt_secret_key: str = "jwt-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Slack (Optional - configured via portal)
    slack_bot_token: Optional[str] = None
    slack_app_token: Optional[str] = None
    slack_signing_secret: Optional[str] = None
    
    # Azure OpenAI (Optional - configured via portal)
    azure_openai_endpoint: Optional[str] = None
    azure_openai_api_key: Optional[str] = None
    azure_openai_deployment: Optional[str] = None
    azure_openai_api_version: str = "2023-05-15"
    
    # Google OAuth (Optional - configured via portal)
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    google_redirect_uri: str = "http://localhost:8000/api/oauth/google/callback"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
