# Hands-On 4: Flask App Structure, Routing, Blueprints

## Setup
```bash
pip install -r requirements.txt
python app.py
```
Server runs at http://127.0.0.1:5000

## Test
```bash
curl http://127.0.0.1:5000/api/courses/
curl -X POST http://127.0.0.1:5000/api/courses/ -H "Content-Type: application/json" \
  -d '{"name":"Data Structures","code":"CS101","credits":4}'
curl http://127.0.0.1:5000/api/courses/1/
curl -X DELETE http://127.0.0.1:5000/api/courses/1/
```

## Files
- `app.py` — application factory pattern (`create_app()`), JSON error handlers
- `config.py` — Config class with DB URI, SECRET_KEY, DEBUG
- `courses/routes.py` — Blueprint with full CRUD, request validation, `make_response_json()` envelope

Note: uses in-memory storage. Hands-On 5 replaces this with a real SQLAlchemy database.
