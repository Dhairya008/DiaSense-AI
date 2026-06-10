import pickle
import numpy as np
import pandas as pd
import os

# Define relative paths for model files
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'diabetes_model.pkl')
SCALER_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'scaler.pkl')

def load_model_and_scaler():
    """
    Loads and returns the serialized diabetes model and StandardScaler.
    """
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model not found at: {MODEL_PATH}")
    if not os.path.exists(SCALER_PATH):
        raise FileNotFoundError(f"Scaler not found at: {SCALER_PATH}")
        
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)
        
    return model, scaler

def predict_risk(input_data):
    """
    Takes a dictionary or list of raw feature inputs, scales them,
    and runs prediction on the loaded model.
    
    input_data structure:
    {
        'Pregnancies': value,
        'Glucose': value,
        'BloodPressure': value,
        'SkinThickness': value,
        'Insulin': value,
        'BMI': value,
        'DiabetesPedigreeFunction': value,
        'Age': value
    }
    
    Returns:
        dict: containing prediction (0 or 1), probability, risk percentage, and risk category.
    """
    model, scaler = load_model_and_scaler()
    
    # Feature columns in correct order
    features = [
        'Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
        'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age'
    ]
    
    # Format input into a DataFrame
    if isinstance(input_data, dict):
        df_input = pd.DataFrame([input_data])[features]
    elif isinstance(input_data, list):
        df_input = pd.DataFrame([input_data], columns=features)
    else:
        raise ValueError("Input data must be a dictionary or a list.")
        
    # Scale input
    scaled_input = scaler.transform(df_input)
    scaled_input_df = pd.DataFrame(scaled_input, columns=features)
    
    # Predict
    prediction = int(model.predict(scaled_input_df)[0])
    probability = float(model.predict_proba(scaled_input_df)[0, 1])
    
    # Risk percentage and category
    risk_pct = round(probability * 100, 2)
    
    # Risk Categories:
    # 0-30% = Low Risk
    # 31-70% = Medium Risk
    # 71-100% = High Risk
    if risk_pct <= 30.0:
        risk_category = "Low Risk"
    elif risk_pct <= 70.0:
        risk_category = "Medium Risk"
    else:
        risk_category = "High Risk"
        
    return {
        'prediction': prediction,
        'probability': probability,
        'risk_percentage': risk_pct,
        'risk_category': risk_category,
        'scaled_features_df': scaled_input_df
    }

if __name__ == "__main__":
    # Test script locally
    mock_input = {
        'Pregnancies': 2,
        'Glucose': 130,
        'BloodPressure': 74,
        'SkinThickness': 26,
        'Insulin': 110,
        'BMI': 28.5,
        'DiabetesPedigreeFunction': 0.35,
        'Age': 35
    }
    
    print("Testing Prediction Module...")
    try:
        results = predict_risk(mock_input)
        print("Prediction outputs:")
        print(f"Prediction class: {results['prediction']}")
        print(f"Probability: {results['probability']:.4f}")
        print(f"Risk percentage: {results['risk_percentage']}%")
        print(f"Risk category: {results['risk_category']}")
        print("[OK] Prediction Module test passed successfully!")
    except Exception as e:
        print(f"Prediction Module test failed: {e}")
