import os
os.environ["GRPC_DNS_RESOLVER"] = "native"

import streamlit as st
from utils.auth import is_admin, get_student_data
import pages.admin_dashboard as admin_dashboard
import pages.student_dashboard as student_dashboard

st.set_page_config(page_title="Yoga App", layout="centered")

st.title("Yoga Class Login")

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.user_id = None
    st.session_state.current_page = None

def logout():
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.user_id = None
    st.session_state.current_page = None
    st.rerun()  # correct rerun method

if not st.session_state.logged_in:
    phone = st.text_input("Enter WhatsApp Number")
    if st.button("Login"):
        if is_admin(phone):
            st.session_state.logged_in = True
            st.session_state.user_type = "admin"
            st.session_state.user_id = phone
            st.session_state.current_page = "admin"  # direct to admin dashboard on login
            st.rerun()

        elif get_student_data(phone):
            st.session_state.logged_in = True
            st.session_state.user_type = "student"
            st.session_state.user_id = phone
            st.session_state.current_page = "student"  # direct to student dashboard on login
            st.rerun()

        else:
            st.error("Invalid user. Contact admin.")

else:
    # Show debug info (optional, remove for production)
    st.write(f"DEBUG: logged_in={st.session_state.logged_in}")
    st.write(f"DEBUG: user_type={st.session_state.user_type}")
    st.write(f"DEBUG: user_id={st.session_state.user_id}")
    st.write(f"DEBUG: current_page={st.session_state.current_page}")

    st.success(f"Logged in as {st.session_state.user_type.capitalize()}: {st.session_state.user_id}")

    # Navigation buttons if you want to allow switching dashboards without logout
    if st.session_state.user_type == "admin" and st.session_state.current_page != "admin":
        if st.button("Go to Admin Dashboard"):
            st.session_state.current_page = "admin"
            st.rerun()

    elif st.session_state.user_type == "student" and st.session_state.current_page != "student":
        if st.button("Go to Student Dashboard"):
            st.session_state.current_page = "student"
            st.rerun()

    if st.button("Logout"):
        logout()

    # Show the dashboard based on current page
    if st.session_state.current_page == "admin":
        admin_dashboard.show()
    elif st.session_state.current_page == "student":
        student_dashboard.show()
    else:
        st.info("Please select a dashboard.")
