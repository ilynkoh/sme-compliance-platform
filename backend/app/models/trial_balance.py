from sqlalchemy import Column, String, Integer, ForeignKey, Float, Enum as SQLEnum, Text
from sqlalchemy.orm import relationship
import enum

from app.models.base import Base, TimestampMixin

class AccountType(str, enum.Enum):
    ASSET = "asset"
    LIABILITY = "liability"
    EQUITY = "equity"
    REVENUE = "revenue"
    EXPENSE = "expense"
    OTHER = "other"

class TrialBalanceEntry(Base, TimestampMixin):
    __tablename__ = "trial_balance_entries"
    
    upload_id = Column(Integer, ForeignKey("uploads.id"), nullable=False)
    account_code = Column(String(50), nullable=False)
    account_name = Column(String(255), nullable=False)
    account_type = Column(SQLEnum(AccountType), nullable=False)
    debit_amount = Column(Float, default=0.0)
    credit_amount = Column(Float, default=0.0)
    notes = Column(Text, nullable=True)
    
    # Relationships
    upload = relationship("Upload", back_populates="entries")
    
    def __repr__(self):
        return f"<TrialBalanceEntry(id={self.id}, account={self.account_name}, debit={self.debit_amount}, credit={self.credit_amount})>"