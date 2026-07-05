from flask import Blueprint, request, jsonify

courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

# In-memory store for Hands-On 4 (Hands-On 5 replaces this with SQLAlchemy)
_courses = []
_next_id = 1


def make_response_json(data, status_code=200):
    return jsonify({'status': 'success', 'data': data}), status_code


@courses_bp.route('/', methods=['GET'])
def list_courses():
    return make_response_json(_courses, 200)


@courses_bp.route('/', methods=['POST'])
def create_course():
    global _next_id
    payload = request.get_json()
    if payload is None:
        return jsonify({'status': 'error', 'message': 'Request body must be JSON'}), 400

    required_fields = ['name', 'code', 'credits']
    missing = [f for f in required_fields if f not in payload]
    if missing:
        return jsonify({'status': 'error', 'message': f'Missing fields: {missing}'}), 400

    course = {
        'id': _next_id,
        'name': payload['name'],
        'code': payload['code'],
        'credits': payload['credits'],
    }
    _courses.append(course)
    _next_id += 1
    return make_response_json(course, 201)


@courses_bp.route('/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    course = next((c for c in _courses if c['id'] == course_id), None)
    if course is None:
        return jsonify({'status': 'error', 'message': 'Course not found'}), 404
    return make_response_json(course, 200)


@courses_bp.route('/<int:course_id>/', methods=['PUT'])
def update_course(course_id):
    course = next((c for c in _courses if c['id'] == course_id), None)
    if course is None:
        return jsonify({'status': 'error', 'message': 'Course not found'}), 404
    payload = request.get_json()
    if payload is None:
        return jsonify({'status': 'error', 'message': 'Request body must be JSON'}), 400
    course.update({k: v for k, v in payload.items() if k in ('name', 'code', 'credits')})
    return make_response_json(course, 200)


@courses_bp.route('/<int:course_id>/', methods=['DELETE'])
def delete_course(course_id):
    global _courses
    course = next((c for c in _courses if c['id'] == course_id), None)
    if course is None:
        return jsonify({'status': 'error', 'message': 'Course not found'}), 404
    _courses = [c for c in _courses if c['id'] != course_id]
    return '', 204
