import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import sqlite3
import os

class BeverageClassifier:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = [
            'sweetness', 'acidity', 'bitterness', 'carbonation', 
            'alcohol_content', 'temperature', 'clarity', 'aroma_intensity'
        ]
        self.quality_labels = ['Poor', 'Fair', 'Good', 'Excellent']
        
    def generate_synthetic_data(self, n_samples=1000):
        """Generate synthetic beverage data"""
        np.random.seed(42)
        
        data = []
        for _ in range(n_samples):
            # Generate features with some correlation to quality
            sweetness = np.random.uniform(0, 10)
            acidity = np.random.uniform(0, 10)
            bitterness = np.random.uniform(0, 10)
            carbonation = np.random.uniform(0, 10)
            alcohol_content = np.random.uniform(0, 15)
            temperature = np.random.uniform(0, 25)  # Celsius
            clarity = np.random.uniform(0, 10)
            aroma_intensity = np.random.uniform(0, 10)
            
            # Create quality based on feature combinations
            quality_score = (
                sweetness * 0.15 +
                (10 - acidity) * 0.1 +  # Lower acidity often better
                (10 - bitterness) * 0.1 +
                carbonation * 0.1 +
                clarity * 0.2 +
                aroma_intensity * 0.15 +
                (alcohol_content / 15) * 0.1 +
                (25 - temperature) / 25 * 0.1  # Cooler is often better
            ) * 10
            
            # Add some noise
            quality_score += np.random.normal(0, 1)
            
            # Convert to categorical quality
            if quality_score < 3:
                quality = 0  # Poor
            elif quality_score < 5:
                quality = 1  # Fair
            elif quality_score < 7:
                quality = 2  # Good
            else:
                quality = 3  # Excellent
            
            data.append([
                sweetness, acidity, bitterness, carbonation,
                alcohol_content, temperature, clarity, aroma_intensity, quality
            ])
        
        columns = self.feature_names + ['quality']
        return pd.DataFrame(data, columns=columns)
    
    def train_model(self, data):
        """Train the classification model"""
        X = data[self.feature_names]
        y = data['quality']
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model = RandomForestClassifier(
            n_estimators=100, 
            random_state=42,
            max_depth=10
        )
        self.model.fit(X_train_scaled, y_train)
        
        # Calculate accuracy
        accuracy = self.model.score(X_test_scaled, y_test)
        print(f"Model accuracy: {accuracy:.3f}")
        
        return accuracy
    
    def predict(self, features):
        """Predict beverage quality"""
        if self.model is None:
            raise ValueError("Model not trained yet!")
        
        # Convert to DataFrame if it's a list
        if isinstance(features, list):
            features = pd.DataFrame([features], columns=self.feature_names)
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Make prediction
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        return {
            'quality': self.quality_labels[prediction],
            'quality_index': int(prediction),
            'probabilities': {
                label: float(prob) for label, prob in zip(self.quality_labels, probabilities)
            }
        }
    
    def save_model(self, model_path='models'):
        """Save the trained model"""
        os.makedirs(model_path, exist_ok=True)
        joblib.dump(self.model, f'{model_path}/beverage_classifier.pkl')
        joblib.dump(self.scaler, f'{model_path}/scaler.pkl')
    
    def load_model(self, model_path='models'):
        """Load a trained model"""
        self.model = joblib.load(f'{model_path}/beverage_classifier.pkl')
        self.scaler = joblib.load(f'{model_path}/scaler.pkl')

def init_database():
    """Initialize the SQLite database"""
    conn = sqlite3.connect('beverage_data.db')
    cursor = conn.cursor()
    
    # Create table for beverage data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS beverages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sweetness REAL,
            acidity REAL,
            bitterness REAL,
            carbonation REAL,
            alcohol_content REAL,
            temperature REAL,
            clarity REAL,
            aroma_intensity REAL,
            quality INTEGER,
            quality_label TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create table for predictions
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sweetness REAL,
            acidity REAL,
            bitterness REAL,
            carbonation REAL,
            alcohol_content REAL,
            temperature REAL,
            clarity REAL,
            aroma_intensity REAL,
            predicted_quality INTEGER,
            predicted_quality_label TEXT,
            confidence REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def store_beverage_data(data):
    """Store beverage data in database"""
    conn = sqlite3.connect('beverage_data.db')
    
    # Convert quality index to label
    quality_labels = ['Poor', 'Fair', 'Good', 'Excellent']
    data['quality_label'] = data['quality'].map(lambda x: quality_labels[x])
    
    data.to_sql('beverages', conn, if_exists='append', index=False)
    conn.close()

def store_prediction(features, prediction):
    """Store prediction in database"""
    conn = sqlite3.connect('beverage_data.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO predictions (
            sweetness, acidity, bitterness, carbonation,
            alcohol_content, temperature, clarity, aroma_intensity,
            predicted_quality, predicted_quality_label, confidence
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        features[0], features[1], features[2], features[3],
        features[4], features[5], features[6], features[7],
        prediction['quality_index'], prediction['quality'],
        max(prediction['probabilities'].values())
    ))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # Initialize database
    init_database()
    
    # Create and train model
    classifier = BeverageClassifier()
    
    print("Generating synthetic data...")
    data = classifier.generate_synthetic_data(n_samples=2000)
    
    print("Training model...")
    accuracy = classifier.train_model(data)
    
    print("Saving model...")
    classifier.save_model()
    
    print("Storing training data in database...")
    store_beverage_data(data)
    
    print(f"Setup complete! Model accuracy: {accuracy:.3f}")
    
    # Test prediction
    test_features = [7.5, 3.2, 2.1, 8.0, 5.5, 4.0, 9.0, 8.5]
    prediction = classifier.predict(test_features)
    print(f"Test prediction: {prediction}")
