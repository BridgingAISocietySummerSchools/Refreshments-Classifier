import json
import os
import random
from typing import Dict, List, Optional
import sqlite3
from datetime import datetime

class BavarianBeverageRecommender:
    def __init__(self):
        # Use local recommendations instead of LLM for reliability
        self.use_llm = False  # Set to True if you have OpenAI API key
        
        # Initialize OpenAI client only if needed
        self.client = None
        if self.use_llm and os.getenv("OPENAI_API_KEY"):
            try:
                import openai
                self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
                self.use_llm = True
            except ImportError:
                print("OpenAI not available, using local recommendations")
                self.use_llm = False
        
        # Comprehensive Bavarian beverage database
        self.bavarian_beverages = {
            "beers": {
                "light": [
                    {"name": "Augustiner Lagerbier Hell", "description": "Munich's oldest brewery's smooth golden lager", "abv": 5.2, "occasion": ["casual", "beer garden"], "taste": ["smooth", "crisp"]},
                    {"name": "Tegernseer Hell", "description": "Refreshing Bavarian lager from Alpine region", "abv": 4.8, "occasion": ["casual", "outdoor"], "taste": ["light", "refreshing"]},
                    {"name": "Spaten Münchner Hell", "description": "Classic Munich-style light beer", "abv": 5.2, "occasion": ["oktoberfest", "casual"], "taste": ["malty", "balanced"]}
                ],
                "wheat": [
                    {"name": "Franziskaner Weissbier", "description": "Traditional Bavarian wheat beer with banana and clove notes", "abv": 5.0, "occasion": ["traditional", "casual"], "taste": ["fruity", "smooth"]},
                    {"name": "Erdinger Weissbier", "description": "Premium wheat beer with fine yeast character", "abv": 5.3, "occasion": ["restaurant", "celebration"], "taste": ["creamy", "fruity"]},
                    {"name": "Schneider Weisse", "description": "Original Bavarian wheat beer since 1872", "abv": 5.4, "occasion": ["traditional", "dinner"], "taste": ["complex", "spicy"]}
                ],
                "strong": [
                    {"name": "Andechser Bergbock Hell", "description": "Strong monastery beer with rich character", "abv": 6.9, "occasion": ["winter", "contemplative"], "taste": ["rich", "warming"]},
                    {"name": "Augustiner Maximator", "description": "Double bock beer for special occasions", "abv": 7.5, "occasion": ["celebration", "cold weather"], "taste": ["malty", "strong"]},
                    {"name": "Spaten Oktoberfest", "description": "Traditional Märzen for Oktoberfest", "abv": 5.9, "occasion": ["oktoberfest", "festive"], "taste": ["malty", "amber"]}
                ]
            },
            "non_alcoholic": [
                {"name": "Apfelschorle", "description": "Refreshing apple juice with sparkling water", "abv": 0, "occasion": ["any", "refreshing"], "taste": ["fruity", "light"]},
                {"name": "Spezi", "description": "Bavarian cola-orange mix", "abv": 0, "occasion": ["casual", "summer"], "taste": ["sweet", "citrus"]},
                {"name": "Holunderblütenschorle", "description": "Elderflower spritzer", "abv": 0, "occasion": ["elegant", "summer"], "taste": ["floral", "refreshing"]},
                {"name": "Johannisbeerenschorle", "description": "Blackcurrant spritzer", "abv": 0, "occasion": ["casual", "fruity"], "taste": ["berry", "tart"]}
            ],
            "spirits": [
                {"name": "Obstler", "description": "Traditional fruit brandy from Bavarian orchards", "abv": 40, "occasion": ["digestif", "traditional"], "taste": ["fruity", "strong"]},
                {"name": "Enzian", "description": "Gentian root schnapps from Alpine regions", "abv": 38, "occasion": ["after dinner", "winter"], "taste": ["herbal", "warming"]},
                {"name": "Zirbenschnaps", "description": "Stone pine schnapps with unique flavor", "abv": 42, "occasion": ["special", "alpine"], "taste": ["pine", "distinctive"]}
            ],
            "hot_drinks": [
                {"name": "Glühwein", "description": "Traditional mulled wine with spices", "abv": 7, "occasion": ["winter", "christmas market"], "taste": ["spiced", "warming"]},
                {"name": "Feuerzangenbowle", "description": "Rum punch with sugar cone", "abv": 12, "occasion": ["celebration", "winter"], "taste": ["sweet", "theatrical"]},
                {"name": "Heisse Schokolade mit Rum", "description": "Hot chocolate with Bavarian rum", "abv": 8, "occasion": ["dessert", "cozy"], "taste": ["chocolate", "warming"]}
            ]
        }
        
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
        Get beverage recommendation based on user preferences
        """
        try:
            if self.use_llm and self.client:
                return self._get_llm_recommendation(user_preferences)
            else:
                return self._get_local_recommendation(user_preferences)
        except Exception as e:
            return self._get_fallback_recommendation(user_preferences)
    
    def _get_local_recommendation(self, preferences: Dict) -> Dict:
        """Get recommendation using local logic"""
        
        # Extract key preferences
        beverage_type = preferences.get('beverage_type', 'Beer').lower()
        occasion = preferences.get('occasion', 'casual').lower()
        alcohol_pref = preferences.get('alcohol_preference', 5)
        flavor_pref = preferences.get('flavor_preference', 'balanced').lower()
        temperature = preferences.get('temperature', 'chilled').lower()
        
        # Select beverage category
        if 'non' in beverage_type or alcohol_pref == 0:
            selected_beverage = self._select_non_alcoholic(preferences)
        elif 'beer' in beverage_type or beverage_type == 'traditional bavarian':
            selected_beverage = self._select_beer(preferences)
        elif 'spirit' in beverage_type or alcohol_pref >= 8:
            selected_beverage = self._select_spirit(preferences)
        elif 'hot' in temperature or 'warm' in temperature:
            selected_beverage = self._select_hot_drink(preferences)
        else:
            selected_beverage = self._select_beer(preferences)  # Default to beer
        
        # Generate recommendation text
        recommendation_text = self._format_recommendation(selected_beverage, preferences)
        
        # Store the recommendation
        recommendation_id = self._store_recommendation(preferences, recommendation_text)
        
        return {
            "id": recommendation_id,
            "name": selected_beverage["name"],
            "type": selected_beverage.get("type", "Traditional Bavarian"),
            "description": selected_beverage["description"],
            "reasoning": self._get_reasoning(selected_beverage, preferences),
            "serving_suggestion": self._get_serving_suggestion(selected_beverage),
            "cultural_note": self._get_cultural_note(selected_beverage),
            "abv": selected_beverage.get("abv", 0),
            "preferences_used": preferences,
            "timestamp": datetime.now().isoformat()
        }
    
    def _select_beer(self, preferences: Dict) -> Dict:
        """Select appropriate beer based on preferences"""
        alcohol_pref = preferences.get('alcohol_preference', 5)
        flavor_pref = preferences.get('flavor_preference', '').lower()
        occasion = preferences.get('occasion', '').lower()
        
        if alcohol_pref <= 3 or 'light' in flavor_pref:
            options = self.bavarian_beverages["beers"]["light"]
        elif 'wheat' in flavor_pref or 'fruity' in flavor_pref or 'smooth' in flavor_pref:
            options = self.bavarian_beverages["beers"]["wheat"]
        elif alcohol_pref >= 7 or 'strong' in flavor_pref or 'winter' in occasion:
            options = self.bavarian_beverages["beers"]["strong"]
        else:
            options = self.bavarian_beverages["beers"]["light"]  # Default
        
        # Filter by occasion if possible
        filtered = [beer for beer in options if any(occ in occasion for occ in beer["occasion"])]
        if filtered:
            options = filtered
            
        selected = random.choice(options)
        selected["type"] = "Traditional Bavarian Beer"
        return selected
    
    def _select_non_alcoholic(self, preferences: Dict) -> Dict:
        """Select non-alcoholic beverage"""
        flavor_pref = preferences.get('flavor_preference', '').lower()
        
        if 'fruity' in flavor_pref or 'sweet' in flavor_pref:
            candidates = [drink for drink in self.bavarian_beverages["non_alcoholic"] 
                         if 'fruity' in drink["taste"] or 'sweet' in drink["taste"]]
        elif 'floral' in flavor_pref or 'elegant' in preferences.get('occasion', ''):
            candidates = [drink for drink in self.bavarian_beverages["non_alcoholic"] 
                         if 'floral' in drink["taste"]]
        else:
            candidates = self.bavarian_beverages["non_alcoholic"]
        
        if not candidates:
            candidates = self.bavarian_beverages["non_alcoholic"]
            
        selected = random.choice(candidates)
        selected["type"] = "Traditional Non-Alcoholic"
        return selected
    
    def _select_spirit(self, preferences: Dict) -> Dict:
        """Select appropriate spirit"""
        occasion = preferences.get('occasion', '').lower()
        
        if 'dinner' in occasion or 'digestif' in occasion:
            candidates = [spirit for spirit in self.bavarian_beverages["spirits"] 
                         if 'digestif' in spirit["occasion"]]
        else:
            candidates = self.bavarian_beverages["spirits"]
        
        selected = random.choice(candidates)
        selected["type"] = "Traditional Bavarian Spirit"
        return selected
    
    def _select_hot_drink(self, preferences: Dict) -> Dict:
        """Select hot beverage"""
        occasion = preferences.get('occasion', '').lower()
        alcohol_pref = preferences.get('alcohol_preference', 5)
        
        if alcohol_pref == 0:
            # Non-alcoholic hot chocolate variant
            return {
                "name": "Heisse Schokolade", 
                "description": "Rich Bavarian hot chocolate with whipped cream",
                "abv": 0,
                "occasion": ["cozy", "dessert"],
                "taste": ["chocolate", "warming"],
                "type": "Traditional Hot Beverage"
            }
        
        candidates = self.bavarian_beverages["hot_drinks"]
        if 'celebration' in occasion or 'festive' in occasion:
            candidates = [drink for drink in candidates if 'celebration' in drink["occasion"]]
        
        selected = random.choice(candidates)
        selected["type"] = "Traditional Hot Beverage"
        return selected
    
    def _get_reasoning(self, beverage: Dict, preferences: Dict) -> str:
        """Generate reasoning for the recommendation"""
        reasons = []
        
        if preferences.get('alcohol_preference', 5) == 0 and beverage.get('abv', 0) == 0:
            reasons.append("Perfect for your non-alcoholic preference")
        elif preferences.get('alcohol_preference', 5) >= 7 and beverage.get('abv', 0) >= 6:
            reasons.append("Matches your preference for stronger beverages")
        
        flavor_pref = preferences.get('flavor_preference', '').lower()
        if any(taste in flavor_pref for taste in beverage.get('taste', [])):
            reasons.append(f"Aligns with your {flavor_pref} flavor preference")
        
        occasion = preferences.get('occasion', '').lower()
        if any(occ in occasion for occ in beverage.get('occasion', [])):
            reasons.append(f"Ideal for {occasion}")
        
        if not reasons:
            reasons.append("A classic Bavarian choice that suits your preferences")
        
        return ". ".join(reasons) + "."
    
    def _get_serving_suggestion(self, beverage: Dict) -> str:
        """Get serving suggestion for the beverage"""
        suggestions = {
            "beer": "Serve in a traditional Bavarian beer mug at 6-8°C. Best enjoyed with friends!",
            "spirit": "Serve at room temperature in a small glass. Perfect as a digestif after a hearty meal.",
            "hot": "Serve steaming hot in a warmed mug. Perfect for cold evenings.",
            "non_alcoholic": "Serve chilled with ice if desired. Refreshing any time of day!"
        }
        
        beverage_type = beverage.get('type', '').lower()
        if 'beer' in beverage_type:
            return suggestions["beer"]
        elif 'spirit' in beverage_type:
            return suggestions["spirit"]
        elif 'hot' in beverage_type:
            return suggestions["hot"]
        else:
            return suggestions["non_alcoholic"]
    
    def _get_cultural_note(self, beverage: Dict) -> str:
        """Get cultural note about the beverage"""
        cultural_notes = {
            "Augustiner": "Bavaria's oldest brewery, beloved by Munich locals since 1328",
            "Weissbier": "Traditional Bavarian wheat beer, often enjoyed with a slice of lemon",
            "Apfelschorle": "The most popular non-alcoholic drink in Bavaria",
            "Obstler": "Traditional after-dinner drink, often homemade in Bavarian households",
            "Glühwein": "Essential at Christmas markets throughout Bavaria",
            "Spezi": "Invented in Bavaria, this cola-orange mix is a regional favorite"
        }
        
        name = beverage.get('name', '')
        for key, note in cultural_notes.items():
            if key in name:
                return note
        
        return "A cherished part of Bavarian drinking culture and tradition"
    
    def _format_recommendation(self, beverage: Dict, preferences: Dict) -> str:
        """Format the complete recommendation text"""
        return f"""
