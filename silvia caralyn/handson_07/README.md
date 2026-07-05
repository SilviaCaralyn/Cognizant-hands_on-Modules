# Hands-On 7: FastAPI — Dependency Injection, CRUD & OpenAPI

## Setup
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
Swagger docs: http://127.0.0.1:8000/docs (endpoints grouped by tag: Courses / Students / Enrollments)

## Note on trailing slashes
Detail routes (e.g. `/api/courses/{id}`) are defined WITHOUT a trailing slash.
Calling them with a trailing slash triggers FastAPI's automatic 307 redirect —
use the exact path shown below.

## Test
```bash
curl -X POST http://127.0.0.1:8000/api/courses/ -H "Content-Type: application/json" \
  -d '{"name":"Data Structures","code":"CS101","credits":4,"department_id":1}'

curl -X POST http://127.0.0.1:8000/api/enrollments/ -H "Content-Type: application/json" \
  -d '{"student_id":1,"course_id":1}'
# returns 201 immediately; check the server console for the
# "Sending confirmation to ..." print from the background task

curl -X DELETE http://127.0.0.1:8000/api/courses/1   # 204 No Content
curl http://127.0.0.1:8000/api/courses/1              # 404 Not Found
```

## Files
- `models.py` — SQLAlchemy models (Department, Course, Student, Enrollment)
- `schemas.py` — Pydantic Create/Response schemas
- `database.py` — async engine + `get_db()` dependency
- `main.py` — full CRUD for courses/students/enrollments, `response_model`,
  correct status codes (201/204/404), `HTTPException`, `BackgroundTasks`
  for simulated email confirmation, OpenAPI tags/summary/description/contact
