# Hands-On 1: QA Concepts, Functional Testing & Defect Lifecycle

## Task 1: Map Testing Types to a Real System

### 1. Test cases by testing level (Course Management API)

**Unit Testing** — Test a single function in isolation.
- Test that `validate_course_code(code)` returns `False` when the course code is empty or exceeds 10 characters, without touching the database or API layer.

**Integration Testing** — Test two components working together.
- Test that calling `POST /api/courses/` with valid data correctly inserts a row into the `courses` table, and that the returned `course_id` matches the database primary key.

**System Testing** — Test a full end-to-end flow.
- Submit a `POST /api/courses/` request through the live API, then call `GET /api/courses/{id}` to confirm the created course is retrievable, and finally `DELETE` it, verifying each step returns the correct status code and payload.

**User Acceptance Testing (UAT)** — Test from the perspective of an actual college admin.
- A college admin logs into the admin portal, creates a new course "Data Structures - CS201" with a start date and seat limit, and confirms it appears correctly in the course listing page exactly as they expect it to look.

### 2. Functional vs Non-Functional Classification

| Test Case | Classification |
|---|---|
| Unit test (validate_course_code) | Functional |
| Integration test (DB insert) | Functional |
| System test (create-retrieve-delete flow) | Functional |
| UAT (admin creates course) | Functional |

**Non-functional example:** Performance test — `POST /api/courses/` must respond within 300ms under a load of 100 concurrent requests, and the API must not return 5xx errors under that load (reliability + performance).

### 3. Black-Box vs White-Box Testing

- **Black-Box Testing**: Testing the system's behavior without any knowledge of the internal code — inputs are provided and outputs are verified against expected results. Example: sending a `POST /api/courses/` request and checking the HTTP status code and response body.
- **White-Box Testing**: Testing with full knowledge of the internal code structure, logic branches, and paths. Example: writing a unit test that exercises every `if/else` branch inside `validate_course_code()`.

**Who performs which:** QA testers typically perform Black-Box testing (they validate behavior against requirements without needing to read the source). Developers typically perform White-Box testing (they know the internals and write unit tests targeting specific code paths).

### 4. Formal Test Cases — `POST /api/courses/`

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|---|
| TC_COURSE_001 | Create course with valid data | API is running, DB is reachable | 1. Send POST /api/courses/ with valid JSON body (name, code, credits) 2. Read response | HTTP 201 returned, response body contains the new course with a generated `id` | | |
| TC_COURSE_002 | Create course with duplicate course code | A course with code "CS201" already exists | 1. Send POST /api/courses/ with code "CS201" again | HTTP 409 Conflict returned with an error message indicating duplicate course code | | |
| TC_COURSE_003 | Create course with missing required field | API is running | 1. Send POST /api/courses/ with the `name` field omitted | HTTP 422/400 returned listing `name` as a required field | | |

---

## Task 2: Defect Lifecycle & Severity Classification

### 5. Defect Lifecycle

```
New → Assigned → Open → Fixed → Retest → Verified → Closed
                    │
                    ├──> Rejected   (dev determines it's not a valid bug)
                    └──> Deferred   (valid bug, but fixed in a later release)
```

- **New**: Defect logged by QA, not yet reviewed.
- **Assigned**: Triaged and assigned to a developer.
- **Open**: Developer has started work.
- **Fixed**: Developer believes the issue is resolved and hands it back to QA.
- **Retest**: QA re-executes the original failing steps against the fix.
- **Verified**: QA confirms the fix works as expected.
- **Closed**: Defect lifecycle complete.
- **Rejected**: Developer/lead determines the reported behavior is not actually a defect (e.g., working as designed) — cycle ends without a code change.
- **Deferred**: Confirmed as a valid defect but intentionally postponed to a future release/sprint due to low priority or scope constraints.

### 6. Severity & Priority Classification

| Bug | Severity | Priority | Justification |
|---|---|---|---|
| (a) POST /api/courses/ returns 500 for all requests | Critical | P1 | Core functionality completely broken for every user — blocks all course creation. |
| (b) Course names >150 chars silently truncated | Medium | P3 | Data-quality issue, not a crash; affects a subset of edge-case inputs and doesn't block usage. |
| (c) Typo in Swagger /docs description | Low | P4 | Cosmetic, no functional impact. |
| (d) Intermittent 401 on correct-credential login | High | P2 | Doesn't happen every time (lower than Critical), but authentication instability erodes trust and is hard to reproduce/diagnose, so it needs urgent investigation. |

### 7. Defect Report — Bug (a)

| Field | Value |
|---|---|
| Defect ID | DEF-1042 |
| Title | POST /api/courses/ returns 500 Internal Server Error for all requests |
| Environment | Staging, Ubuntu 22.04, Python 3.11, FastAPI 0.110 |
| Build Version | v2.3.1-rc1 |
| Severity | Critical |
| Priority | P1 |
| Steps to Reproduce | 1. Authenticate as admin. 2. Send POST /api/courses/ with a valid JSON payload (name, code, credits). 3. Observe response. |
| Expected Result | HTTP 201 Created with the newly created course object in the response body. |
| Actual Result | HTTP 500 Internal Server Error returned for every request, regardless of payload validity. |
| Attachments | screenshot of 500 error |

### 8. Severity vs Priority

- **Severity** measures the *impact* of the defect on the system's functionality.
- **Priority** measures how *urgently* it needs to be fixed relative to other work.

**Example where High Severity ≠ High Priority:** A rarely-used "Export to PDF" feature crashes the entire browser tab (High Severity — it's a hard crash) but only 2 users out of 5,000 use that feature, and a workaround (manual export via admin panel) exists. The team may set this to Medium Priority, fixing it in a later sprint, while a cosmetic misalignment on the CEO's dashboard (Low Severity — nothing breaks) gets High Priority because leadership sees it daily.
