# AnalytIQ - AI-Powered Data Analysis Platform

A complete full-stack application that provides automated data analysis, cleaning, visualization, and AI-generated insights for CSV files.

## 🚀 Features

- **User Authentication**: JWT-based secure authentication with bcrypt password hashing
- **CSV Upload**: Drag-and-drop file upload interface
- **Automated Data Cleaning**: 
  - Missing value imputation (median for numeric, mode for categorical)
  - Duplicate removal
  - Outlier detection using IQR method
- **Exploratory Data Analysis (EDA)**:
  - Summary statistics
  - Correlation analysis
  - Column-level analysis
  - Data quality assessment
- **Interactive Visualizations**:
  - Histograms
  - Boxplots
  - Correlation heatmaps
  - Bar charts
- **AI-Powered Insights**: LLM-generated business insights using Hugging Face API
- **Real-time Processing**: Background task processing with status updates

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **MongoDB**: NoSQL database with Motor (async driver)
- **Pandas & NumPy**: Data manipulation
- **Plotly**: Interactive visualizations
- **scikit-learn**: Statistical analysis
- **Hugging Face API**: LLM insights generation
- **JWT**: Authentication

### Frontend
- **React.js**: UI framework
- **Tailwind CSS**: Styling
- **React Router**: Navigation
- **Axios**: HTTP client
- **Plotly.js**: Chart rendering

## 📋 Prerequisites

- Python 3.9+
- Node.js 18+
- MongoDB 4.4+
- Hugging Face API key (optional, fallback insights provided)

## 🔧 Installation

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
```

5. Configure `.env`:
```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=analytiq_db
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
HUGGINGFACE_API_KEY=your-huggingface-api-key-optional
```

6. Start MongoDB:
```bash
mongod
```

7. Run the backend:
```bash
python main.py
```

Backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm run dev
```

Frontend will run on `http://localhost:3000`

## 📊 API Endpoints

### Authentication
- `POST /auth/signup` - Create new user account
- `POST /auth/login` - Login and receive JWT token

### Datasets
- `POST /datasets/upload` - Upload CSV file (requires auth)
- `GET /datasets/analysis/{dataset_id}` - Get analysis results (requires auth)
- `GET /datasets/list` - List all user datasets (requires auth)

## 🎯 Usage Flow

1. **Sign Up**: Create an account with email and password
2. **Login**: Authenticate and receive JWT token
3. **Upload CSV**: Upload your dataset file
4. **Processing**: System automatically:
   - Cleans the data
   - Performs EDA
   - Generates visualizations
   - Creates AI insights
5. **View Results**: Interactive dashboard with:
   - Data overview
   - Cleaning report
   - Statistical analysis
   - Interactive charts
   - AI-generated insights

## 🤖 AI Agent Architecture

### Orchestrator Agent
Coordinates all analysis agents and manages the workflow.

### Data Cleaning Agent
- Detects and handles missing values
- Removes duplicates
- Identifies outliers
- Fixes data types

### EDA Agent
- Generates summary statistics
- Calculates correlations
- Analyzes column distributions
- Assesses data quality

### Visualization Agent
- Creates histograms for numeric columns
- Generates boxplots for outlier visualization
- Builds correlation heatmaps
- Creates bar charts for categorical data

### Insight Agent
- Integrates with Hugging Face LLM
- Generates business-focused insights
- Provides actionable recommendations
- Fallback to rule-based insights if API unavailable

## 🗄️ Database Schema

### Users Collection
```javascript
{
  _id: ObjectId,
  email: String,
  hashed_password: String,
  created_at: DateTime
}
```

### Datasets Collection
```javascript
{
  _id: ObjectId,
  user_id: String,
  filename: String,
  file_path: String,
  upload_date: DateTime,
  status: String, // "processing", "completed", "failed"
  analysis_result: {
    cleaning_report: Object,
    eda_results: Object,
    visualizations: Array,
    ai_insights: String
  }
}
```

## 🔐 Security Features

- Password hashing with bcrypt
- JWT token authentication
- Protected API routes
- CORS configuration
- Input validation

## 🚀 Production Deployment

### Backend
1. Set strong SECRET_KEY in production
2. Use production MongoDB instance
3. Configure proper CORS origins
4. Use environment variables
5. Deploy with Gunicorn/Uvicorn

### Frontend
1. Build production bundle: `npm run build`
2. Deploy to Vercel/Netlify/AWS
3. Update API base URL

## 📝 Example API Calls

### Sign Up
```bash
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### Upload CSV
```bash
curl -X POST http://localhost:8000/datasets/upload \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@data.csv"
```

### Get Analysis
```bash
curl -X GET http://localhost:8000/datasets/analysis/DATASET_ID \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## 🎨 Frontend Components

- **Navbar**: Navigation with authentication state
- **ProtectedRoute**: Route guard for authenticated pages
- **Home**: Landing page
- **SignUp/Login**: Authentication forms
- **Dashboard**: Dataset list view
- **Upload**: CSV upload interface
- **Analysis**: Results visualization page

## 🧪 Testing

Upload sample CSV files with:
- Numeric columns
- Categorical columns
- Missing values
- Duplicates
- Various data types

## 📈 Future Enhancements

- Export analysis reports (PDF/Excel)
- Advanced ML model training
- Time-series forecasting
- Collaborative features
- Dataset versioning
- Custom visualization builder
- Scheduled analysis
- Email notifications

## 🤝 Contributing

This is a portfolio project demonstrating full-stack AI development capabilities.

## 📄 License

MIT License

## 👨‍💻 Author

Built with ❤️ as a demonstration of modern full-stack AI engineering.
