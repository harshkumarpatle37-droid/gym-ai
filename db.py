"""
Database utilities for the FitBot application.
Provides a connection context manager and helper functions so that
connection/commit/close boilerplate is written once.
"""

import sqlite3
from contextlib import contextmanager

import pandas as pd

from constants import DB_PATH


@contextmanager
def get_connection():
    """Yield a SQLite connection and close it when done."""
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()


def init_database():
    """Create the users table if it does not already exist.

    Returns True on success, False on failure.
    """
    try:
        with get_connection() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    height REAL NOT NULL,
                    weight REAL NOT NULL,
                    bmi REAL NOT NULL,
                    bmi_category TEXT NOT NULL,
                    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()
        return True
    except Exception:
        return False


def save_user_data(name, age, height, weight, bmi, bmi_category):
    """Insert a user record. Returns True on success, False on failure."""
    try:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO users (name, age, height, weight, bmi, bmi_category)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (name, age, height, weight, bmi, bmi_category),
            )
            conn.commit()
        return True
    except Exception:
        return False


def get_recent_users(limit=5):
    """Return a DataFrame of the most recent users, or None on error."""
    try:
        with get_connection() as conn:
            return pd.read_sql_query(
                "SELECT name, bmi, bmi_category FROM users ORDER BY id DESC LIMIT ?",
                conn,
                params=(limit,),
            )
    except Exception:
        return None
