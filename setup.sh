#!/bin/bash

echo "🍺 Bavarian Beverage Recommender (LLM Branch) - Setup Script"
echo "==========================================================="

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

# Initialize the LLM recommender and database
echo "🤖 Setting up LLM-based recommender..."
python llm_recommender.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To run the Bavarian Beverage Recommender:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Start the API server: python llm_api.py"
echo "3. In another terminal, start Streamlit: streamlit run streamlit_app.py"
echo ""
echo "📊 The Streamlit app will be available at: http://localhost:8501"
echo "🔧 The API will be available at: http://localhost:8000"
echo ""
echo "🔑 IMPORTANT: Set your OpenAI API key in the .env file for full functionality"
echo "💡 Or simply run: ./start.sh (after setup)"
