from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os

def generate_pdf_report(user_inputs, prediction_results, explanation_text, output_pdf_path):
    """
    Generates a professional clinical-style PDF report for DiaSense AI.
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#1A365D'),
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#4A5568'),
        spaceAfter=20
    )
    
    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#2C5282'),
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyText',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#2D3748'),
        spaceAfter=8
    )
    
    disclaimer_style = ParagraphStyle(
        'MedicalDisclaimer',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=12,
        textColor=colors.HexColor('#718096'),
        spaceBefore=15
    )
    
    story = []
    
    # 1. Header Section
    story.append(Paragraph("DiaSense AI", title_style))
    story.append(Paragraph("Explainable Diabetes Risk Prediction & Health Intelligence Platform", subtitle_style))
    story.append(Spacer(1, 10))
    
    # 2. Risk Assessment Summary Table
    story.append(Paragraph("Risk Assessment Summary", heading_style))
    
    risk_pct = prediction_results['risk_percentage']
    risk_cat = prediction_results['risk_category']
    pred_val = prediction_results['prediction']
    pred_label = "Diabetic" if pred_val == 1 else "Non-Diabetic"
    
    # Set color based on risk category
    if risk_cat == "Low Risk":
        risk_color = '#2F855A' # Green
    elif risk_cat == "Medium Risk":
        risk_color = '#D69E2E' # Yellow/Orange
    else:
        risk_color = '#C53030' # Red
        
    summary_data = [
        [Paragraph("<b>Diagnostic Prediction:</b>", body_style), Paragraph(pred_label, body_style)],
        [Paragraph("<b>Risk Probability:</b>", body_style), Paragraph(f"{risk_pct}%", body_style)],
        [Paragraph("<b>Risk Category:</b>", body_style), Paragraph(f"<font color='{risk_color}'><b>{risk_cat}</b></font>", body_style)]
    ]
    
    t_summary = Table(summary_data, colWidths=[200, 300])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F7FAFC')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#E2E8F0')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_summary)
    story.append(Spacer(1, 15))
    
    # 3. Patient Vitals (User Inputs) Table
    story.append(Paragraph("Patient Clinical Vitals", heading_style))
    
    vitals_data = [
        [Paragraph("<b>Parameter</b>", body_style), Paragraph("<b>Value Entered</b>", body_style), Paragraph("<b>Normal Range / Note</b>", body_style)]
    ]
    
    ranges = {
        'Pregnancies': 'N/A (Number of times pregnant)',
        'Glucose': '70 - 100 mg/dL (Fasting)',
        'BloodPressure': '80 mmHg (Diastolic pressure)',
        'SkinThickness': 'N/A (Triceps skinfold, mm)',
        'Insulin': '2 - 20 mu U/ml (Fasting insulin)',
        'BMI': '18.5 - 24.9 kg/m² (Body Mass Index)',
        'DiabetesPedigreeFunction': 'N/A (Genetics metric)',
        'Age': 'N/A (Years)'
    }
    
    for k, v in user_inputs.items():
        vitals_data.append([
            Paragraph(k, body_style),
            Paragraph(str(v), body_style),
            Paragraph(ranges.get(k, 'N/A'), body_style)
        ])
        
    t_vitals = Table(vitals_data, colWidths=[200, 100, 200])
    t_vitals.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EDF2F7')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_vitals)
    story.append(Spacer(1, 15))
    
    # 4. Explainable AI Insights (SHAP Summary)
    story.append(Paragraph("Explainable AI Insights (Clinical Interpretability)", heading_style))
    story.append(Paragraph(explanation_text, body_style))
    story.append(Spacer(1, 15))
    
    # 5. General Suggestions
    story.append(Paragraph("Lifestyle Suggestions & General Guidance", heading_style))
    suggestions = [
        "Regularly monitor blood sugar levels and consult a certified healthcare professional.",
        "Incorporate a balanced diet low in processed sugars, refined carbohydrates, and saturated fats.",
        "Engage in moderate physical exercise (e.g., brisk walking, swimming) for at least 150 minutes per week.",
        "Manage stress levels through mindfulness, meditation, or adequate sleep (7-8 hours per night).",
        "Maintain a healthy body mass index (BMI) within normal ranges."
    ]
    
    for sug in suggestions:
        story.append(Paragraph(f"• {sug}", body_style))
        
    # 6. Disclaimer
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>Disclaimer:</b> This project is for educational purposes only and is not medical advice. The prediction results and health insights generated by DiaSense AI are computed by machine learning models and must not be used for diagnosis or treatment decisions. Always consult with a registered healthcare provider for clinical decisions.", disclaimer_style))
    
    # Build PDF
    doc.build(story)
    print(f"PDF report successfully written to: {output_pdf_path}")

if __name__ == "__main__":
    # Test generation script locally
    mock_inputs = {
        'Pregnancies': 2,
        'Glucose': 130,
        'BloodPressure': 74,
        'SkinThickness': 26,
        'Insulin': 110,
        'BMI': 28.5,
        'DiabetesPedigreeFunction': 0.35,
        'Age': 35
    }
    
    mock_results = {
        'prediction': 0,
        'probability': 0.2845,
        'risk_percentage': 28.45,
        'risk_category': 'Low Risk'
    }
    
    mock_explanation = "Glucose level of 130 mg/dL moderately increases diabetes risk. BMI of 28.5 kg/m² moderately increases diabetes risk. Age of 35 years moderately decreases diabetes risk."
    
    test_pdf_path = "reports/test_report.pdf"
    
    print("Testing PDF Generation Module...")
    try:
        generate_pdf_report(mock_inputs, mock_results, mock_explanation, test_pdf_path)
        assert os.path.exists(test_pdf_path), "PDF file was not created!"
        print("[OK] PDF Generation test passed successfully!")
    except Exception as e:
        print(f"PDF Generation test failed: {e}")
