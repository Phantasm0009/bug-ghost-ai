# Bug Ghost AI - Deployment Guide

## Overview

This guide covers deploying Bug Ghost AI to production environments. We'll cover several popular platforms and best practices.

---

## Pre-Deployment Checklist

### Backend
- [ ] Set production `DATABASE_URL`
- [ ] Configure `LLM_API_KEY`
- [ ] Update `CORS_ORIGINS` to production domain(s)
- [ ] Set secure environment variables
- [ ] Test database migrations
- [ ] Configure logging and monitoring
- [ ] Set up error tracking (Sentry)
- [ ] Enable HTTPS
- [ ] Configure rate limiting
- [ ] Review security settings

### Frontend
- [ ] Set `NEXT_PUBLIC_API_URL` to production backend
- [ ] Build and test production bundle
- [ ] Configure CDN for static assets
- [ ] Set up analytics (optional)
- [ ] Configure error tracking
- [ ] Test all pages and features
- [ ] Verify API integration

### Database
- [ ] Set up automated backups
- [ ] Configure connection pooling
- [ ] Add indexes for performance
- [ ] Test disaster recovery
- [ ] Monitor query performance

---

## Deployment Options

### Option 1: Render (Recommended for MVP)

**Why Render?**
- Free tier available
- Easy PostgreSQL hosting
- Automatic deploys from Git
- SSL certificates included
- Good for both backend and frontend

#### Deploy Backend

1. **Create PostgreSQL Database**
   - Go to https://render.com
   - New → PostgreSQL
   - Name: `bug-ghost-db`
   - Copy the "Internal Database URL"

2. **Create Backend Web Service**
   - New → Web Service
   - Connect your GitHub repository
   - Name: `bug-ghost-backend`
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   
3. **Set Environment Variables**
   ```
   DATABASE_URL=<your-postgres-internal-url>
   LLM_PROVIDER=openai
   LLM_API_KEY=<your-api-key>
   LLM_MODEL=gpt-4-turbo-preview
   CORS_ORIGINS=https://your-frontend.onrender.com
   ```

4. **Deploy**
   - Render will auto-deploy
   - Note your backend URL: `https://bug-ghost-backend.onrender.com`

#### Deploy Frontend

1. **Create Static Site**
   - New → Static Site
   - Connect your GitHub repository
   - Name: `bug-ghost-frontend`
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/.next`

2. **Set Environment Variable**
   ```
   NEXT_PUBLIC_API_URL=https://bug-ghost-backend.onrender.com
   ```

3. **Deploy**
   - Frontend will be available at `https://bug-ghost-frontend.onrender.com`

---

### Option 2: Railway

**Why Railway?**
- Simple deployment
- Good free tier
- Built-in PostgreSQL
- Easy environment management

#### Steps

1. **Install Railway CLI**
   ```bash
   npm install -g railway
   railway login
   ```

2. **Initialize Project**
   ```bash
   cd bug-ghost-ai
   railway init
   ```

3. **Add PostgreSQL**
   ```bash
   railway add postgresql
   ```

4. **Deploy Backend**
   ```bash
   cd backend
   railway up
   ```

5. **Deploy Frontend**
   ```bash
   cd ../frontend
   railway up
   ```

6. **Set Environment Variables**
   - Use Railway dashboard or CLI
   - Add all required variables from `.env.example`

---

### Option 3: Vercel (Frontend) + Railway (Backend)

**Best for:** Optimal performance

#### Frontend on Vercel

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Deploy**
   ```bash
   cd frontend
   vercel
   ```

3. **Set Environment Variables**
   - In Vercel dashboard
   - Add `NEXT_PUBLIC_API_URL`

#### Backend on Railway

Follow Railway steps above for backend only.

---

### Option 4: DigitalOcean App Platform

**Why DigitalOcean?**
- Predictable pricing
- Full control
- Managed databases
- Docker support

#### Steps

1. **Create App**
   - Go to DigitalOcean App Platform
   - Connect GitHub repository

2. **Configure Components**
   
   **Database:**
   - Type: PostgreSQL
   - Plan: Basic ($15/mo)
   
   **Backend:**
   - Type: Web Service
   - Dockerfile: `backend/Dockerfile`
   - HTTP Port: 8000
   
   **Frontend:**
   - Type: Static Site
   - Build Command: `cd frontend && npm install && npm run build`
   - Output Directory: `frontend/.next`

3. **Set Environment Variables**
   - Add to each component
   - Use App Platform secrets for sensitive data

4. **Deploy**
   - Click "Create Resources"

---

### Option 5: AWS (Advanced)

**Components:**
- **Frontend**: S3 + CloudFront
- **Backend**: ECS Fargate or Lambda
- **Database**: RDS PostgreSQL
- **Load Balancer**: ALB

#### Quick Setup with AWS Copilot

```bash
# Install AWS Copilot
brew install aws/tap/copilot-cli

# Initialize
copilot init

# Deploy
copilot deploy
```

---

## Docker Production Build

### Create Production docker-compose

`docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:15-alpine
    restart: always
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: bug_ghost_ai
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    restart: always
    environment:
      DATABASE_URL: postgresql://postgres:${DB_PASSWORD}@db:5432/bug_ghost_ai
      LLM_API_KEY: ${LLM_API_KEY}
      LLM_MODEL: ${LLM_MODEL}
      CORS_ORIGINS: ${FRONTEND_URL}
    ports:
      - "8000:8000"
    depends_on:
      - db

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    restart: always
    environment:
      NEXT_PUBLIC_API_URL: ${BACKEND_URL}
    ports:
      - "3000:3000"
    depends_on:
      - backend

  nginx:
    image: nginx:alpine
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend

volumes:
  postgres_data:
```

