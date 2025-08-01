"""
Demo script showing how to use the Beverage Quality Classifier API
"""

import requests
import json
import time

# API Configuration
API_BASE_URL = "http://localhost:8000"

def test_api_connection():
    """Test if the API is running"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ API is running and healthy")
            return True
        else:
            print("❌ API is not healthy")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure it's running on port 8000")
        return False
    except requests.exceptions.Timeout:
        print("❌ API connection timeout")
        return False

def get_feature_info():
    """Get information about features"""
    response = requests.get(f"{API_BASE_URL}/feature-info")
    return response.json()

def predict_beverage_quality(features):
    """Make a prediction"""
    response = requests.post(f"{API_BASE_URL}/predict", json=features)
    return response.json()

def demo_predictions():
    """Run demo predictions with different beverage profiles"""
    
    # Sample beverages
    beverages = [
        {
            "name": "Premium Craft Beer",
            "features": {
                "sweetness": 3.0,
                "acidity": 4.5,
                "bitterness": 7.5,
                "carbonation": 8.0,
                "alcohol_content": 6.5,
                "temperature": 4.0,
                "clarity": 8.5,
                "aroma_intensity": 9.0
            }
        },
        {
            "name": "Fresh Orange Juice",
            "features": {
                "sweetness": 8.5,
                "acidity": 6.0,
                "bitterness": 1.0,
                "carbonation": 0.0,
                "alcohol_content": 0.0,
                "temperature": 8.0,
                "clarity": 7.0,
                "aroma_intensity": 8.0
            }
        },
        {
            "name": "Flat Soda",
            "features": {
                "sweetness": 9.0,
                "acidity": 3.0,
                "bitterness": 0.5,
                "carbonation": 1.0,
                "alcohol_content": 0.0,
                "temperature": 15.0,
                "clarity": 6.0,
                "aroma_intensity": 4.0
            }
        },
        {
            "name": "High-Quality Wine",
            "features": {
                "sweetness": 4.0,
                "acidity": 5.5,
                "bitterness": 3.0,
                "carbonation": 0.5,
                "alcohol_content": 12.5,
                "temperature": 16.0,
                "clarity": 9.5,
                "aroma_intensity": 9.5
            }
        },
        {
            "name": "Poor Quality Energy Drink",
            "features": {
                "sweetness": 10.0,
                "acidity": 8.0,
                "bitterness": 8.5,
                "carbonation": 9.0,
                "alcohol_content": 0.0,
                "temperature": 20.0,
                "clarity": 3.0,
                "aroma_intensity": 6.0
            }
        }
    ]
    
    print("\n" + "="*60)
    print("🥤 BEVERAGE QUALITY CLASSIFIER DEMO")
    print("="*60)
    
    for i, beverage in enumerate(beverages, 1):
        print(f"\n{i}. Testing: {beverage['name']}")
        print("-" * 40)
        
        # Show features
        print("Features:")
        for feature, value in beverage['features'].items():
            print(f"  • {feature.replace('_', ' ').title()}: {value}")
        
        # Make prediction
        try:
            prediction = predict_beverage_quality(beverage['features'])
            
            print(f"\n🎯 Prediction Results:")
            print(f"  • Quality: {prediction['quality']}")
            print(f"  • Confidence: {prediction['confidence']:.1%}")
            print(f"  • Quality Score: {prediction['quality_index'] + 1}/4")
            
            print(f"\n📊 Probability Distribution:")
            for quality, prob in prediction['probabilities'].items():
                bar = "█" * int(prob * 20)  # Visual bar
                print(f"  • {quality:9}: {prob:.1%} {bar}")
            
        except Exception as e:
            print(f"❌ Error making prediction: {e}")
        
        print()

def interactive_demo():
    """Interactive demo where user can input features"""
    print("\n" + "="*60)
    print("🔬 INTERACTIVE BEVERAGE QUALITY PREDICTION")
    print("="*60)
    print("Enter beverage characteristics (0-10 scale, except where noted):")
    
    try:
        features = {}
        features['sweetness'] = float(input("Sweetness (0-10): "))
        features['acidity'] = float(input("Acidity (0-10): "))
        features['bitterness'] = float(input("Bitterness (0-10): "))
        features['carbonation'] = float(input("Carbonation (0-10): "))
        features['alcohol_content'] = float(input("Alcohol Content % (0-15): "))
        features['temperature'] = float(input("Temperature °C (0-25): "))
        features['clarity'] = float(input("Clarity (0-10): "))
        features['aroma_intensity'] = float(input("Aroma Intensity (0-10): "))
        
        print("\n🔮 Making prediction...")
        prediction = predict_beverage_quality(features)
        
        print(f"\n🎯 Your beverage quality prediction:")
        print(f"  • Quality: {prediction['quality']}")
        print(f"  • Confidence: {prediction['confidence']:.1%}")
        print(f"  • Quality Score: {prediction['quality_index'] + 1}/4")
        
        print(f"\n📊 Detailed probabilities:")
        for quality, prob in prediction['probabilities'].items():
            print(f"  • {quality}: {prob:.1%}")
        
    except ValueError:
        print("❌ Invalid input. Please enter numeric values.")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("🥤 Beverage Quality Classifier API Demo")
    print("=" * 50)
    
    # Test API connection
    if not test_api_connection():
        print("\n💡 To start the API, run: python api.py")
        return
    
    # Get feature information
    try:
        feature_info = get_feature_info()
        print(f"\n📋 Available features: {len(feature_info['features'])}")
        print(f"📊 Quality levels: {', '.join(feature_info['quality_labels'])}")
    except Exception as e:
        print(f"❌ Error getting feature info: {e}")
        return
    
    # Menu
    while True:
        print("\n" + "="*40)
        print("Choose an option:")
        print("1. Run demo predictions")
        print("2. Interactive prediction")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            demo_predictions()
        elif choice == "2":
            interactive_demo()
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
