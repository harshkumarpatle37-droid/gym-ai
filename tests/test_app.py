"""Tests for the app module's database functions."""

import os
import sqlite3
import pytest


# We need to test init_database and save_user_data without running Streamlit.
# These functions use st.error internally, so we mock streamlit.
@pytest.fixture(autouse=True)
def test_db(tmp_path, monkeypatch):
    """Use a temporary database for each test."""
    db_path = str(tmp_path / "test_gym.db")
    monkeypatch.chdir(tmp_path)
    yield db_path


@pytest.fixture
def mock_streamlit(monkeypatch):
    """Mock streamlit functions used in app.py."""
    import types

    mock_st = types.ModuleType("streamlit")
    mock_st.error = lambda msg: None
    mock_st.success = lambda msg: None
    mock_st.stop = lambda: None
    mock_st.set_page_config = lambda **kwargs: None
    mock_st.markdown = lambda *args, **kwargs: None
    mock_st.columns = lambda x: (None, None)
    monkeypatch.setitem(__import__("sys").modules, "streamlit", mock_st)


class TestInitDatabase:
    """Tests for init_database function."""

    def test_creates_database_file(self, mock_streamlit, test_db):
        from app import init_database

        result = init_database()
        assert result is True
        assert os.path.exists("gym.db")

    def test_creates_users_table(self, mock_streamlit, test_db):
        from app import init_database

        init_database()
        conn = sqlite3.connect("gym.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
        )
        table = cursor.fetchone()
        conn.close()
        assert table is not None
        assert table[0] == "users"

    def test_users_table_has_correct_columns(self, mock_streamlit, test_db):
        from app import init_database

        init_database()
        conn = sqlite3.connect("gym.db")
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(users)")
        columns = {row[1] for row in cursor.fetchall()}
        conn.close()
        expected = {"id", "name", "age", "height", "weight", "bmi", "bmi_category", "created_date"}
        assert columns == expected

    def test_idempotent_init(self, mock_streamlit, test_db):
        from app import init_database

        assert init_database() is True
        assert init_database() is True

    def test_returns_true_on_success(self, mock_streamlit, test_db):
        from app import init_database

        assert init_database() is True


class TestSaveUserData:
    """Tests for save_user_data function."""

    def test_saves_user_data(self, mock_streamlit, test_db):
        from app import init_database, save_user_data

        init_database()
        result = save_user_data("Alice", 25, 170.0, 65.0, 22.5, "Normal Weight")
        assert result is True

    def test_data_persisted_in_db(self, mock_streamlit, test_db):
        from app import init_database, save_user_data

        init_database()
        save_user_data("Bob", 30, 180.0, 85.0, 26.2, "Overweight")
        conn = sqlite3.connect("gym.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, age, height, weight, bmi, bmi_category FROM users")
        row = cursor.fetchone()
        conn.close()
        assert row == ("Bob", 30, 180.0, 85.0, 26.2, "Overweight")

    def test_multiple_users_saved(self, mock_streamlit, test_db):
        from app import init_database, save_user_data

        init_database()
        save_user_data("Alice", 25, 170.0, 65.0, 22.5, "Normal Weight")
        save_user_data("Bob", 30, 180.0, 85.0, 26.2, "Overweight")
        save_user_data("Charlie", 40, 165.0, 100.0, 36.7, "Obese")
        conn = sqlite3.connect("gym.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        conn.close()
        assert count == 3

    def test_auto_increment_id(self, mock_streamlit, test_db):
        from app import init_database, save_user_data

        init_database()
        save_user_data("Alice", 25, 170.0, 65.0, 22.5, "Normal Weight")
        save_user_data("Bob", 30, 180.0, 85.0, 26.2, "Overweight")
        conn = sqlite3.connect("gym.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users ORDER BY id")
        ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        assert ids == [1, 2]

    def test_returns_true_on_success(self, mock_streamlit, test_db):
        from app import init_database, save_user_data

        init_database()
        result = save_user_data("Test", 20, 160.0, 55.0, 21.5, "Normal Weight")
        assert result is True
