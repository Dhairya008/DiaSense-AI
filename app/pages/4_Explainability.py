import streamlit as st
import matplotlib.pyplot as plt
import sys
import os

# Set page configuration
st.set_page_config(page_title="DiaSense AI - Explainability", page_icon="🔍", layout="wide")

# Append project root to import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utils.explainability import explain_prediction

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
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-header'>🔍 Explainable AI (SHAP)</h1>", unsafe_allow_html=True)
st.markdown("Inspect how individual parameters contribute to the model's diagnostic risk predictions.")
st.markdown("---")

# Use session state inputs or fallback to mock inputs
if 'user_inputs' in st.session_state:
    st.info("Showing SHAP Explainability for the active patient prediction calculated on the Prediction Page.")
    user_inputs = st.session_state['user_inputs']
else:
    st.warning("No active patient prediction found in session state. Showing SHAP explanations for a sample patient profile. (Go to Prediction Page to customize.)")
    # Default patient profile
    user_inputs = {
        'Pregnancies': 2,
        'Glucose': 130,
        'BloodPressure': 74,
        'SkinThickness': 26,
        'Insulin': 110,
        'BMI': 28.5,
        'DiabetesPedigreeFunction': 0.35,
        'Age': 35
    }

# Compute SHAP explanation
try:
    with st.spinner("Computing SHAP values and rendering plots..."):
        shap_res = explain_prediction(user_inputs)
        
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Patient Feature Contributions (SHAP Waterfall)")
        st.pyplot(shap_res['waterfall_fig'])
        st.caption("Red bars increase diabetes risk; blue bars decrease risk. Length represents magnitude of impact.")
        
    with col2:
        st.markdown("### Clinical Risk Narrative")
        st.markdown(f"""
        <div class='glass-card' style='border-left: 5px solid #818cf8; background: rgba(129, 140, 248, 0.05);'>
            <h4>AI Health Insight Engine Output:</h4>
            <p style='font-size: 1.1rem; line-height: 1.6;'>
                "{shap_res['explanation_text']}"
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Feature Contribution Values")
        st.dataframe(shap_res['contributions_df'].style.format({'SHAP': "{:.4f}", 'Raw': "{:.2f}"}), use_container_width=True)

except Exception as e:
    st.error(f"Error computing SHAP explainability: {e}")
