import streamlit as st
from utils.db import get_attendance_for_student, get_timetable
from datetime import datetime

if st.session_state.get("user_type") != "student":
    st.warning("Access Denied. Only Students Allowed.")
    st.stop()

st.title("Student Dashboard")

phone = st.session_state.get("user_id")

# Fetch student's batch info
from utils.db import get_all_students

students = get_all_students()
batch = None
for s in students:
    data = s.to_dict()
    if data.get("phone") == phone:
        batch = data.get("batch")
        break

st.subheader(f"Welcome! ({phone})")
st.write(f"Your Batch: {batch}")

st.write("Your Attendance:")
attendance_data = get_attendance_for_student(phone)
if not attendance_data:
    st.info("No attendance records found.")
else:
    # Sort attendance by date descending
    attendance_data = sorted(attendance_data, key=lambda x: x["date"], reverse=True)
    for record in attendance_data:
        st.write(f"{record['date']}: {record['status']}")

# Get current week string in ISO format e.g., "2025-W23"
today = datetime.today()
iso_year, iso_week, _ = today.isocalendar()
current_week = f"{iso_year}-W{iso_week:02d}"

st.write(f"Timetable for Week {current_week}:")

if not batch:
    st.error("Batch info not found for your account.")
else:
    timetables = get_timetable(batch)
    if not timetables:
        st.info("No timetable documents found for your batch.")
    else:
        st.write("Available timetable weeks for your batch:")
        for t in timetables:
            st.write(f"- Week: {t.get('week')}")

        week_timetable = None
        for t in timetables:
            if t.get("week") == current_week:
                week_timetable = t.get("timetable")
                break

        if week_timetable:
            st.write(week_timetable)
        else:
            st.info("No timetable found for this week.")
