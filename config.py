# Application Configuration
API_HOST = "localhost"
API_PORT = 8000
STREAMLIT_PORT = 8501

# Database Configuration
DATABASE_NAME = "beverage_data.db"

# Model Configuration
MODEL_DIR = "models"
MODEL_NAME = "beverage_classifier.pkl"
SCALER_NAME = "scaler.pkl"

# Data Configuration
SYNTHETIC_DATA_SIZE = 2000
RANDOM_SEED = 42

# Feature Configuration
FEATURE_NAMES = [
    'sweetness', 
    'acidity', 
    'bitterness', 
    'carbonation',
    'alcohol_content', 
    'temperature', 
    'clarity', 
    'aroma_intensity'
]

FEATURE_RANGES = {
    'sweetness': (0, 10),
    'acidity': (0, 10),
    'bitterness': (0, 10),
    'carbonation': (0, 10),
    'alcohol_content': (0, 15),
    'temperature': (0, 25),
    'clarity': (0, 10),
    'aroma_intensity': (0, 10)
}

QUALITY_LABELS = ['Poor', 'Fair', 'Good', 'Excellent']

# Model Parameters
MODEL_PARAMS = {
    'n_estimators': 100,
    'max_depth': 10,
    'random_state': RANDOM_SEED
}
