from fastapi import APIRouter, HTTPException
from ..models.user import UserCreate, UserLogin, LoginResponse, MagicwordRequest
from ..services.auth_service import AuthService

router = APIRouter(prefix="/api/auth", tags=["authentication"])

@router.post("/signup")
async def signup(user: UserCreate):
    """Create a new user account"""
    return await AuthService.create_user(user)

@router.post("/login", response_model=LoginResponse)
async def login(user: UserLogin):
    """Authenticate user and return access token"""
    result = await AuthService.authenticate_user(user)
    return LoginResponse(
        message=result["message"],
        access_token=result["access_token"],
        user=result["user"]
    )

@router.get("/user")
async def get_user(token: str):
    """Get user information from token"""
    return await AuthService.get_user_by_token(token)

@router.post("/magicword", response_model=LoginResponse)
async def check_magicword(request: MagicwordRequest):
    """Check if magicword is correct"""
    return await AuthService.check_magicword(request.magicword)