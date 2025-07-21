from pydantic import BaseModel
from typing import List, Any, Dict, Optional

class WordMatchingEntry(BaseModel):
    id: Optional[int] = None
    english_word: str
    malayalam_word: str
    difficulty_level: Optional[int] = None
    category: Optional[str] = None

class WordMatchingResponse(BaseModel):
    data: List[Dict[str, Any]] 