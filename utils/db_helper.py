"""SQLite Database Helper for backend data verification and query execution."""
import sqlite3
from typing import Any, Dict, List, Optional, Tuple

class DatabaseHelper:
    """Provides reusable database operations and SQL assertions."""

    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def init_schema(self) -> None:
        """Initializes tables for e-commerce testing: users and orders."""
        self.cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT NOT NULL,
                status TEXT DEFAULT 'ACTIVE'
            );

            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                amount REAL NOT NULL,
                status TEXT NOT NULL,
                item_count INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES users(username)
            );
            """
        )
        self.connection.commit()

    def seed_test_data(self) -> None:
        """Seeds baseline accounts and orders."""
        users_data = [
            ("standard_user", "standard@example.com", "ACTIVE"),
            ("locked_out_user", "locked@example.com", "LOCKED"),
            ("problem_user", "problem@example.com", "ACTIVE"),
        ]
        self.cursor.executemany(
            "INSERT OR IGNORE INTO users (username, email, status) VALUES (?, ?, ?)",
            users_data,
        )

        orders_data = [
            ("ORD-1001", "standard_user", 29.99, "COMPLETED"),
            ("ORD-1002", "standard_user", 49.99, "PENDING"),
            ("ORD-1003", "problem_user", 15.50, "CANCELLED"),
        ]
        self.cursor.executemany(
            "INSERT OR IGNORE INTO orders (order_id, username, amount, status, item_count) VALUES (?, ?, ?, ?, 1)",
            orders_data,
        )
        self.connection.commit()

    def execute_query(self, query: str, params: Tuple = ()) -> None:
        """Executes DDL/DML query (INSERT, UPDATE, DELETE)."""
        self.cursor.execute(query, params)
        self.connection.commit()

    def fetch_one(self, query: str, params: Tuple = ()) -> Optional[Dict[str, Any]]:
        """Executes SELECT query and returns a single row as a dictionary."""
        self.cursor.execute(query, params)
        row = self.cursor.fetchone()
        return dict(row) if row else None

    def fetch_all(self, query: str, params: Tuple = ()) -> List[Dict[str, Any]]:
        """Executes SELECT query and returns all matching rows as dictionaries."""
        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        return [dict(r) for r in rows]

    def insert_order(
        self, order_id: str, username: str, amount: float, status: str, item_count: int
    ) -> None:
        """Inserts a new order record."""
        query = """
            INSERT INTO orders (order_id, username, amount, status, item_count)
            VALUES (?, ?, ?, ?, ?)
        """
        self.execute_query(query, (order_id, username, amount, status, item_count))

    def get_order_by_id(self, order_id: str) -> Optional[Dict[str, Any]]:
        """Fetches an order by its unique order_id."""
        query = "SELECT * FROM orders WHERE order_id = ?"
        return self.fetch_one(query, (order_id,))

    def update_order_status(self, order_id: str, new_status: str) -> None:
        """Updates the status of an existing order."""
        query = "UPDATE orders SET status = ? WHERE order_id = ?"
        self.execute_query(query, (new_status, order_id))

    def get_user_order_summary(self, username: str) -> Dict[str, Any]:
        """Runs aggregate SQL calculation for total orders and total spent by user."""
        query = """
            SELECT 
                COUNT(*) as total_orders, 
                COALESCE(SUM(amount), 0.0) as total_spent 
            FROM orders 
            WHERE username = ?
        """
        return self.fetch_one(query, (username,)) or {"total_orders": 0, "total_spent": 0.0}

    def close(self) -> None:
        """Closes the active database connection."""
        self.connection.close()
