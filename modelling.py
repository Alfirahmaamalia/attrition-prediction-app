"""
modelling.py - Model training dengan MLflow tracking
"""
import os
import sys
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

# Load environment variables
load_dotenv()

# Configuration
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
DAGSHUB_USERNAME = os.getenv("DAGSHUB_USERNAME")
DAGSHUB_TOKEN = os.getenv("DAGSHUB_TOKEN")
EXPERIMENT_NAME = "attrition-prediction"
DATA_PATH = os.getenv("DATA_PATH", "attrition_final_fikss.csv")
MODEL_PATH = os.getenv("MODEL_PATH", "models/model.pkl")



def load_data(data_path: str = DATA_PATH):
    """Load dataset"""
    try:
        df = pd.read_csv(data_path)
        print(f"Data loaded: {data_path}")
        print(f"Shape: {df.shape}")
        return df
    except FileNotFoundError:
        print(f"Error: Data file not found at {data_path}")
        return None

def preprocess_data(df):
    """Preprocessing dan feature engineering"""
    try:
        # Copy dataframe
        df_processed = df.copy()
        
        # Handle missing values (jika ada)
        df_processed = df_processed.dropna()
        
        # Pisahkan features dan target
        # Sesuaikan nama kolom target dengan dataset Anda
        target_column = 'Attrition'  # Ubah jika nama kolom berbeda
        
        if target_column not in df_processed.columns:
            print(f"Warning: Target column '{target_column}' not found in data")
            print(f"Available columns: {df_processed.columns.tolist()}")
            return None, None, None
        
        # Hanya gunakan fitur yang ada di web form HTML
        selected_features = ['Age', 'MonthlyIncome', 'YearsAtCompany', 'YearsInCurrentRole', 
                             'YearsWithCurrManager', 'Department', 'JobRole', 'MaritalStatus', 'OverTime']
        
        X = df_processed[selected_features]
        y = df_processed[target_column]
        
        # Konversi fitur kategorikal ke numerik (One-Hot Encoding)
        X = pd.get_dummies(X, drop_first=True)
        
        # Convert categorical target to binary (0/1) jika perlu
        if y.dtype == 'object':
            y = (y == 'Yes').astype(int)
        
        print(f"Features shape: {X.shape}")
        print(f"Target shape: {y.shape}")
        
        return X, y, df_processed.columns.tolist()
    except Exception as e:
        print(f"Error in preprocessing: {e}")
        return None, None, None

def train_model(X, y, test_size=0.2, random_state=42, n_estimators=100):
    """Train Random Forest model"""
    try:
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Scaling
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        print("Training Random Forest model...")
        model = RandomForestClassifier(
            n_estimators=n_estimators,
            random_state=random_state,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2
        )
        model.fit(X_train_scaled, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test_scaled)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        metrics = {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1_score": f1
        }
        
        # Save model locally
        os.makedirs(os.path.dirname(MODEL_PATH) or ".", exist_ok=True)
        joblib.dump(model, MODEL_PATH)
        
        # Save scaler
        scaler_path = MODEL_PATH.replace(".pkl", "_scaler.pkl")
        joblib.dump(scaler, scaler_path)
        
        print(f"\n{'='*50}")
        print(f"Model Training Complete!")
        print(f"{'='*50}")
        print(f"Accuracy:  {accuracy:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall:    {recall:.4f}")
        print(f"F1-Score:  {f1:.4f}")
        print(f"{'='*50}")
        
        return model, scaler, metrics
            
    except Exception as e:
        print(f"Error in training: {e}")
        return None, None, None

def predict(input_data):
    """
    Make predictions using the trained model
    
    Args:
        input_data: Input data untuk prediksi (berupa dictionary)
    
    Returns:
        Prediction result
    """
    try:
        from model_util import get_model
        import pandas as pd
        import joblib
        
        model = get_model(use_local=True)
        if model is None:
            return "Error: Model not found"
        
        # Konversi input dict dari Flask ke DataFrame dan OHE
        df_input = pd.DataFrame([input_data])
        df_input = pd.get_dummies(df_input, drop_first=True)
        
        # Standarisasi nilai fitur & Ambil referensi kolom aslinya
        scaler_path = MODEL_PATH.replace(".pkl", "_scaler.pkl")
        scaler = joblib.load(scaler_path)
        
        # Samakan kolom input dengan model referensi training
        expected_cols = scaler.feature_names_in_
        for col in expected_cols:
            if col not in df_input.columns:
                df_input[col] = 0
        df_input = df_input[expected_cols]
        
        # Eksekusi Transform & Prediksi
        df_scaled = scaler.transform(df_input)
        prediction = model.predict(df_scaled)
        
        return f"Attrition: {'Yes' if prediction[0] == 1 else 'No'}"
    except Exception as e:
        print(f"Error in prediction: {e}")
        import traceback
        traceback.print_exc()
        return f"Error: {str(e)}"

if __name__ == "__main__":
    print("Starting model training pipeline...")
    
    # Load data
    df = load_data()
    if df is None:
        sys.exit(1)
    
    # Preprocess
    X, y, columns = preprocess_data(df)
    if X is None:
        sys.exit(1)
    
    # Train
    model, scaler, metrics = train_model(X, y)
    
    if model is not None:
        print("\nModel training successful!")
    else:
        print("\nModel training failed!")
        sys.exit(1)