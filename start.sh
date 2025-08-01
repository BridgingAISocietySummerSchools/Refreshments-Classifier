#!/bin/bash

echo "🚀 Starting Beverage Quality Classifier"
echo "======================================="

# Activate virtual environment
if [ -d "venv" ]; then
    echo "🔌 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Running setup first..."
    ./setup.sh
    source venv/bin/activate
fi

# Check if models exist
if [ ! -f "models/beverage_classifier.pkl" ]; then
    echo "⚠️  Models not found. Training model..."
    python ml_classifier.py
fi

echo ""
echo "🔧 Starting API server..."
python api.py &
API_PID=$!

# Wait a moment for API to start
sleep 3

echo "🎨 Starting Streamlit app..."
streamlit run streamlit_app.py &
STREAMLIT_PID=$!

echo ""
echo "✅ Applications started!"
echo "📊 Streamlit app: http://localhost:8501"
echo "🔧 API server: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt signal
trap "echo 'Stopping services...'; kill $API_PID $STREAMLIT_PID; exit" INT
wait
