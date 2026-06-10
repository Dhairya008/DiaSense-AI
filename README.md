# DiaSense AI 🧬
### Explainable Diabetes Risk Prediction & Health Intelligence Platform

DiaSense AI is an end-to-end Machine Learning and Full-Stack AI platform designed to predict diabetes risk and present clinical explanations for individual patient profiles using Explainable AI (SHAP). It provides clinical decision support with interactive charts, population analytics, and professional PDF report generation.

---

## 🚀 Key Features
* **Interactive Risk Calculator**: Assesses diabetes likelihood and classifies patient risk (Low, Medium, High) in real time.
* **Explainable AI (SHAP)**: Generates clinical waterfall charts displaying exactly how each vital parameter (e.g., Glucose, BMI) drives the outcome.
* **Interactive Analytics**: Features Plotly charts exploring database correlations, class distributions, and feature properties.
* **Diagnostic PDF Export**: Compiles inputs, diagnostic metrics, and SHAP narratives into a physician-ready PDF.
* **Robust Preprocessing Pipeline**: Handles physiological anomalies (replacing invalid zeros with medians) and applies standard scaling.

---

## 🛠️ Tech Stack
* **Language**: Python 3.10+
* **ML Libraries**: Scikit-Learn, XGBoost, SHAP
* **Visualization**: Plotly, Matplotlib, Seaborn
* **Frontend**: Streamlit
* **PDF Compilation**: ReportLab

---

## 📊 Dataset Information
The model was trained on the authentic PIMA Indians Diabetes Dataset (from UCI ML Repository), mapped with the following parameters:
* `Pregnancies`: Number of times pregnant.
* `Glucose`: Plasma glucose concentration (2 hours in an oral glucose tolerance test).
* `BloodPressure`: Diastolic blood pressure (mmHg).
* `SkinThickness`: Triceps skin fold thickness (mm).
* `Insulin`: 2-Hour serum insulin (mu U/ml).
* `BMI`: Body Mass Index (weight in kg / height in m²).
* `DiabetesPedigreeFunction`: Genetic pedigree scores.
* `Age`: Patient age (Years).
* `Outcome`: Target class (0 = Non-Diabetic, 1 = Diabetic).

---

## 📂 Project Structure
```
DiaSense-AI/
├── datasets/
│   └── Dataset of Diabetes.csv     # Cleaned PIMA dataset
├── notebooks/
│   ├── EDA.ipynb                   # Exploratory Data Analysis
│   └── Model_Training.ipynb        # ML comparisons and SHAP plots
├── models/
│   ├── diabetes_model.pkl          # Saved XGBoost classifier
│   └── scaler.pkl                  # Serialized StandardScaler
├── app/
│   ├── streamlit_app.py            # Streamlit landing page
│   └── pages/
│       ├── 1_Prediction.py         # Diagnostic calculator
│       ├── 2_Analytics.py          # Interactive database graphs
│       ├── 3_Model_Performance.py  # Model metric evaluation
│       ├── 4_Explainability.py     # Local SHAP interpretations
│       └── 5_Health_Report.py      # Downloadable PDF compilation
├── utils/
│   ├── preprocessing.py            # Data cleaning and scaling
│   ├── prediction.py               # Model prediction wrappers
│   ├── explainability.py           # SHAP waterfalls & narratives
│   └── report_generator.py         # PDF reports using ReportLab
├── reports/                        # Saved PDF reports
├── requirements.txt                # Fixed dependencies
└── README.md                       # Repository documentation
```

---

## ⚙️ Installation & Local Setup

### 1. Clone the repository:
```bash
git clone https://github.com/your-username/DiaSense-AI.git
cd DiaSense-AI
```

### 2. Initialize Virtual Environment:
```bash
# On Windows
python -m venv .venv
.venv\Scripts\activate

# On Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies:
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Application:
```bash
streamlit run app/streamlit_app.py
```

---

## ⚙️ Model Comparison & Metrics

| Algorithm | Accuracy | Precision | Recall | F1 Score | ROC AUC |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Logistic Regression | 70.78% | 60.00% | 50.00% | 54.55% | 0.8130 |
| Decision Tree | 75.97% | 63.93% | 72.22% | 67.83% | 0.7610 |
| Random Forest | 74.03% | 66.67% | 51.85% | 58.33% | 0.8063 |
| **XGBoost (Selected)** | **77.27%** | **71.11%** | **59.26%** | **64.65%** | **0.8135** |

---

## 🔮 Future Enhancements
* Integrate real-time EHR API endpoints (e.g. FHIR standards).
* Add deep neural network comparisons (using PyTorch or TensorFlow).
* Support automated multi-class risk analysis for pre-diabetic monitoring.

---

## ⚖️ License & Disclaimer
This repository is licensed under the MIT License. This tool is built strictly for **educational and demonstrational purposes** and does not constitute medical advice or diagnostics.
