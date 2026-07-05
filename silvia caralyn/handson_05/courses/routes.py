from flask import Blueprint, request, jsonify
from extensions import db
from .models import Course, Student, Enrollment

courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')


def make_response_json(data, status_code=200):
    return jsonify({'status': 'success', 'data': data}), status_code


@courses_bp.route('/', methods=['GET'])
def list_courses():
    courses = Course.query.all()
    return make_response_json([c.to_dict() for c in courses], 200)


@courses_bp.route('/', methods=['POST'])
def create_course():
    payload = request.get_json()
    if payload is None:
        return jsonify({'status': 'error', 'message': 'Request body must be JSON'}), 400

    required_fields = ['name', 'code', 'credits', 'department_id']
    missing = [f for f in required_fields if f not in payload]
    if missing:
        return jsonify({'status': 'error', 'message': f'Missing fields: {missing}'}), 400

    course = Course(
        name=payload['name'],
        code=payload['code'],
        credits=payload['credits'],
        department_id=payload['department_id'],
    )
    db.session.add(course)
    db.session.commit()
    return make_response_json(course.to_dict(), 201)


@courses_bp.route('/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    course = Course.query.get_or_404(course_id)
    return make_response_json(course.to_dict(), 200)


@courses_bp.route('/<int:course_id>/', methods=['PUT'])
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    payload = request.get_json()
    if payload is None:
        return jsonify({'status': 'error', 'message': 'Request body must be JSON'}), 400
    for field in ('name', 'code', 'credits', 'department_id'):
        if field in payload:
            setattr(course, field, payload[field])
    db.session.commit()
    return make_response_json(course.to_dict(), 200)


@courses_bp.route('/<int:course_id>/', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return '', 204


@courses_bp.route('/<int:course_id>/students/', methods=['GET'])
def course_students(course_id):
    course = Course.query.get_or_404(course_id)
    students = [e.student for e in course.enrollments]
    return make_response_json([s.to_dict() for s in students], 200)
