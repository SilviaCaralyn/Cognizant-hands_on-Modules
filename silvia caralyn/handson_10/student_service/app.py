"""
Student Service — owns Student + Enrollment data.
Runs independently on port 5002 with its own database. To enroll a student
it must verify the course exists by calling Course Service over HTTP
(Step 100) — services never share a database directly.
"""
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

COURSE_SERVICE_URL = 'http://127.0.0.1:5001'

_students = [
    {'id': 1, 'first_name': 'Asha', 'last_name': 'Menon', 'email': 'asha@college.edu'},
]
_enrollments = []
_next_enrollment_id = 1


@app.route('/api/students/', methods=['GET'])
def list_students():
    return jsonify(_students), 200


@app.route('/api/students/<int:student_id>/enroll', methods=['POST'])
def enroll_student(student_id):
    global _next_enrollment_id
    student = next((s for s in _students if s['id'] == student_id), None)
    if student is None:
        return jsonify({'error': 'Student not found'}), 404

    payload = request.get_json()
    course_id = payload.get('course_id')

    # Step 100: verify the course exists by calling Course Service
    try:
        resp = requests.get(f'{COURSE_SERVICE_URL}/api/courses/{course_id}/', timeout=3)
    except requests.ConnectionError:
        # Step 101: Course Service is unavailable
        return jsonify({'error': 'Course Service unavailable'}), 503

    if resp.status_code == 404:
        return jsonify({'error': f'Course {course_id} does not exist'}), 400

    enrollment = {
        'id': _next_enrollment_id,
        'student_id': student_id,
        'course_id': course_id,
        'course_snapshot': resp.json(),
    }
    _enrollments.append(enrollment)
    _next_enrollment_id += 1
    return jsonify(enrollment), 201


if __name__ == '__main__':
    app.run(port=5002, debug=True)
