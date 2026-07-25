# Deployment Guide

## Quick Start with Docker Compose

### Prerequisites

- Docker & Docker Compose installed
- Git
- 4GB RAM minimum
- 10GB disk space

### Local Development Deployment

1. **Clone the repository**

```bash
git clone https://github.com/ilynkoh/sme-compliance-platform.git
cd sme-compliance-platform
```

2. **Setup environment**

```bash
cp .env.example .env
```

Edit `.env` with your configuration:
```env
# Change these for production
SECRET_KEY=your-super-secret-key-change-this
OPENAI_API_KEY=sk-your-key-here
DATABASE_URL=postgresql://sme_user:sme_password@db:5432/sme_compliance
```

3. **Start services**

```bash
docker-compose up -d
```

4. **Initialize database**

```bash
# Create tables
docker-compose exec backend python -c "from app.utils.db import init_db; import asyncio; asyncio.run(init_db())"
```

5. **Access the application**

- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs
- Database: localhost:5432

### Verify Services

```bash
# Check services
docker-compose ps

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Test API
curl http://localhost:8000/api/health
```

## Production Deployment

### Using AWS EC2

1. **Launch EC2 Instance**

- Instance type: t3.medium or larger
- Storage: 30GB EBS
- Security group: Allow ports 80, 443, 3000, 8000

2. **Install Docker**

```bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
sudo usermod -aG docker $USER
```

3. **Deploy application**

```bash
git clone https://github.com/ilynkoh/sme-compliance-platform.git
cd sme-compliance-platform

# Setup production env
cp .env.example .env
# Edit .env with production values

docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

4. **Setup reverse proxy (Nginx)**

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
    }
}
```

5. **Setup SSL with Let's Encrypt**

```bash
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot certonly --nginx -d yourdomain.com
```

### Using Railway/Render

1. **Push to GitHub**

```bash
git push origin main
```

2. **Railway Setup**

- Connect GitHub repository
- Create PostgreSQL plugin
- Set environment variables
- Deploy

### Environment Variables for Production

```env
# Security
SECRET_KEY=<generate-secure-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Database (use managed service)
DATABASE_URL=postgresql://user:pass@db-host:5432/sme_compliance
SQLALCHEMY_ECHO=False

# API
FRONTEND_URL=https://yourdomain.com
ALLOWED_ORIGINS=https://yourdomain.com

# AI
OPENAI_API_KEY=<your-key>
OPENAI_MODEL=gpt-4

# Logging
LOG_LEVEL=INFO

# Email
SMTP_HOST=<smtp-server>
SMTP_PORT=587
SMTP_USER=<email>
SMTP_PASSWORD=<password>
```

## Scaling Considerations

### Horizontal Scaling

1. **Multiple Backend Instances**

```yaml
backend:
  replicas: 3
  load_balancer: true
```

2. **Database Connection Pooling**

- Use PgBouncer for connection management
- Configure pool size based on load

3. **Caching Layer**

- Add Redis for session/cache storage
- Cache compliance check results

### Monitoring

1. **Health Checks**

```bash
# API health
GET /api/health

# Database
GET /api/config
```

2. **Logging**

```bash
# View logs
docker-compose logs -f

# Ship to external service
# - AWS CloudWatch
# - Datadog
# - ELK Stack
```

3. **Metrics**

- Request count
- Response times
- Error rates
- Database performance

## Database Backup & Recovery

### Regular Backups

```bash
# Daily backup
docker-compose exec db pg_dump -U sme_user sme_compliance > backup_$(date +%Y%m%d).sql

# Store in S3
aws s3 cp backup_*.sql s3://your-bucket/backups/
```

### Recovery

```bash
# Restore from backup
psql -U sme_user -d sme_compliance < backup_20240725.sql
```

## Maintenance

### Update Application

```bash
git pull origin main
docker-compose build
docker-compose up -d
```

### Update Dependencies

```bash
# Backend
cd backend
pip install --upgrade -r requirements.txt

# Frontend
cd frontend
npm update
```

### Database Maintenance

```bash
# Vacuum (optimize)
docker-compose exec db vacuumdb -U sme_user sme_compliance

# Analyze (update statistics)
docker-compose exec db analyzedb -U sme_user sme_compliance
```

## Troubleshooting

### Common Issues

**1. Port already in use**

```bash
# Change ports in docker-compose.yml
ports:
  - "8001:8000"  # Backend on 8001
  - "3001:3000"  # Frontend on 3001
```

**2. Database connection failed**

```bash
# Check database container
docker-compose logs db

# Verify connection
docker-compose exec db psql -U sme_user -d sme_compliance -c "SELECT 1"
```

**3. Out of memory**

```bash
# Increase Docker memory
# Docker Desktop: Preferences → Resources → Memory
# Or in docker-compose.yml:
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 2G
```

### Check Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db

# Last 100 lines
docker-compose logs -f --tail=100 backend
```

## Security Hardening

1. **Secrets Management**
   - Never commit `.env` files
   - Use environment variable services
   - Rotate secrets regularly

2. **API Security**
   - Enable CORS restrictions
   - Implement rate limiting
   - Use HTTPS only in production

3. **Database**
   - Strong passwords
   - Regular backups
   - Encrypted connections

4. **Infrastructure**
   - Firewall rules
   - Security groups
   - DDoS protection

## Performance Optimization

1. **Database**
   - Add indexes on frequently queried columns
   - Implement query caching
   - Monitor slow queries

2. **API**
   - Implement pagination
   - Add response caching
   - Use async operations

3. **Frontend**
   - Enable gzip compression
   - Optimize images
   - Lazy load components

## Support & Resources

- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check `/docs` folder
- **API Docs**: http://localhost:8000/docs
- **Email**: support@smecompliance.my
