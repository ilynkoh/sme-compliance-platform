from fastapi import APIRouter, File, UploadFile, Form, HTTPException, status
from sqlalchemy.orm import Session
import os
import uuid

from app.config import settings
from app.utils.db import get_db_session
from app.models.upload import Upload, UploadStatus
from app.models.company import Company
from app.models.trial_balance import TrialBalanceEntry
from app.schemas.upload import UploadResponse
from app.utils.validators import validate_file_upload, validate_fiscal_year
from app.utils.errors import ResourceNotFoundException, FileProcessingException
from app.services.excel_parser import ExcelParser

router = APIRouter()

@router.post("/trial-balance", response_model=UploadResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_trial_balance(
    file: UploadFile = File(...),
    company_id: int = Form(...),
    fiscal_year: str = Form(None)
):
    db = get_db_session()
    try:
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            raise ResourceNotFoundException("Company not found")
        
        if fiscal_year:
            validate_fiscal_year(fiscal_year)
        
        file_content = await file.read()
        file_size_mb = len(file_content) / (1024 * 1024)
        
        validate_file_upload(file.filename, file_size_mb)
        
        upload_id = str(uuid.uuid4())
        file_path = os.path.join(settings.UPLOAD_DIR, upload_id, file.filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'wb') as f:
            f.write(file_content)
        
        upload = Upload(
            company_id=company_id,
            filename=file.filename,
            file_path=file_path,
            file_size=file_size_mb,
            fiscal_year=fiscal_year,
            status=UploadStatus.UPLOADED
        )
        db.add(upload)
        db.commit()
        db.refresh(upload)
        
        try:
            parser = ExcelParser(file_path)
            entries = parser.parse()
            
            for entry_data in entries:
                entry = TrialBalanceEntry(
                    upload_id=upload.id,
                    **entry_data
                )
                db.add(entry)
            
            upload.status = UploadStatus.PARSED
            db.commit()
        except Exception as e:
            upload.status = UploadStatus.FAILED
            upload.error_message = str(e)
            db.commit()
        
        return upload
    except Exception as e:
        db.rollback()
        raise
    finally:
        db.close()

@router.get("/{upload_id}", response_model=UploadResponse)
async def get_upload(upload_id: int):
    db = get_db_session()
    try:
        upload = db.query(Upload).filter(Upload.id == upload_id).first()
        if not upload:
            raise ResourceNotFoundException("Upload not found")
        return upload
    finally:
        db.close()