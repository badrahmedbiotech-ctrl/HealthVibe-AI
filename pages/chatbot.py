import os
import uuid
from datetime import datetime

import pandas as pd
from groq import Groq
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()  # بيلقط المفاتيح من ملف .env تلقائياً
# ==========================
# Page Config
# ==========================
st.set_page_config(
    page_title="HealthVibe AI",
    page_icon="🩺",
    layout="centered",
)

# ==========================
# Title
# ==========================
st.title("🩺 HealthVibe AI")
st.caption("Your healthcare assistant")

# ==========================
# LOAD DATASETS (تلقائي في الخلفية)
# ==========================

@st.cache_resource
def load_datasets():
    """تحميل جميع ملفات البيانات تلقائياً"""
    datasets = {}
    
    # تحديد المسار للـ dataset سواء كانت برة أو جوة مجلد dataset
    base_path = "dataset/" if os.path.exists("dataset") else ""
    
    try:
        datasets["medical_data"] = pd.read_csv(os.path.join(base_path, "filtered_medical_data.csv"))
    except Exception:
        datasets["medical_data"] = None
    
    try:
        datasets["diabetes"] = pd.read_csv(os.path.join(base_path, "diabetes_filtered.csv"))
    except Exception:
        datasets["diabetes"] = None
    
    try:
        datasets["thrombosis"] = pd.read_csv(os.path.join(base_path, "thrombosis_filtered.csv"))
    except Exception:
        datasets["thrombosis"] = None
    
    try:
        datasets["heart_risk"] = pd.read_csv(os.path.join(base_path, "DOC-20260722-WA0080_.csv"))
    except Exception:
        datasets["heart_risk"] = None
    
    return datasets

# تحميل البيانات تلقائياً في الخلفية
if "datasets" not in st.session_state:
    st.session_state.datasets = load_datasets()

# ==========================
# Sidebar (Chat History)
# ==========================

if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}

if "current_chat" not in st.session_state:
    chat_id = str(uuid.uuid4())
    st.session_state.current_chat = chat_id
    st.session_state.all_chats[chat_id] = {
        "title": "New Chat",
        "messages": [
            {
                "role": "assistant",
                "content": "مرحباً 👋 أنا مساعدك الصحي الذكي HealthVibe AI. كيف يمكنني مساعدتك اليوم؟"
            }
        ]
    }

with st.sidebar:
    st.subheader("Chat History")
    
    if st.button("➕ New Chat", use_container_width=True):
        new_id = str(uuid.uuid4())
        st.session_state.all_chats[new_id] = {
            "title": "New Chat",
            "messages": [
                {
                    "role": "assistant",
                    "content": "مرحباً 👋 أنا مساعدك الصحي الذكي HealthVibe AI. كيف يمكنني مساعدتك اليوم؟"
                }
            ]
        }
        st.session_state.current_chat = new_id
        st.rerun()
    
    st.divider()
    
    for cid, data in list(st.session_state.all_chats.items()):
        if st.button(data["title"], key=cid, use_container_width=True):
            st.session_state.current_chat = cid
            st.rerun()

# تعيين الرسائل للمحادثة الحالية
current_chat_id = st.session_state.current_chat
st.session_state.messages = st.session_state.all_chats[current_chat_id]["messages"]

# ==========================
# Groq Client
# ==========================

# هيحاول يقرأ الأول من st.secrets، ولو مش لاقيه هيقرأ من os.getenv
api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

# ==========================
# Search Functions
# ==========================

def search_in_dataset(query, datasets):
    """البحث عن معلومات في الـ Dataset"""
    results = []
    
    if datasets.get("medical_data") is not None:
        medical = datasets["medical_data"]
        
        # البحث في الأعراض والأمراض
        symptoms = medical[
            medical["Symptoms"].str.contains(query, case=False, na=False)
        ] if "Symptoms" in medical.columns else []
        
        diseases = medical[
            medical["Disease"].str.contains(query, case=False, na=False)
        ] if "Disease" in medical.columns else []
        
        if len(symptoms) > 0:
            for _, row in symptoms.head(3).iterrows():
                results.append({
                    "type": "symptom",
                    "symptom": row.get("Symptoms", ""),
                    "disease": row.get("Disease", ""),
                    "treatment": row.get("Treatment", "")
                })
        
        if len(diseases) > 0:
            for _, row in diseases.head(3).iterrows():
                results.append({
                    "type": "disease",
                    "disease": row.get("Disease", ""),
                    "treatment": row.get("Treatment", "")
                })
    
    return results

