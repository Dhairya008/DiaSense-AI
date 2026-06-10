import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pickle
import os

def load_and_clean_data(file_path):
    """
    Reads the CSV data, replaces invalid zero values with NaN for selected features,
    and imputes them using the median of each column.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset not found at: {file_path}")
        
    df = pd.read_csv(file_path)
    
    # Columns where zero is medically invalid
    invalid_zero_cols = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
    
    # Replace zeros with NaN
    df[invalid_zero_cols] = df[invalid_zero_cols].replace(0, np.nan)
    
    # Impute NaN values with Median of the column
    for col in invalid_zero_cols:
        median_value = df[col].median()
        df[col] = df[col].fillna(median_value)
        
    return df

def split_data(df, target_col='Outcome', test_size=0.2, random_state=42):
    """
    Splits the cleaned dataset into features (X) and target (y)
    with stratified 80-20 train-test split.
    """
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Use stratify=y to ensure outcome ratio is maintained in both splits
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    return X_train, X_test, y_train, y_test

def scale_features(X_train, X_test, scaler_save_path=None):
    """
    Scales features using StandardScaler fitted on training set.
    Optionally saves the fitted scaler pickle object for inference.
    """
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Convert back to DataFrame to preserve feature names for SHAP and models
    X_train_scaled_df = pd.DataFrame(X_train_scaled, columns=X_train.columns)
    X_test_scaled_df = pd.DataFrame(X_test_scaled, columns=X_test.columns)
    
    if scaler_save_path:
        os.makedirs(os.path.dirname(scaler_save_path), exist_ok=True)
        with open(scaler_save_path, 'wb') as f:
            pickle.dump(scaler, f)
        print(f"Scaler saved successfully to: {scaler_save_path}")
        
    return X_train_scaled_df, X_test_scaled_df, scaler

if __name__ == "__main__":
    # Self-test script execution
    dataset_path = "datasets/Dataset of Diabetes.csv"
    scaler_path = "models/scaler.pkl"
    
    print("Testing Preprocessing Pipeline...")
    try:
        # Load and Clean
        df_clean = load_and_clean_data(dataset_path)
        print(f"Cleaned dataset shape: {df_clean.shape}")
        assert df_clean[df_clean.columns[:-1]].isnull().sum().sum() == 0, "Null imputation failed!"
        print("[OK] Clean and Null-Imputation passed.")
        
        # Split
        X_train, X_test, y_train, y_test = split_data(df_clean)
        print(f"Train features: {X_train.shape}, Test features: {X_test.shape}")
        assert len(X_train) + len(X_test) == len(df_clean), "Splitting size mismatch!"
        print("[OK] Splitting passed.")
        
        # Scale
        X_train_scaled, X_test_scaled, scaler = scale_features(X_train, X_test, scaler_path)
        print(f"Scaled Train Mean (should be near 0): {X_train_scaled.mean().mean():.4f}")
        print(f"Scaled Train Std (should be near 1): {X_train_scaled.std().mean():.4f}")
        print("[OK] Scaling and Scaler saving passed.")
        print("All tests passed successfully!")
    except Exception as e:
        print(f"Test failed: {e}")
