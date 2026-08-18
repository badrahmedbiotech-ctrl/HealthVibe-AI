import os
import uuid

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

import translation
from components.branding import LOGO
from utils.navigation import sidebar


# ==========================================================
# ENVIRONMENT
# ==========================================================

load_dotenv()

API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="HealthVibe AI",
    page_icon=str(LOGO),
    layout="wide",
)


# ==========================================================
# TRANSLATION
# ==========================================================

translation.init()


# ==========================================================
# MAIN SIDEBAR
# ==========================================================

# Uses the same HealthVibe sidebar used by the other pages.
sidebar()


# ==========================================================
# PAGE HEADER
# ==========================================================

st.title("🩺 HealthVibe AI")
st.caption("Your healthcare assistant")


# ==========================================================
# CONSTANTS
# ==========================================================

WELCOME_MESSAGE = (
    "مرحباً 👋 أنا مساعدك الصحي الذكي HealthVibe AI. "
    "كيف يمكنني مساعدتك اليوم؟"
)


# ==========================================================
# CHAT MANAGEMENT
# ==========================================================

def create_new_chat():
    """Create a new empty chat and make it the active chat."""

    chat_id = str(uuid.uuid4())

    st.session_state.all_chats[chat_id] = {
        "title": "New Chat",
        "messages": [
            {
                "role": "assistant",
                "content": WELCOME_MESSAGE,
            }
        ],
    }

    st.session_state.current_chat = chat_id


if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}


if "current_chat" not in st.session_state:

    create_new_chat()


current_chat_id = st.session_state.current_chat


if current_chat_id not in st.session_state.all_chats:

    create_new_chat()

    current_chat_id = st.session_state.current_chat


st.session_state.messages = (
    st.session_state.all_chats[current_chat_id]["messages"]
)


# ==========================================================
# CHAT HISTORY
# ==========================================================

# Keep chat history inside the SAME HealthVibe sidebar.
with st.sidebar:

    st.subheader("💬 Chat History")

    if st.button(
        "➕ New Chat",
        use_container_width=True,
    ):

        create_new_chat()
        st.rerun()

    st.divider()

    for chat_id, chat_data in list(
        st.session_state.all_chats.items()
    ):

        chat_title = chat_data.get(
            "title",
            "New Chat",
        )

        if st.button(
            chat_title,
            key=f"chat_{chat_id}",
            use_container_width=True,
        ):

            st.session_state.current_chat = chat_id
            st.rerun()


# ==========================================================
# DATASET LOADING
# ==========================================================

@st.cache_resource
def load_datasets():

    datasets = {}

    possible_paths = [
        "dataset",
        "datasets",
    ]

    base_path = None

    for path in possible_paths:

        if os.path.exists(path):
            base_path = path
            break

    if base_path is None:
        return datasets

    dataset_files = {
        "medical_data": "filtered_medical_data.csv",
        "diabetes": "diabetes_filtered.csv",
        "thrombosis": "thrombosis_filtered.csv",
        "heart_risk": "DOC-20260722-WA0080_.csv",
    }

    for name, filename in dataset_files.items():

        file_path = os.path.join(
            base_path,
            filename,
        )

        try:

            if os.path.exists(file_path):

                datasets[name] = pd.read_csv(
                    file_path
                )

            else:

                datasets[name] = None

        except Exception:

            datasets[name] = None

    return datasets


if "datasets" not in st.session_state:

    st.session_state.datasets = load_datasets()


# ==========================================================
# GROQ CLIENT
# ==========================================================

client = None

if API_KEY:

    try:

        client = Groq(
            api_key=API_KEY
        )

    except Exception as error:

        st.error(
            f"تعذر تشغيل المساعد الذكي: {error}"
        )

else:

    st.warning(
        "مفتاح GROQ_API_KEY غير موجود. "
        "تأكد من إعداد المفتاح في المشروع."
    )


# ==========================================================
# DATASET SEARCH
# ==========================================================

def search_in_dataset(query, datasets):

    results = []

    medical_data = datasets.get(
        "medical_data"
    )

    if medical_data is None:
        return results

    query = str(query).strip()

    if not query:
        return results

    # ------------------------------------------------------
    # Search symptoms
    # ------------------------------------------------------

    if "Symptoms" in medical_data.columns:

        symptoms = medical_data[
            medical_data["Symptoms"]
            .astype(str)
            .str.contains(
                query,
                case=False,
                na=False,
                regex=False,
            )
        ]

        for _, row in symptoms.head(3).iterrows():

            results.append(
                {
                    "type": "symptom",
                    "symptom": row.get(
                        "Symptoms",
                        "",
                    ),
                    "disease": row.get(
                        "Disease",
                        "",
                    ),
                    "treatment": row.get(
                        "Treatment",
                        "",
                    ),
                }
            )

    # ------------------------------------------------------
    # Search diseases
    # ------------------------------------------------------

    if "Disease" in medical_data.columns:

        diseases = medical_data[
            medical_data["Disease"]
            .astype(str)
            .str.contains(
                query,
                case=False,
                na=False,
                regex=False,
            )
        ]

        for _, row in diseases.head(3).iterrows():

            results.append(
                {
                    "type": "disease",
                    "disease": row.get(
                        "Disease",
                        "",
                    ),
                    "treatment": row.get(
                        "Treatment",
                        "",
                    ),
                }
            )

    return results


