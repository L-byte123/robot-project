from types import SimpleNamespace

import bot as bot_module


class FakeOpenAI:
    def __init__(self):
        self.responses = SimpleNamespace(
            create=lambda **kwargs: SimpleNamespace(output_text="模拟回复")
        )


def test_ask_uses_mock_api_and_saves_messages(monkeypatch, database_file):
    monkeypatch.setattr(bot_module, "OpenAI", FakeOpenAI)
    monkeypatch.setattr("storage.DATABASE_FILE", database_file)
    chatbot = bot_module.ChatBot("test")

    assert chatbot.ask("你好") == "模拟回复"
    assert chatbot.storage.load() == [
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "模拟回复"},
    ]
