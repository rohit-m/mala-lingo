from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    created_at: Optional[str] = None

class LoginResponse(BaseModel):
    message: str
    access_token: str
    user: dict 

class MagicwordRequest(BaseModel):
    magicword: str