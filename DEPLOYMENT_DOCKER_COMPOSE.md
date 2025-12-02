# Deploying Bug Ghost AI with Docker Compose 🚀

Guide for deploying the full stack (including sandbox execution) to cloud platforms.

---

## Platform Support

| Platform | Docker Compose | DinD Support | Difficulty |
|----------|----------------|--------------|------------|
| **Railway** | ✅ Native | ✅ Yes | ⭐ Easy |
| **Fly.io** | ✅ Via flyctl | ✅ Yes | ⭐⭐ Medium |
| **DigitalOcean** | ✅ App Platform | ✅ Yes | ⭐ Easy |
| **Render** | ❌ No | ⚠️ Workaround | ⭐⭐⭐ Hard |
| **Self-hosted** | ✅ Yes | ✅ Yes | ⭐ Easy |

---

## Option 1: Railway (Recommended)

Railway has native Docker Compose support with privileged containers.

### Setup

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   railway login
   ```

2. **Create Project**
   ```bash
   railway init
   # Follow prompts to create project
   ```

3. **Configure Environment**
   
   Set via Railway dashboard:
   ```
   LLM_PROVIDER=openai
   LLM_API_KEY=sk-...
   LLM_MODEL=gpt-4-turbo-preview
   DATABASE_URL=<provided by Railway Postgres plugin>
   ```

4. **Deploy**
   ```bash
   railway up
   ```

5. **Add Domain**
   ```bash
   railway domain
   ```

### Notes

- Railway auto-provisions PostgreSQL if detected in `docker-compose.yml`
- DinD works out of the box (privileged flag supported)
- Auto-scaling available on Pro plan
- Cost: ~$10-20/month for small workloads

---

## Option 2: Fly.io

Fly.io supports Docker Compose via `flyctl`.

### Setup

1. **Install flyctl**
   ```bash
   curl -L https://fly.io/install.sh | sh
   fly auth login
   ```

2. **Initialize App**
   ```bash
   fly launch
   # Choose "No" when asked to overwrite docker-compose.yml
   ```

3. **Configure fly.toml**
   
   Create `fly.toml`:
   ```toml
   app = "bug-ghost-ai"
   
   [build]
     dockerfile = "docker-compose.yml"
   
   [[services]]
     internal_port = 8000
     protocol = "tcp"
   
     [[services.ports]]
       handlers = ["http"]
       port = 80
     
     [[services.ports]]
       handlers = ["tls", "http"]
       port = 443
   
   [[services]]
     internal_port = 3000
     protocol = "tcp"
   
     [[services.ports]]
       handlers = ["http"]
       port = 80
   ```

4. **Set Secrets**
   ```bash
   fly secrets set LLM_API_KEY=sk-...
   fly secrets set LLM_PROVIDER=openai
   fly secrets set LLM_MODEL=gpt-4-turbo-preview
   ```

5. **Deploy**
   ```bash
   fly deploy
   ```

### Notes

- Fly.io provisions volumes for `dind-storage` automatically
- Supports privileged containers (needed for DinD)
- Free tier available (3GB RAM)
- Cost: ~$5-15/month for hobby projects

---

## Option 3: DigitalOcean App Platform

DigitalOcean supports Docker Compose deployments.

### Setup

1. **Push to GitHub**
   ```bash
   git remote add origin https://github.com/yourusername/bug-ghost-ai.git
   git push -u origin main
   ```

2. **Create App**
   - Go to DigitalOcean App Platform
   - Select "GitHub" source
   - Choose your repository
   - Detect `docker-compose.yml` automatically

3. **Configure Environment**
   
   Add in App Platform UI:
   ```
   LLM_PROVIDER=openai
   LLM_API_KEY=sk-...
   LLM_MODEL=gpt-4-turbo-preview
   ```

4. **Add Database Component**
   - Click "Add Component" → "Database"
   - Select PostgreSQL
   - Connect to backend service

5. **Deploy**
   - Click "Deploy"

### Notes

- Auto-provisions PostgreSQL database
- Supports Docker Compose (preview)
- Free static site tier + paid compute
- Cost: ~$12/month for basic setup

---

## Option 4: Self-Hosted VPS

Deploy to any VPS with Docker installed.

### Setup (Ubuntu/Debian)

1. **Install Docker**
   ```bash
   curl -fsSL https://get.docker.com | sh
   sudo usermod -aG docker $USER
   ```

2. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/bug-ghost-ai.git
   cd bug-ghost-ai
   ```

