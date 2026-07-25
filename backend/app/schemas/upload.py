from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class UploadStatus(str, Enum):
    UPLOADED = "uploaded"
    PARSING = "parsing"
    PARSED = "parsed"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    FAILED = "failed"

class TrialBalanceEntryResponse(BaseModel):
    account_code: str
    account_name: str
    account_type: str
    debit_amount: float
    credit_amount: float
    notes: Optional[str] = None
    
    class Config:
        from_attributes = True

class UploadResponse(BaseModel):
    id: int
    company_id: int
    filename: str
    status: UploadStatus
    file_size: Optional[float]
    fiscal_year: Optional[str]
    error_message: Optional[str]
    created_at: datetime
    entries: Optional[List[TrialBalanceEntryResponse]] = None
    
    class Config:
        from_attributes = True

class UploadCreate(BaseModel):
    company_id: int
    fiscal_year: Optional[str] = None