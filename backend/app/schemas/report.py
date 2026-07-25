from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime
from enum import Enum

class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class CheckStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    WARNING = "warning"
    NOT_APPLICABLE = "not_applicable"

class CheckResultResponse(BaseModel):
    check_name: str
    check_category: str
    status: CheckStatus
    risk_level: RiskLevel
    description: Optional[str]
    finding: Optional[str]
    remediation: Optional[str]
    reference: Optional[str]
    
    class Config:
        from_attributes = True

class ComplianceReportResponse(BaseModel):
    id: int
    upload_id: int
    overall_risk_level: RiskLevel
    compliance_score: float
    total_checks: int
    passed_checks: int
    failed_checks: int
    summary: Optional[str]
    recommendations: Optional[Any]
    created_at: datetime
    check_results: Optional[List[CheckResultResponse]] = None
    
    class Config:
        from_attributes = True

class ReportGenerate(BaseModel):
    upload_id: int
    include_ai_analysis: bool = True