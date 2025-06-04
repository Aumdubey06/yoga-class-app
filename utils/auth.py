from firebase_config import db

def is_admin(phone):
    return phone == "9827998946"

def student_exists(phone):
    students_ref = db.collection("students").where("phone", "==", phone).get()
    return len(students_ref) > 0

from firebase_config import db

def get_student_data(phone):
    students_ref = db.collection("students")
    query = students_ref.where("phone", "==", phone).stream()
    for student in query:
        return student.to_dict()
    return None