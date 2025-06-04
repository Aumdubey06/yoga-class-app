import streamlit as st
import json
import firebase_admin
from firebase_admin import credentials, firestore

# Page setup
st.set_page_config(page_title="Yoga App", layout="centered")
st.title("Yoga Class Login")

# Load and parse the service account JSON from Streamlit secrets
service_account_json_str = st.secrets["SERVICE_ACCOUNT_JSON"]
service_account_info = json.loads(service_account_json_str)

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(service_account_info)
    firebase_admin.initialize_app(cred)

# Initialize Firestore client
db = firestore.client()

# Import utilities and dashboards
from utils.auth import is_admin, get_student_data
import pages.admin_dashboard as admin_dashboard
import pages.student_dashboard as student_dashboard

# Session state setup
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.user_id = None
    st.session_state.current_page = None

# Logout function
def logout():
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.user_id = None
    st.session_state.current_page = None
    st.rerun()

# Login form
if not st.session_state.logged_in:
    phone = st.text_input("Enter WhatsApp Number")
    if st.button("Login"):
        if is_admin(phone):
            st.session_state.logged_in = True
            st.session_state.user_type = "admin"
            st.session_state.user_id = phone
            st.session_state.current_page = "admin"
            st.rerun()
        elif get_student_data(phone):
            st.session_state.logged_in = True
            st.session_state.user_type = "student"
            st.session_state.user_id = phone
            st.session_state.current_page = "student"
            st.rerun()
        else:
            st.error("Invalid user. Contact admin.")
else:
    st.success(f"Logged in as {st.session_state.user_type.capitalize()}: {st.session_state.user_id}")

    # Navigation buttons
    if st.session_state.user_type == "admin":
        if st.button("Go to Admin Dashboard"):
            st.session_state.current_page = "admin"
            st.rerun()

    elif st.session_state.user_type == "student":
        if st.button("Go to Student Dashboard"):
            st.session_state.current_page = "student"
            st.rerun()

    # Logout option
    if st.button("Logout"):
        logout()

    # Show correct dashboard
    if st.session_state.current_page == "admin":
        admin_dashboard.show()
    elif st.session_state.current_page == "student":
        student_dashboard.show()
    else:
        st.info("Please select a dashboard.")
