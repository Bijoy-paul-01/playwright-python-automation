"""UI Tests: Shopping cart interactions and End-to-End Checkout workflows."""
import pytest
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

PRODUCT_NAME_1 = "Sauce Labs Backpack"
PRODUCT_NAME_2 = "Sauce Labs Bike Light"

@pytest.mark.ui
@pytest.mark.regression
def test_add_and_remove_products_cart_badge(
    authenticated_page: InventoryPage, cart_page: CartPage
):
    """
    Scenario: Verify adding and removing items properly updates the cart badge.
    Expectation: Cart counter increments on add and decrements/disappears on remove.
    """
    inventory_page = authenticated_page

    # Add items
    inventory_page.add_item_to_cart_by_name(PRODUCT_NAME_1)
    assert inventory_page.get_cart_item_count() == 1

    inventory_page.add_item_to_cart_by_name(PRODUCT_NAME_2)
    assert inventory_page.get_cart_item_count() == 2

    # Remove item from catalog
    inventory_page.remove_item_from_cart_by_name(PRODUCT_NAME_2)
    assert inventory_page.get_cart_item_count() == 1

    # Remove remaining item from cart page
    inventory_page.go_to_cart()
    assert cart_page.is_at_cart_page()
    assert PRODUCT_NAME_1 in cart_page.get_cart_item_names()

    cart_page.remove_item_by_name(PRODUCT_NAME_1)
    assert inventory_page.get_cart_item_count() == 0

@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.regression
def test_end_to_end_checkout_success(
    authenticated_page: InventoryPage,
    cart_page: CartPage,
    checkout_page: CheckoutPage,
):
    """
    Scenario: Complete positive checkout flow from product selection to purchase order confirmation.
    Expectation: Order completes successfully with confirmation header.
    """
    inventory_page = authenticated_page

    # 1. Add product to cart
    inventory_page.add_item_to_cart_by_name(PRODUCT_NAME_1)
    assert inventory_page.get_cart_item_count() == 1

    # 2. Open cart and proceed to checkout
    inventory_page.go_to_cart()
    cart_page.proceed_to_checkout()

    # 3. Fill customer details (Step One)
    checkout_page.fill_shipping_information(
        first_name="Jane",
        last_name="Doe",
        postal_code="94105",
    )
    checkout_page.continue_checkout()

    # 4. Overview validation (Step Two)
    summary_total = checkout_page.get_summary_total()
    assert "Total: $" in summary_total

    # 5. Finish order
    checkout_page.finish_checkout()
    assert checkout_page.is_checkout_complete()
    assert "Thank you for your order!" in checkout_page.get_complete_header()

@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize(
    "first_name,last_name,postal_code,expected_error",
    [
        ("", "Doe", "94105", "First Name is required"),
        ("Jane", "", "94105", "Last Name is required"),
        ("Jane", "Doe", "", "Postal Code is required"),
    ],
    ids=["missing_first_name", "missing_last_name", "missing_postal_code"],
)
def test_checkout_form_negative_scenarios(
    authenticated_page: InventoryPage,
    cart_page: CartPage,
    checkout_page: CheckoutPage,
    first_name: str,
    last_name: str,
    postal_code: str,
    expected_error: str,
):
    """
    Scenario: Negative form submission tests during checkout step one.
    Expectation: Form displays appropriate field validation errors.
    """
    inventory_page = authenticated_page
    inventory_page.add_item_to_cart_by_name(PRODUCT_NAME_1)
    inventory_page.go_to_cart()
    cart_page.proceed_to_checkout()

    checkout_page.fill_shipping_information(first_name, last_name, postal_code)
    checkout_page.continue_checkout()

    assert expected_error in checkout_page.get_error_message()
