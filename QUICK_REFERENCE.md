# AnalytIQ - Quick Reference Card

## 🚀 Quick Start Commands

### Start All Services
```bash
./start.sh
```

### Start Backend Only
```bash
cd backend
source venv/bin/activate
python main.py
```

### Start Frontend Only
```bash
cd frontend
npm run dev
```

### Start MongoDB
```bash
sudo systemctl start mongod
# or
mongod --dbpath /path/to/data
```

## 🌐 URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |
| MongoDB | mongodb://localhost:27017 |

## 📁 Key Files

### Backend
```
backend/
├── main.py                    # FastAPI app entry
├── app/agents/orchestrator.py # Main analysis coordinator
├── app/api/auth.py            # Auth endpoints
├── app/api/datasets.py        # Dataset endpoints
└── .env                       # Configuration
```

### Frontend
```
frontend/
├── src/App.jsx                # Main app component
├── src/pages/Analysis.jsx     # Results page
├── src/services/api.js        # API client
└── src/utils/AuthContext.jsx  # Auth state
```

## 🔑 API Endpoints

### Authentication
```
POST /auth/signup    # Create account
POST /auth/login     # Get JWT token
```

### Datasets (Requires Auth)
```
POST /datasets/upload           # Upload CSV
GET  /datasets/analysis/{id}    # Get results
GET  /datasets/list             # List datasets
```

## 🔐 Environment Variables

### Backend (.env)
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=analytiq_db
SECRET_KEY=<generate-with-secrets.token_urlsafe(32)>
HUGGINGFACE_API_KEY=<optional>
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

## 📦 Installation

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### Frontend
```bash
cd frontend
npm install
```

## 🧪 Test API with curl

### Sign Up
```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'
```

### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'
```

### Upload (replace TOKEN)
```bash
curl -X POST http://localhost:8000/datasets/upload \
  -H "Authorization: Bearer TOKEN" \
  -F "file=@sample_data.csv"
```

## 🗄️ MongoDB Commands

### Connect
```bash
mongosh
```

### View Data
```javascript
use analytiq_db
db.users.find().pretty()
db.datasets.find().pretty()
```

### Clear Data
```javascript
db.users.deleteMany({})
db.datasets.deleteMany({})
```

### Create Indexes
```javascript
db.users.createIndex({"email": 1}, {unique: true})
db.datasets.createIndex({"user_id": 1, "upload_date": -1})
```

## 🐛 Troubleshooting

### MongoDB Not Running
```bash
sudo systemctl start mongod
sudo systemctl status mongod
```

### Port Already in Use
```bash
# Find process
lsof -i :8000
# Kill process
kill -9 <PID>
```

### Clear Node Modules
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Reset Virtual Environment
```bash
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 🔧 Development Commands

### Backend Auto-Reload
```bash
uvicorn main:app --reload
```

### Frontend Build
```bash
npm run build
npm run preview
```

### Generate Secret Key
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### Check Python Version
```bash
python3 --version  # Need 3.9+
```

### Check Node Version
```bash
node --version     # Need 18+
npm --version
```

## 📊 Project Structure

```
AnalytIQ/
├── backend/           # FastAPI + Python
│   ├── app/
│   │   ├── agents/    # AI analysis agents
│   │   ├── api/       # API routes
│   │   ├── core/      # Config, DB, Security
│   │   ├── models/    # Pydantic schemas
│   │   └── services/  # Business logic
│   └── main.py
├── frontend/          # React + Tailwind
│   └── src/
│       ├── components/
│       ├── pages/
│       ├── services/
│       └── utils/
└── docs/             # Documentation
```

## 🎯 Common Tasks

### Add New User
1. Go to http://localhost:3000
2. Click "Sign Up"
3. Enter email and password
4. Click "Sign Up"

### Upload Dataset
1. Login
2. Click "Upload Dataset"
3. Select CSV file
4. Click "Upload & Analyze"

### View Results
1. Go to Dashboard
2. Click "View Analysis" on completed dataset
3. Scroll through results

### Test with Sample Data
Use `sample_data.csv` in project root

## 🔍 Debugging

### Backend Logs
Check terminal where `python main.py` is running

### Frontend Logs
Open browser DevTools (F12) → Console tab

### Database Logs
```bash
sudo journalctl -u mongod
```

### Check Services
```bash
# MongoDB
sudo systemctl status mongod

# Backend
curl http://localhost:8000

# Frontend
curl http://localhost:3000
```

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| README.md | Project overview |
| SETUP_GUIDE.md | Installation steps |
| API_DOCUMENTATION.md | API reference |
| ARCHITECTURE.md | System design |
| DEPLOYMENT.md | Production deployment |
| HUGGINGFACE_GUIDE.md | LLM integration |
| PROJECT_STRUCTURE.md | File organization |
| PROJECT_SUMMARY.md | Complete summary |

## 🎨 Tech Stack

**Backend:** FastAPI, MongoDB, Pandas, Plotly, scikit-learn, Hugging Face
**Frontend:** React, Tailwind CSS, Axios, Plotly.js, React Router
**Auth:** JWT, bcrypt
**Database:** MongoDB (Motor async driver)

## ⚡ Performance Tips

1. Use production build for frontend: `npm run build`
2. Use Gunicorn for backend: `gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker`
3. Create database indexes
4. Enable compression
5. Use CDN for static assets

## 🔒 Security Checklist

- [ ] Change SECRET_KEY in production
- [ ] Use HTTPS in production
- [ ] Configure CORS properly
- [ ] Set strong passwords
- [ ] Keep dependencies updated
- [ ] Enable rate limiting
- [ ] Use environment variables
- [ ] Never commit .env files

## 🚀 Deployment Quick Steps

1. Setup MongoDB Atlas
2. Deploy backend to Railway/Render
3. Deploy frontend to Vercel/Netlify
4. Update CORS settings
5. Update API URL in frontend
6. Test end-to-end

## 📞 Getting Help

1. Check SETUP_GUIDE.md for installation issues
2. Check API_DOCUMENTATION.md for API questions
3. Check browser console for frontend errors
4. Check terminal for backend errors
5. Verify all services are running
6. Test with sample_data.csv

## ✅ Success Indicators

- [ ] Can access http://localhost:3000
- [ ] Can create account
- [ ] Can login
- [ ] Can upload CSV
- [ ] Can see analysis results
- [ ] Visualizations render
- [ ] AI insights display

## 🎉 You're Ready!

All systems operational. Start building! 🚀

---

**Quick Help:**
- Stuck? Check SETUP_GUIDE.md
- API questions? Check API_DOCUMENTATION.md
- Architecture? Check ARCHITECTURE.md
- Deployment? Check DEPLOYMENT.md
