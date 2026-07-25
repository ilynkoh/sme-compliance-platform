import os
from app.config import settings
from app.utils.errors import ValidationException

def validate_file_upload(filename: str, file_size: float) -> bool:
    """Validate uploaded file"""
    _, ext = os.path.splitext(filename)
    ext = ext.lower().lstrip('.')
    
    if ext not in settings.ALLOWED_FILE_TYPES:
        raise ValidationException(
            f"File type .{ext} not allowed. Allowed: {', '.join(settings.ALLOWED_FILE_TYPES)}"
        )
    
    if file_size > settings.MAX_FILE_SIZE_MB:
        raise ValidationException(
            f"File size {file_size}MB exceeds maximum {settings.MAX_FILE_SIZE_MB}MB"
        )
    
    return True

def validate_fiscal_year(year: str) -> bool:
    """Validate fiscal year format"""
    if not year or len(year) != 4 or not year.isdigit():
        raise ValidationException("Fiscal year must be a 4-digit number")
    return True