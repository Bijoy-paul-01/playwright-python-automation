"""Page Object for SauceDemo Inventory (Products) Page."""
import re
from typing import List
from playwright.sync_api import Page
from pages.base_page import BasePage

class InventoryPage(BasePage):
    """Encapsulates catalog viewing, sorting, adding to cart, and navigation."""

    # Locators
    TITLE = ".title"
    INVENTORY_ITEMS = ".inventory_item"
    ITEM_NAMES = ".inventory_item_name"
    ITEM_PRICES = ".inventory_item_price"
    SHOPPING_CART_LINK = ".shopping_cart_link"
    SHOPPING_CART_BADGE = ".shopping_cart_badge"
    SORT_CONTAINER = "[data-test='product-sort-container']"
    MENU_BUTTON = "#react-burger-menu-btn"
    LOGOUT_LINK = "#logout_sidebar_link"

    def __init__(self, page: Page):
        super().__init__(page)

    def is_at_inventory_page(self) -> bool:
        """Returns True if the user is currently on the inventory page."""
        try:
            self.page.wait_for_url("**/inventory.html", timeout=self.default_timeout)
            return self.is_visible(self.TITLE)
        except Exception:
            return False

    def get_item_count(self) -> int:
        """Returns the total number of products displayed in the catalog."""
        return self.page.locator(self.INVENTORY_ITEMS).count()

    def get_all_item_names(self) -> List[str]:
        """Returns a list of all product names visible on the page."""
        return self.page.locator(self.ITEM_NAMES).all_inner_texts()

    def get_all_item_prices(self) -> List[float]:
        """Returns a list of all product prices as floats."""
        raw_prices = self.page.locator(self.ITEM_PRICES).all_inner_texts()
        cleaned_prices = []
        for p in raw_prices:
            numeric_val = re.sub(r"[^\d.]", "", p)
            cleaned_prices.append(float(numeric_val))
        return cleaned_prices

    def add_item_to_cart_by_name(self, product_name: str) -> None:
        """Finds a product card by name and clicks its Add to Cart button."""
        # Find item card that has the text
        item_card = self.page.locator(self.INVENTORY_ITEMS).filter(has_text=product_name)
        item_card.locator("button[id^='add-to-cart']").click()

    def remove_item_from_cart_by_name(self, product_name: str) -> None:
        """Finds a product card by name and clicks its Remove button."""
        item_card = self.page.locator(self.INVENTORY_ITEMS).filter(has_text=product_name)
        item_card.locator("button[id^='remove']").click()

    def get_cart_item_count(self) -> int:
        """Returns the number shown on the cart badge, or 0 if badge is not present."""
        badge = self.page.locator(self.SHOPPING_CART_BADGE)
        if badge.count() > 0 and badge.is_visible():
            text = badge.inner_text()
            return int(text) if text.isdigit() else 0
        return 0

    def go_to_cart(self) -> None:
        """Clicks the shopping cart badge icon to open the Cart page."""
        self.click_element(self.SHOPPING_CART_LINK)

    def sort_products(self, sort_value: str) -> None:
        """
        Selects a sorting option from dropdown.
        Options:
            'az'   - Name (A to Z)
            'za'   - Name (Z to A)
            'lohi' - Price (low to high)
            'hilo' - Price (high to low)
        """
        self.page.locator(self.SORT_CONTAINER).select_option(sort_value)

    def logout(self) -> None:
        """Opens hamburger sidebar and clicks Logout."""
        self.click_element(self.MENU_BUTTON)
        # Wait for sidebar animation
        self.wait_for_selector(self.LOGOUT_LINK, state="visible")
        self.click_element(self.LOGOUT_LINK)
