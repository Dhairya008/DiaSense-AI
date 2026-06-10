import streamlit as st
import sys
import os

# Set page configuration (must be called first if page is executed independently, 
# but Streamlit's multi-page setup inherits configs. Calling it just in case)
st.set_page_config(page_title="DiaSense AI - Calculator", page_icon="🧬", layout="wide")

# Append project root to import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utils.prediction import predict_risk

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f1f5f9;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(to right, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 20px;
    }
    .prediction-title {
        font-size: 1.5rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>🧬 Risk Calculator</h1>", unsafe_allow_html=True)
st.markdown("Enter patient clinical parameters below to assess diabetes risk.")
st.markdown("---")

# Form for user inputs
st.markdown("### Patient Vitals & Clinical Data")

col1, col2 = st.columns(2)

with col1:
    pregnancies = st.number_input("Pregnancies (Number of times pregnant)", min_value=0, max_value=20, value=2, step=1, key="input_pregnancies")
    glucose = st.slider("Glucose (Fasting plasma glucose concentration, mg/dL)", min_value=0, max_value=300, value=120, step=1, key="input_glucose")
    blood_pressure = st.slider("Blood Pressure (Diastolic blood pressure, mmHg)", min_value=0, max_value=150, value=70, step=1, key="input_bp")
    skin_thickness = st.slider("Skin Thickness (Triceps skin fold thickness, mm)", min_value=0, max_value=99, value=20, step=1, key="input_skin")

with col2:
    insulin = st.slider("Insulin (2-Hour serum insulin, mu U/ml)", min_value=0, max_value=846, value=80, step=1, key="input_insulin")
    bmi = st.number_input("BMI (Body Mass Index, kg/m²)", min_value=0.0, max_value=70.0, value=28.5, step=0.1, key="input_bmi")
    dpf = st.number_input("Diabetes Pedigree Function (Genetics likelihood score)", min_value=0.0, max_value=3.0, value=0.375, step=0.001, format="%.3f", key="input_dpf")
    age = st.slider("Age (Years)", min_value=21, max_value=120, value=30, step=1, key="input_age")

st.markdown("---")

if st.button("Calculate Risk Analysis", type="primary", key="btn_calculate"):
    # Formulate inputs dict
    user_inputs = {
        'Pregnancies': pregnancies,
        'Glucose': glucose,
        'BloodPressure': blood_pressure,
        'SkinThickness': skin_thickness,
        'Insulin': insulin,
        'BMI': bmi,
        'DiabetesPedigreeFunction': dpf,
        'Age': age
    }
    
    # Store in session state for other pages
    st.session_state['user_inputs'] = user_inputs
    
    # Run prediction
    try:
        results = predict_risk(user_inputs)
        st.session_state['prediction_results'] = results
        
        # Display Results Card
        st.markdown("## 📊 Risk Diagnostic Output")
        res_col1, res_col2 = st.columns([1, 1])
        
        risk_pct = results['risk_percentage']
        risk_cat = results['risk_category']
        pred_label = "Diabetic (High Risk)" if results['prediction'] == 1 else "Non-Diabetic (Low/Normal)"
        
        with res_col1:
            st.markdown(f"""
            <div class='glass-card'>
                <div class='prediction-title'>Risk Diagnostics</div>
                <hr style='margin: 10px 0;'>
                <p style='font-size: 1.1rem;'><b>Predicted Category:</b> {pred_label}</p>
                <p style='font-size: 1.1rem;'><b>Risk Probability Score:</b> {results['probability']:.4f}</p>
                <p style='font-size: 1.1rem;'><b>Risk Percentage:</b> {risk_pct}%</p>
            </div>
            """, unsafe_allow_html=True)
            
        with res_col2:
            # Set background color based on risk category
            if risk_cat == "Low Risk":
                color_hex = "#2F855A"
                text_color = "#E6FFFA"
            elif risk_cat == "Medium Risk":
                color_hex = "#D69E2E"
                text_color = "#FEFCBF"
            else:
                color_hex = "#C53030"
                text_color = "#FFF5F5"
                
            st.markdown(f"""
            <div class='glass-card' style='background-color: {color_hex}; color: {text_color}; text-align: center;'>
                <div style='font-size: 1.4rem; font-weight: bold;'>Risk Classification</div>
                <h1 style='font-size: 3rem; margin: 15px 0; color: white;'>{risk_cat}</h1>
                <p style='font-size: 1rem;'>For further details, navigate to the <b>Explainability Page</b> or export the <b>Health Report Page</b>.</p>
            </div>
            """, unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error executing model prediction: {e}")
else:
    # If already calculated, show saved results
    if 'prediction_results' in st.session_state:
        st.success("Calculated parameters loaded. Navigate to Explainability or Report pages to inspect.")
