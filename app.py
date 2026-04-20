import streamlit as st
import re

st.set_page_config(page_title="Patient Login", layout="centered")

st.title("🧾 Patient Registration")

# SESSION
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# FORM
name = st.text_input("Full Name")
age = st.number_input("Age", 1, 120, 25)
gender = st.selectbox("Gender", ["Male", "Female", "Other"])
height = st.number_input("Height (cm)", 100, 220, 160)
weight = st.number_input("Weight (kg)", 30, 150, 60)
contact = st.text_input("Contact Number")

# VALIDATION FUNCTION
def validate():
    if not name.isalpha():
        st.error("❌ Name should contain only alphabets")
        return False
    
    if not re.fullmatch(r"\d{10}", contact):
        st.error("❌ Contact must be 10 digits")
        return False

    return True

# BUTTON
if st.button("Continue ➡️"):
    if validate():
        st.session_state.logged_in = True
        st.session_state.user = {
            "name": name,
            "age": age,
            "gender": gender,
            "height": height,
            "weight": weight,
            "contact": contact
        }
        st.success("✅ Details Saved")
        st.switch_page("pages/dashboard.py")