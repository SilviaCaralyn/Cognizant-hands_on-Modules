# Hands-On 1: Web Framework Foundations & Django Project Setup

## Setup
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Test
Visit or curl:
```bash
curl http://127.0.0.1:8000/api/hello/
```
Expected: `Course Management API is running`

## Files
- `notes.py` — Task 1 answers (request-response cycle, middleware, WSGI vs ASGI, MVC->MVT)
- `coursemanager/` — Django project (settings.py, urls.py, wsgi.py, asgi.py)
- `courses/` — Django app with `views.py` (hello_view) and `urls.py`
