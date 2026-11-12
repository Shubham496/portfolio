from pydantic_settings import BaseSettings

class BaseConfig(BaseSettings):
    """Common configurations shared across environments."""
    APP_NAME: str = "MYTHOS | Data Systems & Analytics Engine"
    APP_VERSION: str = "1.0.0"
    
    # Platform Information & Contact
    OWNER_NAME: str = "Mythos Lead Mentor"
    OWNER_TITLE: str = "Data Architecture & Analytics Mentorship"
    OWNER_BIO: str = (
        "Rigorous hands-on mentorship designed for practical execution across Python, SQL, Power BI, "
        "Excel modeling, and Tableau. Building production data systems with live weekend cohort execution."
    )
    OWNER_PHONE: str = "8727864157"
    OWNER_LOCATION: str = "Live Online Weekend Cohort"
    GITHUB_URL: str = ""
    LINKEDIN_URL: str = ""
    EMAIL: str = "shubhamsinghh057@gmail.com"
    RESUME_PATH: str = ""
    PROFILE_PHOTO_PATH: str = "/static/Images/mythos/mythos_icon_transparent.png"

    class Config:
        env_file = ".env"
        extra = "ignore"
