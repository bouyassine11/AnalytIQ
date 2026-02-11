# Complete Setup Guide

## Prerequisites Installation

### 1. Install Python 3.9+

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
```

**macOS:**
```bash
brew install python@3.11
python3 --version
```

**Windows:**
Download from https://www.python.org/downloads/

### 2. Install Node.js 18+

**Ubuntu/Debian:**
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
node --version
npm --version
```

**macOS:**
```bash
brew install node@18
node --version
npm --version
```

**Windows:**
Download from https://nodejs.org/

### 3. Install MongoDB

**Ubuntu/Debian:**
```bash
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt update
sudo apt install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

**macOS:**
```bash
brew tap mongodb/brew
brew install mongodb-community@7.0
brew services start mongodb-community@7.0
```

**Windows:**
Download from https://www.mongodb.com/try/download/community

Verify MongoDB:
```bash
mongosh
# Should connect to MongoDB shell
```

## Project Setup

### Step 1: Clone or Download Project

```bash
cd ~/Documents
# If using git:
git clone <repository-url> AnalytIQ
# Or create the directory if building from scratch
cd AnalytIQ
```

### Step 2: Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env file with your settings
nano .env  # or use your preferred editor
```

**Configure .env:**
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=analytiq_db
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
HUGGINGFACE_API_KEY=your-huggingface-api-key-optional
```

**Generate Secret Key:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Step 3: Get Hugging Face API Key (Optional)

1. Go to https://huggingface.co/
2. Create free account
3. Go to Settings → Access Tokens
4. Create new token with "Read" permission
5. Copy token to .env file

**Note:** If you skip this, the system will use fallback insights.

### Step 4: Test Backend

```bash
# Make sure you're in backend/ directory with venv activated
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

Test in browser: http://localhost:8000
You should see: `{"message": "AnalytIQ API is running"}`

API Documentation: http://localhost:8000/docs

**Stop the server:** Press `Ctrl+C`

### Step 5: Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

You should see:
```
  VITE v5.0.11  ready in 500 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

Open browser: http://localhost:3000

### Step 6: Verify Everything Works

1. **Check MongoDB:**
```bash
mongosh
> show dbs
> use analytiq_db
> show collections
> exit
```

2. **Check Backend:**
- Visit http://localhost:8000/docs
- You should see Swagger UI with all endpoints

3. **Check Frontend:**
- Visit http://localhost:3000
- You should see the AnalytIQ landing page

## Quick Start (All Services)

### Option 1: Using Start Script

```bash
# Make script executable (first time only)
chmod +x start.sh

# Run script
./start.sh
```

This will:
- Check MongoDB is running
- Setup backend virtual environment
- Install dependencies
- Start backend on port 8000
- Start frontend on port 3000

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Terminal 3 - MongoDB (if not running as service):**
```bash
mongod --dbpath /path/to/data
```

## First Time Usage

### 1. Create Account

1. Go to http://localhost:3000
2. Click "Sign Up"
3. Enter email and password (min 6 characters)
4. Click "Sign Up"
5. You'll be redirected to login

### 2. Login

1. Enter your email and password
2. Click "Login"
3. You'll be redirected to Dashboard

### 3. Upload CSV

1. Click "Upload Dataset" or go to Upload page
2. Drag and drop a CSV file or click to browse
3. Click "Upload & Analyze"
4. You'll be redirected to analysis page

### 4. View Results

- Analysis runs in background (usually 5-30 seconds)
- Page auto-refreshes every 3 seconds
- Once complete, you'll see:
  - Data overview
  - Cleaning report
  - AI insights
  - Interactive visualizations

### 5. Test with Sample Data

Use the included `sample_data.csv`:
```bash
# From project root
cat sample_data.csv
```

This file has:
- 20 rows
- 7 columns
- 1 missing value (for testing cleaning)
- Mix of numeric and categorical data

## Troubleshooting

### MongoDB Connection Error

**Error:** `ServerSelectionTimeoutError`

**Solution:**
```bash
# Check if MongoDB is running
sudo systemctl status mongod

