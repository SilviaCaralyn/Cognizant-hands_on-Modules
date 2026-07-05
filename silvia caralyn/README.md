# Digital Nurture 5.0 — Python Backend Frameworks
## Hands-On Exercise Submission

All 10 hands-on exercises for the Course Management API, covering Django,
Flask, and FastAPI. Every exercise has been built AND tested end-to-end
(migrations run, servers started, endpoints hit with curl) before being
included here.

| # | Title | Framework | Folder |
|---|---|---|---|
| 1 | Web Framework Foundations & Django Setup | Django | `handson_01/` |
| 2 | Django Models, ORM & Admin | Django | `handson_02/` |
| 3 | Django REST Views, Serializers, ViewSets | Django + DRF | `handson_03/` |
| 4 | Flask App Structure, Routing, Blueprints | Flask | `handson_04/` |
| 5 | Flask + SQLAlchemy ORM | Flask | `handson_05/` |
| 6 | FastAPI, Pydantic, Async Endpoints | FastAPI | `handson_06/` |
| 7 | FastAPI Full CRUD, Background Tasks, OpenAPI | FastAPI | `handson_07/` |
| 8 | RESTful API Design Best Practices | FastAPI (refactor) | `handson_08/` |
| 9 | JWT Auth, Password Hashing, CORS | FastAPI | `handson_09/` |
| 10 | Microservices — Course/Student services + Gateway | Flask | `handson_10/` |

## How to run any exercise

Each folder is self-contained with its own `requirements.txt` and `README.md`
with exact setup/run/test commands. General pattern:

```bash
cd handson_0X
pip install -r requirements.txt
python app.py            # Flask exercises
# or
python manage.py runserver   # Django exercises (01-03)
# or
uvicorn main:app --reload    # FastAPI exercises (06-09)
```

## Notes
- Hands-On 1–3 use Django (each is a separate, complete Django project).
- Hands-On 4–5 use Flask.
- Hands-On 6–7 use FastAPI.
- Hands-On 8 refactors the FastAPI implementation to meet REST best
  practices (versioning, pagination, PATCH, standardized errors).
- Hands-On 9 adds JWT auth on top of the FastAPI course API.
- Hands-On 10 is framework-agnostic in the brief; implemented in Flask as
  three independent micro-apps (Course Service, Student Service, Gateway).
- Database files (`*.sqlite3`, `*.db`) are intentionally excluded — they
  regenerate automatically the first time you run migrations / `create_all`.
