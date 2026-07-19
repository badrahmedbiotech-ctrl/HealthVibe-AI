import streamlit as st
import pandas as pd
import numpy as np
import fpdf
from fpdf import FPDF
import io

# دالة لتوليد تقرير الـ PDF بالشكل الطبي والمُنظم
def generate_pdf(user_data, result, recommendations, medications):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # 1. الهيدر
    pdf.set_font("Arial", "B", 24)
    pdf.set_text_color(26, 82, 118)
    pdf.cell(0, 15, "HealthVibe-AI", ln=1, align="L")
    
    pdf.set_font("Arial", "I", 12)
    pdf.set_text_color(127, 140, 141)
    pdf.cell(0, 5, "Thrombosis Risk Assessment Report", ln=1, align="L")
    
    pdf.ln(8)
    
    # 2. البيانات
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 10, "Patient Clinical Parameters:", ln=1)
    
    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(60, 60, 60)
    for key, value in user_data.items():
        formatted_key = str(key).replace("_", " ").title()
        pdf.cell(0, 7, f"  - {formatted_key}: {value}", ln=1)
    
    pdf.ln(5)
    
    # 3. النتيجة
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 10, "AI Screening Evaluation:", ln=1)
    
    pdf.set_fill_color(240, 244, 248)
    pdf.set_text_color(26, 82, 118)
    pdf.set_draw_color(26, 82, 118)
    
    pdf.set_font("Arial", "B", 12)
    pdf.multi_cell(180, 10, f"Result Status: {result}", border=1, align="C", fill=True)
    pdf.ln(8)
    
    # 4. الأدوية المقترحة (المضافة حديثاً)
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 10, "Suggested Medications & Medical Options (Consult Doctor):", ln=1)
    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(60, 60, 60)
    for med in medications:
        pdf.set_x(10)
        pdf.multi_cell(180, 7, f"  - {med}")
        
    pdf.ln(5)
    
    # 5. التوصيات
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 10, "Personalized Recommendations:", ln=1)
    
    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(60, 60, 60)
    
    if isinstance(recommendations, list):
        for rec in recommendations:
            pdf.set_x(10) # 🌟 السطر السحري عشان يرجع المؤشر لأول الشمال دايماً
            pdf.multi_cell(180, 7, f"  - {rec}")
    else:
        pdf.set_x(10)
        pdf.multi_cell(180, 7, f"  - {str(recommendations)}")
        
    return bytes(pdf.output())

# إعدادات الصفحة الخاصة بـ Streamlit والأيقونة
st.set_page_config(page_title="Thrombosis Assessment", page_icon="🩸")

st.title("🩸 Thrombosis Risk Assessment & AI Screening")
st.write("Enter the patient health parameters below to analyze the risk of Thrombosis (Blood Clots).")

# بناء الاستمارة (Form) ليدخل المريض بياناته
with st.form("thrombosis_form"):
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input("Age", min_value=1, max_value=120, value=45)
        d_dimer = st.number_input("D-Dimer Level (ng/mL)", min_value=0.0, value=250.0, help="Normal is typically < 500 ng/mL")
        swelling = st.selectbox("Leg Swelling / Edema", ["No", "Yes"])
    with col2:
        pain = st.selectbox("Leg Pain / Tenderness", ["No", "Yes"])
        history = st.selectbox("Previous History of Blood Clots", ["No", "Yes"])
        mobility = st.selectbox("Recent Prolonged Immobility (Bed rest/Long travel)", ["No", "Yes"])
        
    submit = st.form_submit_button("Analyze Risk Status")

# عند ضغط زر التحليل وحساب النتيجة
if submit:
    # منطق حسابي يحاكي فحص الـ AI وقواعد Wells' Score الطبية
    risk_score = 0
    if d_dimer > 500: risk_score += 2
    if swelling == "Yes": risk_score += 1
    if pain == "Yes": risk_score += 1
    if history == "Yes": risk_score += 2
    if mobility == "Yes": risk_score += 1
    if age > 60: risk_score += 1
    
    user_data = {
        "Age": age,
        "D-Dimer Level": f"{d_dimer} ng/mL",
        "Leg Swelling": swelling,
        "Leg Pain": pain,
        "Previous History": history,
        "Prolonged Immobility": mobility
    }
    
    st.subheader("Analysis Results:")

    # ضبط منطق حساب نتيجة الـ Risk بناءً على الـ D-Dimer
    if d_dimer < 500:
            if history == "Yes" and swelling == "Yes":
                result = "Moderate Risk (D-Dimer Normal, but Clinical Signs Present)"
            else:
                result = "Low Risk / Negative"
    else:
            if history == "Yes" or swelling == "Yes" or pain == "Yes" or mobility == "Yes":
                result = "High Risk / Positive"
            else:
                result = "Moderate Risk (Elevated D-Dimer, No Major Symptoms)"
    result_status = result 
        # الأدوية في حالة الخطورة العالية
    meds = [
            "Anticoagulants (Blood Thinners) like Low-Molecular-Weight Heparin (LMWH) injections (e.g., Enoxaparin/Clexane).",
            "Oral Anticoagulants (DOACs) like Rivaroxaban (Xarelto) or Apixaban (Eliquis) as prescribed by your doctor.",
            "Note: Medication dosage and duration must be strictly tailored by a cardiologist or hematologist."
        ]
    
    recs = [
            "Please consult a cardiovascular specialist or visit an emergency room immediately.",
            "Avoid sitting or standing still for long periods; keep your legs slightly elevated when resting.",
            "Do not massage the affected leg, as this could dislodge a potential clot.",
            "An ultrasound (Doppler) or further clinical imaging is highly recommended to confirm diagnosis."
        ]

        # عرض النتيجة على المنصة
    st.success(f"Result: {result}")
        
        # الأدوية/الإجراءات الوقائية في حالة الخطورة المنخفضة
    meds = [
            "No immediate therapeutic anticoagulation is needed.",
            "Prophylactic options (for long travel/immobility): Low-dose Aspirin or Compression Stockings may be advised.",
            "Always review with your physician before starting any preventive medication."
        ]
        
    recs = [
            "Maintain an active lifestyle with regular walking or exercise.",
            "Stay well-hydrated throughout the day to support healthy blood flow.",
            "If taking long flights or trips, remember to stretch and move your legs every 1-2 hours.",
            "Keep monitoring for any sudden symptoms like swelling, redness, or shortness of breath."
        ]
        
    st.write("**Suggested Medications / Clinical Approach:**")
    for m in meds:
        st.write(f"- {m}")
        
    st.write("**Recommendations:**")
    for r in recs:
        st.write(f"- {r}")
        
    # توليد ملف الـ PDF وحفظه في الذاكرة للتحميل (مع تمرير قائمة الأدوية الجديدة)
    pdf_bytes = generate_pdf(user_data, result_status, recs, meds)
    
    # زر تحميل التقرير الطبي بصيغة PDF
    st.download_button(
        label="📥 Download PDF Medical Report",
        data=pdf_bytes,
        file_name="Thrombosis_AI_Report.pdf",
        mime="application/pdf"
    )