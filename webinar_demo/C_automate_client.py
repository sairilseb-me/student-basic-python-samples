"""
C - Automating a Whole Workflow with Requests
--------------------------------------
Goal: Connect the dots back to automation. A person using the
clearance app's frontend clicks a button once per student. Since
the frontend is just sending requests to the same backend, a
script can do the exact same thing, for every student, without
any clicking at all.
"""

import requests

BASE_URL = "http://127.0.0.1:5000"


def get_all_students():
    response = requests.get(f"{BASE_URL}/api/students")
    return response.json()


def clear_student(student_id: str):
    response = requests.post(f"{BASE_URL}/api/students/{student_id}/sign")
    return response.json()


def run_batch_clearance():
    students = get_all_students()
    print(f"Found {len(students)} student(s).\n")

    for student in students:
        # Rebuild the same student_id format used in the URL
        student_id = student["name"].lower().replace(" ", "-")

        if student["status"] == "pending":
            result = clear_student(student_id)
            print(f"Cleared: {result['student']['name']}")
        else:
            print(f"Already cleared: {student['name']}")

    print("\nDone. Every pending student has been cleared automatically.")


if __name__ == "__main__":
    run_batch_clearance()
