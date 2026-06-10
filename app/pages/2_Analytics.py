import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import sys
import os

# Set page configuration
st.set_page_config(page_title="DiaSense AI - Analytics", page_icon="📊", layout="wide")

# Append project root to import path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from utils.preprocessing import load_and_clean_data

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

st.markdown("<h1 class='main-header'>📊 Population Analytics</h1>", unsafe_allow_html=True)
st.markdown("Interactive exploration of the clinical database used to train DiaSense AI models.")
st.markdown("---")

# Load clean data
dataset_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'datasets', 'Dataset of Diabetes.csv')

try:
    df = load_and_clean_data(dataset_path)
    
    # Grid summary layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Feature Distribution & Density")
        selected_feature = st.selectbox(
            "Select Clinical Parameter to Visualize",
            options=df.columns[:-1],
            index=1 # Glucose default
        )
        
        # Plotly Histogram
        fig_hist = px.histogram(
            df, x=selected_feature, color="Outcome",
            marginal="box", barmode="overlay",
            color_discrete_map={0: '#1f77b4', 1: '#ff7f0e'},
            labels={'0': 'Non-Diabetic', '1': 'Diabetic'}
        )
        fig_hist.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#f1f5f9',
            title=f"Distribution of {selected_feature} by Outcome Class"
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        
    with col2:
        st.markdown("### Patient Outcome Ratio")
        # Plotly Pie Chart
        outcome_counts = df['Outcome'].value_counts().reset_index()
        outcome_counts.columns = ['Outcome', 'Count']
        outcome_counts['OutcomeLabel'] = outcome_counts['Outcome'].map({0: 'Non-Diabetic', 1: 'Diabetic'})
        
        fig_pie = px.pie(
            outcome_counts, values='Count', names='OutcomeLabel',
            hole=0.4, color='OutcomeLabel',
            color_discrete_map={'Non-Diabetic': '#1f77b4', 'Diabetic': '#ff7f0e'}
        )
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#f1f5f9',
            title="Database Class Balance"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
    st.markdown("---")
    
    col3, col4 = st.columns([2, 1])
    
    with col3:
        st.markdown("### Correlation Matrix Heatmap")
        corr = df.corr()
        
        # Interactive Heatmap
        fig_heat = px.imshow(
            corr, text_auto=".2f",
            color_continuous_scale="RdBu_r",
            aspect="auto"
        )
        fig_heat.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='#f1f5f9'
        )
        st.plotly_chart(fig_heat, use_container_width=True)
        
    with col4:
        st.markdown("### Descriptive Statistics Summary")
        st.dataframe(df.describe().T[['mean', 'std', 'min', 'max']], use_container_width=True)
        st.markdown("""
        <div style='font-size: 0.9rem; color: #94a3b8; line-height: 1.5; margin-top: 15px;'>
            <b>Analytical Insights:</b><br>
            • Imputed zero vitals are represented by their respective feature median, restoring physiological ranges.<br>
            • Fasting plasma glucose has a strong linear alignment with diabetes incidence.<br>
            • Standard scaling helps balance features with broad variance (like Insulin and Age) during model training.
        </div>
        """, unsafe_allow_html=True)
        
except Exception as e:
    st.error(f"Error loading analytics data: {e}")
