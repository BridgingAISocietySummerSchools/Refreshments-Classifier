#!/bin/bash

echo "🍺 Starting Bavarian Beverage Recommender (LLM Branch)"
echo "===================================================="

# Activate virtual environment
if [ -d "venv" ]; then
    echo "🔌 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Running setup first..."
    ./setup.sh
    source venv/bin/activate
fi

# Check if database exists
if [ ! -f "bavarian_recommendations.db" ]; then
    echo "⚠️  Database not found. Initializing..."
    python llm_recommender.py
fi

echo ""
echo "🔧 Starting LLM API server..."
python llm_api.py &
API_PID=$!

# Wait a moment for API to start
sleep 3

echo "🎨 Starting Bavarian Streamlit app..."
streamlit run streamlit_app.py &
STREAMLIT_PID=$!

echo ""
echo "✅ Bavarian applications started!"
echo "🍺 Streamlit app: http://localhost:8501"
echo "🔧 API server: http://localhost:8000"
echo ""
echo "🔑 Remember to set your OpenAI API key in .env for full functionality"
echo "Press Ctrl+C to stop all services"

# Wait for interrupt signal
trap "echo 'Auf Wiedersehen! Stopping services...'; kill $API_PID $STREAMLIT_PID; exit" INT
wait
