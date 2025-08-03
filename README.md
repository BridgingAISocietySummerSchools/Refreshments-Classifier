# 🍺 Bavarian Beverage Recommender (LLM Branch)

An AI-powered beverage recommendation system that suggests authentic Bavarian drinks based on personal preferences. This branch uses Large Language Models (LLM) to provide culturally-aware, personalized recommendations with traditional Bavarian knowledge.

## Features

- **🤖 LLM-Powered Recommendations**: Uses OpenAI GPT-4 for intelligent, contextual beverage suggestions
- **🏔️ Bavarian Cultural Expertise**: Deep knowledge of traditional Bavarian beverages and customs
- **🎨 Bavarian-Themed UI**: Streamlit frontend with authentic Bavarian blue and gold styling
- **👥 Personal Preference Analysis**: Considers taste, occasion, mood, social setting, and experience level
- **🍺 Traditional Beverage Knowledge**: Covers beers, spirits, non-alcoholic drinks, and seasonal specialties
- **💾 Feedback System**: Collects user ratings to improve recommendations
- **📊 Analytics Dashboard**: View recommendation statistics and trends

## Bavarian Beverages Covered

### Traditional Beers
- **Weissbier** (Wheat Beer) - Bavaria's cloudy specialty
- **Märzen** (Oktoberfest Beer) - The famous festival beer
- **Helles** - Light, refreshing Munich-style lager
- **Augustiner, Spaten, Löwenbräu** - Historic brewery selections

### Non-Alcoholic Specialties
- **Apfelschorle** - Apple juice with sparkling water
- **Spezi** - Traditional cola-orange mix
- **Radler** - Beer and lemonade combination
- **Various Schorles** - Fruit juice spritzers

### Spirits & Seasonal Drinks
- **Obstler** - Traditional fruit brandy
- **Enzian** - Gentian root schnapps
- **Glühwein** - Mulled wine for winter
- **Feuerzangenbowle** - Traditional fire punch

## Personal Preference Categories

The system analyzes:
- **Taste Profile**: Sweet, bitter, refreshing, strong, etc.
- **Alcohol Preference**: Beer, wine, spirits, non-alcoholic
- **Occasion**: Oktoberfest, casual evening, celebration, business
- **Social Setting**: Alone, friends, family, colleagues
- **Experience Level**: Beginner to Bavarian beverage connoisseur
- **Mood & Season**: Matching drinks to your current state
- **Dietary Restrictions**: Accommodating special needs

## Installation & Setup

### Prerequisites
- Python 3.8+
- OpenAI API key (optional - fallback recommendations available)

### Quick Start

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd Refreshments-Classifier
   git checkout llm
   chmod +x setup.sh start.sh
   ./setup.sh
   ```

2. **Configure API key** (optional):
   ```bash
   # Edit .env file
   OPENAI_API_KEY=your-openai-api-key-here
   ```

3. **Start the application**:
   ```bash
   ./start.sh
   ```

### Manual Setup

1. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize database**:
   ```bash
   python llm_recommender.py
   ```

4. **Run services**:
   ```bash
   # Terminal 1: Start API
   python llm_api.py
   
   # Terminal 2: Start Streamlit
   streamlit run streamlit_app.py
   ```

## Usage

### Web Interface
1. Visit `http://localhost:8501`
2. Navigate through the Bavarian-themed interface
3. Fill out your preferences in the consultation form
4. Get personalized recommendations with cultural context
5. Rate recommendations to help improve the system

### API Endpoints
- `POST /recommend`: Get personalized recommendations
- `GET /preferences-options`: Available preference choices
- `GET /bavarian-beverages`: List of traditional beverages
- `POST /feedback`: Submit recommendation ratings
- `GET /statistics`: View recommendation analytics

### Example API Usage

```python
import requests

preferences = {
    "taste_profile": ["refreshing", "not too bitter"],
    "alcohol_preference": "beer",
    "occasion": "casual_evening",
    "social_setting": "with_friends",
    "experience_level": "beginner",
    "season": "summer",
    "mood": "relaxed"
}

response = requests.post(
    "http://localhost:8000/recommend", 
    json=preferences
)
recommendation = response.json()
print(recommendation["recommendation"])
```

