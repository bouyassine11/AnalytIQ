from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, Dict, Any, List
from datetime import datetime

class UserSignUp(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    confirm_password: str
    
    @field_validator('full_name')
    def validate_full_name(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Full name must be at least 2 characters')
        return v.strip()
    
    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        return v
    
    @field_validator('confirm_password')
    def passwords_match(cls, v, info):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('Passwords do not match')
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    id: str
    full_name: str
    email: str
    created_at: datetime

class DatasetUploadResponse(BaseModel):
    dataset_id: str
    filename: str
    status: str
    message: str

class AnalysisResponse(BaseModel):
    dataset_id: str
    filename: str
    status: str
    cleaning_report: Optional[Dict[str, Any]] = None
    eda_results: Optional[Dict[str, Any]] = None
    visualizations: Optional[List[Dict[str, Any]]] = None
    ai_insights: Optional[str] = None
    created_at: datetime