# ==========================================================
# DISPLAY CHAT MESSAGES
# ==========================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )


# ==========================================================
# CHAT INPUT
# ==========================================================

prompt = st.chat_input(
    "اكتب سؤالك..."
)


if prompt:

    prompt = prompt.strip()

    if not prompt:
        st.stop()

    # ------------------------------------------------------
    # Save user message
    # ------------------------------------------------------

    user_message = {
        "role": "user",
        "content": prompt,
    }

    st.session_state.messages.append(
        user_message
    )

    # ------------------------------------------------------
    # Update chat title
    # ------------------------------------------------------

    if len(st.session_state.messages) == 2:

        title = prompt[:30]

        if len(prompt) > 30:
            title += "..."

        st.session_state.all_chats[
            current_chat_id
        ]["title"] = title

    # ------------------------------------------------------
    # Display user message
    # ------------------------------------------------------

    with st.chat_message("user"):

        st.write(prompt)

    # ------------------------------------------------------
    # Generate AI response
    # ------------------------------------------------------

    with st.chat_message("assistant"):

        if client is None:

            st.error(
                "لا يمكن تشغيل المساعد حالياً. "
                "تأكد من إعداد GROQ_API_KEY."
            )

        else:

            with st.spinner(
                "جاري التفكير..."
            ):

                try:

                    # ======================================
                    # DATASET SEARCH
                    # ======================================

                    search_results = search_in_dataset(
                        prompt,
                        st.session_state.datasets,
                    )

                    context_data = ""

                    for result in search_results[:3]:

                        if result["type"] == "symptom":

                            context_data += (
                                f"- العرض: "
                                f"{result['symptom']}\n"
                                f"- المرض المرتبط: "
                                f"{result['disease']}\n"
                                f"- العلاج الموجود في "
                                f"البيانات: "
                                f"{result['treatment']}\n\n"
                            )

                        elif result["type"] == "disease":

                            context_data += (
                                f"- المرض: "
                                f"{result['disease']}\n"
                                f"- العلاج الموجود في "
                                f"البيانات: "
                                f"{result['treatment']}\n\n"
                            )

                    if not context_data:

                        context_data = (
                            "لا توجد مطابقة مباشرة "
                            "في قاعدة البيانات المحلية."
                        )

                    # ======================================
                    # SYSTEM PROMPT
                    # ======================================

                    system_prompt = f"""
أنت HealthVibe AI، مساعد صحي ذكي
يقدم معلومات صحية وتثقيفية باللغة العربية.

قواعد الإجابة:

- أجب باللغة العربية الواضحة.
- لا تقدم تشخيصاً نهائياً بناءً على الأعراض فقط.
- وضح أن الأعراض قد يكون لها أكثر من سبب.
- لا تذكر أمراضاً بعيدة أو غير مدعومة بالمعلومات.
- إذا كانت المعلومات غير كافية، اطرح أسئلة متابعة مناسبة.
- لا تقدم جرعات دوائية أو وصفات علاجية خطرة.
- قدم معلومات تثقيفية وليست بديلاً عن الطبيب.
- استخدم الاختصارات الطبية المعروفة فقط عند الحاجة مثل:
  ECG, MRI, CT, HbA1c.

حالات الطوارئ:

إذا ذكر المستخدم أعراضاً قد تشير إلى حالة طارئة،
مثل ألم شديد في الصدر، صعوبة شديدة في التنفس،
فقدان الوعي، أعراض السكتة الدماغية،
نزيف شديد أو حساسية شديدة:

1. نبه أولاً إلى أن الحالة قد تكون طارئة.
2. انصح بطلب الرعاية الطبية العاجلة.
3. وضح السبب بشكل مختصر.
4. لا تؤخر النصيحة الطارئة بأسئلة كثيرة.

تنسيق الإجابة:

1. ملخص المشكلة
2. الأسباب أو الاحتمالات المحتملة
3. أسئلة إضافية عند الحاجة
4. نصائح عامة
5. علامات تستدعي الطوارئ
6. تنويه طبي مختصر

بيانات قاعدة البيانات المحلية:

{context_data}
"""

                    # ======================================
                    # GROQ REQUEST
                    # ======================================

                    response = client.chat.completions.create(

                        model=(
                            "llama-3.3-70b-versatile"
                        ),

                        temperature=0.2,

                        top_p=0.9,

                        max_tokens=800,

                        messages=[
                            {
                                "role": "system",
                                "content": system_prompt,
                            }
                        ]
                        + st.session_state.messages,
                    )

                    # ======================================
                    # GET RESPONSE
                    # ======================================

                    answer = (
                        response
                        .choices[0]
                        .message
                        .content
                        .strip()
                    )

                    # ======================================
                    # DISPLAY RESPONSE
                    # ======================================

                    st.write(answer)

                    # ======================================
                    # SAVE RESPONSE
                    # ======================================

                    assistant_message = {
                        "role": "assistant",
                        "content": answer,
                    }

                    st.session_state.messages.append(
                        assistant_message
                    )

                    st.session_state.all_chats[
                        current_chat_id
                    ]["messages"] = (
                        st.session_state.messages
                    )

                except Exception as error:

                    st.error(
                        f"حدث خطأ أثناء تشغيل المساعد: "
                        f"{error}"
                    )