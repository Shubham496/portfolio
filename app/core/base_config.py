from pydantic_settings import BaseSettings

class BaseConfig(BaseSettings):
    """Common configurations shared across environments."""
    APP_NAME: str = "Shubham Singh | Portfolio & App Hub"
    APP_VERSION: str = "1.0.0"
    
    # Portfolio Personal Information
    OWNER_NAME: str = "Shubham Singh"
    OWNER_TITLE: str = "Data Engineer & Python Consultant | Analytics & Automation"
    OWNER_BIO: str = (
        "Data Analyst and Python Consultant with 3+ years of experience transforming complex datasets into "
        "high-impact business intelligence, automated ETL pipelines, and scalable backend applications. "
        "Proven expertise in Python, SQL, Power BI, workflow orchestration, and building production-ready data systems."
    )
    OWNER_PHONE: str = "+91 9520132466"
    OWNER_LOCATION: str = "India (Open to Global & Remote Roles)"
    GITHUB_URL: str = "https://github.com/Shubham496"
    LINKEDIN_URL: str = "https://linkedin.com/in/shubham469"
    EMAIL: str = "shubhamsingh41100@gmail.com"
    RESUME_PATH: str = "/static/pdf/resume.pdf"
    PROFILE_PHOTO_PATH: str = "/static/Images/Profile/profilePhoto.jpeg"

    class Config:
        env_file = ".env"
        extra = "ignore"
