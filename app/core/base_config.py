import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class BaseConfig(BaseSettings):
    """Common configurations shared across environments."""
    APP_NAME: str = "MYTHOS | Online Institute of Technology & Digital Sciences"
    APP_VERSION: str = "2.0.0"
    
    # Cryptographic secret for session cookie signing
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")

    # Platform Information & Contact
    BASE_URL: str = os.getenv("BASE_URL", "https://mythostech.in").rstrip("/")
    GOOGLE_SITE_VERIFICATION: str = os.getenv("GOOGLE_SITE_VERIFICATION", "")
    GSC_VERIFICATION_TOKEN: str = os.getenv("GSC_VERIFICATION_TOKEN", "")
    ANALYTICS_SCRIPT: str = os.getenv("ANALYTICS_SCRIPT", "")
    GA4_MEASUREMENT_ID: str = os.getenv("GA4_MEASUREMENT_ID", "")
    OWNER_NAME: str = "Mythos Academic Council"
    OWNER_TITLE: str = "Faculty of Digital Marketing & Data Analytics"
    OWNER_BIO: str = (
        "Premier full online educational institute providing structured, cohort-based live education "
        "across Digital Marketing (Performance Marketing, Paid Ads, SEO, Content Growth) and "
        "Data Analytics & Business Intelligence (Python, SQL, Power BI, Excel, Tableau)."
    )
    # Dynamic Business Contact Details (Loaded from env, no hardcoded personal details)
    BUSINESS_EMAIL: str = os.getenv("BUSINESS_EMAIL", "admissions@mythostech.in")
    BUSINESS_WHATSAPP: str = os.getenv("BUSINESS_WHATSAPP", "[BUSINESS_WHATSAPP]")
    EMAIL: str = os.getenv("BUSINESS_EMAIL", "admissions@mythostech.in")
    OWNER_PHONE: str = os.getenv("BUSINESS_WHATSAPP", "[BUSINESS_WHATSAPP]")
    OWNER_LOCATION: str = "Live Online Weekend Cohorts"
    
    # Social & Community Links
    GITHUB_URL: str = os.getenv("GITHUB_URL", "")
    LINKEDIN_URL: str = os.getenv("LINKEDIN_PAGE_URL", "")
    WHATSAPP_CHANNEL_URL: str = os.getenv("WHATSAPP_CHANNEL_URL", "[WHATSAPP_CHANNEL_URL]")
    TELEGRAM_URL: str = os.getenv("TELEGRAM_URL", "[TELEGRAM_URL]")
    INSTAGRAM_URL: str = os.getenv("INSTAGRAM_URL", "[INSTAGRAM_URL]")
    YOUTUBE_URL: str = os.getenv("YOUTUBE_URL", "[YOUTUBE_URL]")

    # Dual Mentors & Academic Specifications
    DM_MENTOR_NAME: str = os.getenv("DM_MENTOR_NAME", "[DM_MENTOR_NAME]")
    DM_MENTOR_PHOTO: str = os.getenv("DM_MENTOR_PHOTO", "[DM_MENTOR_PHOTO]")
    DM_MENTOR_BIO: str = os.getenv("DM_MENTOR_BIO", "[DM_MENTOR_BIO]")
    DM_MENTOR_LINKEDIN: str = os.getenv("DM_MENTOR_LINKEDIN", "[DM_MENTOR_LINKEDIN]")
    DM_SCHEDULE: str = os.getenv("DM_SCHEDULE", "[DM_SCHEDULE]")
    TRUST_CLAIM: str = os.getenv("TRUST_CLAIM", "400+ learners taught by our mentors over 3+ years")
    SUBJECT_ORDER: str = os.getenv("SUBJECT_ORDER", "SQL, Excel, Power BI, Python, Tableau, Git & GitHub")
    DEMO_CLASS_DATETIME: str = os.getenv("DEMO_CLASS_DATETIME", "[DEMO_CLASS_DATETIME]")

    RESUME_PATH: str = ""
    PROFILE_PHOTO_PATH: str = "/static/Images/mythos/mythos_icon_transparent.png"

    @property
    def subject_order_list(self) -> list:
        return [s.strip() for s in self.SUBJECT_ORDER.split(",") if s.strip()]

    @property
    def whatsapp_url(self) -> str:
        digits = "".join(filter(str.isdigit, self.BUSINESS_WHATSAPP))
        if digits:
            return f"https://wa.me/{digits}"
        return f"https://wa.me/{self.BUSINESS_WHATSAPP}" if self.BUSINESS_WHATSAPP else "#about"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

