# Web Application Test Automation Framework

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-v1.40%2B-2EAD33?logo=playwright&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-26%20Passed-0A9EDC?logo=pytest&logoColor=white)
![CI/CD](https://img.shields.io/badge/GitHub%20Actions-CI%2FCD-2088FF?logo=github-actions&logoColor=white)
![API Testing](https://img.shields.io/badge/REST%20API-Postman%20%26%20Requests-FF6C37?logo=postman&logoColor=white)
![Database](https://img.shields.io/badge/Database-SQLite%20Validation-003B57?logo=sqlite&logoColor=white)

An end-to-end automated testing framework built with **Python**, **Playwright**, **Pytest**, **Requests**, and **SQLite**, integrated with **Postman** and **GitHub Actions** for CI/CD continuous regression testing.

---

## 🚀 Key Highlights & Capabilities

- **Web UI Functional & Regression Testing**:
  - Implemented the **Page Object Model (POM)** pattern for clean separation of test scripts and UI locators.
  - Automated positive and negative workflows for authentication, catalog navigation, sorting, cart interactions, and multi-step checkout.
  - Parameterized negative test scenarios to validate field boundary conditions and error messaging.
- **REST API Testing & Response Validation**:
  - Reusable HTTP client wrapping `requests.Session` for CRUD endpoints (`GET`, `POST`, `PUT`, `DELETE`).
  - Status code assertions, JSON schema integrity checks, and negative response verification (`404 Not Found`).
  - Pre-configured **Postman Collection & Environment** files included with JavaScript test scripts.
- **Backend Data & SQL Validation**:
  - Direct database layer validation using SQL queries.
  - Verification of data persistence, state transitions (`PENDING` → `DELIVERED`), and SQL aggregations (`COUNT`, `SUM`).
- **CI/CD Integration**:
  - Automated headless execution on every `git push` and pull request using **GitHub Actions**.
  - Automatic generation and publishing of HTML test reports and failure screenshots as pipeline artifacts.

---

## 📁 Repository Structure

```text
playwright-python-automation/
├── .github/
│   └── workflows/
│       └── regression-tests.yml      # GitHub Actions CI/CD Pipeline
├── config/
│   └── config.py                      # Centralized configuration (URLs, users, timeouts)
├── pages/                             # Page Object Model (POM)
│   ├── base_page.py                   # Reusable web interactions & screenshot helpers
│   ├── login_page.py                  # Login locators and actions
│   ├── inventory_page.py              # Catalog items, sorting, and cart actions
│   ├── cart_page.py                   # Shopping cart page actions
│   └── checkout_page.py               # Multi-step checkout forms & confirmations
├── tests/
│   ├── conftest.py                    # Pytest fixtures (DB, API, Page, failure hooks)
│   ├── test_ui_login.py               # Positive & negative login scenarios
│   ├── test_ui_navigation.py          # Catalog sorting & sidebar navigation
│   ├── test_ui_checkout_flow.py       # End-to-end cart & checkout flow
│   ├── test_api_rest.py               # REST API CRUD and response validation
│   └── test_database_validation.py    # SQL query backend validation
├── postman/
│   ├── Web_Automation_API_Collection.postman_collection.json
│   └── Web_Automation_Environment.postman_environment.json
├── utils/
│   ├── api_client.py                  # Session-based REST API wrapper
│   └── db_helper.py                   # SQLite query executor & seed helper
├── pytest.ini                         # Pytest configuration & markers
├── requirements.txt                   # Project dependencies
└── README.md                          # Documentation
```

---

## 🛠️ Getting Started (Local Setup)

### 1. Prerequisites
- Python 3.10+ installed
- Git installed

### 2. Clone & Setup Virtual Environment
```bash
# Clone the repository
git clone <your-repo-url>
cd playwright-python-automation

# Create and activate virtual environment
python -m venv venv

# Windows (Command Prompt / PowerShell):
venv\Scripts\activate

# macOS / Linux:
source venv/bin/activate
```

### 3. Install Dependencies & Playwright Browsers
```bash
pip install -r requirements.txt
playwright install chromium
```

---

## 🧪 Running Automated Tests

### Run the entire test suite
```bash
pytest
```

### Run with an HTML Report
```bash
pytest --html=reports/report.html --self-contained-html
```

### Run specific test groups using Pytest Markers
```bash
# UI tests only
pytest -m ui

# API tests only
pytest -m api

# Database verification tests only
pytest -m db

# Smoke tests (fast sanity check)
pytest -m smoke

# Full regression suite
pytest -m regression
```

### Run UI tests in headed mode (see the browser in action)
```bash
pytest -m ui --headed --slowmo 500
```

---

## 📮 API Testing via Postman

The `postman/` directory contains an exportable test suite:
1. Open **Postman**.
2. Click **Import** and select:
   - `postman/Web_Automation_API_Collection.postman_collection.json`
   - `postman/Web_Automation_Environment.postman_environment.json`
3. Select the `Web Automation Environment` from the environment dropdown.
4. Click **Run collection** to execute all requests and view assertion results.

---

## ⚙️ CI/CD Pipeline (GitHub Actions)

The workflow file [`.github/workflows/regression-tests.yml`](file:///.github/workflows/regression-tests.yml) automatically executes on push to `main` or pull requests:
1. Provisions an Ubuntu container with Python 3.10.
2. Installs dependencies and headless Chromium.
3. Executes the full test suite (`pytest -v --html=reports/report.html --self-contained-html`).
4. Uploads the HTML report as an artifact accessible from the GitHub Actions dashboard.
5. Captures and uploads failure screenshots if any UI test encounters an issue.

---

## 💼 Resume Highlights

- Built an end-to-end web application test automation framework using Playwright, Python, and Pytest following the Page Object Model (POM).
- Automated functional and regression scenarios covering authentication, navigation, product sorting, cart operations, and checkout workflows.
- Implemented REST API and SQL database validation to verify API responses, data persistence, and backend state transitions.
- Integrated automated regression testing with GitHub Actions, including HTML reports and failure screenshots.

## 🔍 Key Engineering Practices

- Page Object Model (POM)
- Reusable Pytest fixtures
- Positive and negative test scenarios
- API response validation
- SQL backend validation
- Test parameterization
- CI/CD automation
- Failure screenshot capture

  ## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
