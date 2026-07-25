import logging
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, Session

from app.config import settings
from app.models.base import Base

logger = logging.getLogger(__name__)

# Sync engine and session factory
engine = create_engine(
    settings.DATABASE_URL.replace('postgresql://', 'postgresql+psycopg2://'),
    echo=settings.SQLALCHEMY_ECHO,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=40,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session
)

async def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def init_db():
    """Initialize database and create tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

def get_db_session() -> Session:
    """Get a new database session (sync)"""
    return SessionLocal()