## System Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Streamlit UI   │───▶│   FastAPI API    │───▶│  LLM Provider   │
│ (Bavarian Theme)│    │ (llm_api.py)     │    │  (OpenAI GPT-4) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       
         │                       ▼                       
         │              ┌──────────────────┐              
         │              │ LLM Recommender  │              
         │              │(llm_recommender.py)│              
         │              └──────────────────┘              
         │                       │                       
         ▼                       ▼                       
┌─────────────────┐    ┌──────────────────┐              
│   User Feedback │    │  SQLite Database │              
│     System      │    │  (Preferences &  │              
│                 │    │ Recommendations) │              
└─────────────────┘    └──────────────────┘              
```

## Bavarian Cultural Features

### Gemütlichkeit Integration
The system understands and incorporates the Bavarian concept of "Gemütlichkeit" - the warm, friendly, cheerful atmosphere that defines Bavarian social drinking culture.

### Seasonal Awareness
- **Spring**: Maibock celebrations and fresh seasonal beers
- **Summer**: Beer garden culture and refreshing drinks
- **Autumn**: Oktoberfest traditions and Märzen beers
- **Winter**: Warming beverages like Glühwein and Feuerzangenbowle

### Regional Expertise
Knowledge of specific breweries, their histories, and regional specialties:
- Munich: Augustiner (1328), Spaten, Löwenbräu
- Freising: Weihenstephaner (world's oldest brewery)
- Kelheim: Schneider Weisse (wheat beer specialists)

## Configuration

### Environment Variables (.env)
```bash
OPENAI_API_KEY=your-openai-api-key-here
```

### API Configuration (llm_api.py)
- Model: GPT-4 (configurable)
- Temperature: 0.7 (balanced creativity/consistency)
- Max tokens: 800 (detailed recommendations)

## Project Structure (LLM Branch)

```
Refreshments-Classifier/ (llm branch)
├── streamlit_app.py          # Bavarian-themed Streamlit frontend
├── llm_api.py               # FastAPI backend for LLM recommendations
├── llm_recommender.py       # Core LLM recommendation engine
├── streamlit_app_ml.py      # Original ML-based app (preserved)
├── requirements.txt         # Dependencies (includes OpenAI)
├── setup.sh                # LLM branch setup script
├── start.sh                # Quick start script
├── .env                    # Environment configuration
├── README.md               # This file
├── venv/                   # Virtual environment
└── bavarian_recommendations.db  # SQLite database
```

## Differences from Main Branch

| Feature | Main Branch | LLM Branch |
|---------|-------------|------------|
| **Recommendation Engine** | Scikit-learn ML | OpenAI GPT-4 |
| **Input Type** | Beverage characteristics | Personal preferences |
| **Cultural Knowledge** | Generic quality | Bavarian traditions |
| **UI Theme** | Standard | Bavarian blue/gold |
| **Database** | beverage_data.db | bavarian_recommendations.db |
| **Output** | Quality rating | Cultural recommendations |

## Fallback System

If OpenAI API is unavailable:
- System provides traditional Bavarian recommendations
- Based on preference patterns and cultural knowledge
- Ensures continuous functionality without external dependencies

## Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/bavarian-enhancement`
3. Make changes respecting Bavarian cultural authenticity
4. Test with various preference combinations
5. Submit pull request

## Traditional Bavarian Expressions

The system incorporates authentic Bavarian expressions:
- **Prost!** - Cheers!
- **Grüß Gott!** - Traditional Bavarian greeting
- **Gemütlichkeit** - Cozy, friendly atmosphere
- **Auf geht's!** - Let's go!
- **Auf Wiedersehen!** - Goodbye!

## License

This project is open source and available under the MIT License.

---

**Prost! Enjoy discovering the rich beverage culture of Bavaria! 🍺🥨**
