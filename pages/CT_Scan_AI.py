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

import translation
translation.init()

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

st.markdown(f"""
<div class="hero">

<h1>{translation.t("🩻 Lung CT Scan AI")}</h1>

<p>
{translation.t("Artificial Intelligence for Lung Cancer Detection")}
</p>

</div>
""",unsafe_allow_html=True)

st.divider()

# =============================
# TensorFlow Check
# =============================

if not TF_AVAILABLE:

    st.error(translation.t("tf_not_found"))

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

    st.error(translation.t("❌ Unable to load AI Model"))

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

st.info(translation.t("ct_instructions"))

# =============================
# Upload
# =============================

uploaded=st.file_uploader(

translation.t("Upload Lung CT Scan"),

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

            width="stretch",

            caption=translation.t("Uploaded CT")

        )

    img=image.resize((224,224))

    img=np.array(img)

    img=img.astype(np.float32)/255.0

    img=np.expand_dims(img,0)

    with right:

        st.subheader(translation.t("AI Analysis"))

        if st.button(

            translation.t("🤖 Analyze CT Scan"),

            width="stretch"

        ):

            if not model_loaded:

                st.error(translation.t("Model Not Loaded"))

                st.stop()

            with st.spinner(translation.t("Analyzing...")):

                prediction=model.predict(

                    img,

                    verbose=0

                )

            pred=np.argmax(prediction)

            confidence=float(np.max(prediction))*100

            disease=classes[pred]

            st.success(translation.t("Analysis Completed"))

            st.metric(

                translation.t("Prediction"),

                translation.t(disease)

            )

            st.metric(

                translation.t("Confidence"),

                f"{confidence:.2f}%"

            )

            st.progress(int(confidence))

# =====================================
# Diagnosis Dashboard
# =====================================

if disease is not None:

    st.divider()

    st.subheader(translation.t("🩺 AI Diagnosis Dashboard"))

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            translation.t("Detected Disease"),
            translation.t(disease)
        )

        st.metric(
            translation.t("Confidence"),
            f"{confidence:.2f}%"
        )

    with col2:

        st.write(f"### {translation.t('AI Confidence Level')}")

        st.progress(int(confidence))

        if confidence >= 90:

            st.success(translation.t("🟢 Very High Confidence"))

        elif confidence >= 75:

            st.info(translation.t("🔵 High Confidence"))

        elif confidence >= 50:

            st.warning(translation.t("🟡 Moderate Confidence"))

        else:

            st.error(translation.t("🔴 Low Confidence"))

# =====================================
# Probability Distribution
# =====================================

    st.divider()

    st.subheader(translation.t("📊 Prediction Probability"))

    probs = prediction[0]

    chart = {}

    for i in range(len(classes)):

        chart[translation.t(classes[i])] = float(probs[i] * 100)

    st.bar_chart(chart)

# =====================================
# AI Summary
# =====================================

    st.divider()

    st.subheader(translation.t("🤖 AI Summary"))

    if disease == "Normal":

        st.success(translation.t("summary_normal"))

    elif disease == "Adenocarcinoma":

        st.error(translation.t("summary_adenocarcinoma"))

    elif disease == "Large Cell Carcinoma":

        st.error(translation.t("summary_large_cell"))

    elif disease == "Squamous Cell Carcinoma":

        st.error(translation.t("summary_squamous"))

# =====================================
# Disease Information
# =====================================

    st.divider()

    st.subheader(translation.t("📖 Disease Information"))

    if disease == "Normal":

        st.info(translation.t("info_normal"))

    elif disease == "Adenocarcinoma":

        st.info(translation.t("info_adenocarcinoma"))

    elif disease == "Large Cell Carcinoma":

        st.info(translation.t("info_large_cell"))

    elif disease == "Squamous Cell Carcinoma":

        st.info(translation.t("info_squamous"))

# =====================================
# Risk Indicator
# =====================================

if disease is not None:

    st.divider()

    st.subheader(translation.t("🚨 Risk Assessment"))

    if confidence >= 90:

        st.success(translation.t("🟢 AI Confidence: Very High"))

    elif confidence >= 75:

        st.info(translation.t("🔵 AI Confidence: High"))

    elif confidence >= 50:

        st.warning(translation.t("🟡 AI Confidence: Moderate"))

    else:

        st.error(translation.t("🔴 AI Confidence: Low"))

# =====================================
# Future PDF Report
# =====================================

    st.divider()

    st.subheader(translation.t("📄 Medical Report"))

    st.info(translation.t("pdf_report_info"))

    st.button(
        translation.t("📥 Download PDF Report"),
        disabled=True,
        width="stretch"
    )

# =====================================
# Future Grad-CAM
# =====================================

    st.divider()

    st.subheader(translation.t("🧠 Explainable AI"))

    st.info(translation.t("gradcam_info"))

# =====================================
# Recommendations
# =====================================

st.divider()

st.subheader(translation.t("📋 General Recommendations"))

st.write(translation.t("✅ Always consult a chest physician."))

st.write(translation.t("✅ AI results should never replace medical diagnosis."))

st.write(translation.t("✅ Compare the CT scan with previous examinations."))

st.write(translation.t("✅ Additional laboratory investigations may be required."))

st.write(translation.t("✅ Early diagnosis significantly improves treatment outcomes."))

# =====================================
# Disclaimer
# =====================================

st.warning(translation.t("ct_disclaimer"))

# =====================================
# Footer
# =====================================

st.divider()

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(translation.t("AI Model"), "EfficientNetB0")

with c2:
    st.metric(translation.t("Image Size"), "224 × 224")

with c3:
    st.metric(translation.t("Classes"), "4")

st.caption(
    translation.t("HealthVibe AI © 2026 | Artificial Intelligence for Healthcare")
)