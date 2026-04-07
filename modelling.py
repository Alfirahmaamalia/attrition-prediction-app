"""
modelling.py - Model training dengan MLflow tracking
"""
import os
import sys
import numpy as np
import pandas as pd
import mlflow
import mlflow.sklearn
from dotenv import load_dotenv
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

# Load environment variables
load_dotenv()

# Configuration
DAGSHUB_USERNAME = "Alfirahmaamalia"
DAGSHUB_TOKEN = "0c17740769ba0ad2bbd3571d3cbc214816579a02"
# MLflow Authentication Injection
os.environ["MLFLOW_TRACKING_USERNAME"] = DAGSHUB_USERNAME
os.environ["MLFLOW_TRACKING_PASSWORD"] = DAGSHUB_TOKEN

MLFLOW_TRACKING_URI = f"https://dagshub.com/{DAGSHUB_USERNAME}/attrition-prediction.mlflow"
EXPERIMENT_NAME = "attrition-prediction"
DATA_PATH = os.getenv("DATA_PATH", "attrition_final_fikss.csv")
MODEL_PATH = os.getenv("MODEL_PATH", "models/model.pkl")

def setup_mlflow():
    """Setup tracking URI spesifik ke DagsHub"""
    try:
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        print(f"MLflow dihubungkan ke: {MLFLOW_TRACKING_URI}")
    except Exception as e:
        print(f"Warning: Gagal menghubungkan ke MLflow: {e}")



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
        selected_features = ['Age', 'MonthlyIncome', 'YearsAtCompany', 'YearsWithCurrManager', 
                             'Department', 'JobRole', 'MaritalStatus', 'OverTime',
                             'Gender', 'JobSatisfaction', 'EnvironmentSatisfaction']
        
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
    """Train Random Forest model dgn Tracking MLflow ke DagsHub"""
    try:
        setup_mlflow()
        mlflow.set_experiment(EXPERIMENT_NAME)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        
        # Scaling
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        with mlflow.start_run(run_name="RandomForest_Run"):
            # Log params
            mlflow.log_params({
                "model_type": "RandomForest",
                "n_estimators": n_estimators,
                "test_size": test_size,
                "random_state": random_state,
                "input_features": len(X.columns)
            })

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
            probabilities = model.predict_proba(X_test_scaled)
            
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
            mlflow.log_metrics(metrics)
            
            # Tambahkan Deskripsi Run
            mlflow.set_tag("mlflow.note.content", "Model Random Forest untuk memprediksi probabilitas Attrition karyawan menggunakan 11 fitur dataset IBM HR.")
            
            # Save model secara resmi ke MLflow Model Registry
            from mlflow.models.signature import infer_signature
            signature = infer_signature(X_test_scaled, y_pred)
            
            mlflow.sklearn.log_model(
                sk_model=model,
                artifact_path="model",
                signature=signature,
                registered_model_name="attrition_model"
            )
            
            # Save model locally untuk keperluan Flask Web App
            os.makedirs(os.path.dirname(MODEL_PATH) or ".", exist_ok=True)
            joblib.dump(model, MODEL_PATH)
            
            # Save scaler
            scaler_path = MODEL_PATH.replace(".pkl", "_scaler.pkl")
            joblib.dump(scaler, scaler_path)
            
            print(f"\n{'='*50}")
            print(f"Model Training Complete!")
            print(f"Log berhasil di-push ke DagsHub Experiments!")
            print(f"{'='*50}")
            print(f"Accuracy:  {accuracy:.4f}")
            print(f"Precision: {precision:.4f}")
            print(f"Recall:    {recall:.4f}")
            print(f"F1-Score:  {f1:.4f}")
            print(f"{'='*50}")
            
            return model, scaler, metrics
            
    except Exception as e:
        print(f"Error in training: {e}")
        import traceback
        traceback.print_exc()
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
        probabilities = model.predict_proba(df_scaled)
        
        # Probabilitas kelas 1 (Attrition = Yes)
        attrition_prob = probabilities[0][1] * 100
        
        return {
            "prediction": "Yes" if prediction[0] == 1 else "No",
            "probability": f"{attrition_prob:.2f}%"
        }
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