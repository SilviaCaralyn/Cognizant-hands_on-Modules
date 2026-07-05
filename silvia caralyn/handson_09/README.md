# Hands-On 9: Authentication & Security — JWT, OAuth2 & OWASP

## Setup
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Test flow
```bash
# 1. Register
curl -X POST http://127.0.0.1:8000/api/v1/auth/register/ -H "Content-Type: application/json" \
  -d '{"email":"asha@college.edu","password":"Secret123"}'
# repeat -> 409 Conflict

# 2. Login (get JWT)
curl -X POST http://127.0.0.1:8000/api/v1/auth/login/ -H "Content-Type: application/json" \
  -d '{"email":"asha@college.edu","password":"Secret123"}'

# 3. GET courses — no auth required
curl http://127.0.0.1:8000/api/v1/courses/

# 4. POST course without token -> 401
curl -X POST http://127.0.0.1:8000/api/v1/courses/ -H "Content-Type: application/json" \
  -d '{"name":"DS","code":"CS101","credits":4,"department_id":1}'

# 5. POST course WITH token -> 201
curl -X POST http://127.0.0.1:8000/api/v1/courses/ \
  -H "Content-Type: application/json" -H "Authorization: Bearer <token>" \
  -d '{"name":"DS","code":"CS101","credits":4,"department_id":1}'
```

## Files
- `security.py` — `get_password_hash`/`verify_password` (bcrypt via passlib),
  `create_access_token`/`decode_access_token` (JWT via python-jose)
- `models.py` — User, Department, Course
- `schemas.py` — UserRegister, LoginRequest, TokenResponse, CourseCreate/Response
- `main.py` — register (409 on duplicate email), login (JWT), `get_current_user`
  dependency, protected POST/DELETE course routes (401 without token), CORS
  configured for `http://localhost:3000`

Verified: passwords are stored only as bcrypt hashes, never plain text.
