from datetime import datetime
from sqlalchemy import Column, DateTime, func, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class TimestampMixin:
    """Mixin to add created_at and updated_at columns"""
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)