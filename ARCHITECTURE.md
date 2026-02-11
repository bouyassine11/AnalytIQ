# System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              React Frontend (Port 3000)                   │  │
│  │  • Authentication UI    • Dashboard                       │  │
│  │  • File Upload          • Visualization Display           │  │
│  │  • Protected Routes     • Real-time Status Updates        │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓ HTTP/REST
┌─────────────────────────────────────────────────────────────────┐
│                         API LAYER                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              FastAPI Backend (Port 8000)                  │  │
│  │  ┌────────────────┐  ┌────────────────┐                  │  │
│  │  │  Auth Routes   │  │ Dataset Routes │                  │  │
│  │  │  /auth/signup  │  │ /datasets/*    │                  │  │
│  │  │  /auth/login   │  │                │                  │  │
│  │  └────────────────┘  └────────────────┘                  │  │
│  │           ↓                    ↓                          │  │
│  │  ┌────────────────────────────────────────┐              │  │
│  │  │      JWT Authentication Middleware      │              │  │
│  │  └────────────────────────────────────────┘              │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      SERVICE LAYER                               │
│  ┌──────────────────┐         ┌──────────────────┐             │
│  │  Auth Service    │         │  Dataset Service │             │
│  │  • User CRUD     │         │  • File Upload   │             │
│  │  • Password Hash │         │  • Metadata Mgmt │             │
│  │  • Token Gen     │         │  • Status Track  │             │
│  └──────────────────┘         └──────────────────┘             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    AI AGENT LAYER                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Orchestrator Agent                           │  │
│  │  Coordinates all analysis agents and manages workflow    │  │
│  └──────────────────────────────────────────────────────────┘  │
│         ↓              ↓              ↓              ↓          │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐   │
│  │ Cleaning │   │   EDA    │   │   Viz    │   │ Insight  │   │
│  │  Agent   │   │  Agent   │   │  Agent   │   │  Agent   │   │
│  │          │   │          │   │          │   │          │   │
│  │ • Fill   │   │ • Stats  │   │ • Plots  │   │ • LLM    │   │
│  │   Missing│   │ • Corr   │   │ • Charts │   │ • HF API │   │
│  │ • Remove │   │ • Quality│   │ • Heatmap│   │ • Fallbk │   │
│  │   Dups   │   │ • Column │   │ • JSON   │   │          │   │
│  │ • Outlier│   │   Analysis│   │          │   │          │   │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                    │
│  ┌──────────────────┐         ┌──────────────────┐             │
│  │    MongoDB       │         │  File System     │             │
│  │  • users         │         │  • uploads/      │             │
│  │  • datasets      │         │  • CSV files     │             │
│  │  • analysis      │         │                  │             │
│  └──────────────────┘         └──────────────────┘             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                  EXTERNAL SERVICES                               │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │         Hugging Face Inference API                        │  │
│  │         Model: mistralai/Mistral-7B-Instruct-v0.2        │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. User Registration Flow
```
User → SignUp Form → POST /auth/signup → Auth Service
                                        ↓
                                   Hash Password
                                        ↓
                                   MongoDB (users)
                                        ↓
                                   Success Response
```

### 2. Authentication Flow
```
User → Login Form → POST /auth/login → Auth Service
                                      ↓
                                 Verify Password
                                      ↓
                                 Generate JWT
                                      ↓
                                 Return Token
                                      ↓
                            Store in localStorage
```

### 3. CSV Upload & Analysis Flow
```
User → Upload CSV → POST /datasets/upload → Dataset Service
                                           ↓
                                    Save File to Disk
                                           ↓
                                    Create Dataset Doc
                                           ↓
                                    MongoDB (datasets)
                                           ↓
                                    Background Task
                                           ↓
                                    Orchestrator Agent
                                           ↓
                    ┌──────────────────────┼──────────────────────┐
                    ↓                      ↓                      ↓
            Cleaning Agent            EDA Agent              Viz Agent
                    ↓                      ↓                      ↓
            Clean DataFrame        Generate Stats         Create Plots
                    ↓                      ↓                      ↓
                    └──────────────────────┼──────────────────────┘
                                           ↓
                                    Insight Agent
                                           ↓
                                    Hugging Face API
                                           ↓
                                    Generate Insights
                                           ↓
                                    Combine Results
                                           ↓
                                    Update MongoDB
                                           ↓
                                    Status: "completed"
```

### 4. Results Retrieval Flow
```
User → View Analysis → GET /datasets/analysis/{id} → Dataset Service
                                                    ↓
                                              MongoDB Query
                                                    ↓
                                              Return Results
                                                    ↓
                                              Frontend Display
                                                    ↓
                                    ┌───────────────┼───────────────┐
                                    ↓               ↓               ↓
                            Overview Stats    Visualizations    AI Insights
```

## Component Interactions

### Backend Components

```
main.py (FastAPI App)
    ├── Middleware (CORS, Auth)
    ├── Routes
    │   ├── auth.py
    │   │   └── AuthService
    │   └── datasets.py
    │       └── DatasetService
    │           └── OrchestratorAgent
    │               ├── CleaningAgent
    │               ├── EDAAgent
    │               ├── VisualizationAgent
    │               └── InsightAgent
    └── Database (MongoDB)
```

### Frontend Components

```
App.jsx
    ├── AuthProvider (Context)
    ├── Router
    │   ├── Public Routes
    │   │   ├── Home
    │   │   ├── SignUp
    │   │   └── Login
    │   └── Protected Routes
    │       ├── Dashboard
    │       ├── Upload
    │       └── Analysis
    └── Navbar
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Layers                           │
├─────────────────────────────────────────────────────────────┤
│  1. Transport Layer                                          │
│     • HTTPS/TLS encryption                                   │
│     • Secure headers                                         │
├─────────────────────────────────────────────────────────────┤
│  2. Authentication Layer                                     │
│     • JWT tokens (HS256)                                     │
│     • Token expiration (24h)                                 │
│     • HTTPBearer scheme                                      │
├─────────────────────────────────────────────────────────────┤
│  3. Authorization Layer                                      │
│     • User-specific data access                              │
│     • Protected routes                                       │
│     • Dependency injection                                   │
├─────────────────────────────────────────────────────────────┤
│  4. Data Layer                                               │
│     • Password hashing (bcrypt)                              │
│     • Input validation                                       │
│     • File type validation                                   │
├─────────────────────────────────────────────────────────────┤
│  5. Application Layer                                        │
│     • CORS configuration                                     │
│     • Rate limiting (future)                                 │
│     • Error handling                                         │
└─────────────────────────────────────────────────────────────┘
```

## Database Schema

### Users Collection
```javascript
{
  _id: ObjectId("507f1f77bcf86cd799439011"),
  email: "user@example.com",
  hashed_password: "$2b$12$...",
  created_at: ISODate("2024-01-15T10:30:00Z")
}
```

### Datasets Collection
```javascript
{
  _id: ObjectId("507f1f77bcf86cd799439012"),
  user_id: "507f1f77bcf86cd799439011",
  filename: "sales_data.csv",
  file_path: "/uploads/507f1f77bcf86cd799439013_sales_data.csv",
  upload_date: ISODate("2024-01-15T10:30:00Z"),
  status: "completed",
  analysis_result: {
    cleaning_report: { ... },
    eda_results: { ... },
    visualizations: [ ... ],
    ai_insights: "..."
  },
  completed_at: ISODate("2024-01-15T10:31:30Z")
}
```

## Scalability Considerations

### Horizontal Scaling
```
                    Load Balancer
                         |
        ┌────────────────┼────────────────┐
        ↓                ↓                ↓
   Backend 1        Backend 2        Backend 3
        ↓                ↓                ↓
        └────────────────┼────────────────┘
                         ↓
                    MongoDB Cluster
                    (Replica Set)
```

### Microservices Architecture (Future)
```
API Gateway
    ├── Auth Service
    ├── Upload Service
    ├── Analysis Service
    │   ├── Cleaning Worker
    │   ├── EDA Worker
    │   ├── Viz Worker
    │   └── Insight Worker
    └── Storage Service
```

## Technology Stack Summary

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React 18 | UI Framework |
| Styling | Tailwind CSS | Responsive Design |
| Routing | React Router | Navigation |
| HTTP Client | Axios | API Communication |
| Charts | Plotly.js | Interactive Visualizations |
| Backend | FastAPI | REST API |
| Database | MongoDB | NoSQL Data Store |
| Auth | JWT + bcrypt | Security |
| Data Processing | Pandas, NumPy | Data Manipulation |
| Visualization | Plotly, Matplotlib | Chart Generation |
| ML | scikit-learn | Statistical Analysis |
| AI | Hugging Face | LLM Insights |
| Async | Motor | Async MongoDB Driver |

## Performance Metrics

### Target Performance
- API Response Time: < 200ms (excluding analysis)
- Analysis Processing: < 30s for 10K rows
- Frontend Load Time: < 2s
- Database Query Time: < 100ms

### Optimization Strategies
1. **Database Indexing**: User_id, upload_date
2. **Connection Pooling**: MongoDB connection reuse
3. **Lazy Loading**: Load visualizations on demand
4. **Caching**: Redis for frequent queries
5. **CDN**: Static asset delivery
6. **Code Splitting**: React lazy loading
7. **Compression**: Gzip for API responses

## Monitoring & Observability

```
Application Metrics
    ├── Request Rate
    ├── Error Rate
    ├── Response Time
    └── Active Users

System Metrics
    ├── CPU Usage
    ├── Memory Usage
    ├── Disk I/O
    └── Network Traffic

Business Metrics
    ├── Datasets Uploaded
    ├── Analysis Completed
    ├── User Signups
    └── API Usage
```

## Deployment Architecture

### Development
```
localhost:3000 (Frontend) → localhost:8000 (Backend) → localhost:27017 (MongoDB)
```

### Production
```
CDN (Frontend) → Load Balancer → Backend Cluster → MongoDB Atlas
                                      ↓
                                 File Storage (S3)
                                      ↓
                              Hugging Face API
```
