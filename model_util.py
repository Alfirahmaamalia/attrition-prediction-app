"""
model_util.py - Utility functions for loading and managing ML models
"""
import os
import joblib
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

LOCAL_MODEL_PATH = os.getenv("LOCAL_MODEL_PATH", "models/model.pkl")

def load_model_from_local(model_path: str = None):
    """
    Load model dari file lokal
    """
    try:
        if model_path is None:
            model_path = LOCAL_MODEL_PATH
        
        if not os.path.exists(model_path):
            print(f"Model file not found: {model_path}")
            return None
        
        model = joblib.load(model_path)
        print(f"Model loaded successfully from local file: {model_path}")
        return model
    except Exception as e:
        print(f"Error loading model from local file: {e}")
        return None

def get_model(use_local: bool = True):
    """
    Get model dari local
    """
    return load_model_from_local()

def get_feature_names():
    features = [
        'Age',
        'MonthlyIncome',
        'YearsAtCompany',
        'YearsInCurrentRole',
        'YearsWithCurrManager',
        'Department',
        'JobRole',
        'MaritalStatus',
        'OverTime',
    ]
    return features

if __name__ == "__main__":
    # Test loading model
    print("Testing model loading...")
    
    model = get_model()
    
    if model:
        print("Model loaded successfully!")
        print(f"Model type: {type(model)}")
        print(f"Features: {get_feature_names()}")
    else:
        print("Failed to load model")
