import streamlit as st
import numpy as np
from PIL import Image
from utils.navigation import sidebar
from components.language import apply_language
from translations import get_text

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

lang = apply_language()

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

<h1>{get_text(lang, "ct_title")}</h1>

<p>
{get_text(lang, "ct_subtitle")}
</p>

</div>
""", unsafe_allow_html=True)

st.divider()

# =============================
# TensorFlow Check
# =============================

if not TF_AVAILABLE:
    st.error(get_text(lang, "tf_not_available"))
    st.stop()

# =============================
# Load Model
# =============================

@st.cache_resource
def load_model():
    return tf.keras.models.load_model(
        "models/lung_cancer_model.keras"
    )

model = None
model_loaded = False

try:
    model = load_model()
    model_loaded = True
except Exception as e:
    st.error(get_text(lang, "model_load_error"))
    st.code(str(e))

# =============================
# Classes (internal names - matches model output order, don't translate here)
# =============================

classes = [
    "Adenocarcinoma",
    "Large Cell Carcinoma",
    "Normal",
    "Squamous Cell Carcinoma"
]

# ربط كل اسم داخلي بمفتاح الترجمة الخاص بيه
DISEASE_KEYS = {
    "Adenocarcinoma": "adenocarcinoma",
    "Large Cell Carcinoma": "large_cell",
    "Normal": "normal",
    "Squamous Cell Carcinoma": "squamous",
}

def disease_label(disease_name: str) -> str:
    """يرجع اسم المرض مترجم للعرض للمستخدم"""
    key = DISEASE_KEYS.get(disease_name)
    return get_text(lang, f"disease_{key}") if key else disease_name

# =============================
# Instructions
# =============================

st.info(f"""

### {get_text(lang, "instructions_header")}

• {get_text(lang, "instructions_upload")}

• {get_text(lang, "instructions_analyze")}

• {get_text(lang, "instructions_wait")}

• {get_text(lang, "instructions_review")}

""")

# =============================
# Upload
# =============================

uploaded = st.file_uploader(
    get_text(lang, "upload_label"),
    type=["png", "jpg", "jpeg"]
)

prediction = None
confidence = None
disease = None

if uploaded is not None:

    image = Image.open(uploaded).convert("RGB")

    left, right = st.columns([1, 1])

    with left:
        st.image(
            image,
            use_container_width=True,
            caption=get_text(lang, "uploaded_caption")
        )

    img = image.resize((224, 224))
    img = np.array(img)
    img = img.astype(np.float32) / 255.0
    img = np.expand_dims(img, 0)

    with right:
        st.subheader(get_text(lang, "ai_analysis_header"))

        if st.button(
            get_text(lang, "analyze_button"),
            use_container_width=True
        ):
            if not model_loaded:
                st.error(get_text(lang, "model_not_loaded"))
                st.stop()

            with st.spinner(get_text(lang, "analyzing")):
                prediction = model.predict(
                    img,
                    verbose=0
                )

            pred = np.argmax(prediction)
            confidence = float(np.max(prediction)) * 100
            disease = classes[pred]

            st.success(get_text(lang, "analysis_completed"))

            st.metric(
                get_text(lang, "prediction_label"),
                disease_label(disease)
            )

            st.metric(
                get_text(lang, "confidence_label"),
                f"{confidence:.2f}%"
            )

            st.progress(int(confidence))

# =====================================
# Diagnosis Dashboard
# =====================================

if disease is not None:

    st.divider()

    st.subheader(get_text(lang, "diagnosis_dashboard_header"))

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            get_text(lang, "detected_disease_label"),
            disease_label(disease)
        )

        st.metric(
            get_text(lang, "confidence_label"),
            f"{confidence:.2f}%"
        )

    with col2:
        st.write(f"### {get_text(lang, 'ai_confidence_level_header')}")

        st.progress(int(confidence))

        if confidence >= 90:
            st.success(get_text(lang, "conf_very_high"))
        elif confidence >= 75:
            st.info(get_text(lang, "conf_high"))
        elif confidence >= 50:
            st.warning(get_text(lang, "conf_moderate"))
        else:
            st.error(get_text(lang, "conf_low"))

    # =====================================
    # Probability Distribution
    # =====================================

    st.divider()

    st.subheader(get_text(lang, "prob_dist_header"))

    probs = prediction[0]

    chart = {}
    for i in range(len(classes)):
        chart[disease_label(classes[i])] = float(probs[i] * 100)

    st.bar_chart(chart)

    # =====================================
    # AI Summary
    # =====================================

    st.divider()

    st.subheader(get_text(lang, "ai_summary_header"))

    summary_key = DISEASE_KEYS.get(disease)
    summary_text = get_text(lang, f"summary_{summary_key}")

    if disease == "Normal":
        st.success(summary_text)
    else:
        st.error(summary_text)

    # =====================================
    # Disease Information
    # =====================================

    st.divider()

    st.subheader(get_text(lang, "disease_info_header"))

    info_key = DISEASE_KEYS.get(disease)
    desc_text = get_text(lang, f"desc_{info_key}")
    rec_text = get_text(lang, f"rec_{info_key}")

    st.info(f"""

### {get_text(lang, "description_label")}

{desc_text}

### {get_text(lang, "recommendation_label")}

{rec_text}

""")

# =====================================
# Risk Indicator
# =====================================

if disease is not None:

    st.divider()

    st.subheader(get_text(lang, "risk_assessment_header"))

    if confidence >= 90:
        st.success(get_text(lang, "risk_very_high"))
    elif confidence >= 75:
        st.info(get_text(lang, "risk_high"))
    elif confidence >= 50:
        st.warning(get_text(lang, "risk_moderate"))
    else:
        st.error(get_text(lang, "risk_low"))

    # =====================================
    # Future PDF Report
    # =====================================

    st.divider()

    st.subheader(get_text(lang, "medical_report_header"))

    st.info(get_text(lang, "pdf_report_info"))

    st.button(
        get_text(lang, "download_pdf_button"),
        disabled=True,
        use_container_width=True
    )

    # =====================================
    # Future Grad-CAM
    # =====================================

    st.divider()

    st.subheader(get_text(lang, "explainable_ai_header"))

    st.info(get_text(lang, "gradcam_info"))

# =====================================
# Recommendations
# =====================================

st.divider()

st.subheader(get_text(lang, "general_recommendations_header"))

st.write(get_text(lang, "rec_bullet_1"))
st.write(get_text(lang, "rec_bullet_2"))
st.write(get_text(lang, "rec_bullet_3"))
st.write(get_text(lang, "rec_bullet_4"))
st.write(get_text(lang, "rec_bullet_5"))

# =====================================
# Disclaimer
# =====================================

st.warning(get_text(lang, "disclaimer_text"))

# =====================================
# Footer
# =====================================

st.divider()

c1, c2, c3 = st.columns(3)

with c1:
    st.metric(get_text(lang, "ai_model_label"), "EfficientNetB0")

with c2:
    st.metric(get_text(lang, "image_size_label"), "224 × 224")

with c3:
    st.metric(get_text(lang, "classes_label"), "4")

st.caption(get_text(lang, "footer_caption"))