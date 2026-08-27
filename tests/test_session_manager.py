import pytest

from storage import ChatStorage


def test_create_switch_and_list_sessions(session_manager):
    session_manager.create("python")
    session_manager.switch("default")
    assert {item["name"] for item in session_manager.list_sessions()} == {"default", "python"}


def test_delete_session_cascades_messages(session_manager, database_file):
    session_manager.create("temporary")
    ChatStorage("temporary", database_file).save_message("user", "test")
    session_manager.switch("default")
    session_manager.delete("temporary")
    assert {item["name"] for item in session_manager.list_sessions()} == {"default"}


def test_invalid_session_operations(session_manager):
    with pytest.raises(ValueError, match="不能删除当前会话"):
        session_manager.delete("default")
    with pytest.raises(ValueError, match="会话不存在"):
        session_manager.switch("missing")
