from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
from ml_classifier import BeverageClassifier, store_prediction
import os

app = FastAPI(title="Beverage Quality Classifier API", version="1.0.0")

# Global classifier instance
classifier = BeverageClassifier()

class BeverageFeatures(BaseModel):
    sweetness: float
    acidity: float
    bitterness: float
    carbonation: float
    alcohol_content: float
    temperature: float
    clarity: float
    aroma_intensity: float

class PredictionResponse(BaseModel):
    quality: str
    quality_index: int
    probabilities: dict
    confidence: float

@app.on_event("startup")
async def startup_event():
    """Load the trained model on startup"""
    try:
        if os.path.exists('models/beverage_classifier.pkl'):
            classifier.load_model()
            print("Model loaded successfully!")
        else:
            print("No trained model found. Please run ml_classifier.py first.")
    except Exception as e:
        print(f"Error loading model: {e}")

@app.get("/")
async def root():
    return {"message": "Beverage Quality Classifier API", "version": "1.0.0"}

@app.post("/predict", response_model=PredictionResponse)
async def predict_quality(features: BeverageFeatures):
    """Predict beverage quality based on features"""
    try:
        # Convert features to list
        feature_list = [
            features.sweetness,
            features.acidity,
            features.bitterness,
            features.carbonation,
            features.alcohol_content,
            features.temperature,
            features.clarity,
            features.aroma_intensity
        ]
        
        # Make prediction
        prediction = classifier.predict(feature_list)
        
        # Store prediction in database
        store_prediction(feature_list, prediction)
        
        # Calculate confidence as the max probability
        confidence = max(prediction['probabilities'].values())
        
        return PredictionResponse(
            quality=prediction['quality'],
            quality_index=prediction['quality_index'],
            probabilities=prediction['probabilities'],
            confidence=confidence
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    model_loaded = classifier.model is not None
    return {
        "status": "healthy" if model_loaded else "unhealthy",
        "model_loaded": model_loaded
    }

@app.get("/feature-info")
async def get_feature_info():
    """Get information about the features"""
    return {
        "features": {
            "sweetness": {"range": [0, 10], "description": "Sweetness level of the beverage"},
            "acidity": {"range": [0, 10], "description": "Acidity level of the beverage"},
            "bitterness": {"range": [0, 10], "description": "Bitterness level of the beverage"},
            "carbonation": {"range": [0, 10], "description": "Carbonation level of the beverage"},
            "alcohol_content": {"range": [0, 15], "description": "Alcohol content percentage"},
            "temperature": {"range": [0, 25], "description": "Serving temperature in Celsius"},
            "clarity": {"range": [0, 10], "description": "Clarity/transparency of the beverage"},
            "aroma_intensity": {"range": [0, 10], "description": "Intensity of the beverage's aroma"}
        },
        "quality_labels": ["Poor", "Fair", "Good", "Excellent"]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
