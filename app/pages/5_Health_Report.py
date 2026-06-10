import streamlit as st
import sys
import os

# Set page configuration
st.set_page_config(page_title="DiaSense AI - Health Report", page_icon="📋", layout="wide")

# Append project root to import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utils.prediction import predict_risk
from utils.explainability import explain_prediction
from utils.report_generator import generate_pdf_report

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

st.markdown("<h1 class='main-header'>📋 Export Diagnostic Health Report</h1>", unsafe_allow_html=True)
st.markdown("Compile patient details, prediction probability, risk categories, and clinical SHAP interpretations into a PDF report.")
st.markdown("---")

# Load session state inputs or fallback to mock
if 'user_inputs' in st.session_state:
    st.info("Exporting report for the active patient prediction calculated on the Prediction Page.")
    user_inputs = st.session_state['user_inputs']
    pred_results = st.session_state['prediction_results']
else:
    st.warning("No active patient prediction found in session state. Showing PDF report preview for a sample patient profile. (Go to Prediction Page to customize.)")
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
    pred_results = predict_risk(user_inputs)

try:
    # Get explainability text
    shap_res = explain_prediction(user_inputs)
    explanation_text = shap_res['explanation_text']
    
    # Path for temporary generated PDF
    pdf_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'reports')
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, 'patient_health_report.pdf')
    
    # Generate the PDF
    generate_pdf_report(user_inputs, pred_results, explanation_text, pdf_path)
    
    # Read PDF to bytes for Streamlit download button
    with open(pdf_path, 'rb') as f:
        pdf_bytes = f.read()
        
    st.markdown("### Report Preview Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class='glass-card'>
            <h4>Assessment Classification</h4>
            <p><b>Diagnostic Class:</b> {"Diabetic" if pred_results['prediction'] == 1 else "Non-Diabetic"}</p>
            <p><b>Probability Score:</b> {pred_results['probability']:.4f}</p>
            <p><b>Risk Band:</b> {pred_results['risk_category']} ({pred_results['risk_percentage']}%)</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class='glass-card'>
            <h4>Key Contributing Factors</h4>
            <p style='font-size: 0.95rem; line-height: 1.5; color: #cbd5e1;'>
                "{explanation_text}"
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    # Download Button
    st.download_button(
        label="📥 Download Clinical PDF Report",
        data=pdf_bytes,
        file_name="DiaSense_AI_Health_Report.pdf",
        mime="application/pdf",
        key="btn_download_pdf"
    )
    
    st.success("PDF successfully compiled and ready for download.")

except Exception as e:
    st.error(f"Error compiling diagnostic health report: {e}")
