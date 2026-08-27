import json
import os

from logger import get_logger


logger = get_logger()


class ChatStorage:
    def __init__(self, session_name):
        self.session_name = session_name
        self.history_file = f"chat_history_{session_name}.json"

    def load(self):
        if not os.path.exists(self.history_file):
            return []

        try:
            with open(
                self.history_file,
                "r",
                encoding="utf-8"
            ) as file:
                return json.load(file)

        except Exception:
            logger.exception("读取聊天记录失败")
            return []

    def save(self, messages):
        try:
            with open(
                self.history_file,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    messages,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

        except Exception:
            logger.exception("保存聊天记录失败")

    def clear(self):
        if os.path.exists(self.history_file):
            try:
                os.remove(self.history_file)

            except Exception:
                logger.exception("删除聊天记录失败")