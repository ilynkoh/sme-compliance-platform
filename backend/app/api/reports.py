from fastapi import APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from app.utils.db import get_db_session
from app.models.report import ComplianceReport
from app.models.upload import Upload
from app.schemas.report import ComplianceReportResponse, ReportGenerate
from app.utils.errors import ResourceNotFoundException
from app.services.report_generator import ReportGenerator

router = APIRouter()

@router.post("/generate", response_model=ComplianceReportResponse, status_code=status.HTTP_201_CREATED)
async def generate_report(report_data: ReportGenerate):
    db = get_db_session()
    try:
        upload = db.query(Upload).filter(Upload.id == report_data.upload_id).first()
        if not upload:
            raise ResourceNotFoundException("Upload not found")
        
        generator = ReportGenerator(upload, db)
        report = generator.generate(include_ai_analysis=report_data.include_ai_analysis)
        
        return report
    finally:
        db.close()

@router.get("/{report_id}", response_model=ComplianceReportResponse)
async def get_report(report_id: int):
    db = get_db_session()
    try:
        report = db.query(ComplianceReport).filter(ComplianceReport.id == report_id).first()
        if not report:
            raise ResourceNotFoundException("Report not found")
        return report
    finally:
        db.close()

@router.get("/upload/{upload_id}")
async def get_reports_by_upload(upload_id: int):
    db = get_db_session()
    try:
        reports = db.query(ComplianceReport).filter(ComplianceReport.upload_id == upload_id).all()
        return reports
    finally:
        db.close()