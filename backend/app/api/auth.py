from fastapi import APIRouter, HTTPException, status
from app.models.schemas import UserSignUp, UserLogin, Token
from app.services.auth_service import AuthService
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserSignUp):
    user = await AuthService.create_user(user_data.full_name, user_data.email, user_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    return {"message": "User created successfully", "full_name": user["full_name"], "email": user["email"]}

@router.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    user = await AuthService.authenticate_user(user_data.email, user_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(data={"sub": user["email"]})
    return {"access_token": access_token, "token_type": "bearer"}
