from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from typing import Optional, List
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
        "http://malayaliah.com",  # Production domain with http
        "http://www.malayaliah.com"  # Production domain with www and http
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

# Environment variables for Supabase auth
SUPABASE_EMAIL = os.getenv("SUPABASE_EMAIL")
SUPABASE_PASSWORD = os.getenv("SUPABASE_PASSWORD")

class UserCreate(BaseModel):
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class LessonResponse(BaseModel):
    id: int
    title: str
    description: str
    order: int
    vocab_count: int
    verb_count: int
    exercise_count: int

# Authenticate with Supabase using service account credentials
async def authenticate_with_supabase():
    try:
        if not SUPABASE_EMAIL or not SUPABASE_PASSWORD:
            raise Exception('Supabase email or password is not configured')

        response = supabase.auth.sign_in_with_password({
            "email": SUPABASE_EMAIL,
            "password": SUPABASE_PASSWORD
        })

        if response.session is None:
            raise Exception('Authentication failed')

        return response.session
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication error: {str(e)}")

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

@app.get("/api/lessons", response_model=List[LessonResponse])
async def get_lessons():
    """
    Fetch all lessons with their vocabulary, verb, and exercise counts.
    """
    try:
        # Authenticate with Supabase first
        await authenticate_with_supabase()

        # Fetch lessons
        response = supabase.table("lessons").select("*").order("order").execute()
        
        if not response.data:
            return []

        lessons_data = response.data

        # For each lesson, get counts of vocab, verbs, and exercises
        lessons_with_counts = []
        for lesson in lessons_data:
            # Count vocabulary items
            vocab_response = supabase.table("lesson_vocab").select("*", count="exact").eq("lesson_id", lesson["id"]).execute()
            vocab_count = vocab_response.count if vocab_response.count is not None else 0

            # Count verbs
            verb_response = supabase.table("lesson_verbs").select("*", count="exact").eq("lesson_id", lesson["id"]).execute()
            verb_count = verb_response.count if verb_response.count is not None else 0

            # Count exercises
            exercise_response = supabase.table("exercises").select("*", count="exact").eq("lesson_id", lesson["id"]).execute()
            exercise_count = exercise_response.count if exercise_response.count is not None else 0

            lesson_with_counts = {
                "id": lesson["id"],
                "title": lesson["title"],
                "description": lesson["description"],
                "order": lesson["order"],
                "vocab_count": vocab_count,
                "verb_count": verb_count,
                "exercise_count": exercise_count
            }
            lessons_with_counts.append(lesson_with_counts)

        return lessons_with_counts

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching lessons: {str(e)}")

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