# Start MongoDB
sudo systemctl start mongod

# Or on macOS:
brew services start mongodb-community
```

### Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000
# Kill the process
kill -9 <PID>

# Or use different port
uvicorn main:app --port 8001
```

### Python Module Not Found

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Build Errors

**Error:** `Cannot find module 'react'`

**Solution:**
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### CORS Errors

**Error:** `Access to XMLHttpRequest blocked by CORS policy`

**Solution:**
Check backend CORS configuration in `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Hugging Face API Errors

**Error:** `401 Unauthorized` or `503 Service Unavailable`

**Solution:**
- Check API key in .env
- Verify key has "Read" permission
- System will use fallback insights if API fails

### File Upload Errors

**Error:** `Only CSV files are allowed`

**Solution:**
- Ensure file has .csv extension
- Check file is valid CSV format
- Try opening in Excel/LibreOffice first

### Analysis Stuck in "Processing"

**Solution:**
1. Check backend logs for errors
2. Verify CSV file is valid
3. Check MongoDB connection
4. Restart backend server

## Development Tips

### Backend Development

**Auto-reload on changes:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**View logs:**
```bash
# Add to main.py
import logging
logging.basicConfig(level=logging.INFO)
```

**Test API with curl:**
```bash
# Sign up
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'
```

### Frontend Development

**Clear browser cache:**
- Chrome: Ctrl+Shift+Delete
- Firefox: Ctrl+Shift+Delete

**React DevTools:**
Install React Developer Tools browser extension

**Check console:**
Open browser DevTools (F12) and check Console tab for errors

### Database Management

**View data:**
```bash
mongosh
> use analytiq_db
> db.users.find().pretty()
> db.datasets.find().pretty()
```

**Clear data:**
```bash
mongosh
> use analytiq_db
> db.users.deleteMany({})
> db.datasets.deleteMany({})
```

**Backup database:**
```bash
mongodump --db analytiq_db --out backup/
```

**Restore database:**
```bash
mongorestore --db analytiq_db backup/analytiq_db/
```

## Performance Optimization

### Backend

1. **Use production ASGI server:**
```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

2. **Enable compression:**
```python
from fastapi.middleware.gzip import GZipMiddleware
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### Frontend

1. **Build for production:**
```bash
npm run build
```

2. **Preview production build:**
```bash
npm run preview
```

### Database

1. **Create indexes:**
```bash
mongosh
> use analytiq_db
> db.users.createIndex({"email": 1}, {unique: true})
> db.datasets.createIndex({"user_id": 1, "upload_date": -1})
```

## Next Steps

1. ✅ Complete setup and test with sample data
2. 📚 Read API_DOCUMENTATION.md for API details
3. 🏗️ Read ARCHITECTURE.md to understand system design
4. 🚀 Read DEPLOYMENT.md for production deployment
5. 🤖 Read HUGGINGFACE_GUIDE.md for LLM customization
6. 💻 Start building your own features!

## Getting Help

- Check documentation files in project root
- Review code comments
- Check browser console for frontend errors
- Check terminal for backend errors
- Verify all services are running
- Test with sample_data.csv first

## Common Workflows

### Adding New User
```bash
# Via API
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"newuser@example.com","password":"password123"}'
```

### Uploading Dataset
```bash
# Get token first (from login response)
TOKEN="your-jwt-token"

# Upload CSV
curl -X POST http://localhost:8000/datasets/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@sample_data.csv"
```

### Checking Analysis Status
```bash
# Get dataset ID from upload response
DATASET_ID="your-dataset-id"

curl -X GET http://localhost:8000/datasets/analysis/$DATASET_ID \
  -H "Authorization: Bearer $TOKEN"
```

## Success Checklist

- [ ] MongoDB running and accessible
- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] Can access http://localhost:3000
- [ ] Can create account
- [ ] Can login
- [ ] Can upload CSV
- [ ] Can view analysis results
- [ ] Visualizations render correctly
- [ ] AI insights display

Congratulations! Your AnalytIQ platform is ready! 🎉
