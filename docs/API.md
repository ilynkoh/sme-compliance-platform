# API Documentation

## Overview

The SME Compliance Platform provides a RESTful API for managing financial compliance analysis. All endpoints require authentication via JWT tokens.

## Base URL

```
http://localhost:8000
```

## Authentication

All endpoints (except `/auth/register` and `/auth/login`) require a Bearer token:

```
Authorization: Bearer <access_token>
```

## Endpoints

### Authentication

#### Register
```
POST /api/auth/register
```

Request body:
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "full_name": "John Doe",
  "phone": "+60123456789"
}
```

Response:
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_verified": false,
  "created_at": "2026-07-25T10:00:00Z"
}
```

#### Login
```
POST /api/auth/login
```

Request body:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

#### Get Current User
```
GET /api/auth/me
```

Response:
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_verified": false,
  "created_at": "2026-07-25T10:00:00Z"
}
```

### File Upload

#### Upload Trial Balance
```
POST /api/uploads/trial-balance
Content-Type: multipart/form-data
```

Form parameters:
- `file` (required): Excel file (.xlsx, .xls, .csv)
- `company_id` (required): Company ID
- `fiscal_year` (optional): Fiscal year (YYYY format)

Response:
```json
{
  "id": 1,
  "company_id": 1,
  "filename": "trial_balance_2024.xlsx",
  "status": "parsed",
  "file_size": 0.5,
  "fiscal_year": "2024",
  "error_message": null,
  "created_at": "2026-07-25T10:00:00Z"
}
```

#### Get Upload Details
```
GET /api/uploads/{upload_id}
```

Response: Upload object with parsed trial balance entries

### Reports

#### Generate Report
```
POST /api/reports/generate
```

Request body:
```json
{
  "upload_id": 1,
  "include_ai_analysis": true
}
```

Response:
```json
{
  "id": 1,
  "upload_id": 1,
  "overall_risk_level": "medium",
  "compliance_score": 75.5,
  "total_checks": 10,
  "passed_checks": 8,
  "failed_checks": 1,
  "summary": "...",
  "recommendations": {...},
  "created_at": "2026-07-25T10:00:00Z",
  "check_results": [...]
}
```

#### Get Report
```
GET /api/reports/{report_id}
```

Response: Complete compliance report

#### Get Reports by Upload
```
GET /api/reports/upload/{upload_id}
```

Response: Array of reports for the upload

## Error Handling

Errors are returned with appropriate HTTP status codes:

- `200`: Success
- `201`: Created
- `400`: Bad Request
- `401`: Unauthorized
- `403`: Forbidden
- `404`: Not Found
- `422`: Validation Error
- `500`: Server Error

Error response format:
```json
{
  "detail": "Error message describing the issue"
}
```

## Rate Limiting

No rate limiting is currently implemented. Production deployment should add appropriate limits.

## Pagination

List endpoints support pagination via query parameters:
- `?page=1`
- `?per_page=50`

## File Format Requirements

### Excel File Structure

Your Excel file must contain these columns:
- **Account Code**: Unique account identifier (e.g., "1000")
- **Account Name**: Full account name (e.g., "Cash")
- **Account Type**: One of: asset, liability, equity, revenue, expense
- **Debit**: Debit amount (number)
- **Credit**: Credit amount (number)

Example:
| Account Code | Account Name | Account Type | Debit | Credit |
|--------------|-------------|--------------|-------|--------|
| 1000 | Cash | asset | 50000 | 0 |
| 2000 | Accounts Payable | liability | 0 | 40000 |
| 3000 | Share Capital | equity | 0 | 60000 |

## Testing the API

### Using curl

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'

# Upload file
curl -X POST http://localhost:8000/api/uploads/trial-balance \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@trial_balance.xlsx" \
  -F "company_id=1" \
  -F "fiscal_year=2024"
```

### Using Swagger UI

Access interactive API documentation at:
```
http://localhost:8000/docs
```

## Response Examples

### Successful Compliance Report

```json
{
  "id": 1,
  "upload_id": 1,
  "overall_risk_level": "low",
  "compliance_score": 92.5,
  "total_checks": 12,
  "passed_checks": 11,
  "failed_checks": 0,
  "summary": "**Compliance Report Summary**\n\n- Total Compliance Checks: 12\n- Passed: 11\n- Failed: 0\n- Warnings: 1\n\n- Financial Risks Identified: 0",
  "recommendations": {
    "ai_recommendations": "Based on the analysis, the company...",
    "risks": []
  },
  "created_at": "2026-07-25T10:00:00Z",
  "check_results": [
    {
      "check_name": "Trial Balance Totals",
      "check_category": "Financial Statement",
      "status": "pass",
      "risk_level": "low",
      "description": "Debits (RM150000.00) = Credits (RM150000.00)",
      "reference": "Fundamental Accounting Principle"
    }
  ]
}
```
