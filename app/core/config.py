import os
from dotenv import load_dotenv

# Load .env file for environment variables
load_dotenv()

from app.core.local import LocalSettings
from app.core.deployment import DeploymentSettings

# Read ENV variable, default to 'development' on your PC
ENV = os.getenv("ENVIRONMENT", "development").lower()

if ENV in ("production", "prod", "deploy", "deployment"):
    settings = DeploymentSettings()
else:
    settings = LocalSettings()
