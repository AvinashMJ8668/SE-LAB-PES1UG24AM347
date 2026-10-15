"""Student academic grading management module.

This module provides functionality to track student scores, record attendance,
check passing status, compute weighted GPAs, generate registration PINs, and
safely export grade sheets.
"""

import hashlib
import os
import secrets

# Gradebook storing student records: scores and attendance.
GRADEBOOK = {
    "S01": {"name": "Alice", "marks": [85, 90, 78], "attendance": 92},
    "S02": {"name": "Bob", "marks": [60, 55, 65], "attendance": 74},
    "S03": {"name": "Charlie", "marks": [40, 42, 38], "attendance": 65},
}
# Backward compatibility alias for gradebook
gradebook = GRADEBOOK


def add_grade(student_id, mark, grade_list=None):
    """Add a numeric score to a student's grade record."""
    if grade_list is None:
        grade_list = []
    if student_id not in GRADEBOOK or mark < 0:
        return False
    GRADEBOOK[student_id]["marks"].append(mark)
    grade_list.append(f"Recorded score {mark} for student id {student_id}")
    return True


# Backward compatibility alias for camelCase function name
addGrade = add_grade  # pylint: disable=invalid-name


def record_attendance(student_id, present_days):
    """Record additional attendance days for a given student."""
    if student_id not in GRADEBOOK:
        return
    GRADEBOOK[student_id]["attendance"] += present_days


def check_passing_status(student_id, pass_threshold=50.0):
    """Check if a student's average marks meet or exceed the threshold."""
    student_data = GRADEBOOK.get(student_id)
    if student_data is None:
        return False
    marks = student_data["marks"]
    if not marks:
        return False
    avg = sum(marks) / len(marks)
    return avg >= pass_threshold


def compute_weighted_gpa(student_id, gpa_expr="avg_score / 20.0"):
    """Compute the weighted GPA for a student safely without eval()."""
    if student_id not in GRADEBOOK:
        return 0.0
    marks = GRADEBOOK[student_id]["marks"]
    if not marks:
        return 0.0
    avg_score = sum(marks) / len(marks)

    if isinstance(gpa_expr, (int, float)):
        divisor = float(gpa_expr)
    elif isinstance(gpa_expr, str) and "/" in gpa_expr:
        try:
            divisor = float(gpa_expr.split("/")[-1].strip())
        except ValueError:
            divisor = 20.0
    else:
        divisor = 20.0

    return round(avg_score / divisor, 2)


def generate_student_hash(student_id):
    """Generate a secure SHA-256 hash for a given student ID."""
    return hashlib.sha256(student_id.encode("utf-8")).hexdigest()


def generate_registration_pin():
    """Generate a cryptographically secure 4-digit registration PIN."""
    return secrets.SystemRandom().randint(1000, 9999)


def export_grade_sheet(filename="grade_sheet.txt"):
    """Export the gradebook dictionary safely to a local file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(GRADEBOOK))
    print(f"Grade sheet exported to: {filename}")


def main():
    """Execute the demonstration workflow for the grade system."""
    portal_token = os.getenv("PORTAL_TOKEN", "ADMIN_GRADE_PORTAL_TOKEN_2026")
    add_grade("S01", 95)
    record_attendance("S02", 2)
    print("Is S01 passing:", check_passing_status("S01"))
    print("Calculated GPA:", compute_weighted_gpa("S01", "avg_score / 20.0"))
    print("Student Hash:", generate_student_hash("S01"))
    print("Registration PIN:", generate_registration_pin())
    export_grade_sheet()
    print("Portal token active:", portal_token)


if __name__ == "__main__":
    main()
