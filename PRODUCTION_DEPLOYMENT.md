# AI Prompt Generator SaaS - Production Deployment Guide

## Pre-Deployment Checklist

**Security:**
- [ ] Change all default passwords
- [ ] Generate new SECRET_KEY using `openssl rand -hex 32`
- [ ] Update environment variables for production
- [ ] Enable HTTPS/SSL certificates
- [ ] Configure firewall rules
- [ ] Set up API rate limiting
- [ ] Enable CORS for specific domains only
- [ ] Review database permissions

**Database:**
- [ ] Create automated backups
- [ ] Test backup recovery
- [ ] Set up connection pooling
- [ ] Optimize indexes for expected workload
- [ ] Enable query logging for monitoring
- [ ] Configure log retention

**Backend:**
- [ ] Set `DEBUG=false`
- [ ] Configure logging to file/service
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Configure email notifications
- [ ] Set up API monitoring
- [ ] Test all endpoints
- [ ] Generate API documentation

**Frontend:**
- [ ] Build with production optimizations
- [ ] Configure correct API endpoint
- [ ] Test all features
- [ ] Optimize images and assets
- [ ] Set up CDN for static files
- [ ] Configure analytics

**Infrastructure:**
- [ ] Choose hosting provider (AWS, Azure, GCP, etc.)
- [ ] Set up monitoring and alerting
- [ ] Configure auto-scaling
- [ ] Set up CI/CD pipelines
- [ ] Configure backup strategies
- [ ] Plan disaster recovery

---

## Deployment Options

### Option 1: Docker Compose on VPS

```bash
# SSH into VPS
ssh root@your-vps-ip

# Install Docker and Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Clone repository
git clone your-repo-url
cd ai-prompt-generator

# Configure environment
cp backend/.env.example backend/.env
# Edit .env with production values

# Start services
docker compose -f deployment/docker-compose.yml up -d

# Configure Nginx reverse proxy
# See deployment/nginx.conf for reference
```

### Option 2: Kubernetes Cluster

```bash
# Prerequisites
# - kubectl configured
# - Cluster access

# Create namespace
kubectl create namespace prompt-generator

# Create secrets
kubectl create secret generic app-secrets \
  --from-literal=database-url="..." \
  --from-literal=secret-key="..." \
  -n prompt-generator

# Deploy
kubectl apply -f deployment/kubernetes.yaml -n prompt-generator

# Verify
kubectl get pods -n prompt-generator
kubectl get svc -n prompt-generator
```

### Option 3: AWS Deployment

```bash
# Using AWS CloudFormation or Terraform

# Prerequisites
# - AWS account
# - AWS CLI configured
# - RDS PostgreSQL instance
# - ECR repositories created

# Build and push images
docker build -f deployment/Dockerfile.backend -t $ECR_REPO/backend:latest .
docker push $ECR_REPO/backend:latest

# Deploy using ECS or EKS
# See AWS specific documentation
```

### Option 4: Azure App Service

```bash
# Using Azure Container Instances or App Service

# Prerequisites
# - Azure subscription
# - Azure CLI installed

# Create resource group
az group create --name prompt-generator --location eastus

# Deploy using Azure Resource Manager or Terraform
# See Azure specific documentation
```

---

## Production Configuration

### Environment Variables
```env
# Database (Production RDS/CloudSQL/etc.)
DATABASE_URL=postgresql://user:secure-password@your-db-host:5432/prompt_generator_db

# Security
SECRET_KEY="generated-with-openssl-rand-hex-32"
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=false

# CORS (Your domain)
CORS_ORIGINS=["https://yourdomain.com", "https://www.yourdomain.com"]

# Email Service
SMTP_SERVER=smtp.sendgrid.com
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=your-sendgrid-key

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/app/app.log

# Environment
ENVIRONMENT=production
```

### Nginx Configuration
```nginx
# Run behind Nginx for better performance
# See deployment/nginx.conf for complete config

upstream backend {
    server backend:8000;
}

server {
    listen 80;
    server_name yourdomain.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location /api {
        proxy_pass http://backend;
        # ... proxy settings
    }
}
```

---

