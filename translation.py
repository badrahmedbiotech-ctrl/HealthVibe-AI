import streamlit as st

LANG_META = {
    "en": {"name": "English", "dir": "ltr", "switch_label": "العربية 🇪🇬"},
    "ar": {"name": "العربية", "dir": "rtl", "switch_label": "English 🇬🇧"},
}

TRANSLATIONS = {
    "en": {
        "about_intro": """
Welcome to *HealthVibe AI*.

HealthVibe AI is an intelligent healthcare platform that combines Artificial Intelligence and medical data analysis to support both patients and healthcare professionals.

Our platform provides:

- Early disease prediction
- Personalized health insights
- AI-powered medical assistance
- Automated medical reports
- Continuous patient monitoring

within one integrated healthcare ecosystem.
""",
        "about_vision": """
To become a leading AI-powered healthcare platform that transforms preventive medicine by enabling early disease detection, intelligent clinical decision support, and continuous patient monitoring.

HealthVibe aims to make healthcare more accessible, personalized, and data-driven, empowering both patients and healthcare professionals to improve health outcomes through innovative technology.
""",
        "about_mission": """
Our mission is to transform preventive healthcare by developing an intelligent platform that connects Artificial Intelligence with medical expertise.

HealthVibe helps patients understand their health risks through early disease prediction while enabling healthcare professionals to monitor patients, generate comprehensive medical reports, and make data-driven clinical decisions.

We strive to improve healthcare accessibility, reduce diagnostic delays, and promote healthier lives through innovative digital technology.
""",
        "reco_high_risk": """
### High Risk

• Visit an Internal Medicine doctor.

• Perform HbA1c Test.

• Monitor Blood Glucose.

• Reduce Sugar Intake.

• Exercise 30 minutes daily.

• Lose excess weight.

• Repeat laboratory tests.
""",
        "reco_healthy_lifestyle": """
### Healthy Lifestyle

• Continue healthy nutrition.

• Exercise regularly.

• Drink enough water.

• Annual Diabetes Screening.

• Maintain healthy body weight.
""",

        # --- CT_Scan_AI.py ---
        "tf_not_found": """
TensorFlow is not available on this machine.

The current processor does not support
the modern version of TensorFlow.

You can use Google Colab or a newer device.
""",
        "ct_instructions": """

### Instructions

• Upload CT Scan

• Click Analyze

• Wait for AI

• Review Results

""",
        "Analyzing...": "Analyzing...",
        "summary_normal": """

No obvious abnormality detected.

The lungs appear normal according
to the trained AI model.

""",
        "summary_adenocarcinoma": """

Possible Adenocarcinoma detected.

Further investigations are required.

""",
        "summary_large_cell": """

Possible Large Cell Carcinoma detected.

Immediate clinical evaluation is recommended.

""",
        "summary_squamous": """

Possible Squamous Cell Carcinoma detected.

Smoking history should be reviewed.

""",
        "info_normal": """

### Description

Healthy lung appearance.

### Recommendation

• Regular medical check-up

• Healthy lifestyle

• Avoid smoking

""",
        "info_adenocarcinoma": """

### Description

Most common type of lung cancer.

Usually develops in the outer lung.

### Recommendation

• Chest CT

• PET Scan

• Biopsy

• Oncology consultation

""",
        "info_large_cell": """

### Description

Aggressive non-small cell lung cancer.

### Recommendation

• Immediate specialist referral

• Additional imaging

• Tissue biopsy

""",
        "info_squamous": """

### Description

Usually associated with smoking.

Often develops near central bronchi.

### Recommendation

• Smoking cessation

• Bronchoscopy

• Oncology consultation

""",
        "pdf_report_info": """
PDF Report will include:

• Patient Information

• AI Prediction

• Confidence Score

• CT Scan Result

• Medical Recommendations

• Doctor Notes

(Coming Soon)
""",
        "gradcam_info": """
Grad-CAM Visualization

This feature will highlight the region
that the AI focused on while making
its prediction.

(Coming Soon)
""",
        "ct_disclaimer": """
This application is intended for educational
and research purposes only.

HealthVibe AI does NOT replace
professional medical diagnosis.
""",
    },
    "ar": {
        # --- app.py ---
        "HealthVibe AI": "HealthVibe AI",
        "AI Clinical Decision Support Platform": "منصة دعم القرار السريري بالذكاء الاصطناعي",
        "Choose how you want to continue": "اختر كيف تريد المتابعة",
        "Patient": "مريض",
        "Access your medical dashboard": "الوصول إلى لوحة بياناتك الطبية",
        "Continue as Patient": "المتابعة كمريض",
        "Doctor": "طبيب",
        "Access your doctor dashboard": "الوصول إلى لوحة بيانات الطبيب",
        "Continue as Doctor": "المتابعة كطبيب",

        # --- Home.py / Dashboard.py ---
        "🟢 AI Clinical Decision Support Platform": "🟢 منصة دعم القرار السريري بالذكاء الاصطناعي",
        "🩺 Welcome to HealthVibe AI": "🩺 مرحبًا بك في HealthVibe AI",
        "Welcome to HealthVibe AI": "مرحبًا بك في HealthVibe AI",
        "Predict diseases early.": "التنبؤ بالأمراض مبكرًا.",
        "Generate smart medical reports.": "إنشاء تقارير طبية ذكية.",
        "Empower doctors and patients using Artificial Intelligence.": "تمكين الأطباء والمرضى باستخدام الذكاء الاصطناعي.",

        "🚀 Start Diagnosis": "🚀 ابدأ التشخيص",
        "🤖 AI Assistant": "🤖 المساعد الذكي",
        "📋 Medical History": "📋 السجل الطبي",
        "👤 My Profile": "👤 ملفي الشخصي",

        "✨ Platform Features": "✨ ميزات المنصة",
        "AI Diagnosis": "تشخيص بالذكاء الاصطناعي",
        "Predict diseases using Artificial Intelligence.": "التنبؤ بالأمراض باستخدام الذكاء الاصطناعي.",
        "Medical Reports": "التقارير الطبية",
        "Generate downloadable clinical reports.": "إنشاء تقارير سريرية قابلة للتحميل.",
        "Risk Assessment": "تقييم المخاطر",
        "Evaluate patient risk level instantly.": "تقييم مستوى خطورة المريض فوريًا.",
        "Secure Data": "بيانات آمنة",
        "Protected patient records and authentication.": "سجلات مرضى محمية وتوثيق آمن.",

        "📊 HealthVibe AI Statistics": "📊 إحصائيات HealthVibe AI",
        "Patients": "المرضى",
        "Predictions": "التنبؤات",
        "Doctors": "الأطباء",
        "Accuracy": "الدقة",

        "🩺 AI Prediction Modules": "🩺 وحدات التنبؤ بالذكاء الاصطناعي",
        "Diabetes Prediction": "التنبؤ بمرض السكري",
        "AI-based Blood Glucose Risk Prediction": "تنبؤ بمخاطر سكر الدم بالذكاء الاصطناعي",
        "Open Diabetes": "فتح السكري",
        "Hypertension": "ضغط الدم المرتفع",
        "Blood Pressure Prediction": "التنبؤ بضغط الدم",
        "Open Hypertension": "فتح ضغط الدم",
        "Lipid Profile": "تحليل الدهون",
        "Lipid": "الدهون",
        "Cholesterol Risk Analysis": "تحليل مخاطر الكوليسترول",
        "Open Lipid": "فتح الدهون",
        "Obesity": "السمنة",
        "BMI & Obesity Risk Prediction": "التنبؤ بمؤشر كتلة الجسم والسمنة",
        "Open Obesity": "فتح السمنة",
        "Pulmonary Fibrosis": "تليّف الرئة",
        "Lung Disease Prediction": "التنبؤ بأمراض الرئة",
        "Open Pulmonary": "فتح تليّف الرئة",
        "CT Scan AI": "الذكاء الاصطناعي للأشعة المقطعية",
        "CT Scan": "الأشعة المقطعية",
        "Medical Image Detection": "كشف الصور الطبية",
        "Open CT Scan": "فتح الأشعة المقطعية",

        "🌍 Why Choose HealthVibe AI ?": "🌍 لماذا تختار HealthVibe AI؟",
        "🏥 Intelligent Healthcare Platform": "🏥 منصة رعاية صحية ذكية",
        "✔ Early Disease Detection": "✔ الكشف المبكر عن الأمراض",
        "✔ AI Clinical Decision Support": "✔ دعم القرار السريري بالذكاء الاصطناعي",
        "✔ Instant Medical Reports": "✔ تقارير طبية فورية",
        "✔ Patient History Tracking": "✔ تتبع السجل الطبي للمريض",
        "✔ Doctor Dashboard": "✔ لوحة بيانات الطبيب",
        "✔ Secure Database": "✔ قاعدة بيانات آمنة",
        "✔ Fast Predictions": "✔ تنبؤات سريعة",
        "❤️ HealthVibe Score": "❤️ درجة HealthVibe",
        "AI Accuracy": "دقة الذكاء الاصطناعي",
        "Prediction Speed": "سرعة التنبؤ",
        "Availability": "التوفر",

        "🚀 Upcoming Features": "🚀 ميزات قادمة",
        "📅 Smart Appointment System": "📅 نظام مواعيد ذكي",
        "💊 Medication Reminder": "💊 تذكير بالأدوية",
        "📱 Mobile Application": "📱 تطبيق الموبايل",

        "🎯 Ready to Start?": "🎯 جاهز تبدأ؟",
        "🩺 Start Your First Diagnosis": "🩺 ابدأ تشخيصك الأول",
        "🤖 Talk with AI Assistant": "🤖 تحدث مع المساعد الذكي",

        "🩺 HealthVibe AI": "🩺 HealthVibe AI",
        "Empowering Healthcare with Artificial Intelligence": "تمكين الرعاية الصحية بالذكاء الاصطناعي",
        "Developed by ": "تم التطوير بواسطة ",
        "Version 2.0": "الإصدار 2.0",
        "© 2026 HealthVibe AI • All Rights Reserved": "© 2026 HealthVibe AI • جميع الحقوق محفوظة",

        # --- About.py ---
        "💙 About HealthVibe AI": "💙 عن HealthVibe AI",

        "about_intro": """مرحبًا بك في *HealthVibe AI*.

HealthVibe AI هي منصة رعاية صحية ذكية تجمع بين الذكاء الاصطناعي وتحليل البيانات الطبية لدعم المرضى والكوادر الطبية.

توفر منصتنا:

- التنبؤ المبكر بالأمراض
- رؤى صحية شخصية
- مساعدة طبية بالذكاء الاصطناعي
- تقارير طبية آلية
- متابعة مستمرة للمريض

ضمن منظومة رعاية صحية متكاملة.""",

        "🌍 Vision": "🌍 الرؤية",

        "about_vision": """أن نصبح منصة رائدة في الرعاية الصحية بالذكاء الاصطناعي تُحدث نقلة في الطب الوقائي من خلال الكشف المبكر عن الأمراض، ودعم القرار السريري الذكي، والمتابعة المستمرة للمريض.

تسعى HealthVibe لجعل الرعاية الصحية أكثر سهولة وتخصيصًا واعتمادًا على البيانات، بما يمكّن المرضى والكوادر الطبية من تحسين النتائج الصحية عبر تقنيات مبتكرة.""",

        "🎯 Mission": "🎯 الرسالة",

        "about_mission": """رسالتنا هي إحداث نقلة في الرعاية الصحية الوقائية من خلال تطوير منصة ذكية تربط الذكاء الاصطناعي بالخبرة الطبية.

تساعد HealthVibe المرضى على فهم مخاطرهم الصحية عبر التنبؤ المبكر بالأمراض، وفي نفس الوقت تمكّن الكوادر الطبية من متابعة المرضى، وإنشاء تقارير طبية شاملة، واتخاذ قرارات سريرية مبنية على البيانات.

نسعى لتحسين إمكانية الوصول للرعاية الصحية، وتقليل تأخير التشخيص، وتعزيز حياة أكثر صحة من خلال التكنولوجيا الرقمية المبتكرة.""",

        "⭐ Core Values": "⭐ القيم الأساسية",
        "🩺 Early Disease Detection": "🩺 الكشف المبكر عن الأمراض",
        "🤖 AI-Powered Healthcare": "🤖 رعاية صحية بالذكاء الاصطناعي",
        "📄 Smart Medical Reports": "📄 تقارير طبية ذكية",
        "👨‍⚕️ Clinical Decision Support": "👨‍⚕️ دعم القرار السريري",
        "❤️ Patient-Centered Care": "❤️ رعاية محورها المريض",
        "🌍 Innovation & Accessibility": "🌍 الابتكار وسهولة الوصول",

        # --- Profile.py ---
        "🟢 Medical Profile": "🟢 الملف الطبي",
        "Manage your medical information securely": "إدارة معلوماتك الطبية بأمان",
        "Age": "السن",
        "Gender": "النوع",
        "Weight": "الوزن",
        "Height": "الطول",
        "👤 Personal Information": "👤 البيانات الشخصية",
        "Full Name": "الاسم بالكامل",
        "Birth Date": "تاريخ الميلاد",
        "Phone Number": "رقم الهاتف",
        "Address": "العنوان",
        "Weight (kg)": "الوزن (كجم)",
        "Height (cm)": "الطول (سم)",
        "🩺 Medical Information": "🩺 المعلومات الطبية",
        "Blood Group": "فصيلة الدم",
        "Choose Blood Group": "اختر فصيلة الدم",
        "Smoking": "التدخين",
        "Alcohol": "الكحول",
        "Allergies": "الحساسية",
        "Chronic Diseases": "الأمراض المزمنة",
        "Current Medications": "الأدوية الحالية",
        "🚨 Emergency Contact": "🚨 جهة اتصال الطوارئ",
        "Contact Name": "اسم جهة الاتصال",
        "Relationship": "صلة القرابة",
        "💾 Save Changes": "💾 حفظ التغييرات",
        "💾 Save Medical Profile": "💾 حفظ الملف الطبي",
        "✅ Medical Profile Updated Successfully": "✅ تم تحديث الملف الطبي بنجاح",
        "📊 Profile Summary": "📊 ملخص الملف الشخصي",
        "Profile Completion": "نسبة اكتمال الملف",
        "BMI": "مؤشر كتلة الجسم",
        "⚠ Underweight": "⚠ نقص في الوزن",
        "✅ Normal Weight": "✅ وزن طبيعي",
        "⚠ Overweight": "⚠ زيادة في الوزن",
        "🔴 Obesity": "🔴 سمنة",
        "⚡ Quick Actions": "⚡ إجراءات سريعة",
        "🏠 Back To Dashboard": "🏠 العودة للوحة الرئيسية",
        "📋 View Medical History": "📋 عرض السجل الطبي",
        "💡 Personalized Health Tips": "💡 نصائح صحية مخصصة",
        "🥛 Increase healthy calories.": "🥛 زد من السعرات الحرارية الصحية.",
        "🍗 Eat more protein.": "🍗 تناول المزيد من البروتين.",
        "🏋️ Start resistance training.": "🏋️ ابدأ تمارين المقاومة.",
        "🥗 Maintain your balanced diet.": "🥗 حافظ على نظامك الغذائي المتوازن.",
        "🚶 Walk daily.": "🚶 امشِ يوميًا.",
        "🏃 Increase physical activity.": "🏃 زد من النشاط البدني.",
        "🍟 Reduce fast food.": "🍟 قلل الوجبات السريعة.",
        "🥦 Eat more vegetables.": "🥦 تناول المزيد من الخضروات.",
        "👨‍⚕️ Consult your physician.": "👨‍⚕️ استشر طبيبك.",
        "🥗 Follow a weight-loss diet.": "🥗 اتبع نظامًا غذائيًا لإنقاص الوزن.",
        "🚶 Exercise regularly.": "🚶 مارس الرياضة بانتظام.",
        "🔐 Account": "🔐 الحساب",
        "Name": "الاسم",
        "Email": "البريد الإلكتروني",
        "Role": "الدور",
        "Your Complete AI Healthcare Platform": "منصتك الطبية الكاملة بالذكاء الاصطناعي",
        "Made with ❤️ using Streamlit & AI": "صُنع بـ ❤️ باستخدام Streamlit والذكاء الاصطناعي",
        "© 2026 HealthVibe AI": "© 2026 HealthVibe AI",

        # --- lipid.py ---
        "Please complete your profile first.": "من فضلك أكمل ملفك الشخصي أولاً.",
        "Model Loading Error: ": "خطأ في تحميل النموذج: ",
        "Lipid Risk Prediction": "التنبؤ بمخاطر الدهون",
        "AI Clinical Decision Support System": "نظام دعم القرار السريري بالذكاء الاصطناعي",
        "Step": "الخطوة",
        "Patient information loaded successfully.": "تم تحميل بيانات المريض بنجاح.",
        "Next ➜": "التالي ➜",
        "🩺 Clinical Information": "🩺 المعلومات السريرية",
        "Total Cholesterol (mg/dL)": "الكوليسترول الكلي (mg/dL)",
        "LDL Cholesterol (mg/dL)": "الكوليسترول الضار LDL (mg/dL)",
        "HDL Cholesterol (mg/dL)": "الكوليسترول النافع HDL (mg/dL)",
        "Triglycerides (mg/dL)": "الدهون الثلاثية (mg/dL)",
        "Fasting Blood Sugar": "سكر الدم الصائم",
        "HbA1c (%)": "السكر التراكمي HbA1c (%)",
        "Systolic Blood Pressure": "ضغط الدم الانقباضي",
        "Smoking Status": "حالة التدخين",
        "⬅ Back": "⬅ رجوع",
        "🧠 AI Prediction": "🧠 تنبؤ الذكاء الاصطناعي",
        "🧠 Predict": "🧠 تنبؤ",
        "Prediction Error : ": "خطأ في التنبؤ : ",
        "Low Risk": "خطورة منخفضة",
        "Borderline Risk": "خطورة حدّية",
        "High Risk": "خطورة مرتفعة",
        "Unknown": "غير معروف",
        "📊 AI Prediction Result": "📊 نتيجة تنبؤ الذكاء الاصطناعي",
        "AI Prediction Completed Successfully": "اكتمل تنبؤ الذكاء الاصطناعي بنجاح",
        "💾 Save Result": "💾 حفظ النتيجة",
        "Saved Successfully ✅": "تم الحفظ بنجاح ✅",
        "Database Error : ": "خطأ في قاعدة البيانات : ",
        "PDF Error : ": "خطأ في PDF : ",
        "📄 Download Report": "📄 تحميل التقرير",
        "⬇ Download PDF": "⬇ تحميل PDF",

        # --- patient_summary.py ---
        "📋 Patient Summary": "📋 ملخص المريض",
        "Feature": "البيان",
        "Value": "القيمة",
        "Total Cholesterol": "الكوليسترول الكلي",
        "LDL Cholesterol": "الكوليسترول الضار LDL",
        "HDL Cholesterol": "الكوليسترول النافع HDL",
        "Triglycerides": "الدهون الثلاثية",
        "Probability": "نسبة الاحتمال",
        "Prediction": "التشخيص المتوقع",
        "Prediction Result": "نتيجة التشخيص",

        # --- stepper.py ---
        "Medical": "طبي",
        "Analysis": "تحليل",
        "Result": "النتيجة",

        # --- ai_gauge.py ---
        "LOW RISK": "خطورة منخفضة",
        "MODERATE": "متوسطة",
        "HIGH RISK": "خطورة مرتفعة",

        # --- loading_animation.py ---
        "🩸 Reading Patient Data...": "🩸 جاري قراءة بيانات المريض...",
        "🧠 Running AI Model...": "🧠 جاري تشغيل نموذج الذكاء الاصطناعي...",
        "📊 Calculating Risk Score...": "📊 جاري حساب نسبة الخطورة...",
        "💡 Generating Recommendation...": "💡 جاري إنشاء التوصيات...",
        "✅ Finalizing Report...": "✅ جاري إنهاء التقرير...",

        # --- pdf_report.py ---
        "Clinical Decision Support Report": "تقرير دعم القرار السريري",
        "Patient:": "المريض:",
        "Age:": "السن:",
        "Gender:": "النوع:",
        "Date:": "التاريخ:",
        "AI Prediction": "تنبؤ الذكاء الاصطناعي",
        "Confidence : ": "نسبة الثقة : ",
        "Clinical Data": "البيانات السريرية",
        "Generated by HealthVibe AI": "تم إنشاؤه بواسطة HealthVibe AI",

        # --- sidebar.py ---
        "Clinical Decision Support Platform": "منصة دعم القرار السريري",
        "Role:": "الدور:",
        "Status:": "الحالة:",
        "Online": "متصل",
        "📂 Navigation": "📂 التنقل",
        "🏠 Dashboard": "🏠 اللوحة الرئيسية",
        "👤 Profile": "👤 الملف الشخصي",
        "📋 Patient History": "📋 السجل الطبي",
        "🩸 Diabetes": "🩸 السكري",
        "❤️ Hypertension": "❤️ ضغط الدم",
        "⚖️ Obesity": "⚖️ السمنة",
        "🫀 Lipid": "🫀 الدهون",
        "🧬 Thrombosis": "🧬 الجلطات",
        "🫁 Pulmonary AI": "🫁 تليّف الرئة",
        "🩻 CT Analysis": "🩻 تحليل الأشعة المقطعية",
        "🤖 AI Assistant": "🤖 المساعد الذكي",
        "👨‍⚕️ Doctor Dashboard": "👨‍⚕️ لوحة الطبيب",
        "ℹ️ About": "ℹ️ عن المنصة",
        "⚡ System Status": "⚡ حالة النظام",
        "🟢 AI Server": "🟢 خادم الذكاء الاصطناعي",
        "🟢 Database": "🟢 قاعدة البيانات",
        "🟢 Models Loaded": "🟢 النماذج محمّلة",
        "💙 Daily Health Tip": "💙 نصيحة صحية يومية",
        "💧 Drink enough water": "💧 اشرب كمية كافية من الماء",
        "🥗 Eat healthy meals": "🥗 تناول وجبات صحية",
        "🏃 Exercise at least 30 minutes": "🏃 مارس الرياضة 30 دقيقة على الأقل",
        "😴 Sleep 7–8 hours": "😴 نم 7-8 ساعات",
        "🚪 Logout": "🚪 تسجيل الخروج",

        # --- result_card.py ---
        "High Risk of Diabetes": "خطورة مرتفعة للإصابة بالسكري",
        "Low Risk of Diabetes": "خطورة منخفضة للإصابة بالسكري",

        # --- recommendation.py ---
        "💡 Medical Recommendation": "💡 التوصية الطبية",
        "reco_high_risk": """
### خطورة مرتفعة

• قم بزيارة طبيب باطنة.

• أجرِ تحليل HbA1c.

• راقب مستوى السكر في الدم.

• قلل من تناول السكريات.

• مارس الرياضة 30 دقيقة يوميًا.

• قلل الوزن الزائد.

• أعد إجراء التحاليل المعملية.
""",
        "reco_healthy_lifestyle": """
### نمط حياة صحي

• استمر في التغذية الصحية.

• مارس الرياضة بانتظام.

• اشرب كمية كافية من الماء.

• افحص السكري سنويًا.

• حافظ على وزن جسم صحي.
""",

        # --- risk_meter.py ---
        "📊 Risk Score": "📊 نسبة الخطورة",
        "Risk": "الخطورة",

        # --- CT_Scan_AI.py ---
        "🩻 Lung CT Scan AI": "🩻 الذكاء الاصطناعي لأشعة الرئة المقطعية",
        "Artificial Intelligence for Lung Cancer Detection": "الذكاء الاصطناعي للكشف عن سرطان الرئة",
        "tf_not_found": """
TensorFlow غير موجود على الجهاز.

سبب المشكلة هو أن المعالج الحالي لا يدعم
الإصدار الحديث من TensorFlow.

يمكنك استخدام Google Colab أو جهاز أحدث.
""",
        "❌ Unable to load AI Model": "❌ تعذّر تحميل نموذج الذكاء الاصطناعي",
        "Adenocarcinoma": "سرطان غدي",
        "Large Cell Carcinoma": "سرطان الخلايا الكبيرة",
        "Normal": "طبيعي",
        "Squamous Cell Carcinoma": "سرطان الخلايا الحرشفية",
        "ct_instructions": """

### التعليمات

• ارفع الأشعة المقطعية

• اضغط تحليل

• انتظر الذكاء الاصطناعي

• راجع النتائج

""",
        "Upload Lung CT Scan": "ارفع أشعة الرئة المقطعية",
        "Uploaded CT": "الأشعة المرفوعة",
        "AI Analysis": "تحليل الذكاء الاصطناعي",
        "🤖 Analyze CT Scan": "🤖 تحليل الأشعة المقطعية",
        "Model Not Loaded": "النموذج غير محمّل",
        "Analyzing...": "جاري التحليل...",
        "Analysis Completed": "اكتمل التحليل",
        "Confidence": "نسبة الثقة",
        "🩺 AI Diagnosis Dashboard": "🩺 لوحة تشخيص الذكاء الاصطناعي",
        "Detected Disease": "المرض المكتشف",
        "AI Confidence Level": "مستوى ثقة الذكاء الاصطناعي",
        "🟢 Very High Confidence": "🟢 ثقة عالية جدًا",
        "🔵 High Confidence": "🔵 ثقة عالية",
        "🟡 Moderate Confidence": "🟡 ثقة متوسطة",
        "🔴 Low Confidence": "🔴 ثقة منخفضة",
        "📊 Prediction Probability": "📊 احتمالية التنبؤ",
        "🤖 AI Summary": "🤖 ملخص الذكاء الاصطناعي",
        "summary_normal": """

لم يتم اكتشاف أي خلل واضح.

تبدو الرئتان طبيعيتين وفقًا
لنموذج الذكاء الاصطناعي المدرّب.

""",
        "summary_adenocarcinoma": """

احتمال وجود سرطان غدي.

يلزم إجراء فحوصات إضافية.

""",
        "summary_large_cell": """

احتمال وجود سرطان الخلايا الكبيرة.

يُنصح بتقييم سريري فوري.

""",
        "summary_squamous": """

احتمال وجود سرطان الخلايا الحرشفية.

يجب مراجعة تاريخ التدخين.

""",
        "📖 Disease Information": "📖 معلومات عن المرض",
        "info_normal": """

### الوصف

مظهر رئة سليم.

### التوصية

• فحص طبي دوري

• نمط حياة صحي

• تجنب التدخين

""",
        "info_adenocarcinoma": """

### الوصف

أكثر أنواع سرطان الرئة شيوعًا.

يتطور عادةً في الجزء الخارجي من الرئة.

### التوصية

• أشعة مقطعية على الصدر

• أشعة PET

• خزعة

• استشارة أورام

""",
        "info_large_cell": """

### الوصف

سرطان رئة عدواني من النوع غير صغير الخلايا.

### التوصية

• تحويل فوري لطبيب متخصص

• تصوير إضافي

• خزعة نسيجية

""",
        "info_squamous": """

### الوصف

يرتبط عادةً بالتدخين.

يتطور غالبًا بالقرب من الشعب الهوائية المركزية.

### التوصية

• الإقلاع عن التدخين

• تنظير الشعب الهوائية

• استشارة أورام

""",
        "🚨 Risk Assessment": "🚨 تقييم المخاطر",
        "🟢 AI Confidence: Very High": "🟢 ثقة الذكاء الاصطناعي: عالية جدًا",
        "🔵 AI Confidence: High": "🔵 ثقة الذكاء الاصطناعي: عالية",
        "🟡 AI Confidence: Moderate": "🟡 ثقة الذكاء الاصطناعي: متوسطة",
        "🔴 AI Confidence: Low": "🔴 ثقة الذكاء الاصطناعي: منخفضة",
        "📄 Medical Report": "📄 التقرير الطبي",
        "pdf_report_info": """
سيتضمن تقرير PDF:

• بيانات المريض

• تنبؤ الذكاء الاصطناعي

• نسبة الثقة

• نتيجة الأشعة المقطعية

• التوصيات الطبية

• ملاحظات الطبيب

(قريبًا)
""",
        "📥 Download PDF Report": "📥 تحميل تقرير PDF",
        "🧠 Explainable AI": "🧠 الذكاء الاصطناعي القابل للتفسير",
        "gradcam_info": """
تصور Grad-CAM

ستقوم هذه الميزة بتمييز المنطقة
التي ركّز عليها الذكاء الاصطناعي
أثناء إجراء التنبؤ.

(قريبًا)
""",
        "📋 General Recommendations": "📋 توصيات عامة",
        "✅ Always consult a chest physician.": "✅ استشر دائمًا طبيب الصدرية.",
        "✅ AI results should never replace medical diagnosis.": "✅ نتائج الذكاء الاصطناعي لا تغني أبدًا عن التشخيص الطبي.",
        "✅ Compare the CT scan with previous examinations.": "✅ قارن الأشعة المقطعية بالفحوصات السابقة.",
        "✅ Additional laboratory investigations may be required.": "✅ قد يلزم إجراء تحاليل معملية إضافية.",
        "✅ Early diagnosis significantly improves treatment outcomes.": "✅ التشخيص المبكر يحسّن نتائج العلاج بشكل كبير.",
        "ct_disclaimer": """
هذا التطبيق مخصص لأغراض تعليمية
وبحثية فقط.

HealthVibe AI لا يغني
عن التشخيص الطبي المتخصص.
""",
        "AI Model": "نموذج الذكاء الاصطناعي",
        "Image Size": "حجم الصورة",
        "Classes": "الفئات",
        "HealthVibe AI © 2026 | Artificial Intelligence for Healthcare": "HealthVibe AI © 2026 | الذكاء الاصطناعي للرعاية الصحية",

        # --- Doctors.py ---
        "👨‍⚕️ Doctors Management": "👨‍⚕️ إدارة الأطباء",
        "Manage Doctors, Departments and Availability": "إدارة الأطباء والأقسام والتوفر",
        "🔍 Search Doctor": "🔍 بحث عن طبيب",
        "Search by doctor's name...": "ابحث باسم الطبيب...",
        "➕ Add New Doctor": "➕ إضافة طبيب جديد",
        "Doctor Name": "اسم الطبيب",
        "Department": "القسم",
        "Internal Medicine": "الباطنة",
        "Cardiology": "القلب",
        "Neurology": "المخ والأعصاب",
        "Radiology": "الأشعة",
        "Pulmonology": "الصدر",
        "Oncology": "الأورام",
        "Endocrinology": "الغدد الصماء",
        "Pediatrics": "الأطفال",
        "Orthopedics": "العظام",
        "General Surgery": "الجراحة العامة",
        "Specialization": "التخصص",
        "Years of Experience": "سنوات الخبرة",
        "Available": "متاح",
        "💾 Save Doctor": "💾 حفظ الطبيب",
        "Doctor name is required.": "اسم الطبيب مطلوب.",
        "Doctor added successfully ✅": "تمت إضافة الطبيب بنجاح ✅",
        "👨‍⚕️ Doctors List": "👨‍⚕️ قائمة الأطباء",
        "No doctors found.": "لا يوجد أطباء.",
        "ID": "الرقم",
        "Experience": "الخبرة",
        "Status": "الحالة",
        "Created": "تاريخ الإنشاء",
        "✏️ View / Edit Doctor": "✏️ عرض / تعديل طبيب",
        "Select Doctor": "اختر الطبيب",
        "💾 Update Doctor": "💾 تحديث الطبيب",
        "Doctor updated successfully ✅": "تم تحديث الطبيب بنجاح ✅",
        "🗑 Delete Doctor": "🗑 حذف طبيب",
        "Choose Doctor": "اختر الطبيب",
        "I confirm deleting this doctor": "أؤكد حذف هذا الطبيب",
        "Delete Doctor": "حذف الطبيب",
        "Please confirm deletion first.": "من فضلك أكّد الحذف أولاً.",
        "Doctor deleted successfully ✅": "تم حذف الطبيب بنجاح ✅",
        "No doctors available.": "لا يوجد أطباء متاحون.",
        "📊 Doctors Statistics": "📊 إحصائيات الأطباء",
        "⭐ Avg Experience": "⭐ متوسط الخبرة",
        "Years": "سنوات",
        "No statistics available.": "لا توجد إحصائيات متاحة.",
        "📈 Doctors Analytics": "📈 تحليلات الأطباء",
        "Doctors by Department": "الأطباء حسب القسم",
        "Availability Status": "حالة التوفر",
        "📄 Export Doctors Data": "📄 تصدير بيانات الأطباء",
        "⬇ Download Doctors List": "⬇ تحميل قائمة الأطباء",
        "No data available to export.": "لا توجد بيانات للتصدير.",
        "📌 Quick Summary": "📌 ملخص سريع",
        "Total Doctors : ": "إجمالي الأطباء : ",
        "Available Doctors : ": "الأطباء المتاحون : ",
        "Unavailable Doctors : ": "الأطباء غير المتاحين : ",
        "Average Experience : ": "متوسط الخبرة : ",
        "No doctors registered yet.": "لا يوجد أطباء مسجلون بعد.",
        "Doctors Management System": "نظام إدارة الأطباء",

        # --- obesity.py ---
        "⚖️ Obesity Prediction": "⚖️ التنبؤ بالسمنة",
        "Height (m)": "الطول (متر)",
        "Next ➡": "التالي ➡",
        "🥗 Lifestyle Information": "🥗 معلومات نمط الحياة",
        "Family History of Overweight": "تاريخ عائلي للسمنة",
        "no": "لا",
        "yes": "نعم",
        "Frequent High Calorie Food": "تناول متكرر لطعام عالي السعرات",
        "Vegetable Consumption": "استهلاك الخضروات",
        "Main Meals Per Day": "الوجبات الرئيسية يوميًا",
        "Daily Water Intake": "كمية الماء اليومية",
        "Physical Activity": "النشاط البدني",
        "Technology Usage": "استخدام التكنولوجيا",
        "Alcohol Consumption": "استهلاك الكحول",
        "Sometimes": "أحيانًا",
        "Frequently": "بكثرة",
        "Transportation": "وسيلة المواصلات",
        "Walking": "المشي",
        "Bike": "دراجة",
        "Motorbike": "دراجة نارية",
        "Automobile": "سيارة",
        "Public_Transportation": "مواصلات عامة",
        "Insufficient Weight": "نقص الوزن",
        "Normal Weight": "وزن طبيعي",
        "Overweight Level I": "زيادة وزن المستوى الأول",
        "Overweight Level II": "زيادة وزن المستوى الثاني",
        "Obesity Type I": "سمنة النوع الأول",
        "Obesity Type II": "سمنة النوع الثاني",
        "Obesity Type III": "سمنة النوع الثالث",

        # --- Register.py ---
        "Create Account": "إنشاء حساب",
        "Register as ": "التسجيل كـ ",
        "👤 Full Name": "👤 الاسم بالكامل",
        "Enter your full name": "أدخل اسمك بالكامل",
        "📧 Email": "📧 البريد الإلكتروني",
        "Enter your email": "أدخل بريدك الإلكتروني",
        "🔒 Password": "🔒 كلمة المرور",
        "Create password": "أنشئ كلمة مرور",
        "🔒 Confirm Password": "🔒 تأكيد كلمة المرور",
        "Confirm password": "أكّد كلمة المرور",
        "🚀 Create Account": "🚀 إنشاء الحساب",
        "Please enter your name.": "من فضلك أدخل اسمك.",
        "Please enter your email.": "من فضلك أدخل بريدك الإلكتروني.",
        "Passwords do not match.": "كلمتا المرور غير متطابقتين.",
        "Password must be at least 6 characters.": "يجب أن تتكون كلمة المرور من 6 أحرف على الأقل.",
        "✅ Account Created Successfully": "✅ تم إنشاء الحساب بنجاح",
        "This email already exists.": "هذا البريد الإلكتروني مستخدم بالفعل.",
        "Already have an account?": "لديك حساب بالفعل؟",
        "🔐 Login": "🔐 تسجيل الدخول",

        # --- Patient_History.py ---
        "📋 Medical History": "📋 السجل الطبي",
        "My Assessments": "تقييماتي",
        "Review all previous AI predictions and reports.": "راجع كل تنبؤات وتقارير الذكاء الاصطناعي السابقة.",
        "Total Tests": "إجمالي الفحوصات",
        "Last Test": "آخر فحص",
        "Highest Risk": "أعلى نسبة خطورة",
        "Most Tested": "الأكثر فحصًا",
        "🔍 Search & Filter": "🔍 بحث وتصفية",
        "Search Disease": "ابحث عن مرض",
        "Disease": "المرض",
        "All": "الكل",
        "Sort By": "ترتيب حسب",
        "Newest": "الأحدث",
        "Oldest": "الأقدم",
        "Lowest Risk": "أقل نسبة خطورة",
        "📭 No assessments found.": "📭 لا توجد تقييمات.",
        "🗑 Delete All History": "🗑 حذف كل السجل",
        "All Assessments Deleted Successfully": "تم حذف جميع التقييمات بنجاح",
        "📄 Download CSV": "📄 تحميل CSV",
        "📋 Assessment History": "📋 سجل التقييمات",
        "**Prediction:** ": "**التشخيص:** ",
        "👁 View Details": "👁 عرض التفاصيل",
        "🗑 Delete": "🗑 حذف",
        "Assessment Deleted Successfully": "تم حذف التقييم بنجاح",
        "📄 Assessment Details": "📄 تفاصيل التقييم",
        "Date": "التاريخ",
        "❌ Close Details": "❌ إغلاق التفاصيل",
        "📊 Assessment Analytics": "📊 تحليلات التقييمات",

        # --- Settings.py ---
        "⚙️ System Settings": "⚙️ إعدادات النظام",
        "Settings": "الإعدادات",
        "Welcome": "أهلاً",
        "👤 Account Settings": "👤 إعدادات الحساب",
        "Username": "اسم المستخدم",
        "Status": "الحالة",
        "Active": "نشط",
        "⚙️ Preferences": "⚙️ التفضيلات",
        "Dark Mode": "الوضع الليلي",
        "Enable Notifications": "تفعيل الإشعارات",
        "AI Recommendations": "توصيات الذكاء الاصطناعي",
        "Language": "اللغة",
        "English": "الإنجليزية",
        "Arabic": "العربية",

        # --- Splash.py ---
        "AI Clinical Decision Support System": "نظام دعم القرار السريري بالذكاء الاصطناعي",
        "Vibe Better, Live Better": "عيش أفضل بحيوية أفضل",
        "Loading...": "جاري التحميل...",

        # --- hypertension.py ---
        "Personal Information": "المعلومات الشخصية",
        "Blood Pressure": "ضغط الدم",
        "Symptoms": "الأعراض",
        "Medications": "الأدوية",
        "Lifestyle": "نمط الحياة",
        "Lab Upload": "رفع التحاليل",
        "AI Result": "نتيجة الذكاء الاصطناعي",

        "Hypertension Assessment": "تقييم ضغط الدم المرتفع",
        "Complete the following assessment to estimate blood pressure risk using AI.":
            "أكمل التقييم التالي لتقدير مخاطر ضغط الدم باستخدام الذكاء الاصطناعي.",

        # Occupations
        "Office / Desk Job": "عمل مكتبي",
        "IT / Software": "تكنولوجيا المعلومات / برمجيات",
        "Teacher": "معلم",
        "Healthcare Worker": "عامل في الرعاية الصحية",
        "Driver / Transport": "سائق / نقل",
        "Military / Police / Security": "عسكري / شرطة / أمن",
        "Construction / Manual Labor": "بناء / عمل يدوي",
        "Business Owner": "صاحب عمل",
        "Student": "طالب",
        "Homemaker": "ربة منزل",
        "Retired": "متقاعد",
        "Other": "أخرى",

        # Symptoms
        "Headache": "صداع",
        "Dizziness": "دوخة",
        "Blurred Vision": "تشوش الرؤية",
        "Chest Pain": "ألم في الصدر",
        "Shortness of Breath": "ضيق في التنفس",
        "Fatigue": "إرهاق",
        "Palpitations": "خفقان القلب",
        "Nosebleeds": "نزيف الأنف",

        # Stress / Sleep / Activity
        "Low": "منخفض",
        "Moderate": "متوسط",
        "High": "مرتفع",
        "Very High": "مرتفع جدًا",
        "Less than 5 hours": "أقل من 5 ساعات",
        "5-6 hours": "5-6 ساعات",
        "7-8 hours": "7-8 ساعات",
        "More than 8 hours": "أكثر من 8 ساعات",
        "Sedentary": "خامل (قليل الحركة)",
        "Light": "خفيف",
        "Active": "نشط",

        # Family history
        "Heart Disease": "أمراض القلب",
        "Stroke": "السكتة الدماغية",
        "Kidney Disease": "أمراض الكلى",

        # Step 1 - Personal Info
        "👤 Patient Information": "👤 بيانات المريض",
        "✅ Patient information loaded from your profile.": "✅ تم تحميل بيانات المريض من ملفك الشخصي.",
        "Occupation": "المهنة",

        # Step 2 - Blood Pressure
        "🩺 Blood Pressure Information": "🩺 معلومات ضغط الدم",
        "Diastolic Blood Pressure": "ضغط الدم الانبساطي",

        # Step 3 - Symptoms
        "🤕 Symptoms": "🤕 الأعراض",
        "Select symptoms you experience": "اختر الأعراض التي تشعر بها",
        "Stress Level": "مستوى التوتر",
        "Average Sleep": "متوسط النوم",

        # Step 4 - Medical History
        "Do you have diabetes?": "هل تعاني من مرض السكري؟",
        "No": "لا",
        "Yes": "نعم",
        "Resting Heart Rate": "معدل ضربات القلب أثناء الراحة",
        "Family Medical History": "التاريخ المرضي للعائلة",

        # Step 5 - Medications
        "💊 Medications": "💊 الأدوية",
        "Are you taking blood pressure medication?": "هل تتناول دواءً لضغط الدم؟",
        "Medication name": "اسم الدواء",

        # Step 6 - Lifestyle
        "🏃 Lifestyle Information": "🏃 معلومات نمط الحياة",
        "Do you smoke?": "هل تدخن؟",
        "Cigarettes Per Day": "عدد السجائر يوميًا",
        "Physical Activity Level": "مستوى النشاط البدني",
        "Salt Intake": "استهلاك الملح",
        "Never": "أبدًا",
        "Regularly": "بانتظام",

        # Step 7 - Lab Upload
        "🧪 Additional Lab Information": "🧪 معلومات معملية إضافية",
        "Additional medical notes (optional)": "ملاحظات طبية إضافية (اختياري)",
        "Upload lab report (optional)": "ارفع تقرير التحاليل (اختياري)",
        "🤖 Analyze With AI": "🤖 تحليل بالذكاء الاصطناعي",

        # Step 8 - AI Result
        "🤖 AI Analysis Result": "🤖 نتيجة تحليل الذكاء الاصطناعي",
        "Analysis Completed Successfully ✅": "تم التحليل بنجاح ✅",
        "Systolic BP": "ضغط الدم الانقباضي",
        "Diastolic BP": "ضغط الدم الانبساطي",
        "Heart Rate": "معدل ضربات القلب",
        "⬇ Download PDF Report": "⬇ تحميل تقرير PDF",
        "🔄 New Assessment": "🔄 تقييم جديد",

        # --- Thrombosis.py ---
        "AI Disease Screening": "الفحص المبكر بالذكاء الاصطناعي",
        "Thrombosis Risk Prediction": "التنبؤ بمخاطر الجلطات",
        "Artificial Intelligence Based Blood Clot Screening System": "نظام فحص الجلطات الدموية بالذكاء الاصطناعي",
        "📊 AI Dashboard": "📊 لوحة الذكاء الاصطناعي",
        "Thrombosis": "الجلطات",
        "Risk Factors": "عوامل الخطورة",
        "🟢 Ready": "🟢 جاهز",

        "Patient Name": "اسم المريض",
        "Male": "ذكر",
        "Female": "أنثى",
        "D-Dimer (ng/mL)": "D-Dimer (ng/mL)",
        "Blood Type": "فصيلة الدم",
        "Step 1 / 3": "الخطوة 1 / 3",

        "Leg Swelling": "تورم الساق",
        "Leg Pain": "ألم في الساق",
        "Previous Blood Clot": "جلطة دموية سابقة",
        "Recent Immobility": "قلة الحركة مؤخرًا",
        "Recent Surgery": "جراحة حديثة",
        "Family History": "التاريخ العائلي",
        "Diabetes": "السكري",
        "High Cholesterol": "ارتفاع الكوليسترول",
        "Step 2 / 3": "الخطوة 2 / 3",
        "Analyze ➜": "تحليل ➜",

        "🤖 AI Prediction": "🤖 تنبؤ الذكاء الاصطناعي",
        "HealthVibe AI is analyzing your clinical data...": "HealthVibe AI بيحلل بياناتك السريرية الآن...",
        "🔴 High Risk": "🔴 خطورة مرتفعة",
        "🟢 Low Risk": "🟢 خطورة منخفضة",
        "Risk Probability": "نسبة الخطورة",
        "Risk %": "نسبة الخطورة %",

        "High D-Dimer": "ارتفاع D-Dimer",
        "Previous Thrombosis": "إصابة سابقة بالجلطات",
        "Immobility": "قلة الحركة",
        "⚠ Risk Factors": "⚠ عوامل الخطورة",
        "No major risk factors detected.": "لم يتم اكتشاف عوامل خطورة رئيسية.",

        "💡 AI Recommendations": "💡 توصيات الذكاء الاصطناعي",
        """
### High Risk

- Consult a vascular specialist immediately.
- Doppler Ultrasound is recommended.
- Avoid prolonged sitting.
- Maintain hydration.
- Follow physician instructions.
""": """
### خطورة مرتفعة

- استشر أخصائي أوعية دموية فورًا.
- يُنصح بإجراء دوبلر بالموجات فوق الصوتية.
- تجنب الجلوس لفترات طويلة.
- حافظ على الترطيب.
- اتبع تعليمات الطبيب.
""",
        """
### Low Risk

- Continue regular physical activity.
- Maintain healthy body weight.
- Drink enough water.
- Avoid smoking.
- Keep regular follow-up if symptoms appear.
""": """
### خطورة منخفضة

- استمر في ممارسة النشاط البدني بانتظام.
- حافظ على وزن جسم صحي.
- اشرب كمية كافية من الماء.
- تجنب التدخين.
- تابع مع الطبيب بانتظام في حالة ظهور أعراض.
""",

        "Artificial Intelligence Disease Prediction Platform": "منصة التنبؤ بالأمراض بالذكاء الاصطناعي",

        # --- diabetes.py ---
        "Pregnancies": "عدد مرات الحمل",
        "Glucose": "الجلوكوز",
        "Insulin": "الأنسولين",
        "📋 Clinical Measurements": "📋 القياسات السريرية",
        "Skin Thickness": "سمك الجلد",
        "Diabetes Pedigree Function": "معامل الوراثة للسكري",
        "Outcome": "النتيجة",
        "📄 Download PDF": "📄 تحميل PDF",

        # --- Pulmonary_Fibrosis.py ---
        "Respiratory Disease Prediction": "التنبؤ بأمراض الجهاز التنفسي",
        "Main Symptom": "العرض الرئيسي",
        "Former": "سابق",
        "Current": "حالي",
        "Regular": "منتظم",
        "Rarely": "نادرًا",
        "Air Pollution Exposure": "التعرض لتلوث الهواء",
        "Medium": "متوسط",
        "Chemical Exposure": "التعرض للمواد الكيميائية",
        "Sleep Hours": "عدد ساعات النوم",

        "❤️ Vital Signs": "❤️ العلامات الحيوية",
        "SpO₂ (%)": "تشبع الأكسجين SpO₂ (%)",
        "Temperature (°C)": "درجة الحرارة (°م)",
        "Heart Rate (bpm)": "معدل ضربات القلب (نبضة/دقيقة)",
        "Respiratory Rate": "معدل التنفس",

        "💊 Suggested Treatment": "💊 العلاج المقترح",
        "Consult your physician.": "استشر طبيبك.",
        "🚨 Disease Severity": "🚨 شدة المرض",
        "🔴 High": "🔴 مرتفعة",
        "🟡 Medium": "🟡 متوسطة",
        "🟢 Low": "🟢 منخفضة",
        "⚠ Medical Disclaimer": "⚠ إخلاء مسؤولية طبي",

        """

This AI prediction is intended for screening purposes only.

It is NOT a confirmed medical diagnosis.

Please consult a qualified healthcare professional
for examination, confirmation and treatment.

""": """

هذا التنبؤ بالذكاء الاصطناعي مخصص لأغراض الفحص المبدئي فقط.

ولا يُعد تشخيصًا طبيًا مؤكدًا.

من فضلك استشر أخصائي رعاية صحية مؤهل
للفحص والتأكيد والعلاج.

""",

        "📊 AI Analysis Result": "📊 نتيجة تحليل الذكاء الاصطناعي",
        "High Confidence": "ثقة عالية",
        "Moderate Confidence": "ثقة متوسطة",
        "Low Confidence": "ثقة منخفضة",
        "AI Confidence": "ثقة الذكاء الاصطناعي",

        """
⚠️ This AI prediction is **not a medical diagnosis**.

Please consult a pulmonologist to confirm the diagnosis and determine the appropriate treatment plan.
""": """
⚠️ هذا التنبؤ بالذكاء الاصطناعي **ليس تشخيصًا طبيًا**.

من فضلك استشر طبيب أمراض الصدر لتأكيد التشخيص وتحديد خطة العلاج المناسبة.
""",

        "💡 General Recommendations": "💡 توصيات عامة",
        "🩺 Visit a chest specialist.": "🩺 قم بزيارة طبيب صدرية.",
        "🚭 Avoid smoking completely.": "🚭 تجنب التدخين تمامًا.",
        "😷 Avoid dust and polluted air.": "😷 تجنب الغبار والهواء الملوث.",
        "💧 Stay hydrated.": "💧 حافظ على شرب كمية كافية من الماء.",
        "🏃 Maintain light physical activity if possible.": "🏃 حافظ على نشاط بدني خفيف إن أمكن.",

        """
⚠️ **Medical Disclaimer**

This AI prediction is intended only for preliminary screening and educational purposes.

It **does not replace a physician's diagnosis**.

If you have persistent symptoms such as:

• Shortness of breath
• Chest pain
• Persistent cough
• Fever
• Coughing blood

Please consult a pulmonologist or healthcare provider immediately.

Further investigations such as Chest X-ray, CT Scan, Pulmonary Function Test (PFT), blood tests, and clinical examination may be required to confirm the diagnosis.
""": """
⚠️ **إخلاء مسؤولية طبي**

هذا التنبؤ بالذكاء الاصطناعي مخصص فقط لأغراض الفحص المبدئي والتثقيف الطبي.

ولا **يغني عن تشخيص الطبيب**.

إذا كانت لديك أعراض مستمرة مثل:

• ضيق في التنفس
• ألم في الصدر
• سعال مستمر
• حمى
• سعال مصحوب بدم

من فضلك استشر طبيب أمراض الصدر أو مقدم الرعاية الصحية فورًا.

قد يلزم إجراء فحوصات إضافية مثل أشعة سينية على الصدر، أشعة مقطعية، اختبار وظائف الرئة (PFT)، تحاليل دم، وفحص سريري لتأكيد التشخيص.
""",

        "Respiratory Disease Screening System": "نظام فحص أمراض الجهاز التنفسي",

        # --- Login.py ---
        "Welcome Back": "أهلاً بعودتك",
        "Login As": "تسجيل الدخول كـ",
        "Enter your password": "أدخل كلمة المرور",
        "Remember me": "تذكرني",
        "🚀 Login": "🚀 تسجيل الدخول",
        "❌ Invalid Email or Password": "❌ البريد الإلكتروني أو كلمة المرور غير صحيحة",
        "This account belongs to a {role}.": "هذا الحساب يخص {role}.",
        "✅ Login Successful": "✅ تم تسجيل الدخول بنجاح",
        "Don't have an account?": "ليس لديك حساب؟",
        "📝 Create New Account": "📝 إنشاء حساب جديد",
    }
}


