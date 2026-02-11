# Project Structure

```
AnalytIQ/
│
├── backend/                          # Python FastAPI Backend
│   ├── app/
│   │   ├── agents/                   # AI Analysis Agents
│   │   │   ├── cleaning_agent.py     # Data cleaning logic
│   │   │   ├── eda_agent.py          # Exploratory data analysis
│   │   │   ├── visualization_agent.py # Chart generation
│   │   │   ├── insight_agent.py      # LLM insights
│   │   │   └── orchestrator.py       # Agent coordinator
│   │   │
│   │   ├── api/                      # API Routes
│   │   │   ├── auth.py               # Authentication endpoints
│   │   │   ├── datasets.py           # Dataset endpoints
│   │   │   └── dependencies.py       # JWT dependency
│   │   │
│   │   ├── core/                     # Core Configuration
│   │   │   ├── config.py             # Settings management
│   │   │   ├── database.py           # MongoDB connection
│   │   │   └── security.py           # JWT & password hashing
│   │   │
│   │   ├── models/                   # Data Models
│   │   │   └── schemas.py            # Pydantic schemas
│   │   │
│   │   └── services/                 # Business Logic
│   │       ├── auth_service.py       # User authentication
│   │       └── dataset_service.py    # Dataset management
│   │
│   ├── uploads/                      # Uploaded CSV files (gitignored)
│   ├── main.py                       # FastAPI application entry
│   ├── requirements.txt              # Python dependencies
│   ├── .env.example                  # Environment template
│   └── .env                          # Environment variables (gitignored)
│
├── frontend/                         # React Frontend
│   ├── public/                       # Static assets
│   ├── src/
│   │   ├── components/               # Reusable Components
│   │   │   ├── Navbar.jsx            # Navigation bar
│   │   │   └── ProtectedRoute.jsx    # Route guard
│   │   │
│   │   ├── pages/                    # Page Components
│   │   │   ├── Home.jsx              # Landing page
│   │   │   ├── SignUp.jsx            # Registration page
│   │   │   ├── Login.jsx             # Login page
│   │   │   ├── Dashboard.jsx         # Dataset list
│   │   │   ├── Upload.jsx            # CSV upload
│   │   │   └── Analysis.jsx          # Results display
│   │   │
│   │   ├── services/                 # API Integration
│   │   │   └── api.js                # Axios configuration
│   │   │
│   │   ├── utils/                    # Utilities
│   │   │   └── AuthContext.jsx       # Auth state management
│   │   │
│   │   ├── App.jsx                   # Main app component
│   │   ├── main.jsx                  # React entry point
│   │   └── index.css                 # Global styles
│   │
│   ├── index.html                    # HTML template
│   ├── package.json                  # Node dependencies
│   ├── vite.config.js                # Vite configuration
│   ├── tailwind.config.js            # Tailwind configuration
│   └── postcss.config.js             # PostCSS configuration
│
├── docs/                             # Documentation (optional)
├── tests/                            # Test files (optional)
│
├── .gitignore                        # Git ignore rules
├── README.md                         # Project overview
├── API_DOCUMENTATION.md              # API reference
├── ARCHITECTURE.md                   # System architecture
├── DEPLOYMENT.md                     # Deployment guide
├── HUGGINGFACE_GUIDE.md             # LLM integration guide
├── sample_data.csv                   # Sample dataset
└── start.sh                          # Quick start script
```

## File Descriptions

### Backend Files

#### `main.py`
- FastAPI application initialization
- CORS middleware configuration
- Route registration
- Database connection lifecycle

#### `app/core/config.py`
- Environment variable management
- Application settings
- Pydantic Settings class

#### `app/core/database.py`
- MongoDB connection setup
- Async Motor client
- Database instance management

#### `app/core/security.py`
- JWT token generation and validation
- Password hashing with bcrypt
- Token decoding utilities

#### `app/models/schemas.py`
- Pydantic models for request/response
- Data validation schemas
- Type definitions

#### `app/api/auth.py`
- POST /auth/signup - User registration
- POST /auth/login - User authentication
- Returns JWT tokens

#### `app/api/datasets.py`
- POST /datasets/upload - CSV upload
- GET /datasets/analysis/{id} - Get results
- GET /datasets/list - List user datasets

#### `app/api/dependencies.py`
- JWT authentication dependency
- Current user extraction
- Token validation

#### `app/services/auth_service.py`
- User CRUD operations
- Password verification
- User authentication logic

#### `app/services/dataset_service.py`
- Dataset creation and storage
- Analysis orchestration
- Status management

#### `app/agents/cleaning_agent.py`
- Missing value imputation
- Duplicate removal
- Outlier detection
- Data type fixing

#### `app/agents/eda_agent.py`
- Summary statistics
- Correlation analysis
- Column-level analysis
- Data quality assessment

