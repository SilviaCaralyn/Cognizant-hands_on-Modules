# Hands-On 5: Flask with SQLAlchemy ORM & Database Integration

## Setup
```bash
pip install -r requirements.txt

# Initialize migrations (first time only)
export FLASK_APP=app.py
flask db init
flask db migrate -m "initial schema"
flask db upgrade

python app.py
```
Server runs at http://127.0.0.1:5000

## Quick smoke test without migrations (create tables directly)
```bash
python -c "
from app import create_app
from extensions import db
app = create_app()
with app.app_context():
    db.create_all()
"
```

## Test
```bash
curl http://127.0.0.1:5000/api/courses/
curl -X POST http://127.0.0.1:5000/api/courses/ -H "Content-Type: application/json" \
  -d '{"name":"Data Structures","code":"CS101","credits":4,"department_id":1}'
curl http://127.0.0.1:5000/api/courses/1/students/
```

## Files
- `extensions.py` — shared `db = SQLAlchemy()` instance (avoids circular imports)
- `courses/models.py` — Department, Course, Student, Enrollment with relationships + `to_dict()`
- `courses/routes.py` — CRUD routes backed by real ORM queries, `get_or_404`, JOIN-based `/students/`
- `app.py` — wires `db.init_app()` and `Flask-Migrate`
