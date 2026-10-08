"""Centralized configuration for test automation framework."""
import os
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DB_FILE_PATH = os.path.join(PROJECT_ROOT, "test_automation.db")
SCREENSHOTS_DIR = os.path.join(PROJECT_ROOT, "screenshots")

# UI Automation Settings
UI_BASE_URL = "https://www.saucedemo.com"
DEFAULT_TIMEOUT_MS = 10000

# Test Credentials (SauceDemo test accounts)
STANDARD_USER = "standard_user"
LOCKED_OUT_USER = "locked_out_user"
PROBLEM_USER = "problem_user"
STANDARD_PASSWORD = "secret_sauce"
INVALID_PASSWORD = "wrong_password_123"

# REST API Automation Settings
API_BASE_URL = "https://jsonplaceholder.typicode.com"
API_TIMEOUT_SECONDS = 10
