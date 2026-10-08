"""Page Object for SauceDemo Checkout Flows (Information, Overview, Complete)."""
from playwright.sync_api import Page
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    """Encapsulates multi-step checkout form submissions, validation, and confirmation."""

    # Step One Locators
    FIRST_NAME_INPUT = "#first-name"
    LAST_NAME_INPUT = "#last-name"
    POSTAL_CODE_INPUT = "#postal-code"
    CONTINUE_BUTTON = "#continue"
    ERROR_CONTAINER = "[data-test='error']"
    CANCEL_BUTTON = "#cancel"

    # Step Two Locators (Overview)
    SUMMARY_SUBTOTAL = ".summary_subtotal_label"
    SUMMARY_TAX = ".summary_tax_label"
    SUMMARY_TOTAL = ".summary_total_label"
    FINISH_BUTTON = "#finish"

    # Complete Step Locators
    COMPLETE_HEADER = ".complete-header"
    COMPLETE_TEXT = ".complete-text"
    BACK_HOME_BUTTON = "#back-to-products"

    def __init__(self, page: Page):
        super().__init__(page)

    def fill_shipping_information(
        self, first_name: str = "", last_name: str = "", postal_code: str = ""
    ) -> None:
        """Fills out the shipping information form."""
        if first_name:
            self.fill_input(self.FIRST_NAME_INPUT, first_name)
        else:
            self.page.locator(self.FIRST_NAME_INPUT).clear()

        if last_name:
            self.fill_input(self.LAST_NAME_INPUT, last_name)
        else:
            self.page.locator(self.LAST_NAME_INPUT).clear()

        if postal_code:
            self.fill_input(self.POSTAL_CODE_INPUT, postal_code)
        else:
            self.page.locator(self.POSTAL_CODE_INPUT).clear()

    def continue_checkout(self) -> None:
        """Clicks the Continue button to proceed to the overview page."""
        self.click_element(self.CONTINUE_BUTTON)

    def get_error_message(self) -> str:
        """Returns the form validation error message if visible."""
        return self.get_text(self.ERROR_CONTAINER)

    def get_summary_total(self) -> str:
        """Returns the total amount string from the checkout overview page."""
        return self.get_text(self.SUMMARY_TOTAL)

    def finish_checkout(self) -> None:
        """Clicks the Finish button to place the order."""
        self.click_element(self.FINISH_BUTTON)

    def get_complete_header(self) -> str:
        """Returns the order completion confirmation banner text."""
        return self.get_text(self.COMPLETE_HEADER)

    def is_checkout_complete(self) -> bool:
        """Checks if the checkout complete screen is displayed."""
        try:
            self.page.wait_for_url("**/checkout-complete.html", timeout=self.default_timeout)
            return self.is_visible(self.COMPLETE_HEADER)
        except Exception:
            return False
