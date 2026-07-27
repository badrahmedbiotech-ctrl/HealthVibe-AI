import streamlit as st
import numpy as np
from PIL import Image
from utils.navigation import sidebar

# =============================
# TensorFlow
# =============================

TF_AVAILABLE = True

try:
    import tensorflow as tf
except Exception:
    TF_AVAILABLE = False

# =============================
# PAGE CONFIG
# =============================

st.set_page_config(
    page_title="CT Scan AI",
    page_icon="🩻",
    layout="wide"
)

sidebar()

# =============================
# CSS
# =============================

try:
    with open("style.css") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )
except:
    pass

# =============================
# HEADER
# =============================

st.markdown("""
<div class="hero">

<h1>🩻 Lung CT Scan AI</h1>

<p>
Artificial Intelligence for Lung Cancer Detection
</p>

</div>
""",unsafe_allow_html=True)

st.divider()

# =============================
# TensorFlow Check
# =============================

if not TF_AVAILABLE:

    st.error("""
TensorFlow غير موجود على الجهاز.

سبب المشكلة هو أن المعالج الحالي لا يدعم
الإصدار الحديث من TensorFlow.

يمكنك استخدام Google Colab أو جهاز أحدث.
""")

    st.stop()

# =============================
# Load Model
# =============================

@st.cache_resource
def load_model():

    return tf.keras.models.load_model(
        "models/lung_cancer_model.keras"
    )

model=None
model_loaded=False

try:

    model=load_model()

    model_loaded=True

except Exception as e:

    st.error("❌ Unable to load AI Model")

    st.code(str(e))

# =============================
# Classes
# =============================

classes=[

"Adenocarcinoma",

"Large Cell Carcinoma",

"Normal",

"Squamous Cell Carcinoma"

]

# =============================
# Instructions
# =============================

st.info("""

### Instructions

• Upload CT Scan

• Click Analyze

• Wait for AI

• Review Results

""")

# =============================
# Upload
# =============================

uploaded=st.file_uploader(

"Upload Lung CT Scan",

type=["png","jpg","jpeg"]

)

prediction=None
confidence=None
disease=None

if uploaded is not None:

    image=Image.open(uploaded).convert("RGB")

    left,right=st.columns([1,1])

    with left:

        st.image(

            image,

            use_container_width=True,

            caption="Uploaded CT"

        )

    img=image.resize((224,224))

    img=np.array(img)

    img=img.astype(np.float32)/255.0

    img=np.expand_dims(img,0)

    with right:

        st.subheader("AI Analysis")

        if st.button(

            "🤖 Analyze CT Scan",

            use_container_width=True

        ):

            if not model_loaded:

                st.error("Model Not Loaded")

                st.stop()

            with st.spinner("Analyzing..."):

                prediction=model.predict(

                    img,

                    verbose=0

                )

            pred=np.argmax(prediction)

            confidence=float(np.max(prediction))*100

            disease=classes[pred]

            st.success("Analysis Completed")

            st.metric(

                "Prediction",

                disease

            )

            st.metric(

                "Confidence",

                f"{confidence:.2f}%"

            )

            st.progress(int(confidence))

            # =====================================
# Diagnosis Dashboard
# =====================================

if disease is not None:

    st.divider()

    st.subheader("🩺 AI Diagnosis Dashboard")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Detected Disease",
            disease
        )

        st.metric(
            "Confidence",
            f"{confidence:.2f}%"
        )

    with col2:

        st.write("### AI Confidence Level")

        st.progress(int(confidence))

        if confidence >= 90:

            st.success("🟢 Very High Confidence")

        elif confidence >= 75:

            st.info("🔵 High Confidence")

        elif confidence >= 50:

            st.warning("🟡 Moderate Confidence")

        else:

            st.error("🔴 Low Confidence")

