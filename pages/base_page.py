"""Base Page class encapsulating shared web interactions and helper utilities."""
import os
from playwright.sync_api import Page, Locator, expect
from config.config import DEFAULT_TIMEOUT_MS, SCREENSHOTS_DIR

class BasePage:
    """Base class for all Page Objects in the framework."""

    def __init__(self, page: Page):
        self.page = page
        self.default_timeout = DEFAULT_TIMEOUT_MS

    def navigate(self, url: str) -> None:
        """Navigates to the specified URL."""
        self.page.goto(url, timeout=self.default_timeout)

    def get_url(self) -> str:
        """Returns the current page URL."""
        return self.page.url

    def get_title(self) -> str:
        """Returns the current page title."""
        return self.page.title()

    def wait_for_selector(self, selector: str, state: str = "visible") -> Locator:
        """Waits for an element to match the given state (attached, detached, visible, hidden)."""
        locator = self.page.locator(selector)
        locator.wait_for(state=state, timeout=self.default_timeout)
        return locator

    def click_element(self, selector: str) -> None:
        """Waits for and clicks an element."""
        self.page.locator(selector).click(timeout=self.default_timeout)

    def fill_input(self, selector: str, value: str) -> None:
        """Clears and fills an input field with the provided string."""
        self.page.locator(selector).fill(value, timeout=self.default_timeout)

    def get_text(self, selector: str) -> str:
        """Gets inner text of an element."""
        return self.page.locator(selector).inner_text(timeout=self.default_timeout)

    def is_visible(self, selector: str, timeout: int = 5000) -> bool:
        """Checks if an element is visible on the page within the specified timeout."""
        try:
            self.page.locator(selector).wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False

    def take_screenshot(self, filename: str) -> str:
        """Captures a screenshot and saves it to the screenshots directory."""
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        file_path = os.path.join(SCREENSHOTS_DIR, filename)
        self.page.screenshot(path=file_path)
        return file_path
