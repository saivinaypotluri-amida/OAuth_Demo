# Deployment Guide

This guide covers deploying the Agentic AI Slack Bot to production environments.

## Production Checklist

Before deploying to production:

- [ ] Update all secret keys in `.env`
- [ ] Configure production database (consider PostgreSQL)
- [ ] Set up HTTPS/SSL certificates
- [ ] Configure CORS for production domains
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy
- [ ] Review security settings
- [ ] Test all integrations
- [ ] Set up error tracking (e.g., Sentry)
- [ ] Configure rate limiting

## Environment Configuration

### Backend (.env)

```bash
# Production settings
APP_ENV=production
SECRET_KEY=<generate-strong-random-key>
JWT_SECRET_KEY=<generate-strong-random-key>

# Database (use PostgreSQL in production)
DATABASE_URL=postgresql://user:password@localhost/dbname

# CORS - Add your production domains
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Service credentials
SLACK_BOT_TOKEN=xoxb-your-production-token
SLACK_SIGNING_SECRET=your-production-secret
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-production-key
AZURE_OPENAI_DEPLOYMENT=your-deployment
GOOGLE_CLIENT_ID=your-production-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-production-client-secret
GOOGLE_REDIRECT_URI=https://yourdomain.com/api/oauth/google/callback
```

### Generate Secure Keys

```bash
# Generate secret keys
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Deployment Options

### Option 1: Docker Deployment

#### Create Dockerfile (Backend)

```dockerfile
# backend/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Create Dockerfile (Frontend)

```dockerfile
# frontend/Dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://postgres:password@db:5432/slack_bot
    depends_on:
      - db
    volumes:
      - ./backend:/app
    restart: unless-stopped

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: slack_bot
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

#### Deploy with Docker

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Option 2: Traditional Server Deployment

#### Backend (Ubuntu/Debian)

```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv nginx

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install supervisor for process management
sudo apt install supervisor

# Create supervisor config
sudo nano /etc/supervisor/conf.d/slack-bot-backend.conf
```

Supervisor config:
```ini
[program:slack-bot-backend]
directory=/var/www/slack-bot/backend
command=/var/www/slack-bot/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/slack-bot-backend.log
```

```bash
# Start service
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start slack-bot-backend
```

#### Frontend (Build and Serve)

```bash
# Build frontend
cd frontend
npm install
npm run build

# Serve with Nginx
sudo cp -r dist/* /var/www/html/

# Configure Nginx
sudo nano /etc/nginx/sites-available/slack-bot
```

Nginx config:
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Frontend
    location / {
        root /var/www/html;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/slack-bot /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Option 3: Cloud Platform Deployment

#### AWS (Elastic Beanstalk)

```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.11 slack-bot

# Create environment
eb create slack-bot-env

# Deploy
eb deploy

# Open in browser
eb open
```

#### Heroku

```bash
# Create Procfile
echo "web: cd backend && uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy
heroku create slack-bot-app
git push heroku main

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DATABASE_URL=your-database-url
```

#### Google Cloud Platform (App Engine)

Create `app.yaml`:
```yaml
runtime: python311
entrypoint: uvicorn main:app --host 0.0.0.0 --port $PORT

env_variables:
  SECRET_KEY: "your-secret-key"
  DATABASE_URL: "your-database-url"

automatic_scaling:
  target_cpu_utilization: 0.65
  min_instances: 1
  max_instances: 10
```

Deploy:
```bash
gcloud app deploy
```

## Database Migration

### From SQLite to PostgreSQL

1. Install PostgreSQL:
```bash
sudo apt install postgresql postgresql-contrib
```

2. Create database:
```bash
sudo -u postgres psql
CREATE DATABASE slack_bot;
CREATE USER slack_bot_user WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE slack_bot TO slack_bot_user;
\q
```

3. Update DATABASE_URL in .env:
```bash
DATABASE_URL=postgresql://slack_bot_user:password@localhost/slack_bot
```

4. Run migrations:
```bash
cd backend
python -c "from database import init_db; init_db()"
```

## SSL/HTTPS Setup

### Using Let's Encrypt (Certbot)

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is set up automatically
# Test renewal
sudo certbot renew --dry-run
```

## Monitoring & Logging

### Application Logging

Update `backend/main.py`:
```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
handler = RotatingFileHandler(
    'logs/app.log',
    maxBytes=10000000,
    backupCount=5
)
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))
logger = logging.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)
```

### Health Check Endpoint

Already implemented at `/health`

### Monitoring Tools

- **Prometheus + Grafana**: Metrics and visualization
- **Sentry**: Error tracking
- **New Relic**: Application performance monitoring
- **Datadog**: Infrastructure monitoring

## Backup Strategy

### Database Backup

```bash
# PostgreSQL backup script
#!/bin/bash
BACKUP_DIR="/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
pg_dump slack_bot > $BACKUP_DIR/slack_bot_$TIMESTAMP.sql
# Keep only last 7 days
find $BACKUP_DIR -name "slack_bot_*.sql" -mtime +7 -delete
```

Add to crontab:
```bash
# Daily backup at 2 AM
0 2 * * * /path/to/backup.sh
```

## Security Best Practices

1. **Keep dependencies updated**:
```bash
pip list --outdated
npm outdated
```

2. **Use environment variables**: Never hardcode secrets

3. **Enable rate limiting**: Implement API rate limiting

4. **Use HTTPS**: Always use SSL in production

5. **Regular security audits**:
```bash
# Python
pip install safety
safety check

# Node.js
npm audit
```

6. **Database security**:
   - Use strong passwords
   - Restrict database access
   - Enable SSL connections
   - Regular backups

7. **API key rotation**: Rotate keys regularly

8. **Access control**: Implement proper authentication and authorization

## Performance Optimization

1. **Enable compression** in Nginx:
```nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
```

2. **Use caching** for static assets

3. **Database indexing**: Add indexes to frequently queried columns

4. **Connection pooling**: Configure SQLAlchemy connection pool

5. **CDN**: Use CDN for static assets

## Scaling

### Horizontal Scaling

- Use load balancer (nginx, HAProxy, or cloud load balancer)
- Deploy multiple backend instances
- Use shared session storage (Redis)
- Use centralized database

### Vertical Scaling

- Increase server resources (CPU, RAM)
- Optimize database queries
- Use caching (Redis, Memcached)

## Troubleshooting Production Issues

### Check Logs

```bash
# Backend logs
tail -f /var/log/slack-bot-backend.log

# Nginx logs
tail -f /var/log/nginx/error.log

# System logs
journalctl -u slack-bot-backend -f
```

### Common Issues

1. **502 Bad Gateway**: Backend not running or wrong port
2. **Database connection errors**: Check DATABASE_URL and credentials
3. **CORS errors**: Update ALLOWED_ORIGINS
4. **OAuth redirect errors**: Verify redirect URI in Google Console

## Rollback Strategy

```bash
# Docker
docker-compose down
git checkout <previous-commit>
docker-compose up -d

# Traditional
sudo supervisorctl stop slack-bot-backend
git checkout <previous-commit>
source venv/bin/activate
pip install -r requirements.txt
sudo supervisorctl start slack-bot-backend
```

## Support

For production deployment support:
1. Review logs for errors
2. Check service status
3. Verify environment variables
4. Test integrations
5. Contact cloud provider support if needed
