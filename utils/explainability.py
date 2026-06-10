import shap
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
import sys

# Append parent directory to path to import utilities
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from prediction import load_model_and_scaler, predict_risk

def get_shap_explainer(model, X_train_scaled=None):
    """
    Creates and returns a SHAP explainer object appropriate for the given model type.
    """
    model_name = type(model).__name__
    
    # Tree explainer for Random Forest, Decision Tree, XGBoost
    if model_name in ['RandomForestClassifier', 'XGBClassifier', 'DecisionTreeClassifier']:
        explainer = shap.TreeExplainer(model)
    else:
        # Fallback to LinearExplainer or KernelExplainer
        if X_train_scaled is not None:
            explainer = shap.LinearExplainer(model, X_train_scaled)
        else:
            explainer = shap.Explainer(model)
            
    return explainer

def explain_prediction(input_data, X_train_scaled=None):
    """
    Computes SHAP explanation for a single user prediction.
    
    Returns:
        dict: containing shap_values, base_value, waterfall_fig, and explanation_text.
    """
    model, scaler = load_model_and_scaler()
    res = predict_risk(input_data)
    scaled_df = res['scaled_features_df']
    
    explainer = get_shap_explainer(model, X_train_scaled)
    
    # Calculate SHAP values
    shap_values_obj = explainer(scaled_df)
    
    # Determine base values and SHAP values for class 1 (diabetes risk)
    # TreeExplainer on RandomForest outputs probability arrays for both classes [p0, p1]
    # So we index class 1 (column index 1)
    if len(shap_values_obj.shape) == 3: # shape: (samples, features, classes)
        shap_values_for_sample = shap_values_obj.values[0, :, 1]
        base_value = shap_values_obj.base_values[0, 1]
    else:
        shap_values_for_sample = shap_values_obj.values[0]
        base_value = shap_values_obj.base_values[0]
        
    # Create Waterfall Plot Figure
    fig, ax = plt.subplots(figsize=(10, 4))
    
    # Reconstruct single sample Explanation object for waterfall plotting
    exp = shap.Explanation(
        values=shap_values_for_sample,
        base_values=base_value,
        data=scaled_df.iloc[0].values,
        feature_names=scaled_df.columns
    )
    
    shap.plots.waterfall(exp, show=False)
    plt.title('Patient Feature Risk Contributions (SHAP Waterfall)', fontsize=12, pad=15)
    plt.tight_layout()
    
    # Generate clinical narrative explanation
    # Map raw input values
    raw_vals = input_data if isinstance(input_data, dict) else dict(zip(scaled_df.columns, input_data))
    
    # Pair feature name, SHAP value, and raw value
    contributions = []
    for col, shap_val in zip(scaled_df.columns, shap_values_for_sample):
        contributions.append({
            'Feature': col,
            'SHAP': shap_val,
            'Raw': raw_vals[col]
        })
        
    df_contrib = pd.DataFrame(contributions)
    # Sort by absolute SHAP value to find top drivers
    df_contrib['AbsSHAP'] = df_contrib['SHAP'].abs()
    df_contrib = df_contrib.sort_values('AbsSHAP', ascending=False)
    
    # Generate text narrative
    narrative_points = []
    top_drivers = df_contrib.head(3)
    
    for _, row in top_drivers.iterrows():
        feat = row['Feature']
        shap_val = row['SHAP']
        raw_val = row['Raw']
        
        effect = "increases" if shap_val > 0 else "decreases"
        importance = "significantly" if abs(shap_val) > 0.05 else "moderately"
        
        if feat == 'Glucose':
            narrative_points.append(f"Glucose level of {raw_val} mg/dL {importance} {effect} diabetes risk.")
        elif feat == 'BMI':
            narrative_points.append(f"BMI of {raw_val} kg/m² {importance} {effect} diabetes risk.")
        elif feat == 'Age':
            narrative_points.append(f"Age of {raw_val} years {importance} {effect} diabetes risk.")
        elif feat == 'Pregnancies':
            narrative_points.append(f"Number of pregnancies ({raw_val}) {importance} {effect} diabetes risk.")
        elif feat == 'DiabetesPedigreeFunction':
            narrative_points.append(f"Diabetes Pedigree Function of {raw_val} {importance} {effect} diabetes risk.")
        elif feat == 'BloodPressure':
            narrative_points.append(f"Diastolic Blood Pressure of {raw_val} mmHg {importance} {effect} diabetes risk.")
        elif feat == 'Insulin':
            narrative_points.append(f"Insulin level of {raw_val} mu U/ml {importance} {effect} diabetes risk.")
        elif feat == 'SkinThickness':
            narrative_points.append(f"Triceps skinfold thickness of {raw_val} mm {importance} {effect} diabetes risk.")
            
    explanation_text = " ".join(narrative_points)
    
    return {
        'shap_values': shap_values_for_sample,
        'base_value': base_value,
        'waterfall_fig': fig,
        'explanation_text': explanation_text,
        'contributions_df': df_contrib.drop(columns=['AbsSHAP'])
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
    
    print("Testing Explainability Module...")
    try:
        results = explain_prediction(mock_input)
        print("\nSHAP Explanation text:")
        print(results['explanation_text'])
        print("\nFeature Contributions DataFrame:")
        print(results['contributions_df'])
        print("[OK] Explainability Module test passed successfully!")
    except Exception as e:
        print(f"Explainability Module test failed: {e}")
