# Hands-On 6: FastAPI — Path Parameters, Pydantic & Async Endpoints

## Setup
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
Server runs at http://127.0.0.1:8000
Swagger docs at http://127.0.0.1:8000/docs

## Test
```bash
curl http://127.0.0.1:8000/
curl -X POST http://127.0.0.1:8000/api/courses/ -H "Content-Type: application/json" \
  -d '{"name":"Data Structures","code":"CS101","credits":4,"department_id":1}'
curl "http://127.0.0.1:8000/api/courses/?skip=0&limit=2"
```
Sending an incomplete body returns a 422 with Pydantic's field-level validation errors.

## Files
- `schemas.py` — CourseCreate, CourseUpdate, CourseResponse, DepartmentResponse (nested)
- `models.py` — SQLAlchemy ORM models (Department, Course)
- `database.py` — async engine, `get_db()` dependency, `init_models()`
- `main.py` — FastAPI app with async CRUD, pagination (`skip`/`limit`), filtering (`department_id`)
