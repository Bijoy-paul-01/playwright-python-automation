"""Pytest fixtures and test suite lifecycle hooks."""
import os
import pytest
from playwright.sync_api import Page
from config.config import (
    STANDARD_USER,
    STANDARD_PASSWORD,
    SCREENSHOTS_DIR,
)
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.api_client import APIClient
from utils.db_helper import DatabaseHelper

@pytest.fixture(scope="session")
def api() -> APIClient:
    """Fixture providing initialized REST API client for test session."""
    return APIClient()

@pytest.fixture(scope="function")
def db() -> DatabaseHelper:
    """Fixture providing an isolated in-memory database with schema & seeded data."""
    helper = DatabaseHelper(":memory:")
    helper.init_schema()
    helper.seed_test_data()
    yield helper
    helper.close()

@pytest.fixture
def login_page(page: Page) -> LoginPage:
    """Provides initialized LoginPage."""
    return LoginPage(page)

@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    """Provides initialized InventoryPage."""
    return InventoryPage(page)

@pytest.fixture
def cart_page(page: Page) -> CartPage:
    """Provides initialized CartPage."""
    return CartPage(page)

@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    """Provides initialized CheckoutPage."""
    return CheckoutPage(page)

@pytest.fixture
def authenticated_page(page: Page, login_page: LoginPage, inventory_page: InventoryPage) -> InventoryPage:
    """Logs into the application using standard credentials and returns the InventoryPage."""
    login_page.navigate()
    login_page.login(STANDARD_USER, STANDARD_PASSWORD)
    assert inventory_page.is_at_inventory_page(), "Failed to reach inventory page after login"
    return inventory_page

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Captures screenshot on UI test failure and saves to screenshots folder."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Check if test uses playwright 'page' fixture
        page = item.funcargs.get("page")
        if page:
            os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
            test_name = item.name.replace("/", "_").replace(":", "_")
            screenshot_path = os.path.join(SCREENSHOTS_DIR, f"failure_{test_name}.png")
            try:
                page.screenshot(path=screenshot_path)
            except Exception:
                pass
