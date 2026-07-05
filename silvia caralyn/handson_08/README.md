# Hands-On 8: RESTful API Design Best Practices

Refactored version of the Course API (FastAPI chosen) meeting all REST
design criteria: versioned URLs, PATCH, Location header, pagination
envelope, search filtering, and standardized error responses.

## Setup
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Test
```bash
# Location header on POST
curl -si -X POST http://127.0.0.1:8000/api/v1/courses/ -H "Content-Type: application/json" \
  -d '{"name":"Data Structures","code":"CS101","credits":4,"department_id":1}'

# Pagination envelope
curl "http://127.0.0.1:8000/api/v1/courses/?page=1&page_size=2"

# Search filter
curl "http://127.0.0.1:8000/api/v1/courses/?search=CS101"

# PATCH partial update
curl -X PATCH http://127.0.0.1:8000/api/v1/courses/1/ -H "Content-Type: application/json" -d '{"credits":5}'

# Standardized error format
curl http://127.0.0.1:8000/api/v1/courses/99/
```

## Files
- `errors.py` — standardized `{'error': {'code','message','field'}}` handlers
  for HTTPException and validation errors
- `schemas.py` — CourseCreate, CoursePatch (all-optional), CourseResponse
- `main.py` — `/api/v1/` versioned routes, PATCH alongside PUT, Location
  header on POST, offset pagination envelope (`count`/`next`/`previous`/`results`),
  `search` query param, versioning-strategy comment (URL vs header-based)
