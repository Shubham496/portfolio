import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class BaseConfig(BaseSettings):
    """Common configurations shared across environments."""
    APP_NAME: str = "MYTHOS | Online Institute of Technology & Digital Sciences"
    APP_VERSION: str = "2.0.0"
    
    # Cryptographic secret for session cookie signing
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")

    # Platform Information & Contact
    OWNER_NAME: str = "Mythos Academic Council"
    OWNER_TITLE: str = "Faculty of Digital Marketing & Data Analytics"
    OWNER_BIO: str = (
        "Premier full online educational institute providing structured, cohort-based live education "
        "across Digital Marketing (Performance Marketing, Paid Ads, SEO, Content Growth) and "
        "Data Analytics & Business Intelligence (Python, SQL, Power BI, Excel, Tableau)."
    )
    OWNER_PHONE: str = os.getenv("BUSINESS_WHATSAPP", "8727864157")
    OWNER_LOCATION: str = "Live Online Weekend Cohorts"
    GITHUB_URL: str = ""
    LINKEDIN_URL: str = ""
    EMAIL: str = os.getenv("BUSINESS_EMAIL", "shubhamsinghh057@gmail.com")
    RESUME_PATH: str = ""
    PROFILE_PHOTO_PATH: str = "/static/Images/mythos/mythos_icon_transparent.png"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

