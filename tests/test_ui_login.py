"""UI Tests: Positive and Negative Login scenarios."""
import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config.config import (
    STANDARD_USER,
    LOCKED_OUT_USER,
    STANDARD_PASSWORD,
    INVALID_PASSWORD,
)

@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.regression
def test_successful_login(login_page: LoginPage, inventory_page: InventoryPage):
    """
    Scenario: Verify valid user can log in successfully.
    Expectation: User is redirected to the products inventory page.
    """
    login_page.navigate()
    login_page.login(STANDARD_USER, STANDARD_PASSWORD)

    assert inventory_page.is_at_inventory_page()
    assert inventory_page.get_item_count() > 0

@pytest.mark.ui
@pytest.mark.regression
def test_login_locked_out_user(login_page: LoginPage):
    """
    Scenario: Verify locked out user cannot log in.
    Expectation: Error banner displays locked out message.
    """
    login_page.navigate()
    login_page.login(LOCKED_OUT_USER, STANDARD_PASSWORD)

    assert login_page.is_error_displayed()
    assert "Sorry, this user has been locked out." in login_page.get_error_message()

@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize(
    "username,password,expected_error",
    [
        ("", STANDARD_PASSWORD, "Username is required"),
        (STANDARD_USER, "", "Password is required"),
        ("", "", "Username is required"),
        (STANDARD_USER, INVALID_PASSWORD, "Username and password do not match"),
        ("invalid_user_99", STANDARD_PASSWORD, "Username and password do not match"),
    ],
    ids=[
        "empty_username",
        "empty_password",
        "empty_credentials",
        "incorrect_password",
        "non_existent_username",
    ],
)
def test_login_negative_validation_errors(
    login_page: LoginPage, username: str, password: str, expected_error: str
):
    """
    Scenario: Parameterized negative tests for missing or incorrect credentials.
    Expectation: Appropriate validation error messages are displayed.
    """
    login_page.navigate()
    login_page.login(username, password)

    assert login_page.is_error_displayed()
    assert expected_error in login_page.get_error_message()
