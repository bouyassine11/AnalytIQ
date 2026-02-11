from datetime import datetime
from bson import ObjectId
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.database import get_database

class AuthService:
    @staticmethod
    async def create_user(full_name: str, email: str, password: str):
        db = await get_database()
        
        existing_user = await db.users.find_one({"email": email})
        if existing_user:
            return None
        
        user_doc = {
            "full_name": full_name,
            "email": email,
            "hashed_password": get_password_hash(password),
            "created_at": datetime.utcnow()
        }
        
        result = await db.users.insert_one(user_doc)
        user_doc["_id"] = result.inserted_id
        return user_doc
    
    @staticmethod
    async def authenticate_user(email: str, password: str):
        db = await get_database()
        user = await db.users.find_one({"email": email})
        
        if not user or not verify_password(password, user["hashed_password"]):
            return None
        
        return user
    
    @staticmethod
    async def get_user_by_email(email: str):
        db = await get_database()
        return await db.users.find_one({"email": email})
