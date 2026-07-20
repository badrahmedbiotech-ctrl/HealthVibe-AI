from pyexpat import features

import streamlit as st
import pandas as pd
import numpy as np
import fpdf
from fpdf import FPDF
import io
import plotly.graph_objects as go

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
    # --- جزء الـ Explainable AI (XAI) ---
        # 1. تحديد وزن مساهمة كل عامل بناءً على المدخلات   
    features = []
    contributions = []
    if d_dimer > 500:
            features.append("Elevated D-Dimer")
            contributions.append(2)
    if swelling == "Yes":
            features.append("Leg Swelling")
            contributions.append(1)
    if pain == "Yes":
            features.append("Leg Pain")
            contributions.append(1)
    if history == "Yes":
            features.append("Previous History")
            contributions.append(2)
    if mobility == "Yes":
            features.append("Prolonged Immobility")
            contributions.append(1)
    if age > 60:
            features.append("Age > 60")
            contributions.append(1)

        # لو مفيش أي أعراض خالص، بنحط قيمة صفرية عشان الرسم البياني ميطلعش فاضي
    if not features:
            features.append("No Risk Factors Present")
            contributions.append(0)
    
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
    

    # ... (الشروط وحساب الـ meds والـ recs اللي عملناهم) ...

        # 1. ارمي كود مؤشر النسبة (Gauge Chart) هنا بالظبط:
    st.write("---")
        
        # تحويل الـ risk_score لنسبة مئوية (بافتراض إن أعلى سكور ممكن يوصل له هو 8)
        # لو الحسبة عندك مختلفة، تقدري تغيري رقم 8 لأقصى سكور ممكن يطلع في الشروط
    percentage_value = min((risk_score / 8) * 100, 100) 
        
    fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = percentage_value,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "💡 Thrombosis Risk Probability (%)", 'font': {'size': 18}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "white"}, # لون مؤشر العداد نفسه
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps' : [
                    {'range': [0, 35], 'color': "#1a9850"},   # الأخضر (Low Risk)
                    {'range': [35, 70], 'color': "#fdae61"},  # الأصفر/البرتقالي (Moderate)
                    {'range': [70, 100], 'color': "#d73027"}  # الأحمر (High Risk)
                ],
            }
        ))
        
    fig_gauge.update_layout(
            template="plotly_dark", # عشان يفضل متناسق مع الـ Dark mode بتاعكم
            height=250, 
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        # عرض العداد على الشاشة
    st.plotly_chart(fig_gauge, use_container_width=True)

    # عرض النتيجة باللون المناسب لدرجة الخطورة
    if "High Risk" in result_status:
            st.error(f"🔴 Result: {result}")  # شريط أحمر
    elif "Moderate Risk" in result_status:
            st.warning(f"⚠️ Result: {result}")  # شريط أصفر
    else:
            st.success(f"🟢 Result: {result}")  # شريط أخضر
        # ... (باقي كود الـ meds والـ recs والـ PDF) ...
        # عرض النتيجة على المنصة
    # 2. رسم شكل بياني يوضح تأثير كل عرض على قرار الـ AI
    st.write("---")
    st.subheader("💡 AI Decision Explanation (Explainable AI)")
    st.write("This chart shows how much each medical parameter contributed to the AI's final risk assessment score:")

        # إنشاء الرسم البياني باستخدام Plotly
    fig = go.Figure(go.Bar(
            x=contributions,
            y=features,
            orientation='h',  # رسم أفقي لسهولة القراءة
            marker=dict(
                color=contributions,
                colorscale='Reds', # تدرج ألوان أحمر ليعبر عن الخطورة
                line=dict(color='rgba(255, 255, 255, 0.5)', width=1)
            )
        ))

        # تحسين مظهر الرسم البياني ليناسب الـ Dark Mode للمنصة
    fig.update_layout(
            xaxis_title="Risk Weight (Contribution Points)",
            yaxis_title="Patient Parameters",
            template="plotly_dark",  # متناسق مع الاستايل الغامق للمشروع
            height=300,
            margin=dict(l=20, r=20, t=20, b=20)
        )

        # عرض الرسم البياني في ستريمليت
    st.plotly_chart(fig, use_container_width=True)
        
        # الأدوية/الإجراءات الوقائية في حالة الخطورة المنخفضة
    # تحديد الأدوية والنصائح الطبية بناءً على نتيجة التحليل
    if "High Risk" in result_status:
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
    elif "Moderate Risk" in result_status:
            meds = [
                "Prophylactic anticoagulation may be considered after specialist consultation.",
                "Review current medications with your physician."
            ]
            recs = [
                "A Leg Duplex Ultrasound (Doppler) is highly recommended to rule out deep vein thrombosis.",
                "Elevate your legs while sitting or lying down.",
                "Avoid prolonged immobility; perform light ankle exercises."
            ]
    else:
            # حالة الـ Low Risk / Negative
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