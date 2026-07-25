# Setup Guide

## Prerequisites

### System Requirements
- **OS**: Linux, macOS, or Windows (with WSL2)
- **Docker**: 20.10+
- **Docker Compose**: 1.29+
- **Git**: 2.30+
- **RAM**: 4GB minimum (8GB recommended)
- **Disk**: 10GB free space

### Install Docker

**macOS:**
```bash
brew install docker docker-compose
# Or download Docker Desktop
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker $USER
logout && login  # Apply group changes
```

**Windows:**
- Download Docker Desktop from docker.com
- Enable WSL2 backend
- Install from Microsoft Store

## Quick Start (5 minutes)

### 1. Clone Repository

```bash
git clone https://github.com/ilynkoh/sme-compliance-platform.git
cd sme-compliance-platform
```

### 2. Configure Environment

```bash
cp .env.example .env
```

The default `.env` is suitable for development. For customization:

```env
# Optional: Change API port
DATABASE_URL=postgresql://sme_user:sme_password@db:5432/sme_compliance

# Optional: Add OpenAI API key for AI analysis
OPENAI_API_KEY=sk-your-openai-api-key
```

### 3. Start Services

```bash
docker-compose up -d
```

This starts:
- PostgreSQL database on `localhost:5432`
- Backend API on `localhost:8000`
- Frontend on `localhost:3000`

### 4. Initialize Database

```bash
# Create tables
docker-compose exec backend python -c "from app.utils.db import init_db; import asyncio; asyncio.run(init_db())"
```

### 5. Access Application

- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **API Health Check**: http://localhost:8000/api/health

## Test the Setup

### Verify Services are Running

```bash
# Check container status
docker-compose ps

# Expected output:
# NAME                    STATUS
# sme_compliance_db       Up (healthy)
# sme_compliance_backend  Up
# sme_compliance_frontend Up
```

### Test API

```bash
# Health check
curl http://localhost:8000/api/health

# Expected response:
# {"status":"healthy","app":"SME Compliance Platform","version":"0.1.0"}
```

### Create Test Account

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!",
    "full_name": "Test User",
    "phone": "+60123456789"
  }'
```

### Login to Frontend

1. Go to http://localhost:3000
2. Click "Sign up" and create account
3. Login with your credentials
4. Upload a trial balance Excel file

## Sample Excel File Format

Create a file `sample_trial_balance.xlsx` with this structure:

| Account Code | Account Name | Account Type | Debit | Credit |
|---|---|---|---|---|
| 1000 | Cash | asset | 50000 | 0 |
| 1100 | Bank | asset | 75000 | 0 |
| 2000 | Accounts Payable | liability | 0 | 40000 |
| 2100 | Loans Payable | liability | 0 | 50000 |
| 3000 | Share Capital | equity | 0 | 60000 |
| 4000 | Revenue | revenue | 0 | 95000 |
| 5000 | Operating Expenses | expense | 50000 | 0 |
| 5100 | Administrative Expenses | expense | 30000 | 0 |

**Total Debits = 205,000 | Total Credits = 245,000**
(Not balanced in this example - fix by adjusting values)

## Project Structure

```
sme-compliance-platform/
├── backend/                    # FastAPI application
│   ├── app/
│   │   ├── main.py            # App entry point
│   │   ├── config.py          # Configuration
│   │   ├── models/            # Database models
│   │   ├── services/          # Business logic
│   │   ├── api/               # API routes
│   │   └── utils/             # Helper functions
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile
├── frontend/                   # React application
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/             # Page components
│   │   ├── services/          # API calls
│   │   └── App.tsx            # Main app component
│   ├── package.json           # Node dependencies
│   └── Dockerfile
├── docker-compose.yml         # Container orchestration
├── .env.example              # Environment template
└── docs/                       # Documentation
```

## Common Tasks

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Last 50 lines
docker-compose logs --tail=50 backend
```

### Stop Services

```bash
# Stop all
docker-compose stop

# Stop specific service
docker-compose stop backend

# Restart
docker-compose restart backend
```

### Access Database

```bash
# Connect to PostgreSQL
docker-compose exec db psql -U sme_user -d sme_compliance

# Sample queries:
# \dt                          # List tables
# SELECT * FROM users;         # Query users
# \q                          # Quit
```

### Rebuild Images

```bash
# Rebuild specific service
docker-compose build backend

# Rebuild all
docker-compose build

# Rebuild and restart
docker-compose up -d --build
```

## Development Workflow

### Making Changes

**Backend:**
```bash
# Services auto-reload with volume mount
# Just edit files in backend/app/
# Changes appear immediately
```

**Frontend:**
```bash
# React dev server auto-refreshes
# Edit files in frontend/src/
# Changes appear in browser
```

### Running Tests

**Backend:**
```bash
# Run tests
docker-compose exec backend pytest

# Run specific test file
docker-compose exec backend pytest tests/test_excel_parser.py

# Run with coverage
docker-compose exec backend pytest --cov=app tests/
```

**Frontend:**
```bash
# Run tests
docker-compose exec frontend npm test

# Run with coverage
docker-compose exec frontend npm test -- --coverage
```

## Next Steps

1. **Read the API documentation**
   - http://localhost:8000/docs
   - See `docs/API.md`

2. **Upload a trial balance**
   - Create Excel file with proper structure
   - Upload via frontend or API

3. **Generate compliance report**
   - System automatically analyzes file
   - Review compliance checks and risk assessment

4. **Integrate with your workflow**
   - Connect to your accounting system
   - Automate regular compliance checks

## Troubleshooting

### Can't connect to localhost:3000

```bash
# Check if frontend container is running
docker-compose ps frontend

# View frontend logs
docker-compose logs frontend

# Try rebuilding
docker-compose up -d --build frontend
```

### Database connection error

```bash
# Check database status
docker-compose logs db

# Verify database is healthy
docker-compose ps db  # Should show "healthy"

# Restart database
docker-compose restart db
```

### Port already in use

```bash
# Change ports in docker-compose.yml
ports:
  - "8001:8000"  # Use 8001 instead of 8000
  - "3001:3000"  # Use 3001 instead of 3000
```

### Out of memory

```bash
# Increase Docker memory
# Docker Desktop: Settings → Resources
# Or set memory limit in docker-compose.yml
```

### Permission denied errors

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Apply group changes
newgrp docker

# Or use sudo
sudo docker-compose up -d
```

## Getting Help

1. **Check logs**: `docker-compose logs -f`
2. **Review documentation**: Read `/docs` folder
3. **API docs**: http://localhost:8000/docs
4. **GitHub Issues**: Report problems
5. **Email Support**: support@smecompliance.my

## What's Next?

- [View API Documentation](API.md)
- [Learn about Companies Act 2016](COMPANIES_ACT_2016.md)
- [Production Deployment](DEPLOYMENT.md)
- [Contribute to Development](../CONTRIBUTING.md)
