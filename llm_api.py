from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn
from llm_recommender import BavarianBeverageRecommender, init_recommendation_database
import sqlite3
import json

app = FastAPI(title="Bavarian Beverage Recommender API", version="1.0.0")

# Global recommender instance
recommender = BavarianBeverageRecommender()

class UserPreferences(BaseModel):
    taste_profile: List[str]  # e.g., ["sweet", "refreshing", "strong"]
    alcohol_preference: str   # "beer", "wine", "spirits", "no_alcohol", "low_alcohol"
    occasion: str            # "oktoberfest", "casual", "celebration", "business", "romantic"
    time_of_day: str         # "morning", "afternoon", "evening", "night"
    season: str              # "spring", "summer", "autumn", "winter"
    social_setting: str      # "alone", "friends", "family", "colleagues", "date"
    experience_level: str    # "beginner", "intermediate", "expert"
    dietary_restrictions: Optional[List[str]] = []  # ["vegetarian", "vegan", "gluten_free"]
    mood: Optional[str] = "neutral"  # "happy", "relaxed", "energetic", "contemplative"
    budget: Optional[str] = "medium"  # "low", "medium", "high"

class RecommendationResponse(BaseModel):
    recommendation: str
    preferences_used: Dict
    timestamp: str

class FeedbackRequest(BaseModel):
    recommendation_id: Optional[int] = None
    rating: int  # 1-5 scale
    comments: Optional[str] = ""

@app.on_event("startup")
async def startup_event():
    """Initialize the database on startup"""
    init_recommendation_database()
    print("Bavarian Beverage Recommender API started!")

@app.get("/")
async def root():
    return {
        "message": "Bavarian Beverage Recommender API", 
        "version": "1.0.0",
        "description": "Get personalized Bavarian beverage recommendations powered by AI"
    }

@app.post("/recommend", response_model=RecommendationResponse)
async def get_recommendation(preferences: UserPreferences):
    """Get a personalized Bavarian beverage recommendation"""
    try:
        # Convert Pydantic model to dict
        pref_dict = preferences.dict()
        
        # Get recommendation from LLM
        result = recommender.get_recommendation(pref_dict)
        
        if 'error' in result:
            raise HTTPException(status_code=500, detail=result['error'])
        
        return RecommendationResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recommendation error: {str(e)}")

@app.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """Submit feedback for a recommendation"""
    try:
        conn = sqlite3.connect('bavarian_recommendations.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO feedback (recommendation_id, rating, comments)
            VALUES (?, ?, ?)
        ''', (feedback.recommendation_id, feedback.rating, feedback.comments))
        
        conn.commit()
        conn.close()
        
        return {"message": "Feedback submitted successfully", "status": "success"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feedback error: {str(e)}")

@app.get("/preferences-options")
async def get_preference_options():
    """Get available options for user preferences"""
    return {
        "taste_profile_options": [
            "sweet", "bitter", "sour", "refreshing", "strong", "mild", "fruity", 
            "hoppy", "malty", "crisp", "smooth", "complex", "traditional", "modern"
        ],
        "alcohol_preference_options": [
            "beer", "wine", "spirits", "no_alcohol", "low_alcohol"
        ],
        "occasion_options": [
            "oktoberfest", "casual_evening", "celebration", "business_meeting", 
            "romantic_dinner", "family_gathering", "after_work", "weekend_relaxation",
            "special_celebration", "traditional_feast"
        ],
        "time_of_day_options": [
            "morning", "afternoon", "evening", "night", "late_night"
        ],
        "season_options": [
            "spring", "summer", "autumn", "winter"
        ],
        "social_setting_options": [
            "alone", "with_friends", "family", "colleagues", "romantic_date", 
            "large_group", "intimate_gathering"
        ],
        "experience_level_options": [
            "beginner", "intermediate", "expert", "connoisseur"
        ],
        "dietary_restrictions_options": [
            "vegetarian", "vegan", "gluten_free", "low_sugar", "organic_only"
        ],
        "mood_options": [
            "happy", "relaxed", "energetic", "contemplative", "adventurous", 
            "nostalgic", "celebratory", "peaceful"
        ],
        "budget_options": [
            "low", "medium", "high", "premium"
        ]
    }

@app.get("/bavarian-beverages")
async def get_bavarian_beverages():
    """Get list of traditional Bavarian beverages"""
    return {
        "traditional_beers": [
            "Weissbier (Wheat Beer)", "Märzen (Oktoberfest Beer)", "Helles", 
            "Augustiner Lagerbier Hell", "Spaten Oktoberfest", "Löwenbräu Original",
            "Franziskaner Weissbier", "Erdinger Weissbier", "Schneider Weisse"
        ],
        "non_alcoholic": [
            "Apfelschorle (Apple Spritzer)", "Spezi (Cola-Orange Mix)", 
            "Johannisbeerenschorle", "Holunderblütenschorle", "Radler", "Russ"
        ],
        "spirits": [
            "Obstler (Fruit Brandy)", "Enzian (Gentian Schnapps)", 
            "Zirbenschnaps (Stone Pine Schnapps)", "Himbeergeist"
        ],
        "seasonal": [
            "Feuerzangenbowle (Winter)", "Glühwein (Winter)", 
            "Maibock (Spring)", "Märzen (Autumn)"
        ]
    }

@app.get("/statistics")
async def get_statistics():
    """Get recommendation statistics"""
    try:
        conn = sqlite3.connect('bavarian_recommendations.db')
        cursor = conn.cursor()
        
        # Total recommendations
        cursor.execute("SELECT COUNT(*) FROM recommendations")
        total_recommendations = cursor.fetchone()[0]
        
        # Average rating from feedback
        cursor.execute("SELECT AVG(rating) FROM feedback WHERE rating IS NOT NULL")
        avg_rating = cursor.fetchone()[0] or 0
        
        # Most common preferences
        cursor.execute("SELECT preferences FROM recommendations")
        preferences_data = cursor.fetchall()
        
        conn.close()
        
        return {
            "total_recommendations": total_recommendations,
            "average_rating": round(avg_rating, 2),
            "database_status": "active"
        }
    
    except Exception as e:
        return {
            "total_recommendations": 0,
            "average_rating": 0,
            "database_status": "error",
            "error": str(e)
        }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "bavarian_beverage_recommender",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
