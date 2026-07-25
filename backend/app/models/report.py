from sqlalchemy import Column, String, Integer, ForeignKey, Float, Enum as SQLEnum, Text, JSON
from sqlalchemy.orm import relationship
import enum

from app.models.base import Base, TimestampMixin

class RiskLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class CheckStatus(str, enum.Enum):
    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"
    NOT_APPLICABLE = "not_applicable"

class ComplianceReport(Base, TimestampMixin):
    __tablename__ = "compliance_reports"
    
    upload_id = Column(Integer, ForeignKey("uploads.id"), nullable=False)
    report_type = Column(String(50), default="compliance")
    overall_risk_level = Column(SQLEnum(RiskLevel), default=RiskLevel.MEDIUM)
    total_checks = Column(Integer, default=0)
    passed_checks = Column(Integer, default=0)
    failed_checks = Column(Integer, default=0)
    compliance_score = Column(Float, default=0.0)  # 0-100
    summary = Column(Text, nullable=True)
    recommendations = Column(JSON, nullable=True)
    
    # Relationships
    upload = relationship("Upload", back_populates="reports")
    check_results = relationship("ComplianceCheckResult", back_populates="report", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ComplianceReport(id={self.id}, upload_id={self.upload_id}, risk={self.overall_risk_level})>"

class ComplianceCheckResult(Base, TimestampMixin):
    __tablename__ = "compliance_check_results"
    
    report_id = Column(Integer, ForeignKey("compliance_reports.id"), nullable=False)
    check_name = Column(String(255), nullable=False)
    check_category = Column(String(100), nullable=False)
    status = Column(SQLEnum(CheckStatus), default=CheckStatus.NOT_APPLICABLE)
    risk_level = Column(SQLEnum(RiskLevel), default=RiskLevel.LOW)
    description = Column(Text, nullable=True)
    finding = Column(Text, nullable=True)
    remediation = Column(Text, nullable=True)
    reference = Column(String(255), nullable=True)
    
    # Relationships
    report = relationship("ComplianceReport", back_populates="check_results")
    
    def __repr__(self):
        return f"<ComplianceCheckResult(id={self.id}, check={self.check_name}, status={self.status})>"