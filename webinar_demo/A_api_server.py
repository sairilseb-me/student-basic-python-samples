"""
A - A Tiny Backend API (simulating the clearance app)
--------------------------------------
Goal: Show what "backend" actually means in practice: a program
that listens for requests and sends back responses, usually as JSON.

This is a stripped-down stand-in for the Django backend in the real
clearance app. Same idea, much smaller.

Run this first, then run B_request_basics.py or C_automate_client.py
in a SEPARATE terminal while this one keeps running.
"""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    """Let a page opened directly in the browser (a different origin) call this API."""
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST"
    return response


# Pretend "database" - just a Python dict in memory
students = {
    "juan-dela-cruz": {"name": "Juan Dela Cruz", "status": "pending"},
    "maria-santos": {"name": "Maria Santos", "status": "pending"},
    "pedro-reyes": {"name": "Pedro Reyes", "status": "pending"},
}


@app.route("/api/students", methods=["GET"])
def list_students():
    """A GET request: 'give me data'. No changes happen on the server."""
    return jsonify(list(students.values()))


@app.route("/api/students/<student_id>", methods=["GET"])
def get_student(student_id):
    """GET one specific record. Returns 404 if it doesn't exist."""
    student = students.get(student_id)
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student)


@app.route("/api/students/<student_id>/sign", methods=["POST"])
def sign_student(student_id):
    """A POST request: 'do something / change data on the server'."""
    student = students.get(student_id)
    if student is None:
        return jsonify({"error": "Student not found"}), 404

    student["status"] = "cleared"
    return jsonify({
        "message": f"{student['name']} has been cleared.",
        "student": student,
    })


if __name__ == "__main__":
    print("Backend running at http://127.0.0.1:5000")
    print("Try opening http://127.0.0.1:5000/api/students in a browser")
    app.run(port=5000)
