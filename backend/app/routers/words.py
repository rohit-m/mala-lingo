from fastapi import APIRouter
from ..models.word_matching import WordMatchingResponse
from ..services.word_service import WordService

router = APIRouter(prefix="/api", tags=["words"])

@router.get("/word-matching", response_model=WordMatchingResponse)
async def get_word_matching():
    """Get random word matching entries for game"""
    data = await WordService.get_random_word_matching()
    return WordMatchingResponse(data=data) 