#### `app/agents/visualization_agent.py`
- Histogram generation
- Boxplot creation
- Correlation heatmaps
- Bar charts for categorical data

#### `app/agents/insight_agent.py`
- Hugging Face API integration
- Prompt engineering
- LLM insight generation
- Fallback insights

#### `app/agents/orchestrator.py`
- Coordinates all agents
- Manages analysis workflow
- Combines results
- Error handling

### Frontend Files

#### `src/main.jsx`
- React application entry point
- Root component rendering
- Global CSS import

#### `src/App.jsx`
- Main application component
- Router configuration
- Route definitions
- AuthProvider wrapper

#### `src/utils/AuthContext.jsx`
- Authentication state management
- Login/logout functions
- User persistence
- Context provider

#### `src/services/api.js`
- Axios instance configuration
- API base URL
- Request interceptors
- Auth token injection

#### `src/components/Navbar.jsx`
- Navigation bar
- User menu
- Conditional rendering based on auth

#### `src/components/ProtectedRoute.jsx`
- Route guard component
- Authentication check
- Redirect to login

#### `src/pages/Home.jsx`
- Landing page
- Feature showcase
- Call-to-action buttons

#### `src/pages/SignUp.jsx`
- User registration form
- Email/password input
- Form validation
- Error handling

#### `src/pages/Login.jsx`
- User login form
- Authentication
- Token storage
- Redirect to dashboard

#### `src/pages/Dashboard.jsx`
- Dataset list view
- Status indicators
- Upload button
- Navigation to analysis

#### `src/pages/Upload.jsx`
- CSV file upload interface
- Drag-and-drop support
- File validation
- Upload progress

#### `src/pages/Analysis.jsx`
- Analysis results display
- Data overview cards
- Cleaning report
- Interactive visualizations
- AI insights
- Plotly chart rendering

## Key Dependencies

### Backend
```
fastapi==0.109.0              # Web framework
uvicorn==0.27.0               # ASGI server
motor==3.3.2                  # Async MongoDB driver
pymongo==4.6.1                # MongoDB driver
pandas==2.1.4                 # Data manipulation
numpy==1.26.3                 # Numerical computing
plotly==5.18.0                # Visualizations
scikit-learn==1.4.0           # ML utilities
python-jose==3.3.0            # JWT handling
passlib==1.7.4                # Password hashing
requests==2.31.0              # HTTP client
```

### Frontend
```
react==18.2.0                 # UI framework
react-dom==18.2.0             # React DOM
react-router-dom==6.21.1      # Routing
axios==1.6.5                  # HTTP client
plotly.js==2.28.0             # Charts
react-plotly.js==2.6.0        # React Plotly wrapper
tailwindcss==3.4.1            # CSS framework
vite==5.0.11                  # Build tool
```

## Environment Variables

### Backend (.env)
```
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=analytiq_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
HUGGINGFACE_API_KEY=your-api-key
```

### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
```

## Build & Run Commands

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Quick Start
```bash
chmod +x start.sh
./start.sh
```

## Port Configuration

| Service | Port | URL |
|---------|------|-----|
| Frontend | 3000 | http://localhost:3000 |
| Backend | 8000 | http://localhost:8000 |
| MongoDB | 27017 | mongodb://localhost:27017 |
| API Docs | 8000 | http://localhost:8000/docs |

## Data Flow Summary

1. **User Registration**: Frontend → POST /auth/signup → MongoDB
2. **User Login**: Frontend → POST /auth/login → JWT Token
3. **CSV Upload**: Frontend → POST /datasets/upload → File System + MongoDB
4. **Analysis**: Background Task → Agents → MongoDB
5. **Results**: Frontend → GET /datasets/analysis/{id} → Display

## Code Organization Principles

1. **Separation of Concerns**: Clear separation between API, business logic, and data access
2. **Modularity**: Each agent is independent and reusable
3. **Dependency Injection**: FastAPI dependencies for auth
4. **Async/Await**: Async operations for database and I/O
5. **Type Hints**: Python type hints for better IDE support
6. **Component-Based**: React components for reusability
7. **Context API**: Centralized state management
8. **Protected Routes**: Security at the routing level

## Testing Structure (Future)

```
tests/
├── backend/
│   ├── test_auth.py
│   ├── test_datasets.py
│   ├── test_agents.py
│   └── test_integration.py
└── frontend/
    ├── components/
    ├── pages/
    └── integration/
```

## Logging Structure (Future)

```
logs/
├── app.log              # Application logs
├── error.log            # Error logs
├── access.log           # API access logs
└── analysis.log         # Analysis job logs
```

## CI/CD Pipeline (Future)

```
.github/workflows/
├── backend-tests.yml
├── frontend-tests.yml
├── deploy-staging.yml
└── deploy-production.yml
```
