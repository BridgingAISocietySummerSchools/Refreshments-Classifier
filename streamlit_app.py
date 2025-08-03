import streamlit as st
import requests
import json
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="🍺 Bavarian Beverage Recommender",
    page_icon="🍺",
    layout="wide"
)

# Custom CSS for Bavarian theme
st.markdown("""
<style>
    .main > div {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #fbbf24 100%);
        color: white;
    }
    
    .stTitle {
        color: #fbbf24 !important;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        font-size: 3rem !important;
    }
    
    .bavarian-header {
        background: linear-gradient(90deg, #1e3a8a, #fbbf24);
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .recommendation-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 15px;
        border: 2px solid #fbbf24;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #1e3a8a, #3b82f6);
        color: white;
        border: 2px solid #fbbf24;
        border-radius: 25px;
        padding: 10px 30px;
        font-weight: bold;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background: linear-gradient(45deg, #fbbf24, #f59e0b);
        color: #1e3a8a;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
    
    .stSelectbox > div > div > div {
        background-color: rgba(255, 255, 255, 0.9);
        color: #1e3a8a;
        border-radius: 10px;
    }
    
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.9);
        color: #1e3a8a;
        border-radius: 10px;
        border: 2px solid #fbbf24;
    }
    
    .stSlider > div > div > div {
        color: #fbbf24;
    }
    
    .stNumberInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.9);
        color: #1e3a8a;
        border-radius: 10px;
        border: 2px solid #fbbf24;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="bavarian-header">
    <h1 style="color: white; margin: 0; font-size: 2.5rem;">🍺 Bavarian Beverage Recommender 🥨</h1>
    <p style="color: #fbbf24; margin: 10px 0 0 0; font-size: 1.2rem;">
        Authentic Bavarian recommendations powered by AI • Prost! 🍻
    </p>
</div>
""", unsafe_allow_html=True)

