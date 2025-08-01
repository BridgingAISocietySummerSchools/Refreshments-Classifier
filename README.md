# Beverage Quality Classifier 🥤

A machine learning web application that classifies beverage quality based on various characteristics. Built with Streamlit for the frontend, FastAPI for the backend, and scikit-learn for machine learning.

## Features

- **🤖 Machine Learning Classifier**: Random Forest model trained on synthetic beverage data
- **🎨 Interactive Frontend**: Streamlit web interface with sliders for feature input
- **🔧 REST API**: FastAPI backend for serving predictions
- **💾 Database Storage**: SQLite database for storing training data and predictions
- **📊 Visualizations**: Interactive charts showing feature profiles and prediction probabilities
- **📈 Statistics Dashboard**: View database statistics and quality distributions

## Beverage Features Analyzed

- **Sweetness** (0-10): How sweet the beverage tastes
- **Acidity** (0-10): Level of acidity
- **Bitterness** (0-10): Level of bitterness
- **Carbonation** (0-10): Amount of carbonation/fizziness
- **Alcohol Content** (0-15%): Percentage of alcohol by volume
- **Temperature** (0-25°C): Serving temperature
- **Clarity** (0-10): How clear/transparent the beverage is
- **Aroma Intensity** (0-10): Strength of the beverage's aroma

## Quality Classifications

- **Poor**: Below average quality, needs significant improvement
- **Fair**: Acceptable quality with room for improvement
- **Good**: Above average quality, quite enjoyable
- **Excellent**: Outstanding quality with exceptional characteristics

## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Refreshments-Classifier
   ```

2. **Run the setup script**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

   Or manually:
   ```bash
   pip install -r requirements.txt
   python ml_classifier.py
   ```

## Usage

### 1. Start the API Server
```bash
python api.py
```
The API will be available at `http://localhost:8000`

### 2. Start the Streamlit App
In a new terminal:
```bash
streamlit run streamlit_app.py
```
The web interface will be available at `http://localhost:8501`

### 3. Using the Application

1. **Navigate to the Classifier page**
2. **Adjust the sliders** to match your beverage's characteristics
3. **Click "Predict Quality"** to get the classification
4. **View results** including:
   - Quality prediction (Poor/Fair/Good/Excellent)
   - Confidence level
   - Probability distribution across all quality levels
   - Feature profile radar chart

## API Endpoints

- `GET /`: API information
- `POST /predict`: Predict beverage quality
- `GET /health`: Health check
- `GET /feature-info`: Get feature information and ranges

### Example API Usage

```python
import requests

# Predict quality
features = {
    "sweetness": 7.5,
    "acidity": 3.2,
    "bitterness": 2.1,
    "carbonation": 8.0,
    "alcohol_content": 5.5,
    "temperature": 4.0,
    "clarity": 9.0,
    "aroma_intensity": 8.5
}

response = requests.post("http://localhost:8000/predict", json=features)
prediction = response.json()
print(f"Quality: {prediction['quality']}")
print(f"Confidence: {prediction['confidence']:.2%}")
```

## Project Structure

```
Refreshments-Classifier/
├── ml_classifier.py      # Machine learning model and data generation
├── api.py               # FastAPI backend server
├── streamlit_app.py     # Streamlit frontend application
├── requirements.txt     # Python dependencies
├── setup.sh            # Setup script
├── README.md           # This file
├── models/             # Saved ML models (created after training)
│   ├── beverage_classifier.pkl
│   └── scaler.pkl
└── beverage_data.db    # SQLite database (created after setup)
```

## Technical Details

### Machine Learning Model
- **Algorithm**: Random Forest Classifier
- **Features**: 8 numerical features representing beverage characteristics
- **Target**: 4-class quality classification
- **Training Data**: 2000 synthetic samples with realistic feature correlations

### Data Generation
The synthetic data is generated with realistic correlations between features and quality:
- Higher clarity and aroma intensity correlate with better quality
- Extreme values in acidity or bitterness may reduce quality
- Optimal temperature ranges enhance quality
- Balanced feature combinations result in higher quality ratings

### Database Schema
- **beverages**: Training data with features and quality labels
- **predictions**: User predictions with timestamps and confidence scores

## Future Enhancements

- [ ] Add real beverage data collection
- [ ] Implement model retraining functionality
- [ ] Add data export capabilities
- [ ] Include more beverage types and categories
- [ ] Add user authentication and personal prediction history
- [ ] Implement A/B testing for model improvements

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.
