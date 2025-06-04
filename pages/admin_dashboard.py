import streamlit as st
from datetime import datetime
from utils.db import (
    add_student, delete_student, get_all_students,
    save_attendance, save_timetable,
    add_batch, delete_batch, get_all_batches
)

def show():
    # Restrict access to admins
    if st.session_state.get("user_type") != "admin":
        st.warning("Access Denied. Only Admins Allowed.")
        st.stop()

    st.title("Admin Dashboard")

    # Load batches once
    batches = get_all_batches()
    if not batches:
        st.info("No batches found. Please add one in 'Manage Batches' tab.")
        batches = []

    tab1, tab2, tab3, tab4 = st.tabs([
        "➕ Add/Delete Student", 
        "📅 Timetable", 
        "✅ Attendance", 
        "🧘 Manage Batches"
    ])

    # ---------------- Tab 1: Student Management ----------------
    with tab1:
        st.subheader("Manage Students")
        name = st.text_input("Student Name")
        phone = st.text_input("WhatsApp Number")
        batch = st.selectbox("Select Batch", batches, key="batch1")

        if st.button("Add Student"):
            if name.strip() and phone.strip() and batch:
                add_student(name.strip(), phone.strip(), batch)
                st.success("Student Added!")
            else:
                st.error("Please fill all fields.")

        if st.button("Delete Student"):
            if phone.strip():
                delete_student(phone.strip())
                st.warning("Student Deleted!")
            else:
                st.error("Enter WhatsApp number to delete student.")

    # ---------------- Tab 2: Timetable ----------------
    with tab2:
        st.subheader("Edit Weekly Timetable")
        week = st.text_input("Week (e.g., 2025-W23)")
        batch = st.selectbox("Batch", batches, key="batch2")
        timetable = st.text_area("Paste timetable content here")

        if st.button("Save Timetable"):
            if week.strip() and timetable.strip():
                save_timetable(week.strip(), batch, {
                    "batch": batch,
                    "week": week.strip(),
                    "timetable": timetable.strip()
                })
                st.success("Timetable saved!")
            else:
                st.error("Week and Timetable content cannot be empty.")

    # ---------------- Tab 3: Attendance ----------------
    with tab3:
        st.subheader("Mark Attendance")
        date = st.date_input("Date", datetime.today())
        batch = st.selectbox("Batch", batches, key="batch3")

        students = get_all_students()
        filtered = [s for s in students if s.to_dict().get("batch") == batch]

        attendance = {}
        for s in filtered:
            student = s.to_dict()
            key = f"{student['phone']}_{date}"  # ensure unique key
            present = st.checkbox(f"{student['name']} ({student['phone']})", key=key)
            attendance[student["phone"]] = "Present" if present else "Absent"

        if st.button("Submit Attendance"):
            save_attendance(date.strftime("%Y-%m-%d"), batch, attendance)
            st.success("Attendance Saved!")

    # ---------------- Tab 4: Batch Management ----------------
    with tab4:
        st.subheader("Manage Batches")

        # Add new batch
        new_batch = st.text_input("New Batch Name (e.g., 6-7AM)")
        if st.button("Add Batch"):
            try:
                add_batch(new_batch.strip())
                st.success(f"Batch '{new_batch}' added. Please reload the page to see it in dropdowns.")
            except ValueError as e:
                st.error(str(e))

        # Delete existing batch
        batch_to_delete = st.selectbox("Select Batch to Delete", get_all_batches(), key="delete_batch")
        if st.button("Delete Batch"):
            delete_batch(batch_to_delete)
            st.warning(f"Batch '{batch_to_delete}' deleted. Please reload the page to refresh dropdowns.")
