from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    # API Settings
    api_title: str = "Mala Lingo API"
    api_version: str = "1.0.0"
    api_description: str = "Language learning application API"
    
    # CORS Settings
    allowed_origins: List[str] = [
        "http://localhost:5173",  # Vue dev server
        "http://localhost",       # Production
        "http://localhost:80",    # Production alternative
        "http://frontend:5173",   # Docker service name
        "http://malayaliah.com",  # Production domain with http
        "http://www.malayaliah.com"  # Production domain with www and http
    ]
    
    # Supabase Settings
    supabase_url: str = os.getenv("SUPABASE_URL", "")
    supabase_key: str = os.getenv("SUPABASE_KEY", "")
    
    # Server Settings
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_file = ".env"

# Global settings instance
settings = Settings() 