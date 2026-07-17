# Hands-On 2: SDLC vs TDLC — V-Model & Agile QA Integration

## Task 1: V-Model Mapping

### 9. V-Model Diagram (ASCII)

```
Requirements  ──────────────────────────  Acceptance Testing
     \                                          /
      System Design ─────────────────  System Testing
           \                                /
            Architecture Design ── Integration Testing
                 \                      /
                  Module Design ── Unit Testing
                       \              /
                          Coding
                       (bottom vertex)
```

### 10. SDLC Phase → Test Artifact Produced

| SDLC Phase | Test Artifact Produced |
|---|---|
| Requirements | Acceptance Test Plan is prepared during this phase. |
| System Design | System Test Plan / test scenarios based on system-level design docs. |
| Architecture Design | Integration Test Plan, identifying component interfaces to be tested together. |
| Module Design | Unit Test Plan / test cases derived from detailed module specs. |
| Coding | Unit tests are actually written and executed alongside code. |

### 11. Entry & Exit Criteria per TDLC Phase

| Testing Phase | Entry Criteria | Exit Criteria |
|---|---|---|
| Unit Testing | Code for the module is complete and compiles; unit test cases are written. | All unit test cases executed; code coverage meets target (e.g. 80%); no known critical defects in the module. |
| Integration Testing | All relevant unit-tested modules are available and integrated in a test environment. | All integration points tested; no critical/high defects on interfaces between modules. |
| System Testing | Fully integrated build deployed to a stable test environment; integration testing exit criteria met. | All planned system test cases executed; defect count below agreed threshold; no open critical/high defects. |
| Acceptance Testing (UAT) | System testing exit criteria met; UAT environment configured with production-like data. | Business stakeholders sign off; all acceptance criteria (Given-When-Then) pass. |

### 12. Early QA Engagement Points (Course Management API)

1. **Requirements review** — QA reviews user stories (e.g., "create a course") for ambiguity and testability before any code is written, catching issues like undefined validation rules for course codes.
2. **Architecture/API design review** — QA reviews the proposed API contract (endpoints, request/response schemas) before implementation begins, flagging missing error-response definitions (e.g., what happens on duplicate course codes) early.

---

## Task 2: Agile QA and Shift-Left Testing

### 13. Problems Caused by Waterfall (testing after development)

1. **Late defect discovery** — bugs found only after full development means fixes are far more expensive and can require re-architecting parts of the Course Management API.
2. **Compressed test schedules** — if development runs long, testing time gets squeezed, leading to under-tested releases.
3. **No feedback loop for requirements gaps** — ambiguities in requirements (e.g., "what counts as a duplicate course?") aren't caught until QA executes tests near the end, by which point the whole team has built on the wrong assumption.

### 14. QA in Agile Ceremonies

- **Sprint Planning**: QA collaborates with the team to define clear, testable acceptance criteria for each story before it's committed to the sprint.
- **Daily Standup**: QA reports blocking issues — e.g., "I can't test the course-creation endpoint because the staging DB migration hasn't run."
- **Sprint Review**: QA helps demo the working, tested feature to stakeholders and calls out known limitations.
- **Retrospective**: QA raises process improvements — e.g., "we need earlier access to test data" or "flaky tests slowed us down this sprint."

### 15. Four Shift-Left Practices Applied to the Course Management API

(a) **Reviewing requirements for testability** — Before development starts, QA checks that the "create course" story specifies exact validation rules (max length, required fields) so test cases can be written unambiguously.

(b) **Writing test cases before code (TDD/BDD)** — QA and devs write Given-When-Then scenarios for `POST /api/courses/` before implementation, so the endpoint is built against a known test contract.

(c) **Static code analysis** — Tools like `flake8`/`pylint` and `bandit` run automatically on every commit to the API codebase, catching style issues and security smells before a PR is even reviewed.

(d) **API contract testing before integration** — Using a schema (OpenAPI) contract test, the frontend team can validate against a mocked `POST /api/courses/` response before the real backend endpoint is finished, catching mismatches early.

### 16. Acceptance Criteria — Given-When-Then

**User Story:** As a college admin, I want to create a new course, so that students can enroll in it.

```gherkin
Scenario: Happy path - create a course successfully
  Given I am logged in as a college admin
  And no course with code "CS201" exists
  When I submit a new course with name "Data Structures", code "CS201", and credits "4"
  Then the course is created successfully
  And I see a confirmation message with the new course ID

Scenario: Duplicate course code
  Given I am logged in as a college admin
  And a course with code "CS201" already exists
  When I submit a new course with code "CS201"
  Then the system rejects the request with a "duplicate course code" error
  And no new course is created

Scenario: Missing required fields
  Given I am logged in as a college admin
  When I submit a new course without a "name" field
  Then the system rejects the request with a validation error indicating "name is required"
  And no new course is created
```
