from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from typing import Optional
import random

# Load environment variables
load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vue dev server
        "http://localhost",       # Production
        "http://localhost:80",    # Production alternative
        "http://frontend:5173",   # Docker service name
        "https://malayaliah.com", # Production domain
        "https://www.malayaliah.com" # Production domain with www
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Supabase client
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

@app.post("/api/auth/signup")
async def signup(user: UserCreate):
    try:
        response = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password
        })
        return {"message": "User created successfully", "user": response.user}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/auth/login")
async def login(user: UserLogin):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })
        return {
            "message": "Login successful",
            "access_token": response.session.access_token,
            "user": response.user
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@app.get("/api/auth/user")
async def get_user(token: str):
    try:
        user = supabase.auth.get_user(token)
        return {"user": user}
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/api/word-matching")
async def get_word_matching():
    try:
        # Fetch all entries from the database
        response = supabase.table("word_matching").select("*").execute()
        all_data = response.data
        
        # If we have fewer than 5 entries, return all of them
        if len(all_data) <= 5:
            return {"data": all_data}
        
        # Otherwise, randomly select 5 entries
        random_entries = random.sample(all_data, 5) 
        return {"data": random_entries}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching word matching data: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 

