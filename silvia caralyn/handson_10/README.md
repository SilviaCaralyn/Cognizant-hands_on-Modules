# Hands-On 10: Microservices Architecture — Concepts & Decomposition

## Task 1 — Service Decomposition (Steps 96–97)

| Service Name | Responsibility | Endpoints it owns | Database it owns |
|---|---|---|---|
| **Course Service** | Department & Course CRUD | `/api/courses/*` | Its own courses DB (course_service) |
| **Student Service** | Student CRUD, enrollment | `/api/students/*` | Its own students DB (student_service) |
| **Auth Service** *(not implemented here — see Hands-On 9)* | Registration, login, token validation | `/api/auth/*` | Users DB |
| **Notification Service** *(not implemented here — conceptual)* | Sends email/SMS confirmations | Internal only, triggered by events | None (stateless) |

This exercise implements two of the four services (Course Service and
Student Service) plus a Gateway, per the "start with 2 services" guidance
in the hint — don't over-engineer.

**Key principle demonstrated:** each service owns its own data. Student
Service never queries Course Service's database directly — it always goes
through Course Service's HTTP API.

## Task 2 — Inter-Service Communication & API Gateway (Steps 100–104)

- `student_service/app.py` calls Course Service's `GET /api/courses/{id}/`
  using Python's `requests` library to verify a course exists before
  enrolling a student.
- If Course Service is unreachable, `student_service` catches
  `requests.ConnectionError` and returns **503 Service Unavailable**.
- `gateway/app.py` is a minimal Flask reverse proxy: `/api/courses/*` routes
  to Course Service (port 5001), `/api/students/*` routes to Student
  Service (port 5002).

### Synchronous (HTTP) vs Asynchronous (message queue) — trade-offs

**Synchronous (HTTP, used here):**
- Simple to reason about — the caller gets an immediate answer or error.
- Creates tight coupling: if Course Service is down, enrollment fails
  immediately (as demonstrated by the 503 test below).
- Good fit when the caller genuinely needs the result before continuing.

**Asynchronous (message queue — RabbitMQ, Kafka):**
- The caller publishes an event ("EnrollmentRequested") and moves on; a
  consumer processes it later. Services are decoupled — Course Service
  being briefly down doesn't fail the request.
- Introduces eventual consistency: there's a window where the enrollment
  isn't confirmed yet, and the caller needs another way to learn the
  outcome (polling, webhook, notification).
- Best for non-critical-path work (sending confirmation emails, analytics,
  audit logging) or high-throughput event pipelines — less ideal when the
  user is waiting on screen for a definite yes/no.

## Setup & Run

Each service is independent — run them in separate terminals:

```bash
# Terminal 1
cd course_service
pip install -r requirements.txt
python app.py            # http://127.0.0.1:5001

# Terminal 2
cd student_service
pip install -r requirements.txt
python app.py            # http://127.0.0.1:5002

# Terminal 3
cd gateway
pip install -r requirements.txt
python app.py            # http://127.0.0.1:5000
```

## Test

```bash
# Direct calls to each service
curl http://127.0.0.1:5001/api/courses/
curl http://127.0.0.1:5002/api/students/

# Through the gateway
curl http://127.0.0.1:5000/api/courses/

# Enroll student 1 in course 1 (gateway -> Student Service -> Course Service)
curl -X POST http://127.0.0.1:5000/api/students/1/enroll \
  -H "Content-Type: application/json" -d '{"course_id":1}'

# Stop Course Service, then retry the enroll call -> 503 Service Unavailable
```

## Files
- `course_service/app.py` — owns Course/Department data, port 5001
- `student_service/app.py` — owns Student/Enrollment data, calls Course
  Service over HTTP, port 5002
- `gateway/app.py` — reverse proxy routing `/api/courses/*` and
  `/api/students/*` to the right backend, port 5000
