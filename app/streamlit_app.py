import streamlit as st
import os

# Set page configuration
st.set_page_config(
    page_title="DiaSense AI - Explainable Health Intelligence",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
<style>
    /* Theme overrides */
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
        color: #f1f5f9;
    }
    
    /* Header styling */
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(to right, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    /* Card design */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 24px;
        backdrop-filter: blur(12px);
        transition: transform 0.2s, border-color 0.2s;
        margin-bottom: 20px;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        border-color: rgba(56, 189, 248, 0.4);
    }
    
    /* Hero button styling */
    .hero-btn {
        background: linear-gradient(135deg, #0284c7 0%, #4f46e5 100%);
        color: white !important;
        border-radius: 8px;
        padding: 10px 20px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin-top: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .hero-btn:hover {
        opacity: 0.9;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# App Title & Navigation info
st.sidebar.markdown("# 🧬 DiaSense AI Navigation")
st.sidebar.info("Use the sidebar links above to explore different pages of the platform.")

# Title
st.markdown("<h1 class='main-header'>DiaSense AI</h1>", unsafe_allow_html=True)
st.markdown("### Explainable Diabetes Risk Prediction & Health Intelligence Platform")
st.markdown("---")

# Hero Section
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class='glass-card'>
        <h2>Welcome to the Future of Explainable Health Intelligence</h2>
        <p style='font-size: 1.15rem; line-height: 1.6; color: #cbd5e1;'>
            DiaSense AI is an internship-grade clinical decision support platform that combines state-of-the-art 
            Machine Learning with <b>Explainable AI (SHAP)</b>. It predicts diabetes risk based on patient clinical vitals 
            and provides physicians and patients with transparent, feature-level reasons behind every diagnosis.
        </p>
        <p style='font-size: 1rem; color: #94a3b8;'>
            Navigate to the <b>Prediction Page</b> in the sidebar to enter patient details and calculate risk.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='glass-card' style='text-align: center; background: rgba(56, 189, 248, 0.05);'>
        <h3 style='color: #38bdf8;'>Core AI Capabilities</h3>
        <p style='text-align: left;'>✔️ <b>XGBoost</b> Classifiers (ROC AUC: 81.35%)</p>
        <p style='text-align: left;'>✔️ <b>SHAP</b> Waterfall & Feature Attributions</p>
        <p style='text-align: left;'>✔️ Interactive Population Analytics</p>
        <p style='text-align: left;'>✔️ Auto-Generated Clinical PDF Reports</p>
    </div>
    """, unsafe_allow_html=True)

# Platform Features
st.markdown("## Platform Key Modules")
f_col1, f_col2, f_col3 = st.columns(3)

with f_col1:
    st.markdown("""
    <div class='glass-card'>
        <h3 style='color: #818cf8;'>1. Interactive Risk Predictor</h3>
        <p style='color: #94a3b8; font-size: 0.95rem;'>
            Input clinical parameters including Glucose, BMI, Age, and Insulin to calculate real-time probability scores, categorized into Low, Medium, and High-risk bands.
        </p>
    </div>
    """, unsafe_allow_html=True)

with f_col2:
    st.markdown("""
    <div class='glass-card'>
        <h3 style='color: #818cf8;'>2. Local Explainability (SHAP)</h3>
        <p style='color: #94a3b8; font-size: 0.95rem;'>
            Demystifies black-box models. Renders SHAP waterfall plots detailing exactly how each feature (e.g., high glucose or BMI) pushed the risk probability.
        </p>
    </div>
    """, unsafe_allow_html=True)

with f_col3:
    st.markdown("""
    <div class='glass-card'>
        <h3 style='color: #818cf8;'>3. Health Intelligence Reports</h3>
        <p style='color: #94a3b8; font-size: 0.95rem;'>
            Download a structured, clinical-grade health report PDF. Perfect for sharing with healthcare professionals or saving to patient charts.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Dataset Summary
st.markdown("---")
st.markdown("### Technology Stack")
st.info("Built with: **Python, Streamlit, Scikit-Learn, XGBoost, SHAP, Plotly, ReportLab**")
st.markdown("""
<div style='font-size: 0.8rem; color: #64748b; text-align: center; margin-top: 20px;'>
    DiaSense AI is for educational and demo purposes only. It is not a medical diagnostic tool and should not be used as clinical advice.
</div>
""", unsafe_allow_html=True)
