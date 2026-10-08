"""Page Object Model package."""
from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

__all__ = [
    "BasePage",
    "LoginPage",
    "InventoryPage",
    "CartPage",
    "CheckoutPage",
]
