import openai
import json
import os
from typing import Dict, List, Optional
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class BavarianBeverageRecommender:
    def __init__(self):
        # Initialize OpenAI client - you'll need to set OPENAI_API_KEY in environment
        self.client = openai.OpenAI(
            api_key=os.getenv("OPENAI_API_KEY", "your-api-key-here")
        )
        
        self.bavarian_beverages = [
            # Traditional Bavarian Beers
            "Weissbier (Wheat Beer)", "Märzen (Oktoberfest Beer)", "Helles", 
            "Augustiner Lagerbier Hell", "Spaten Oktoberfest", "Löwenbräu Original",
            "Franziskaner Weissbier", "Erdinger Weissbier", "Schneider Weisse",
            "Tegernseer Hell", "Chiemseer Hell", "Andechser Bergbock Hell",
            
            # Non-alcoholic Traditional Drinks
            "Apfelschorle (Apple Spritzer)", "Spezi (Cola-Orange Mix)", 
            "Johannisbeerenschorle (Blackcurrant Spritzer)", "Holunderblütenschorle",
            "Radler (Beer and Lemonade Mix)", "Russ (Wheat Beer and Lemonade)",
            
            # Traditional Bavarian Schnapps & Spirits
            "Obstler (Fruit Brandy)", "Enzian (Gentian Schnapps)", 
            "Zirbenschnaps (Stone Pine Schnapps)", "Himbeergeist (Raspberry Spirit)",
            
            # Hot Beverages
            "Feuerzangenbowle (Fire Tongs Punch)", "Glühwein (Mulled Wine)",
            "Heisse Schokolade mit Rum (Hot Chocolate with Rum)",
            
            # Regional Specialties
            "Almdudler (Alpine Herb Lemonade)", "Augustiner Edelstoff",
            "Tegernseer Spezial", "Weihenstephaner Original"
        ]
        
        self.system_prompt = """
You are a traditional Bavarian beverage expert and sommelier with deep knowledge of Bavaria's rich drinking culture. Your role is to provide personalized beverage recommendations based on individual preferences, occasions, and traditional Bavarian customs.

EXPERTISE AREAS:
- Traditional Bavarian beers (Weissbier, Märzen, Helles, etc.)
- Regional breweries (Augustiner, Spaten, Löwenbräu, Franziskaner, etc.)
- Non-alcoholic Bavarian drinks (Apfelschorle, Spezi, various Schorles)
- Traditional spirits and schnapps (Obstler, Enzian, Zirbenschnaps)
- Seasonal beverages (Glühwein, Feuerzangenbowle, etc.)
- Beer garden culture and pairing traditions

RECOMMENDATION PRINCIPLES:
1. Match beverages to personal taste preferences (sweet, bitter, strong, light, etc.)
2. Consider the occasion (Oktoberfest, casual evening, celebration, etc.)
3. Respect traditional Bavarian drinking customs and seasons
4. Provide cultural context and history when relevant
5. Suggest food pairings typical to Bavaria (Weisswurst, Pretzels, etc.)
6. Consider alcohol preferences and tolerance levels
7. Recommend authentic Bavarian brands and breweries

RESPONSE FORMAT:
- Primary recommendation with specific brand/type
- 2-3 alternative options
- Brief cultural context or history
- Suggested food pairings
- Serving suggestions (temperature, glassware, etc.)
- Occasion suitability

Always maintain the warm, welcoming spirit of Bavarian hospitality (Gemütlichkeit) in your recommendations. Use some traditional Bavarian expressions when appropriate (Prost!, Gemütlichkeit, etc.).

Respond in a friendly, knowledgeable manner as if you're a local Bavarian sharing recommendations with a friend visiting Bavaria.
"""

    def get_recommendation(self, user_preferences: Dict) -> Dict:
        """
        Get LLM-based beverage recommendation based on user preferences
        """
        
        # Prepare the user preference prompt
        preference_text = self._format_preferences(user_preferences)
        
        user_prompt = f"""
Based on these personal preferences and situation, please recommend traditional Bavarian beverages:

{preference_text}

Please provide specific recommendations from authentic Bavarian breweries and traditional drinks, considering the person's taste profile and the occasion.
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            recommendation_text = response.choices[0].message.content
            
            # Store the recommendation
            self._store_recommendation(user_preferences, recommendation_text)
            
            return {
                "recommendation": recommendation_text,
                "preferences_used": user_preferences,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "error": f"Failed to get recommendation: {str(e)}",
                "fallback_recommendation": self._get_fallback_recommendation(user_preferences)
            }
    
    def _format_preferences(self, preferences: Dict) -> str:
        """Format user preferences into a readable text"""
        text = []
        
        if preferences.get('taste_profile'):
            text.append(f"Taste Preferences: {', '.join(preferences['taste_profile'])}")
        
        if preferences.get('alcohol_preference'):
            text.append(f"Alcohol Preference: {preferences['alcohol_preference']}")
        
        if preferences.get('occasion'):
            text.append(f"Occasion: {preferences['occasion']}")
        
        if preferences.get('time_of_day'):
            text.append(f"Time of Day: {preferences['time_of_day']}")
        
        if preferences.get('season'):
            text.append(f"Season: {preferences['season']}")
        
        if preferences.get('social_setting'):
            text.append(f"Social Setting: {preferences['social_setting']}")
        
        if preferences.get('experience_level'):
            text.append(f"Bavarian Beverage Experience: {preferences['experience_level']}")
        
        if preferences.get('dietary_restrictions'):
            text.append(f"Dietary Considerations: {', '.join(preferences['dietary_restrictions'])}")
        
        if preferences.get('mood'):
            text.append(f"Current Mood: {preferences['mood']}")
        
        return '\n'.join(text)
    
    def _get_fallback_recommendation(self, preferences: Dict) -> str:
        """Provide a fallback recommendation if LLM fails"""
        alcohol_pref = preferences.get('alcohol_preference', 'beer')
        
        if alcohol_pref == 'no_alcohol':
            return """
            Prost! I recommend a refreshing Apfelschorle (apple spritzer) - a beloved Bavarian classic! 
            This crisp blend of apple juice and sparkling water is perfect for any occasion. 
            Try it with traditional Brezn (pretzels) for an authentic Bavarian experience.
            """
        elif alcohol_pref == 'beer':
            return """
            Prost! For a true Bavarian experience, I recommend Augustiner Lagerbier Hell - 
            Munich's oldest brewery crafts this smooth, golden lager that's beloved by locals. 
            Serve it in a proper Maß (1-liter mug) with Weisswurst and sweet mustard for 
            authentic Gemütlichkeit!
            """
        else:
            return """
            Prost! Try a traditional Obstler (fruit brandy) - this clear, aromatic spirit 
            captures the essence of Bavarian orchards. Serve it slightly chilled as a 
            digestif after a hearty Bavarian meal.
            """
    
    def _store_recommendation(self, preferences: Dict, recommendation: str):
        """Store recommendation in database"""
        try:
            conn = sqlite3.connect('bavarian_recommendations.db')
            cursor = conn.cursor()
            
            # Create table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recommendations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    preferences TEXT,
                    recommendation TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                INSERT INTO recommendations (preferences, recommendation)
                VALUES (?, ?)
            ''', (json.dumps(preferences), recommendation))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            print(f"Error storing recommendation: {e}")

def init_recommendation_database():
    """Initialize the recommendation database"""
    conn = sqlite3.connect('bavarian_recommendations.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recommendations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            preferences TEXT,
            recommendation TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create a table for user feedback
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            recommendation_id INTEGER,
            rating INTEGER,
            comments TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (recommendation_id) REFERENCES recommendations (id)
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Initialize database
    init_recommendation_database()
    
    # Test the recommender
    recommender = BavarianBeverageRecommender()
    
    test_preferences = {
        'taste_profile': ['refreshing', 'not too bitter'],
        'alcohol_preference': 'beer',
        'occasion': 'casual evening',
        'time_of_day': 'evening',
        'season': 'summer',
        'social_setting': 'friends',
        'experience_level': 'beginner',
        'mood': 'relaxed'
    }
    
    print("Testing Bavarian Beverage Recommender...")
    result = recommender.get_recommendation(test_preferences)
    
    if 'error' in result:
        print(f"Error: {result['error']}")
        print(f"Fallback: {result['fallback_recommendation']}")
    else:
        print(f"Recommendation: {result['recommendation']}")