## Monitoring & Maintenance

### Health Checks
```bash
# Manual health check
curl https://yourdomain.com/health

# Monitor response time
curl -w "@curl-format.txt" -o /dev/null -s https://yourdomain.com/health
```

### Database Maintenance
```bash
# Backup database weekly
0 2 * * 0 pg_dump $DB_URL > /backups/db_$(date +\%Y\%m\%d).sql

# Analyze tables monthly
ANALYZE;

# Vacuum for cleanup
VACUUM ANALYZE;
```

### Log Management
```bash
# View application logs
docker logs prompt_generator_backend

# Monitor real-time logs
docker logs -f prompt_generator_backend

# Archive old logs
find /var/log/app -name "*.log" -mtime +30 -delete
```

---

## Security Hardening

### SSL/TLS Certificate
```bash
# Using Let's Encrypt
sudo apt-get install certbot nginx-certbot
sudo certbot certonly --nginx -d yourdomain.com

# Auto-renewal
sudo systemctl enable certbot.timer
```

### Firewall Setup
```bash
# UFW (Ubuntu)
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw enable
```

### Database Security
```sql
-- Create limited user for app
CREATE USER app_user WITH PASSWORD 'strong-password';
GRANT CONNECT ON DATABASE prompt_generator_db TO app_user;
GRANT USAGE ON SCHEMA public TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO app_user;

-- Disable super user
ALTER USER postgres WITH NOSUPERUSER;
```

---

## Performance Tuning

### Database Optimization
```sql
-- Analyze query performance
EXPLAIN ANALYZE SELECT * FROM prompts WHERE topic = 'Python';

-- Create composite indexes
CREATE INDEX idx_prompts_topic_audience ON prompts(topic, audience);

-- Vacuum analyze
VACUUM ANALYZE prompts;
```

### Backend Optimization
```python
# Increase workers
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker

# Enable caching
from fastapi_cache import FastAPICache
```

### Frontend Optimization
```bash
# Build with optimizations
npm run build

# Enable gzip compression
# (Already in nginx.conf)
```

---

## Disaster Recovery

### Backup Strategy
```bash
# Daily backups
0 2 * * * docker exec prompt_generator_db pg_dump -U promptgenerator prompt_generator_db > /backups/daily_$(date +\%d).sql

# Weekly full backup to S3
0 3 * * 0 aws s3 cp /backups/daily_*.sql s3://your-bucket/backups/
```

### Recovery Plan
```bash
# Restore from backup
docker exec prompt_generator_db psql -U promptgenerator < backup_file.sql

# Verify data integrity
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM prompts;
```

---

## Support & Troubleshooting

### Common Issues

#### High CPU Usage
```bash
# Check processes
docker stats
# Check queries
SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;
```

#### Low Disk Space
```bash
# Check usage
df -h
# Clean old logs
find /var/log -name "*.old" -delete
```

#### Database Corruption
```bash
# Check and repair
docker exec prompt_generator_db reindex database prompt_generator_db;
```

---

## Maintenance Schedule

### Daily
- [ ] Monitor logs for errors
- [ ] Check disk space
- [ ] Monitor API response times

### Weekly
- [ ] Analyze database queries
- [ ] Review security logs
- [ ] Test backups

### Monthly
- [ ] Update dependencies (after testing)
- [ ] Security audit
- [ ] Performance analysis
- [ ] Database maintenance

### Quarterly
- [ ] Disaster recovery drill
- [ ] Capacity planning
- [ ] Architecture review

---

##  Learning Resources

- [FastAPI Production Deployment](https://fastapi.tiangolo.com/deployment/)
- [PostgreSQL Administration](https://www.postgresql.org/docs/current/admin.html)
- [Docker Production Best Practices](https://docs.docker.com/config/containers/resource_constraints/)
- [Kubernetes Production Best Practices](https://kubernetes.io/docs/concepts/cluster-administration/manage-deployment/)
- [OWASP Security Guidelines](https://owasp.org/www-project-web-security-testing-guide/)

---

**Production deployment requires careful planning and ongoing maintenance. Refer to your cloud provider's documentation for specific guidance.**
