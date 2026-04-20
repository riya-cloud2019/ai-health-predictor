import streamlit as st
import numpy as np
import pickle
import pandas as pd

# ================= CONFIG =================
st.set_page_config(page_title="AI Health Dashboard", layout="wide")

# ================= DARK MODE =================
dark_mode = st.toggle("🌙 Dark Mode")

# ================= CSS =================
st.markdown(f"""
<style>

/* FULL BACKGROUND */
[data-testid="stAppViewContainer"] {{
    background: {"#0e1117" if dark_mode else "linear-gradient(to right, #fbc2eb, #a6c1ee)"} !important;
}}

/* REMOVE WHITE BLOCK */
[data-testid="stHeader"] {{
    background: transparent !important;
}}

/* TEXT COLOR */
h1, h2, h3, h4, h5, h6, p, label {{
    color: {"white" if dark_mode else "#2c2c2c"} !important;
}}

/* INPUT BOX */
input, .stNumberInput input {{
    background-color: {"#1e1e1e" if dark_mode else "white"} !important;
    color: {"white" if dark_mode else "black"} !important;
    border-radius: 10px !important;
}}

/* SELECT BOX */
div[data-baseweb="select"] > div {{
    background-color: {"#1e1e1e" if dark_mode else "white"} !important;
    color: {"white" if dark_mode else "black"} !important;
}}

/* BUTTON */
.stButton>button {{
    background: {"#00ADB5" if dark_mode else "#ff4b6e"};
    color: white;
    border-radius: 10px;
}}

</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.title("🧠 AI Health Risk Dashboard")

# ================= LOAD MODELS =================
heart_model = pickle.load(open("../heart_model.pkl", "rb"))
diab_model = pickle.load(open("../diabetes_model.pkl", "rb"))

# ================= INPUT LAYOUT =================
col1, col2 = st.columns(2)

with col1:
    st.subheader("❤️ Heart Inputs")
    age = st.number_input("Age", 1, 100, 40)
    bp = st.number_input("Blood Pressure", 80, 200, 120)
    chol = st.number_input("Cholesterol", 100, 400, 200)
    sugar = st.selectbox("Fasting Sugar", ["Low", "High"])
    max_hr = st.number_input("Max Heart Rate", 60, 220, 150)
    angina = st.selectbox("Angina", ["No", "Yes"])
    oldpeak = st.number_input("Oldpeak", 0.0, 6.0, 1.0)

with col2:
    st.subheader("🩺 Diabetes Inputs")
    glucose = st.number_input("Glucose", 70, 300, 120)
    bmi = st.number_input("BMI", 10.0, 40.0, 22.0)

# ================= ENCODING =================
sugar_val = 1 if sugar == "High" else 0
angina_val = 1 if angina == "Yes" else 0

# ================= FUNCTION: CIRCULAR METER =================
def circular_progress(label, value):
    percent = int(value * 100)
    color = "#4CAF50" if percent < 40 else "#FFA500" if percent < 70 else "#FF4B4B"

    st.markdown(f"""
    <div style="text-align:center">
        <div style="
            width:120px;height:120px;
            border-radius:50%;
            background: conic-gradient({color} {percent}%, #eee {percent}%);
            display:flex;align-items:center;justify-content:center;
            margin:auto;font-size:20px;font-weight:bold;">
            {percent}%
        </div>
        <p>{label}</p>
    </div>
    """, unsafe_allow_html=True)

# ================= PREDICT =================
if st.button("🚀 Predict Now"):

    heart_input = np.array([[age, bp, chol, sugar_val, max_hr, angina_val, oldpeak]])
    diab_input = np.array([[glucose, bmi]])

    heart_prob = heart_model.predict_proba(heart_input)[0][1]
    diab_prob = diab_model.predict_proba(diab_input)[0][1]

    st.markdown("## 📊 Results Dashboard")

    r1, r2 = st.columns(2)

    with r1:
        st.image("images/heart.png", width=100)
        circular_progress("Heart Risk", heart_prob)

        if heart_prob > 0.5:
            st.error("High Heart Risk")
        else:
            st.success("Low Heart Risk")

    with r2:
        st.image("images/diabetes.png", width=100)
        circular_progress("Diabetes Risk", diab_prob)

        if diab_prob > 0.5:
            st.error("High Diabetes Risk")
        else:
            st.success("Low Diabetes Risk")

    # ================= LINE CHART =================
    st.markdown("## 📈 Risk Comparison")

    chart_data = pd.DataFrame({
        "Risk": ["Heart", "Diabetes"],
        "Probability": [heart_prob, diab_prob]
    })

    st.line_chart(chart_data.set_index("Risk"))

    # ================= SMART RECOMMENDATIONS =================
    st.markdown("## 💡 Smart Recommendations")

    # HEART
    if heart_prob > 0.5:
        st.error("❤️ High Heart Risk")
        st.markdown("""
        🔹 Diet: Low salt, avoid fried food  
        🔹 Exercise: 30 min walking daily  
        🔹 Lifestyle: Quit smoking, reduce alcohol  
        🔹 Checkup: BP monitoring, ECG  
        """)

    # DIABETES
    if diab_prob > 0.5:
        st.error("🩺 High Diabetes Risk")
        st.markdown("""
        🔹 Avoid sugar & sweets  
        🔹 Eat fiber-rich food  
        🔹 Daily exercise  
        🔹 Monitor glucose levels  
        """)

    # OTHER
    if bmi > 25:
        st.warning("⚠️ High BMI – reduce weight")

    if sugar_val == 1:
        st.warning("🩺 High fasting sugar detected")

    if angina_val == 1:
        st.warning("❤️ Heart stress symptoms")

    if heart_prob <= 0.5 and diab_prob <= 0.5:
        st.success("✅ You are healthy! Maintain lifestyle.")
