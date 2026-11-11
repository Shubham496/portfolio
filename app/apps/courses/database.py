import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger("courses.database")

# Resolve database URL
# Render provides DATABASE_URL in environment. If absent, fallback to local SQLite.
raw_db_url = os.getenv("DATABASE_URL", "")

if raw_db_url:
    # Render and Heroku use 'postgres://', which SQLAlchemy 1.4+ deprecated in favor of 'postgresql://'
    if raw_db_url.startswith("postgres://"):
        raw_db_url = raw_db_url.replace("postgres://", "postgresql://", 1)
    DATABASE_URL = raw_db_url
else:
    # Local fallback file-based SQLite database
    DATABASE_URL = "sqlite:///./course_platform.db"

is_sqlite = DATABASE_URL.startswith("sqlite")

# Engine creation with production-ready connection resilience
if is_sqlite:
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False
    )
else:
    # PostgreSQL settings optimized for Render / Cloud hosted DBs (Neon, Supabase, Render Postgres)
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,      # Tests connection liveness before checking out
        pool_recycle=300,        # Recycles stale connections every 5 minutes
        pool_size=5,
        max_overflow=10,
        echo=False
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI dependency that yields a database session and safely closes it."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