# =====================================
# Probability Distribution
# =====================================

    st.divider()

    st.subheader("📊 Prediction Probability")

    probs = prediction[0]

    chart = {}

    for i in range(len(classes)):

        chart[classes[i]] = float(probs[i] * 100)

    st.bar_chart(chart)

# =====================================
# AI Summary
# =====================================

    st.divider()

    st.subheader("🤖 AI Summary")

    if disease == "Normal":

        st.success("""

No obvious abnormality detected.

The lungs appear normal according
to the trained AI model.

""")

    elif disease == "Adenocarcinoma":

        st.error("""

Possible Adenocarcinoma detected.

Further investigations are required.

""")

    elif disease == "Large Cell Carcinoma":

        st.error("""

Possible Large Cell Carcinoma detected.

Immediate clinical evaluation is recommended.

""")

    elif disease == "Squamous Cell Carcinoma":

        st.error("""

Possible Squamous Cell Carcinoma detected.

Smoking history should be reviewed.

""")

# =====================================
# Disease Information
# =====================================

    st.divider()

    st.subheader("📖 Disease Information")

    if disease == "Normal":

        st.info("""

### Description

Healthy lung appearance.

### Recommendation

• Regular medical check-up

• Healthy lifestyle

• Avoid smoking

""")

    elif disease == "Adenocarcinoma":

        st.info("""

### Description

Most common type of lung cancer.

Usually develops in the outer lung.

### Recommendation

• Chest CT

• PET Scan

• Biopsy

• Oncology consultation

""")

    elif disease == "Large Cell Carcinoma":

        st.info("""

### Description

Aggressive non-small cell lung cancer.

### Recommendation

• Immediate specialist referral

• Additional imaging

• Tissue biopsy

""")

    elif disease == "Squamous Cell Carcinoma":

        st.info("""

### Description

Usually associated with smoking.

Often develops near central bronchi.

### Recommendation

• Smoking cessation

• Bronchoscopy

• Oncology consultation

""")
        
# =====================================
# Risk Indicator
# =====================================

if disease is not None:

    st.divider()

    st.subheader("🚨 Risk Assessment")

    if confidence >= 90:

        st.success("🟢 AI Confidence: Very High")

    elif confidence >= 75:

        st.info("🔵 AI Confidence: High")

    elif confidence >= 50:

        st.warning("🟡 AI Confidence: Moderate")

    else:

        st.error("🔴 AI Confidence: Low")

# =====================================
# Future PDF Report
# =====================================

    st.divider()

    st.subheader("📄 Medical Report")

    st.info("""
PDF Report will include:

• Patient Information

• AI Prediction

• Confidence Score

• CT Scan Result

• Medical Recommendations

• Doctor Notes

(Coming Soon)
""")

    st.button(
        "📥 Download PDF Report",
        disabled=True,
        use_container_width=True
    )

# =====================================
# Future Grad-CAM
# =====================================

    st.divider()

    st.subheader("🧠 Explainable AI")

    st.info("""
Grad-CAM Visualization

This feature will highlight the region
that the AI focused on while making
its prediction.

(Coming Soon)
""")

# =====================================
# Recommendations
# =====================================

st.divider()

st.subheader("📋 General Recommendations")

st.write("✅ Always consult a chest physician.")

st.write("✅ AI results should never replace medical diagnosis.")

st.write("✅ Compare the CT scan with previous examinations.")

st.write("✅ Additional laboratory investigations may be required.")

st.write("✅ Early diagnosis significantly improves treatment outcomes.")

# =====================================
# Disclaimer
# =====================================

st.warning("""
This application is intended for educational
and research purposes only.

HealthVibe AI does NOT replace
professional medical diagnosis.
""")

# =====================================
# Footer
# =====================================

st.divider()

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("AI Model", "EfficientNetB0")

with c2:
    st.metric("Image Size", "224 × 224")

with c3:
    st.metric("Classes", "4")

st.caption(
    "HealthVibe AI © 2026 | Artificial Intelligence for Healthcare"
)