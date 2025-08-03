# Refreshments Classifier - LLM Branch 🍺

A simple and elegant Bavarian beverage recommendation system powered by AI. Get personalized drink recommendations with authentic cultural context, all wrapped in a charming Bavarian-themed interface.

## Features

### 🤖 Smart AI Recommendations
- **OpenAI GPT-4 Integration**: Advanced AI for personalized suggestions
- **Local Fallback System**: Works even without an API key using built-in knowledge
- **Cultural Context**: Authentic Bavarian beverage traditions and stories
- **Beginner Friendly**: Perfect for newcomers to Bavarian drinks

### 🍻 Authentic Bavarian Experience
- **Traditional Beverages**: 20+ authentic Bavarian drinks including beers, spirits, and non-alcoholic options
- **Cultural Stories**: Learn about brewery histories and regional specialties
- **Seasonal Awareness**: Recommendations that match the time of year
- **Gemütlichkeit**: Captures the warm, friendly Bavarian drinking culture

### 🎨 Clean & Simple Interface
- **Streamlit Frontend**: Easy-to-use web interface with Bavarian blue and gold theming
- **Single Page Design**: No complex navigation, just preferences and recommendations
- **Mobile Friendly**: Works great on all devices
- **Fast & Responsive**: Quick recommendations in seconds

## Quick Start

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd Refreshments-Classifier
   git checkout llm
   chmod +x setup.sh start.sh
   ./setup.sh
   ```

2. **Start the application**:
   ```bash
   ./start.sh
   ```

3. **Visit the app**: Open `http://localhost:8502` in your browser

That's it! The system works out of the box with built-in beverage knowledge. For enhanced AI recommendations, you can optionally add an OpenAI API key.

## Optional: OpenAI API Key Setup

For the most sophisticated recommendations, create a `.env` file:

```bash
OPENAI_API_KEY=your-openai-api-key-here
```

Don't have an API key? No problem! The system includes a comprehensive local beverage database with intelligent matching.

## Manual Setup

If you prefer manual installation:

1. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the backend**:
   ```bash
   python llm_api.py
   ```

4. **Run the frontend** (in a new terminal):
   ```bash
   streamlit run streamlit_app.py --server.port 8502
   ```

## Usage

1. Visit `http://localhost:8502`
2. Fill out your beverage preferences
3. Click "Get My Bavarian Recommendation!"
4. Enjoy learning about traditional Bavarian drinks
5. Try different preference combinations to discover new beverages

## Beverage Categories

The system recommends from these authentic Bavarian categories:

### 🍺 Traditional Beers
- **Weissbier** - Bavaria's famous wheat beer
- **Märzen** - Classic Oktoberfest beer
- **Helles** - Light, crisp Munich lager
- **Maß** - The traditional 1-liter serving

### 🥃 Bavarian Spirits
- **Obstler** - Traditional fruit brandy
- **Enzian** - Unique gentian root schnapps
- **Bavarian Gin** - Modern craft distillery creations

### 🍹 Non-Alcoholic Specialties
- **Apfelschorle** - Apple juice with sparkling water
- **Spezi** - Traditional cola-orange mix
- **Various Schorles** - Refreshing fruit spritzers

### ☃️ Seasonal Drinks
- **Glühwein** - Warming mulled wine for winter
- **Maibock** - Strong spring celebration beer
- **Radler** - Perfect summer beer and lemonade mix

## Project Structure

```
Refreshments-Classifier/ (llm branch)
├── streamlit_app.py          # Bavarian-themed frontend
├── llm_api.py               # FastAPI backend
├── llm_recommender.py       # AI recommendation engine
├── bavarian_recommendations.db  # Local beverage database
├── requirements.txt         # Dependencies
├── setup.sh                # Setup script
├── start.sh                # Start script
├── config.py               # Configuration
└── README.md               # This file
```

## API Endpoints

The backend provides simple REST endpoints:

- `POST /recommend` - Get personalized recommendations
- `GET /` - Health check

## Configuration

The system is configured to work out of the box. Optional settings in `config.py`:

- OpenAI API configuration
- Database settings
- Port configurations

## Fallback System

When no OpenAI API key is provided, the system uses:
- Local beverage knowledge base
- Smart preference matching algorithms
- Cultural context from built-in database
- Traditional Bavarian recommendations

This ensures the app always works, regardless of API availability.

## Bavarian Cultural Notes

The system includes authentic Bavarian drinking culture:

- **Gemütlichkeit** - The cozy, friendly atmosphere central to Bavarian social life
- **Seasonal Traditions** - Oktoberfest, Maibock celebrations, winter warming drinks
- **Regional Specialties** - Knowledge of specific breweries and their histories
- **Proper Etiquette** - How to properly enjoy Bavarian beverages

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test the recommendation system
5. Submit a pull request

## Troubleshooting

**App won't start?**
- Make sure you're in the `llm` branch
- Run `chmod +x setup.sh start.sh` to make scripts executable
- Check that Python 3.8+ is installed

**No recommendations appearing?**
- Check that both services are running (API on port 8000, Streamlit on port 8502)
- Try refreshing the browser page
- Check the terminal for any error messages

## License

This project is open source and available under the MIT License.

---

**Prost! Enjoy discovering authentic Bavarian beverages! 🍺🥨**

*Experience the warmth and tradition of Bavaria, one recommendation at a time.*