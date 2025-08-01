#!/bin/bash

echo "🥤 Beverage Quality Classifier - Setup Script"
echo "=============================================="

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📦 Installing Python packages..."
pip install -r requirements.txt

# Train the ML model and set up database
echo "🤖 Training machine learning model..."
python ml_classifier.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To run the application:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Start the API server: python api.py"
echo "3. In another terminal, start Streamlit: streamlit run streamlit_app.py"
echo ""
echo "📊 The Streamlit app will be available at: http://localhost:8501"
echo "🔧 The API will be available at: http://localhost:8000"
echo ""
echo "💡 Or simply run: ./start.sh (after setup)"