def get_recommendation(preferences):
    """Get recommendation from the LLM API"""
    try:
        response = requests.post(
            "http://localhost:8000/recommend",
            json=preferences,
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("🚫 Cannot connect to recommendation API. Please ensure the API server is running on port 8000.")
        return None
    except requests.exceptions.Timeout:
        st.error("⏱️ Request timed out. Please try again.")
        return None
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None

def submit_feedback(recommendation_id, rating, feedback_text):
    """Submit feedback to the API"""
    try:
        response = requests.post(
            "http://localhost:8000/feedback",
            json={
                "recommendation_id": recommendation_id,
                "rating": rating,
                "feedback": feedback_text
            },
            timeout=10
        )
        return response.status_code == 200
    except:
        return False

# Main application
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🎯 Tell us your preferences")
    
    # Beverage preferences
    beverage_type = st.selectbox(
        "🍺 What type of beverage are you in the mood for?",
        ["Beer", "Non-alcoholic", "Wine", "Spirits", "Mixed drinks", "Traditional Bavarian", "Surprise me!"]
    )
    
    # Occasion
    occasion = st.selectbox(
        "🎪 What's the occasion?",
        ["Oktoberfest celebration", "Casual evening", "Festive gathering", "Romantic dinner", 
         "Business meeting", "Outdoor activity", "Cold weather comfort", "Hot summer day"]
    )
    
    # Flavor preferences
    flavor_preference = st.selectbox(
        "😋 Flavor preference?",
        ["Bold and robust", "Light and refreshing", "Sweet and fruity", "Hoppy and bitter", 
         "Smooth and mellow", "Spicy and warming", "Traditional Bavarian flavors"]
    )
    
    # Alcohol strength
    alcohol_preference = st.slider(
        "🌡️ Alcohol strength preference (0 = non-alcoholic, 10 = very strong)",
        min_value=0, max_value=10, value=5
    )
    
    # Additional preferences
    st.markdown("### 🎨 Additional preferences")
    
    col_a, col_b = st.columns(2)
    with col_a:
        temperature = st.selectbox("🌡️ Temperature", ["Ice cold", "Chilled", "Room temperature", "Warm"])
        sweetness = st.slider("🍯 Sweetness level", 1, 10, 5)
    
    with col_b:
        carbonation = st.selectbox("💨 Carbonation", ["Still", "Lightly sparkling", "Highly carbonated"])
        serving_size = st.selectbox("📏 Serving size", ["Small (0.2L)", "Medium (0.5L)", "Large (1L)", "Extra large (1L+)"])
    
    # Special notes
    special_notes = st.text_area(
        "📝 Any special requests or dietary restrictions?",
        placeholder="e.g., gluten-free, low-calorie, traditional recipe, etc."
    )
    
    # Get recommendation button
    if st.button("🍺 Get My Bavarian Recommendation!", use_container_width=True):
        preferences = {
            "beverage_type": beverage_type,
            "occasion": occasion,
            "flavor_preference": flavor_preference,
            "alcohol_preference": alcohol_preference,
            "temperature": temperature,
            "sweetness": sweetness,
            "carbonation": carbonation,
            "serving_size": serving_size,
            "special_notes": special_notes,
            "timestamp": datetime.now().isoformat()
        }
        
        with st.spinner("🔮 Consulting our Bavarian beverage master..."):
            recommendation = get_recommendation(preferences)
            
            if recommendation:
                st.session_state.last_recommendation = recommendation
                st.session_state.show_feedback = True

with col2:
    st.markdown("### 🏔️ About Bavarian Beverages")
    st.markdown("""
    <div class="recommendation-card">
        <h4>🍺 Beer Culture</h4>
        <p>Bavaria is home to over 600 breweries and the famous Oktoberfest!</p>
        
        <h4>🥨 Traditional Pairings</h4>
        <p>Perfect with pretzels, sausages, and hearty Bavarian dishes.</p>
        
        <h4>🎪 Festive Spirit</h4>
        <p>Every recommendation celebrates authentic Bavarian traditions.</p>
    </div>
    """, unsafe_allow_html=True)

# Display recommendation
if hasattr(st.session_state, 'last_recommendation') and st.session_state.last_recommendation:
    st.markdown("---")
    st.markdown("## 🎯 Your Bavarian Recommendation")
    
    rec = st.session_state.last_recommendation
    
    st.markdown(f"""
    <div class="recommendation-card">
        <h3 style="color: #fbbf24; margin-top: 0;">🍺 {rec.get('name', 'Traditional Bavarian Beverage')}</h3>
        <p><strong>Type:</strong> {rec.get('type', 'Traditional')}</p>
        <p><strong>Description:</strong> {rec.get('description', 'A delightful Bavarian beverage.')}</p>
        <p><strong>Why this choice:</strong> {rec.get('reasoning', 'Perfect for your preferences!')}</p>
        <p><strong>Serving suggestion:</strong> {rec.get('serving_suggestion', 'Serve chilled and enjoy!')}</p>
        <p><strong>Cultural note:</strong> {rec.get('cultural_note', 'A beloved Bavarian tradition!')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Feedback section
    if hasattr(st.session_state, 'show_feedback') and st.session_state.show_feedback:
        st.markdown("### 📝 How was this recommendation?")
        
        col_rate, col_feedback = st.columns([1, 2])
        
        with col_rate:
            rating = st.slider("⭐ Rating", 1, 5, 3, key="rating_slider")
        
        with col_feedback:
            feedback_text = st.text_area(
                "💬 Your feedback", 
                placeholder="What did you think? Any suggestions?",
                key="feedback_text"
            )
        
        if st.button("📤 Submit Feedback"):
            if submit_feedback(rec.get('id', 'unknown'), rating, feedback_text):
                st.success("🙏 Thank you for your feedback! Danke schön!")
                st.session_state.show_feedback = False
            else:
                st.warning("⚠️ Could not submit feedback. Please try again.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px; color: #fbbf24;">
    <p>🍺 Prost! Enjoy your Bavarian beverage experience! 🥨</p>
    <p><em>Made with ❤️ in the spirit of Bavarian tradition</em></p>
</div>
""", unsafe_allow_html=True)
