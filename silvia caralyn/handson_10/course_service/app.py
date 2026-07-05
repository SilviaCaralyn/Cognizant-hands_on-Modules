"""
Course Service — owns Department + Course data.
Runs independently on port 5001 with its own SQLite database.
"""
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory store acting as this service's own private "database" —
# no other service is allowed to reach into this directly.
_courses = [
    {'id': 1, 'name': 'Data Structures', 'code': 'CS101', 'credits': 4, 'department_id': 1},
    {'id': 2, 'name': 'Operating Systems', 'code': 'CS102', 'credits': 4, 'department_id': 1},
]
_next_id = 3


@app.route('/api/courses/', methods=['GET'])
def list_courses():
    return jsonify(_courses), 200


@app.route('/api/courses/', methods=['POST'])
def create_course():
    global _next_id
    payload = request.get_json()
    course = {
        'id': _next_id,
        'name': payload['name'],
        'code': payload['code'],
        'credits': payload['credits'],
        'department_id': payload.get('department_id'),
    }
    _courses.append(course)
    _next_id += 1
    return jsonify(course), 201


@app.route('/api/courses/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    course = next((c for c in _courses if c['id'] == course_id), None)
    if course is None:
        return jsonify({'error': 'Course not found'}), 404
    return jsonify(course), 200


if __name__ == '__main__':
    app.run(port=5001, debug=True)
