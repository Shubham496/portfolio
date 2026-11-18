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

    def __init__(self, **values):
        super().__init__(**values)
        insecure_keys = (
            "",
            "shubham-data-analysis-secret-key-2026",
            "your_random_secret_key_here",
            "changeme",
            "secret",
            "default",
        )
        if not self.SECRET_KEY or self.SECRET_KEY.strip() in insecure_keys:
            raise RuntimeError(
                "CRITICAL SECURITY CONFIGURATION ERROR: SECRET_KEY environment variable is required in production and must not be empty or a default placeholder. "
                "Generate a cryptographically secure 256-bit key using: "
                'python -c "import secrets; print(secrets.token_hex(32))"'
            )

