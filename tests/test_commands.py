from commands import CommandRouter


class FakeBot:
    def __init__(self, session_name):
        self.session_name = session_name
        self.history = []

    def get_history(self):
        return self.history

    def clear_history(self):
        self.history = []


def make_router(session_manager):
    output = []
    return CommandRouter(session_manager, FakeBot, output.append), output


def test_non_command_and_unknown_command(session_manager):
    router, output = make_router(session_manager)
    assert router.dispatch("你好").handled is False
    assert router.dispatch("/unknown").handled is True
    assert "未知命令" in output[-1]


def test_new_switch_list_and_delete(session_manager):
    router, output = make_router(session_manager)
    router.dispatch("/new python")
    router.dispatch("/new english")
    router.dispatch("/switch default")
    router.dispatch("/delete-session english")
    router.dispatch("/sessions")
    assert router.bot.session_name == "default"
    assert any("已删除会话：english" in line for line in output)
    assert any("python" in line for line in output)


def test_exit_requests_shutdown(session_manager):
    router, _ = make_router(session_manager)
    assert router.dispatch("/exit").should_exit is True
