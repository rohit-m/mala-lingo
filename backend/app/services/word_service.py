from ..core.database import supabase
import random
from fastapi import HTTPException

class WordService:
    @staticmethod
    async def get_random_word_matching(count: int = 5):
        """Get random word matching entries for the game"""
        try:
            # Fetch all entries from the database
            response = supabase.table("word_matching").select("*").execute()
            all_data = response.data
            
            # If we have fewer than requested count, return all of them
            if len(all_data) <= count:
                return all_data
            
            # Otherwise, randomly select the requested number of entries
            random_entries = random.sample(all_data, count) 
            return random_entries
        except Exception as e:
            raise HTTPException(
                status_code=500, 
                detail=f"Error fetching word matching data: {str(e)}"
            ) 