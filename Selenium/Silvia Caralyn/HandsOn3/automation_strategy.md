# Hands-On 3: Test Automation Process, Lifecycle & Framework Types

## Task 1: Automation Decision and Test Case Selection

### 17. Five Criteria for Deciding What to Automate

1. **Repetitiveness** — Is this test run often (every build/regression)? Applied: `POST /api/courses/` 201 test runs on every commit → strong automation candidate.
2. **Stability** — Is the feature/UI stable, unlikely to change frequently? The endpoint's contract is stable → good candidate.
3. **High business risk** — Would a failure here have serious impact? Course creation is core functionality → high risk if broken → automate.
4. **Time savings / ROI** — Does automating save meaningful time over many runs? Manual verification takes ~2 minutes; automated takes 2 seconds and runs on every CI build → clear ROI.
5. **Objectively verifiable result** — Can pass/fail be determined without human judgment? A 201 status code and JSON body are precisely checkable → ideal for automation.

### 18. Automate or Manual?

| Test Case | Decision | Justification |
|---|---|---|
| (a) Regression test for all CRUD endpoints after every code change | Automate | Repetitive, runs constantly, objectively verifiable. |
| (b) Exploratory testing of a new search feature | Manual | Requires human judgment and creativity to discover unexpected issues. |
| (c) Performance test: 100 concurrent users on GET /api/courses/ | Automate | Needs tooling (e.g., Locust/JMeter) to simulate load reliably and repeatably — not something a human can do manually. |
| (d) UI test for the login form | Automate | Stable, repetitive, well-defined pass/fail criteria — good Selenium candidate. |
| (e) Verify the API documentation (Swagger) is accurate | Manual | Requires human judgment to assess clarity/accuracy of descriptions against intent. |
| (f) Smoke test: verify API is reachable after deployment | Automate | Simple, repetitive, run on every deployment — ideal for a CI pipeline check. |

### 19. Automation ROI Calculation

- Manual run: 30 minutes = 0.5 hours
- Automation build cost: 4 hours (one-time)
- After the 10th run, each automated run costs 20% more in maintenance overhead. Assume automated execution itself is near-instant (say ~0 hours of human time, since it's unattended), so the overhead is what matters after run 10.

**Break-even without overhead:**
Automation pays for itself once the cumulative manual-time saved exceeds the 4-hour build cost.
- Time saved per run = 0.5 hours (manual time no longer spent)
- Runs needed = 4 hours ÷ 0.5 hours/run = **8 runs**

Since break-even (8 runs) happens *before* the 10th run, the 20% maintenance overhead (which only kicks in after run 10) does not change the break-even point. **Automation pays for itself after 8 runs.**

(Note for a QA lead: if overhead had applied earlier, e.g., from run 1, you'd need to add ~20% more time-cost per run into the calculation and solve iteratively — but per the stated conditions, break-even is reached before overhead applies.)

### 20. Flaky Tests

**Definition:** A flaky test is one that produces inconsistent results (sometimes pass, sometimes fail) without any changes to the code being tested — undermining confidence in the whole suite.

**Example:** A Selenium test that clicks "Submit" and immediately asserts a success message, without waiting for the AJAX call to complete — it passes when the network is fast and fails when it's slow.

**3 Prevention Strategies:**
1. Replace `time.sleep()` with explicit `WebDriverWait` + `ExpectedConditions` so tests wait for actual state changes, not a guessed duration.
2. Isolate test data/state per test (e.g., use a fresh test DB or unique course codes per run) to avoid tests interfering with each other.
3. Avoid hard-coded absolute XPaths and other brittle locators that only *sometimes* match due to dynamic DOM ordering; use stable IDs or data-test attributes instead.

---

## Task 2: Compare Automation Framework Types

### 21. Framework Comparison

| Framework | Description | Advantage | Disadvantage | Use Case |
|---|---|---|---|---|
| **Linear** | Scripts recorded/written as a straight-line sequence of steps with no reuse or abstraction — "record and playback" style. | Fast to create for a one-off check. | Extremely hard to maintain; any UI change breaks many duplicated scripts. | A single quick smoke check of the course-creation page during a demo. |
| **Modular** | Breaks the application into independent modules/functions (e.g., `login()`, `createCourse()`) that scripts call and combine. | Reusable functions reduce duplication. | Still requires programming knowledge; test data is often still hard-coded. | Reusing a `login()` function across 20 different Course Management tests. |
| **Data-Driven** | Test logic is separated from test data, which is stored externally (CSV/Excel/JSON) and looped over. | Same test logic validated against many data combinations with no code duplication. | Requires a mechanism to manage and maintain external data files. | Testing course creation with 50 different name/code/credit combinations. |
| **Keyword-Driven** | Test steps are represented as keywords (e.g., "ClickButton", "EnterText") in a table, interpreted by a driver engine. | Non-technical team members can write tests using keywords. | Significant upfront framework-engineering effort to build the keyword interpreter. | Allowing a manual QA analyst to write new course-creation test cases in an Excel sheet without coding. |
| **Hybrid** | Combines Modular (reusable functions) + Data-Driven (external data) + optionally Keyword-Driven abstraction. | Most flexible, scalable, and maintainable for real-world projects. | Most complex to design and set up initially. | The full Course Management System Selenium suite: reusable page objects, data-driven login tests, and CI-integrated reporting. |

### 22. Recommendation for the Given Scenario

**Scenario:** Test login with 50 user/password combos, reuse login steps across 20 test cases, support both technical and non-technical team members.

**Recommendation: Hybrid framework** combining:
- **Modular** (Page Object Model) for the reusable `login()` interaction, used across all 20 test cases.
- **Data-Driven** for the 50 username/password combinations, fed in via a CSV/JSON file and looped with `@pytest.mark.parametrize`.
- **Keyword-Driven** (optional layer) if non-technical team members truly need to author new tests without Python — otherwise, a well-documented Page Object layer with clear method names (`login_page.login(user, pw)`) is often "readable enough" for non-technical stakeholders to follow, avoiding the extra engineering cost of a full keyword engine unless truly necessary.

### 23. Hybrid Framework Folder Structure

```
CourseManagement_Tests/
├── config/
│   └── config.yaml            # base_url, browser, environment settings
├── data/
│   └── login_credentials.csv  # 50 username/password rows
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   └── course_page.py
├── tests/
│   ├── test_login.py
│   └── test_course_creation.py
├── utils/
│   ├── driver_factory.py      # creates/configures WebDriver instances
│   └── data_reader.py         # reads CSV/JSON test data
├── reports/
│   └── report.html
├── conftest.py
├── requirements.txt
└── pytest.ini
```
