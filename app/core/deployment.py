import os
from app.core.base_config import BaseConfig

class DeploymentSettings(BaseConfig):
    """Production / Cloud Deployment Configuration."""
    ENV: str = "production"
    DEBUG: bool = False
    
    # Production database URL (defaults to SQLite or Cloud DB if provided via ENV)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./portfolio.db")
    
    # Cloud hosts automatically supply PORT (e.g., Render, Koyeb, Railway)
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = int(os.getenv("PORT", "10000"))
    
    # Allowed hosts and security flags
    ALLOWED_HOSTS: list[str] = ["*"]