# ==========================
# Display Message History
# ==========================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# ==========================
# Chat Input
# ==========================

if prompt := st.chat_input("اكتب سؤالك..."):
    
    prompt = prompt.strip()
    
    if not prompt:
        st.stop()
    
    # إضافة رسالة المستخدم
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })
    
    # تحديث عنوان المحادثة إذا كانت الرسالة الأولى من المستخدم
    if len(st.session_state.messages) == 2:
        title = prompt[:30] + ("..." if len(prompt) > 30 else "")
        st.session_state.all_chats[current_chat_id]["title"] = title
    
    # عرض رسالة المستخدم فوراً
    with st.chat_message("user"):
        st.write(prompt)
    
    # إنشاء الرد من المساعد الذكي
    with st.chat_message("assistant"):
        with st.spinner("جاري التفكير..."):
            try:
                # البحث في Dataset
                search_results = search_in_dataset(prompt, st.session_state.datasets)
                
                context_data = ""
                if search_results:
                    for result in search_results[:2]:
                        if result["type"] == "symptom":
                            context_data += f"- عرض: {result['symptom']} قد يرتبط بـ: {result['disease']}.\n"
                        elif result["type"] == "disease":
                            context_data += f"- مرض: {result['disease']} علاج مقترح: {result['treatment']}.\n"
                
                # إعداد System Prompt المحسّن
                formatted_context = context_data if context_data else "No direct match in local dataset."
                
                system_prompt = f"""You are HealthVibe AI, a medical assistant that provides educational health information in Arabic.

GENERAL RULES:
- Respond ONLY in Modern Standard Arabic.
- Never mix Arabic with French, Chinese, Russian, Japanese, or any other language.
- Only use internationally accepted medical abbreviations when necessary (ECG, MRI, CT, HbA1c).
- If any foreign word appears, replace it with its Arabic equivalent before finishing the response.

MEDICAL RULES:
- Never provide a definitive diagnosis based only on symptoms.
- Symptoms may have multiple possible causes.
- Mention only the 2–3 most likely causes supported by the reported symptoms.
- Do not mention diseases that are weakly supported or unlikely.
- If information is insufficient, ask 2–5 relevant follow-up questions before suggesting causes.
- Explain the reasoning briefly and logically.
- Separate symptoms from possible causes.
- Keep the response clinically accurate and avoid speculation.

EMERGENCY RULE:
If the user reports symptoms suggesting a medical emergency (such as severe chest pain, pain radiating to the arm or jaw, shortness of breath, stroke symptoms, loss of consciousness, severe allergic reaction, or uncontrolled bleeding):

1. FIRST state that this may be a medical emergency.
2. Advise immediate medical attention or going to the nearest emergency department.
3. Then briefly explain why.
4. Only after that ask follow-up questions if appropriate.

RESPONSE FORMAT:
1. ملخص الأعراض
2. الأسباب المحتملة
3. أسئلة إضافية (إذا لزم الأمر)
4. نصائح عامة
5. علامات تستدعي الطوارئ (إذا وجدت)
6. تنويه طبي قصير

Context from dataset:
{formatted_context}
"""

                # إرسال الطلب لـ Groq
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    temperature=0.2,
                    top_p=0.9,
                    max_tokens=800,
                    messages=[
                        {
                            "role": "system",
                            "content": system_prompt
                        }
                    ] + st.session_state.messages
                )
                
                answer = response.choices[0].message.content.strip()
                
                # عرض الرد وإضافته للجلسة
                st.write(answer)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })
                
                # حفظ المخرجات في سجل المحادثة
                st.session_state.all_chats[current_chat_id]["messages"] = st.session_state. messages
                
            except Exception as e:
                st.error(f"خطأ: {str(e)}")