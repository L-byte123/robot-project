import pytest

from session_manager import SessionManager


@pytest.fixture
def database_file(tmp_path):
    return str(tmp_path / "test_robot.db")


@pytest.fixture
def session_manager(database_file):
    return SessionManager(database_file)
