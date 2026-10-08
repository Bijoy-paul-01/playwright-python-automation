"""Page Object for SauceDemo Login Page."""
from playwright.sync_api import Page
from config.config import UI_BASE_URL
from pages.base_page import BasePage

class LoginPage(BasePage):
    """Encapsulates locators and user actions on the Login page."""

    # Locators
    USERNAME_INPUT = "#user-name"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_CONTAINER = "[data-test='error']"
    ERROR_BUTTON = ".error-button"

    def __init__(self, page: Page):
        super().__init__(page)

    def navigate(self) -> None:
        """Navigates directly to the login page."""
        super().navigate(UI_BASE_URL)

    def login(self, username: str = "", password: str = "") -> None:
        """Enters credentials and clicks the login button."""
        if username:
            self.fill_input(self.USERNAME_INPUT, username)
        else:
            self.page.locator(self.USERNAME_INPUT).clear()

        if password:
            self.fill_input(self.PASSWORD_INPUT, password)
        else:
            self.page.locator(self.PASSWORD_INPUT).clear()

        self.click_element(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        """Returns the text of the displayed validation error banner."""
        return self.get_text(self.ERROR_CONTAINER)

    def is_error_displayed(self) -> bool:
        """Checks if the error banner is currently visible."""
        return self.is_visible(self.ERROR_CONTAINER)
