
# Insider QA Technical Task – End-to-End Automation Suite

> **Author:** Serhii Nadakhovskyi
> **Date:** April 23, 2025
> **Role:** Senior QA Engineer Candidate
> **Project Scope:** UI + API automation with validation & resiliency features

---

## Table of Contents

1. Project Structure
2. Technology Stack
3. Environment Setup
4. Test Execution
5. UI Automation (Task 3)
6. API Automation (Task 4)
7. Design Decisions
8. Resiliency & Flakiness Handling
9. Failure Evidence Capture
10. Future Improvements

---

## Project Structure

```bash
Insider_QA_Tech_Task/
├── pages/
├── petstore_tests/
├── tests/
│   └── screenshots/
├── utils/
└── README_SNadakhovskyi.md
```

---

## Technology Stack

- Selenium (PyTest)
- Requests
- PyTest Hooks
- Chrome/Firefox Support

---

## Environment Setup

```bash
git clone <repo>
cd Insider_QA_Tech_Task
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Test Execution

```bash
pytest                      # All tests
pytest -k chrome            # UI test in Chrome
pytest petstore_tests/      # Only API tests
```

---

## UI Automation (Task 3)

- Career page validation
- Location & department filter
- Retry logic for dropdowns
- Conditional screenshot capture

---

## API Automation (Task 4)

- Full CRUD with retry
- Random pet ID to avoid conflict
- Negative validations (invalid ID, missing fields)

---

## Design Decisions

- POM for UI
- Modular test organization
- Retry wrappers
- Screenshot on failure only
- Parametrized drivers

---

## Flakiness Handling

| Context     | Strategy                |
|-------------|--------------------------|
| Dropdowns   | Retry loop + wait        |
| Job Cards   | Scrolling + retries      |
| API         | Retry wrapper            |
| UI Evidence | Screenshot on fail only  |

---

## Failure Evidence

Screenshots stored in `tests/screenshots` on failure:

```python
driver.save_screenshot("tests/screenshots/screenshot_<test_name>.png")
```

---

## Future Improvements

- Allure/HTML Reporting
- GitHub Actions CI
- Lighthouse audit
- More cross-browser runners

---

## Contact

For questions, improvements, or discussions:
**Serhii Nadakhovskyi nadahov@gmail.com**
