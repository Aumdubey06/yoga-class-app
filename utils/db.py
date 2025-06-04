from firebase_config import db

def add_student(name, phone, batch):
    student_id = f"{batch}_{phone}"
    db.collection("students").document(student_id).set({
        "name": name,
        "phone": phone,
        "batch": batch
    })

def delete_student(phone):
    students = db.collection("students").where("phone", "==", phone).get()
    for student in students:
        db.collection("students").document(student.id).delete()

def get_all_students():
    return db.collection("students").stream()

def save_attendance(date, batch, attendance_data):
    # Ensure all keys are non-empty strings
    cleaned_data = {
        str(k).strip(): v for k, v in attendance_data.items()
        if isinstance(k, str) and k.strip()
    }

    if not cleaned_data:
        raise ValueError("Attendance keys must be non-empty strings.")

    doc_id = f"{date}_{batch.replace(':', '-').replace('/', '-')}"
    db.collection("attendance").document(doc_id).set({
        "date": date,
        "batch": batch,
        "records": cleaned_data
    })

def get_attendance_for_student(phone):
    from firebase_config import db
    records = db.collection("attendance").stream()
    result = []
    for rec in records:
        data = rec.to_dict()
        # Debug: check if phone is in keys
        if phone in data:
            result.append({"date": rec.id.split("_")[0], "status": data[phone]})
    # Sort attendance by date descending
    result.sort(key=lambda x: x["date"], reverse=True)
    return result

def save_timetable(week, batch, timetable):
    db.collection("timetable").document(f"{week}_{batch}").set(timetable)

def get_timetable(batch):
    docs = db.collection("timetable").where("batch", "==", batch).stream()
    result = []
    for doc in docs:
        data = doc.to_dict()
        # Extract week from document ID like "2025-W23_6-7AM"
        week = doc.id.split("_")[0] if "_" in doc.id else ""
        data["week"] = week
        result.append(data)
    return result


def get_timetable_for_batch(batch):
    docs = db.collection("timetable").where("batch", "==", batch).stream()
    timetables = []
    for doc in docs:
        data = doc.to_dict()
        timetables.append(data)
    return timetables

def get_student_by_phone(phone):
    students = db.collection("students").where("phone", "==", phone).stream()
    for student in students:
        return student.to_dict()
    return None

from datetime import datetime, timedelta

def get_timetable_for_batch_and_week(batch, week):
    # Query timetable for specific batch and week
    doc_id = f"{week}_{batch}"
    doc = db.collection("timetable").document(doc_id).get()
    if doc.exists:
        return doc.to_dict()
    return None

def get_current_week_str():
    today = datetime.today()
    year, week_num, _ = today.isocalendar()  # returns (year, week number, weekday)
    return f"{year}-W{week_num:02d}"

def get_student_data(phone):
    docs = db.collection("students").where("phone", "==", phone).stream()
    for doc in docs:
        return doc.to_dict()
    return None

def get_timetable_for_batch_and_week(batch, week):
    doc_ref = db.collection("timetable").document(f"{week}_{batch}")
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    return None

# Batch management

def add_batch(batch_name):
    if not batch_name.strip():
        raise ValueError("Batch name cannot be empty.")
    db.collection("batches").document(batch_name).set({"name": batch_name})

def delete_batch(batch_name):
    db.collection("batches").document(batch_name).delete()

def get_all_batches():
    docs = db.collection("batches").stream()
    return [doc.id for doc in docs]