def init():
    """Setup lang state + sidebar switch button + RTL css. Call once per page, before other markup."""
    if "lang" not in st.session_state:
        st.session_state.lang = "en"

    meta = LANG_META[st.session_state.lang]

    with st.sidebar:
        if st.button(meta["switch_label"], key="lang_switch_btn", width="stretch"):
            st.session_state.lang = "ar" if st.session_state.lang == "en" else "en"
            st.rerun()

    if meta["dir"] == "rtl":
        st.markdown(
            """
            <style>
            html, body,
            [data-testid="stAppViewContainer"],
            [data-testid="stSidebar"],
            [data-testid="stSidebarContent"],
            [data-testid="stMain"] {
                direction: rtl;
            }

            [data-testid="stMarkdownContainer"],
            [data-testid="stMetric"],
            [data-testid="stMetricLabel"],
            [data-testid="stMetricValue"],
            [data-testid="stMetricDelta"],
            [data-testid="stCaptionContainer"],
            [data-testid="stExpander"],
            [data-testid="stAlertContainer"],
            [data-testid="stTextInput"],
            [data-testid="stNumberInput"],
            [data-testid="stSelectbox"],
            [data-testid="stTextArea"],
            [data-testid="stRadio"],
            [data-testid="stCheckbox"],
            [data-testid="stFileUploader"],
            [data-testid="stDateInput"],
            [data-testid="stWidgetLabel"],
            .stTabs, table, th, td,
            h1, h2, h3, h4, h5, h6, p, li, label {
                direction: rtl;
                text-align: right !important;
            }

            [data-testid="stHorizontalBlock"] {
                flex-direction: row-reverse;
            }

            [data-testid="stRadio"] > div,
            [data-testid="stCheckbox"] > label {
                flex-direction: row-reverse;
                justify-content: flex-end;
            }

            ul, ol {
                padding-right: 1.4em;
                padding-left: 0;
            }

            /* Keep code, numbers and PDFs left-to-right for readability */
            code, pre, .stCodeBlock,
            [data-testid="stNumberInput"] input {
                direction: ltr;
                text-align: left !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )


def t(text: str) -> str:
    """Translate a raw English string. Falls back to the original text if no translation exists."""
    lang = st.session_state.get("lang", "en")
    return TRANSLATIONS.get(lang, {}).get(text, text)