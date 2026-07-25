from sqlalchemy import Column, String, Integer, ForeignKey, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from app.models.base import Base, TimestampMixin

class CompanySize(str, enum.Enum):
    MICRO = "micro"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"

class Company(Base, TimestampMixin):
    __tablename__ = "companies"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    registration_number = Column(String(50), unique=True, nullable=False, index=True)
    industry = Column(String(100), nullable=True)
    size = Column(SQLEnum(CompanySize), default=CompanySize.SMALL)
    description = Column(Text, nullable=True)
    address = Column(String(500), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    postal_code = Column(String(10), nullable=True)
    
    # Relationships
    owner = relationship("User", back_populates="companies")
    uploads = relationship("Upload", back_populates="company", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Company(id={self.id}, name={self.name}, reg_no={self.registration_number})>"