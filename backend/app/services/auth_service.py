from ..core.database import supabase
from ..models.user import UserCreate, UserLogin
from fastapi import HTTPException

class AuthService:
    @staticmethod
    async def create_user(user_data: UserCreate):
        """Create a new user account"""
        try:
            response = supabase.auth.sign_up({
                "email": user_data.email,
                "password": user_data.password
            })
            return {"message": "User created successfully", "user": response.user}
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    @staticmethod
    async def authenticate_user(user_credentials: UserLogin):
        """Authenticate user and return session"""
        try:
            response = supabase.auth.sign_in_with_password({
                "email": user_credentials.email,
                "password": user_credentials.password
            })
            return {
                "message": "Login successful",
                "access_token": response.session.access_token,
                "user": response.user
            }
        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    
    @staticmethod
    async def get_user_by_token(token: str):
        """Get user information from token"""
        try:
            user = supabase.auth.get_user(token)
            return {"user": user}
        except Exception as e:
            raise HTTPException(status_code=401, detail="Invalid token") 