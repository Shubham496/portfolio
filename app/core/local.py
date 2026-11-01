from app.core.base_config import BaseConfig

class LocalSettings(BaseConfig):
    """Local Development Configuration."""
    ENV: str = "development"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./portfolio.db"
    SERVER_HOST: str = "127.0.0.1"
    SERVER_PORT: int = 8000
