"""Database Tests: SQL queries for backend data verification and integrity checks."""
import pytest
from utils.db_helper import DatabaseHelper

@pytest.mark.db
@pytest.mark.regression
def test_verify_seeded_user_accounts(db: DatabaseHelper):
    """
    Scenario: Verify initial database state for active test users.
    Expectation: Users table contains required accounts with correct statuses.
    """
    users = db.fetch_all("SELECT username, email, status FROM users WHERE status = ?", ("ACTIVE",))
    assert len(users) >= 2

    usernames = [u["username"] for u in users]
    assert "standard_user" in usernames
    assert "problem_user" in usernames

@pytest.mark.db
@pytest.mark.smoke
@pytest.mark.regression
def test_order_creation_and_sql_verification(db: DatabaseHelper):
    """
    Scenario: Simulate order creation following checkout and verify backend persistence.
    Expectation: Record is retrieved via SQL query with matching fields.
    """
    order_id = "ORD-TEST-999"
    username = "standard_user"
    amount = 59.98
    status = "COMPLETED"
    items_count = 2

    db.insert_order(order_id, username, amount, status, items_count)

    # SQL Backend Query Verification
    saved_order = db.get_order_by_id(order_id)
    assert saved_order is not None, "Order was not found in database"
    assert saved_order["order_id"] == order_id
    assert saved_order["username"] == username
    assert saved_order["amount"] == pytest.approx(59.98, 0.01)
    assert saved_order["status"] == "COMPLETED"
    assert saved_order["item_count"] == 2

@pytest.mark.db
@pytest.mark.regression
def test_update_order_status_sql_verification(db: DatabaseHelper):
    """
    Scenario: Update order lifecycle state and verify database update.
    Expectation: Status changes from PENDING to DELIVERED.
    """
    target_order_id = "ORD-1002"

    initial_order = db.get_order_by_id(target_order_id)
    assert initial_order["status"] == "PENDING"

    db.update_order_status(target_order_id, "DELIVERED")

    updated_order = db.get_order_by_id(target_order_id)
    assert updated_order["status"] == "DELIVERED"

@pytest.mark.db
@pytest.mark.regression
def test_user_order_summary_aggregate_query(db: DatabaseHelper):
    """
    Scenario: Execute SQL aggregate query (COUNT, SUM) for customer order history.
    Expectation: Summary accurately reflects customer order count and total spend.
    """
    # standard_user has ORD-1001 ($29.99) and ORD-1002 ($49.99) initially
    summary = db.get_user_order_summary("standard_user")

    assert summary["total_orders"] == 2
    assert summary["total_spent"] == pytest.approx(79.98, 0.01)

@pytest.mark.db
@pytest.mark.regression
def test_query_non_existent_order_returns_none(db: DatabaseHelper):
    """
    Negative Scenario: Query for non-existent order.
    Expectation: Returns None without raising unhandled errors.
    """
    result = db.get_order_by_id("NON-EXISTENT-ID")
    assert result is None
