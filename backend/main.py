from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import auth, words

def create_application() -> FastAPI:
    """Create and configure the FastAPI application"""
    
    # Create FastAPI instance
    application = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        description=settings.api_description
    )
    
    # Configure CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    application.include_router(auth.router)
    application.include_router(words.router)
    
    return application

# Create the app instance
app = create_application()

@app.get("/")
async def root():
    """Root endpoint for health check"""
    return {"message": "Mala Lingo API is running!", "version": settings.api_version}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": settings.api_title}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=True
    ) 