🍺 {beverage['name']}

{beverage['description']}

Why this choice: {self._get_reasoning(beverage, preferences)}

Serving suggestion: {self._get_serving_suggestion(beverage)}

Cultural note: {self._get_cultural_note(beverage)}

Prost! Enjoy your authentic Bavarian experience! 🥨
        """.strip()
    
    def _get_fallback_recommendation(self, preferences: Dict) -> Dict:
        """Provide a fallback recommendation if everything else fails"""
        alcohol_pref = preferences.get('alcohol_preference', 5)
        
        if alcohol_pref == 0:
            return {
                "id": "fallback_1",
                "name": "Apfelschorle",
                "type": "Traditional Non-Alcoholic",
                "description": "Refreshing apple juice with sparkling water - Bavaria's favorite non-alcoholic drink",
                "reasoning": "A safe, beloved choice that's perfect for any occasion",
                "serving_suggestion": "Serve chilled with ice. Refreshing and authentic!",
                "cultural_note": "The most popular non-alcoholic drink in Bavaria",
                "abv": 0
            }
        elif alcohol_pref <= 6:
            return {
                "id": "fallback_2", 
                "name": "Augustiner Lagerbier Hell",
                "type": "Traditional Bavarian Beer",
                "description": "Munich's oldest brewery's smooth golden lager - beloved by locals",
                "reasoning": "A classic choice that represents authentic Bavarian beer culture",
                "serving_suggestion": "Serve in a traditional Maß at 6-8°C with friends",
                "cultural_note": "Bavaria's oldest brewery, beloved by Munich locals since 1328",
                "abv": 5.2
            }
        else:
            return {
                "id": "fallback_3",
                "name": "Obstler",
                "type": "Traditional Bavarian Spirit", 
                "description": "Traditional fruit brandy capturing the essence of Bavarian orchards",
                "reasoning": "Perfect for those who appreciate stronger, traditional beverages",
                "serving_suggestion": "Serve at room temperature as a digestif after meals",
                "cultural_note": "Traditional after-dinner drink, often homemade in Bavarian households",
                "abv": 40
            }
    
    def _store_recommendation(self, preferences: Dict, recommendation: str) -> str:
        """Store recommendation in database and return ID"""
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
            
            recommendation_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return str(recommendation_id)
            
        except Exception as e:
            print(f"Error storing recommendation: {e}")
            return "unknown"

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
        'beverage_type': 'Beer',
        'alcohol_preference': 5,
        'occasion': 'casual evening',
        'flavor_preference': 'light and refreshing',
        'temperature': 'chilled',
        'sweetness': 3,
        'carbonation': 'highly carbonated',
        'serving_size': 'Medium (0.5L)',
        'special_notes': 'first time trying Bavarian beer'
    }
    
    print("🍺 Testing Bavarian Beverage Recommender...")
    print("=" * 50)
    
    result = recommender.get_recommendation(test_preferences)
    
    print(f"Name: {result.get('name', 'Unknown')}")
    print(f"Type: {result.get('type', 'Unknown')}")
    print(f"Description: {result.get('description', 'No description')}")
    print(f"ABV: {result.get('abv', 0)}%")
    print(f"Reasoning: {result.get('reasoning', 'No reasoning')}")
    print(f"Serving: {result.get('serving_suggestion', 'No serving suggestion')}")
    print(f"Culture: {result.get('cultural_note', 'No cultural note')}")
    print("\nProst! 🍻")