### Deploy

```bash
# Set environment variables
export DB_PASSWORD=secure-password
export LLM_API_KEY=your-key
export FRONTEND_URL=https://yourdomain.com
export BACKEND_URL=https://api.yourdomain.com

# Build and deploy
docker-compose -f docker-compose.prod.yml up -d
```

---

## Environment Variables Reference

### Backend Production Variables

```env
# Database
DATABASE_URL=postgresql://user:password@host:port/database

# LLM
LLM_PROVIDER=openai
LLM_API_KEY=sk-...
LLM_MODEL=gpt-4-turbo-preview

# API
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Security
SECRET_KEY=<generate-random-string>

# Monitoring (optional)
SENTRY_DSN=https://...
LOG_LEVEL=INFO
```

### Frontend Production Variables

```env
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX  # Optional: Google Analytics
```

---

## SSL/HTTPS Setup

### Option 1: Let's Encrypt (Free)

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

### Option 2: Cloudflare (Free)

1. Add domain to Cloudflare
2. Update nameservers
3. Enable SSL/TLS (Full mode)
4. Enable HTTP to HTTPS redirect

---

## Monitoring & Logging

### Sentry for Error Tracking

**Backend:**
```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[FastApiIntegration()],
    traces_sample_rate=1.0,
)
```

**Frontend:**
```typescript
import * as Sentry from "@sentry/nextjs";

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  tracesSampleRate: 1.0,
});
```

### Logging

**Backend:**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

---

## Performance Optimization

### Backend

1. **Database Connection Pooling**
   ```python
   engine = create_engine(
       DATABASE_URL,
       pool_size=20,
       max_overflow=40
   )
   ```

2. **Caching** (Redis)
   ```python
   import redis
   cache = redis.Redis(host='localhost', port=6379)
   ```

3. **Rate Limiting**
   ```python
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)
   ```

### Frontend

1. **Image Optimization**
   - Use Next.js Image component
   - Enable image optimization in `next.config.js`

2. **Code Splitting**
   - Already handled by Next.js

3. **CDN**
   - Use Vercel CDN or CloudFront

---

## Scaling Considerations

### Horizontal Scaling

**Backend:**
- Deploy multiple instances behind load balancer
- Use managed database with read replicas
- Implement session storage in Redis

**Frontend:**
- Static site hosting scales automatically
- Use CDN for global distribution

### Vertical Scaling

Start with:
- **Backend**: 1 CPU, 1GB RAM
- **Database**: 1 CPU, 2GB RAM
- **Frontend**: Static hosting

Scale up as needed based on metrics.

---

## Cost Estimates

### Free Tier (MVP)
- **Render**: Free PostgreSQL + Web Service
- **Vercel**: Free for personal projects
- **Total**: $0/month (+ LLM API costs)

### Production (Low Traffic)
- **Railway**: ~$20/month
- **Vercel Pro**: $20/month
- **Total**: ~$40/month (+ LLM API costs)

### Production (Medium Traffic)
- **DigitalOcean**: ~$50/month
- **Database**: $15/month
- **CDN**: $10/month
- **Total**: ~$75/month (+ LLM API costs)

### LLM API Costs
- **GPT-4 Turbo**: ~$0.01-0.03 per request
- **Claude Opus**: ~$0.015-0.075 per request
- **Budget**: $100/month = ~3,000-10,000 requests

---

## Backup & Disaster Recovery

### Database Backups

**Automated (Recommended):**
```bash
# Daily backups to S3
pg_dump $DATABASE_URL | gzip | aws s3 cp - s3://backups/db-$(date +%Y%m%d).sql.gz
```

**Manual:**
```bash
pg_dump -h host -U user -d bug_ghost_ai > backup.sql
```

### Restore

```bash
psql $DATABASE_URL < backup.sql
```

---

## Health Checks

Add to backend (`app/main.py`):

```python
@app.get("/health")
def health_check():
    try:
        # Check database
        db.execute("SELECT 1")
        return {"status": "healthy", "database": "ok"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

Set up monitoring to ping `/health` every 30 seconds.

---

## Rollback Plan

1. **Keep Previous Versions**
   - Tag releases in Git
   - Keep last 3 Docker images

2. **Quick Rollback**
   ```bash
   # Docker
   docker-compose down
   git checkout previous-tag
   docker-compose up -d
   
   # Platform-specific
   # Use platform's rollback feature
   ```

3. **Database Rollback**
   - Restore from backup if schema changed
   - Test rollback procedure quarterly

---

## Post-Deployment

1. **Test Everything**
   - Create debug session
   - View session list
   - Check API docs

2. **Monitor for 24 Hours**
   - Watch error rates
   - Check performance metrics
   - Review logs

3. **Set Up Alerts**
   - Error rate > 5%
   - Response time > 2s
   - Database connection failures

4. **Document**
   - Update deployment date
   - Note any issues
   - Update runbook

---

## Support

Questions? Check:
- README.md
- DEVELOPER_GUIDE.md
- GitHub Issues

**Happy Deploying! 🚀**
