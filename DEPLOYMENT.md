# Deployment Guide

## Production Deployment Checklist

### Backend Deployment

#### 1. Environment Configuration

Create production `.env` file:
```env
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=analytiq_production
SECRET_KEY=<generate-strong-random-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
HUGGINGFACE_API_KEY=<your-api-key>
```

Generate strong secret key:
```python
import secrets
print(secrets.token_urlsafe(32))
```

#### 2. MongoDB Atlas Setup

1. Create MongoDB Atlas account
2. Create new cluster
3. Configure network access (whitelist IPs)
4. Create database user
5. Get connection string
6. Update MONGODB_URL in .env

#### 3. Deploy to Railway/Render/AWS

**Railway:**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Deploy
railway up
```

**Render:**
1. Connect GitHub repository
2. Select "Web Service"
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables

**AWS EC2:**
```bash
# SSH into EC2 instance
ssh -i key.pem ubuntu@ec2-instance

# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv nginx

# Clone repository
git clone <repo-url>
cd AnalytIQ/backend

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Install Gunicorn
pip install gunicorn

# Run with Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### 4. Nginx Configuration (for EC2)

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

#### 5. SSL Certificate (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d api.yourdomain.com
```

#### 6. Process Manager (PM2 or Systemd)

**Using PM2:**
```bash
npm install -g pm2
pm2 start "gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000" --name analytiq-api
pm2 save
pm2 startup
```

**Using Systemd:**
```ini
# /etc/systemd/system/analytiq.service
[Unit]
Description=AnalytIQ API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/AnalytIQ/backend
Environment="PATH=/home/ubuntu/AnalytIQ/backend/venv/bin"
ExecStart=/home/ubuntu/AnalytIQ/backend/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable analytiq
sudo systemctl start analytiq
```

---

### Frontend Deployment

#### 1. Update API URL

Create `.env.production`:
```env
VITE_API_URL=https://api.yourdomain.com
```

Update `src/services/api.js`:
```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
```

#### 2. Build Production Bundle

```bash
cd frontend
npm run build
```

#### 3. Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod
```

Or connect GitHub repository in Vercel dashboard.

#### 4. Deploy to Netlify

```bash
# Install Netlify CLI
npm i -g netlify-cli

# Deploy
netlify deploy --prod --dir=dist
```

Or drag-and-drop `dist` folder to Netlify dashboard.

#### 5. Deploy to AWS S3 + CloudFront

```bash
# Build
npm run build

# Upload to S3
aws s3 sync dist/ s3://your-bucket-name --delete

# Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

#### 6. Configure CORS

Update backend CORS settings with production frontend URL:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://www.yourdomain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Docker Deployment

### Backend Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile

```dockerfile
FROM node:18-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  mongodb:
    image: mongo:7
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password

  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URL=mongodb://admin:password@mongodb:27017
      - DATABASE_NAME=analytiq_db
      - SECRET_KEY=${SECRET_KEY}
      - HUGGINGFACE_API_KEY=${HUGGINGFACE_API_KEY}
    depends_on:
      - mongodb
    volumes:
      - ./backend/uploads:/app/uploads

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  mongo_data:
```

Run with:
```bash
docker-compose up -d
```

---

## Monitoring & Logging

### 1. Application Monitoring

**Sentry Integration:**
```bash
pip install sentry-sdk[fastapi]
```

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FastApiIntegration()],
)
```

### 2. Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### 3. Health Check Endpoint

```python
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow()}
```

---

## Performance Optimization

1. **Database Indexing:**
```python
# Create indexes
await db.users.create_index("email", unique=True)
await db.datasets.create_index([("user_id", 1), ("upload_date", -1)])
```

2. **Caching:** Implement Redis for frequently accessed data

3. **CDN:** Use CloudFront/Cloudflare for static assets

4. **Compression:** Enable gzip compression

5. **Connection Pooling:** Configure MongoDB connection pool

---

## Security Hardening

1. **Rate Limiting:**
```bash
pip install slowapi
```

2. **HTTPS Only:** Enforce SSL/TLS

3. **Security Headers:** Add helmet middleware

4. **Input Validation:** Validate all user inputs

5. **File Upload Limits:** Restrict file size and type

6. **Environment Variables:** Never commit secrets

---

## Backup Strategy

1. **MongoDB Backups:**
```bash
mongodump --uri="mongodb+srv://..." --out=/backup/$(date +%Y%m%d)
```

2. **Automated Backups:** Use MongoDB Atlas automated backups

3. **File Storage:** Backup uploaded files to S3

---

## Scaling Considerations

1. **Horizontal Scaling:** Deploy multiple backend instances behind load balancer

2. **Database Sharding:** Implement MongoDB sharding for large datasets

3. **Queue System:** Use Celery + Redis for background tasks

4. **Microservices:** Split analysis agents into separate services

5. **Caching Layer:** Implement Redis for session management

---

## Cost Optimization

1. **MongoDB Atlas:** Start with M0 (free tier)
2. **Backend:** Railway/Render free tier or AWS t2.micro
3. **Frontend:** Vercel/Netlify free tier
4. **Hugging Face:** Use free tier (rate limited)

---

## Maintenance

1. **Regular Updates:** Keep dependencies updated
2. **Security Patches:** Monitor CVEs
3. **Database Cleanup:** Archive old datasets
4. **Log Rotation:** Implement log rotation
5. **Monitoring:** Set up alerts for errors/downtime