3. **Configure Environment**
   ```bash
   cp backend/.env.example backend/.env
   nano backend/.env  # Edit with your API key
   
   cp frontend/.env.example frontend/.env.local
   nano frontend/.env.local  # Set NEXT_PUBLIC_API_URL
   ```

4. **Build and Start**
   ```bash
   ./setup-sandbox.sh
   docker-compose up -d --build
   ```

5. **Setup Nginx (Optional)**
   
   `/etc/nginx/sites-available/bug-ghost-ai`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
   
       location / {
           proxy_pass http://localhost:3000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   
       location /api {
           proxy_pass http://localhost:8000;
           proxy_http_version 1.1;
           proxy_set_header Upgrade $http_upgrade;
           proxy_set_header Connection 'upgrade';
           proxy_set_header Host $host;
           proxy_cache_bypass $http_upgrade;
       }
   }
   ```

6. **Enable HTTPS with Certbot**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d your-domain.com
   ```

### Notes

- Full control over resources
- No platform limitations
- Requires manual SSL/backups
- Cost: ~$5-20/month (VPS pricing)

---

## Environment Variables

Required for all platforms:

```env
# Backend
DATABASE_URL=postgresql://user:pass@host:5432/db
LLM_PROVIDER=openai
LLM_API_KEY=sk-...
LLM_MODEL=gpt-4-turbo-preview
DOCKER_HOST=tcp://dind:2375

# Frontend
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

---

## Database Migrations

For production deployments:

1. **Use Alembic** (included in requirements)
   ```bash
   # Create migration
   alembic revision --autogenerate -m "Initial schema"
   
   # Apply migration
   alembic upgrade head
   ```

2. **Or let SQLAlchemy auto-create** (current approach)
   ```python
   # backend/app/main.py
   Base.metadata.create_all(bind=engine)
   ```

---

## Monitoring & Logs

### View Logs
```bash
# Railway
railway logs

# Fly.io
fly logs

# Docker Compose
docker-compose logs -f backend
docker-compose logs -f dind
```

### Health Checks
```bash
curl https://your-app.com/health
# Should return: {"status": "healthy"}
```

### DinD Monitoring
```bash
# Check containers created by sandbox
docker exec <dind-container> docker ps -a

# Check DinD disk usage
docker exec <dind-container> docker system df
```

---

## Security Checklist

Before going to production:

- [ ] Change default database password
- [ ] Restrict CORS origins to your frontend domain
- [ ] Enable rate limiting
- [ ] Add authentication (Phase 3)
- [ ] Set up database backups
- [ ] Enable HTTPS/TLS
- [ ] Monitor DinD resource usage
- [ ] Set up error tracking (Sentry)
- [ ] Review sandbox resource limits
- [ ] Consider gVisor for additional isolation

---

## Scaling Considerations

### Horizontal Scaling

- **Backend**: Stateless, can scale to multiple instances
- **DinD**: Each backend needs its own DinD instance
- **Database**: Use managed PostgreSQL (RDS, Supabase, Neon)

### Resource Limits

Per sandbox run:
- Memory: 256MB (configurable)
- CPU: ~50% of 1 core
- Timeout: 10-60 seconds

Estimate: 1 vCPU can handle ~5-10 concurrent sandbox executions.

---

## Cost Estimates

| Platform | Setup | Monthly |
|----------|-------|---------|
| Railway Hobby | $0 | $10-20 |
| Fly.io Free | $0 | $0-15 |
| DigitalOcean | $0 | $12-24 |
| VPS (Hetzner) | $0 | $5-10 |

Plus:
- Database: $0-10/month (managed services)
- LLM API: Pay-per-use (OpenAI/Anthropic)

---

## Troubleshooting

### "DinD not starting"

Check privileged flag is supported by platform. Some platforms (like Heroku) don't allow privileged containers.

### "Out of disk space"

DinD volume can fill up. Clean periodically:
```bash
docker exec <dind> docker system prune -af
```

### "Slow sandbox execution"

Increase resources allocated to DinD service or reduce concurrent requests.

---

## Support

- **Railway**: https://railway.app/help
- **Fly.io**: https://community.fly.io/
- **DigitalOcean**: https://www.digitalocean.com/support/

---

**Ready to deploy?** Choose your platform and follow the guide above! 🚀
