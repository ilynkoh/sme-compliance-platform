from sqlalchemy import Column, String, Integer, ForeignKey, Enum as SQLEnum, Float, Text
from sqlalchemy.orm import relationship
import enum

from app.models.base import Base, TimestampMixin

class UploadStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    PARSING = "parsing"
    PARSED = "parsed"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    FAILED = "failed"

class Upload(Base, TimestampMixin):
    __tablename__ = "uploads"
    
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Float, nullable=True)  # in MB
    status = Column(SQLEnum(UploadStatus), default=UploadStatus.UPLOADED)
    error_message = Column(Text, nullable=True)
    fiscal_year = Column(String(4), nullable=True)
    
    # Relationships
    company = relationship("Company", back_populates="uploads")
    entries = relationship("TrialBalanceEntry", back_populates="upload", cascade="all, delete-orphan")
    reports = relationship("ComplianceReport", back_populates="upload", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Upload(id={self.id}, company_id={self.company_id}, filename={self.filename}, status={self.status})>"