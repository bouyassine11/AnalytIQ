# API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication

All protected endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <token>
```

---

## Endpoints

### 1. User Sign Up

**POST** `/auth/signup`

Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (201 Created):**
```json
{
  "message": "User created successfully",
  "email": "user@example.com"
}
```

**Error Response (400 Bad Request):**
```json
{
  "detail": "Email already registered"
}
```

---

### 2. User Login

**POST** `/auth/login`

Authenticate user and receive JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Incorrect email or password"
}
```

---

### 3. Upload CSV

**POST** `/datasets/upload`

Upload a CSV file for analysis. Requires authentication.

**Headers:**
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request Body:**
- `file`: CSV file (multipart/form-data)

**Response (200 OK):**
```json
{
  "dataset_id": "507f1f77bcf86cd799439011",
  "filename": "sales_data.csv",
  "status": "processing",
  "message": "File uploaded successfully. Analysis in progress."
}
```

**Error Response (400 Bad Request):**
```json
{
  "detail": "Only CSV files are allowed"
}
```

---

### 4. Get Analysis Results

**GET** `/datasets/analysis/{dataset_id}`

Retrieve analysis results for a specific dataset. Requires authentication.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
{
  "dataset_id": "507f1f77bcf86cd799439011",
  "filename": "sales_data.csv",
  "status": "completed",
  "cleaning_report": {
    "original_shape": [100, 10],
    "final_shape": [98, 10],
    "missing_values": {
      "age": 5,
      "salary": 3
    },
    "duplicates_removed": 2,
    "outliers_detected": {
      "salary": 4
    },
    "actions_taken": [
      "Filled age with median",
      "Filled salary with median",
      "Removed 2 duplicates"
    ]
  },
  "eda_results": {
    "overview": {
      "rows": 98,
      "columns": 10,
      "column_names": ["id", "name", "age", "salary", "department"],
      "memory_usage": "7.66 MB"
    },
    "summary_statistics": {
      "age": {
        "mean": 35.5,
        "std": 8.2,
        "min": 22,
        "max": 65
      }
    },
    "correlation_matrix": {
      "age": {
        "age": 1.0,
        "salary": 0.85
      }
    },
    "data_quality": {
      "completeness": 97.5,
      "duplicate_rows": 0,
      "numeric_columns": 4,
      "categorical_columns": 3
    }
  },
  "visualizations": [
    {
      "type": "histogram",
      "column": "age",
      "data": "{\"data\":[...],\"layout\":{...}}"
    }
  ],
  "ai_insights": "📊 Dataset contains 98 rows and 10 columns...",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Status Values:**
- `processing`: Analysis in progress
- `completed`: Analysis finished successfully
- `failed`: Analysis encountered an error

**Error Response (404 Not Found):**
```json
{
  "detail": "Dataset not found"
}
```

---

### 5. List User Datasets

**GET** `/datasets/list`

Get all datasets uploaded by the authenticated user.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200 OK):**
```json
[
  {
    "dataset_id": "507f1f77bcf86cd799439011",
    "filename": "sales_data.csv",
    "status": "completed",
    "upload_date": "2024-01-15T10:30:00Z"
  },
  {
    "dataset_id": "507f1f77bcf86cd799439012",
    "filename": "customer_data.csv",
    "status": "processing",
    "upload_date": "2024-01-15T11:00:00Z"
  }
]
```

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 404 | Not Found |
| 500 | Internal Server Error |

---

## Rate Limiting

Currently no rate limiting implemented. Consider adding in production.

---

## Hugging Face Integration

The platform uses Hugging Face Inference API for generating AI insights. If the API key is not configured or the service is unavailable, the system falls back to rule-based insights.

**Model Used:** `mistralai/Mistral-7B-Instruct-v0.2`

---

## Data Processing Pipeline

1. **Upload**: CSV file uploaded via multipart/form-data
2. **Storage**: File saved to server, metadata stored in MongoDB
3. **Background Processing**: Orchestrator agent coordinates:
   - Data Cleaning Agent
   - EDA Agent
   - Visualization Agent
   - Insight Agent (LLM)
4. **Storage**: Results stored in MongoDB
5. **Retrieval**: Frontend polls for completion and displays results

---

## WebSocket Support (Future)

Consider implementing WebSocket for real-time progress updates instead of polling.
