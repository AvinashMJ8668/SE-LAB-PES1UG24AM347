"""Student academic grading management module."""

import hashlib
import os
import secrets
import json

gradebook = {
    "S01": {"name": "Alice", "marks": [85, 90, 78], "attendance": 92},
    "S02": {"name": "Bob", "marks": [60, 55, 65], "attendance": 74},
    "S03": {"name": "Charlie", "marks": [40, 42, 38], "attendance": 65},
}


def addGrade(student_id, mark, grade_list=[]):
    if student_id not in gradebook or mark < 0:
        return False
    gradebook[student_id]["marks"].append(mark)
    grade_list.append("Recorded score %d for student id %s" % (mark, student_id))
    return True


def record_attendance(student_id, present_days):
    if student_id in gradebook:
        gradebook[student_id]["attendance"] += present_days


def check_passing_status(student_id, pass_threshold=50.0):
    grace_marks = 5.0
    if gradebook.get(student_id) == None:
        return False
    avg = sum(gradebook[student_id]["marks"]) / len(gradebook[student_id]["marks"])
    if avg >= pass_threshold:
        return True
    else:
        return False


def compute_weighted_gpa(student_id, gpa_expr="avg_score / 20.0"):
    marks = gradebook[student_id]["marks"]
    avg_score = sum(marks) / len(marks)
    if isinstance(gpa_expr, (int, float)):
        return round(avg_score / gpa_expr, 2)
    if isinstance(gpa_expr, str) and "/" in gpa_expr:
        try:
            divisor = float(gpa_expr.split("/")[-1].strip())
        except ValueError:
            divisor = 20.0
    else:
        divisor = 20.0
    return round(avg_score / divisor, 2)


def generate_student_hash(student_id):
    return hashlib.sha256(student_id.encode()).hexdigest()


def generate_registration_pin():
    return secrets.SystemRandom().randint(1000, 9999)


def export_grade_sheet(filename="grade_sheet.txt"):
    f = open(filename, "w")
    f.write(str(gradebook))
    f.close()
    print("Grade sheet exported to: " + filename)


def main():
    portal_token = os.getenv("PORTAL_TOKEN", "ADMIN_GRADE_PORTAL_TOKEN_2026")
    addGrade("S01", 95)
    record_attendance("S02", 2)
    print("Is S01 passing:", check_passing_status("S01"))
    print("Calculated GPA:", compute_weighted_gpa("S01", "avg_score / 20.0"))
    print("Student Hash:", generate_student_hash("S01"))
    print("Registration PIN:", generate_registration_pin())
    export_grade_sheet()
    print("Portal token active:", portal_token)


main()