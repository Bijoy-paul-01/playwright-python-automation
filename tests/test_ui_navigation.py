"""UI Tests: Catalog navigation, product sorting, and sidebar logout."""
import pytest
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

@pytest.mark.ui
@pytest.mark.regression
def test_product_sorting_alphabetical(authenticated_page: InventoryPage):
    """
    Scenario: Verify product sorting by name (A to Z) and (Z to A).
    Expectation: Item titles reflect expected alphabetical ordering.
    """
    inventory_page = authenticated_page

    # Sort A to Z
    inventory_page.sort_products("az")
    items_az = inventory_page.get_all_item_names()
    assert items_az == sorted(items_az), "Items are not sorted A to Z"

    # Sort Z to A
    inventory_page.sort_products("za")
    items_za = inventory_page.get_all_item_names()
    assert items_za == sorted(items_az, reverse=True), "Items are not sorted Z to A"

@pytest.mark.ui
@pytest.mark.regression
def test_product_sorting_by_price(authenticated_page: InventoryPage):
    """
    Scenario: Verify product sorting by price (Low to High and High to Low).
    Expectation: Item prices reflect strictly ordered numerical values.
    """
    inventory_page = authenticated_page

    # Sort Price: Low to High
    inventory_page.sort_products("lohi")
    prices_lohi = inventory_page.get_all_item_prices()
    assert prices_lohi == sorted(prices_lohi), "Prices are not sorted low to high"

    # Sort Price: High to Low
    inventory_page.sort_products("hilo")
    prices_hilo = inventory_page.get_all_item_prices()
    assert prices_hilo == sorted(prices_lohi, reverse=True), "Prices are not sorted high to low"

@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.smoke
def test_sidebar_logout_navigation(authenticated_page: InventoryPage, login_page: LoginPage):
    """
    Scenario: Verify user can log out via hamburger menu.
    Expectation: User is redirected back to the login page and session is terminated.
    """
    inventory_page = authenticated_page
    inventory_page.logout()

    assert "/inventory.html" not in login_page.get_url()
    assert login_page.is_visible(login_page.LOGIN_BUTTON)
