"""Page Object for SauceDemo Shopping Cart Page."""
from typing import List
from playwright.sync_api import Page
from pages.base_page import BasePage

class CartPage(BasePage):
    """Encapsulates Cart view, item verification, item removal, and proceeding to checkout."""

    CART_ITEMS = ".cart_item"
    ITEM_NAMES = ".inventory_item_name"
    CHECKOUT_BUTTON = "#checkout"
    CONTINUE_SHOPPING_BUTTON = "#continue-shopping"

    def __init__(self, page: Page):
        super().__init__(page)

    def is_at_cart_page(self) -> bool:
        """Returns True if current URL is the cart page."""
        try:
            self.page.wait_for_url("**/cart.html", timeout=self.default_timeout)
            return True
        except Exception:
            return False

    def get_cart_item_names(self) -> List[str]:
        """Returns the names of all items in the cart."""
        return self.page.locator(self.ITEM_NAMES).all_inner_texts()

    def remove_item_by_name(self, product_name: str) -> None:
        """Removes a specific product from the cart by name."""
        item = self.page.locator(self.CART_ITEMS).filter(has_text=product_name)
        item.locator("button[id^='remove']").click()

    def proceed_to_checkout(self) -> None:
        """Clicks the Checkout button to begin the checkout process."""
        self.click_element(self.CHECKOUT_BUTTON)

    def continue_shopping(self) -> None:
        """Clicks Continue Shopping to return to the catalog."""
        self.click_element(self.CONTINUE_SHOPPING_BUTTON)
