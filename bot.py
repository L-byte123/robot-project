import json
import os

from openai import (
    OpenAI,
    APIConnectionError,
    AuthenticationError,
    RateLimitError,
    APIStatusError,
)


class ChatBot:
    def __init__(self):
        self.client = OpenAI()
        self.history_file = "chat_history.json"
        self.messages = self.load_history()

        self.system_prompt = """
你是一个耐心的 Python 学习助手。
回答尽量清楚。
遇到代码时要解释每一部分的作用。
"""

    def load_history(self):
        if not os.path.exists(self.history_file):
            return []

        with open(self.history_file, "r", encoding="utf-8") as file:
            return json.load(file)

    def save_history(self):
        with open(self.history_file, "w", encoding="utf-8") as file:
            json.dump(
                self.messages,
                file,
                ensure_ascii=False,
                indent=4
            )

    def get_history(self):
        return self.messages

    def clear_history(self):
        self.messages = []

        if os.path.exists(self.history_file):
            os.remove(self.history_file)

    def ask(self, user_input):
        self.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        try:
            response = self.client.responses.create(
                model="gpt-5.4-mini",
                instructions=self.system_prompt,
                input=self.messages
            )

            robot_reply = response.output_text

            self.messages.append(
                {
                    "role": "assistant",
                    "content": robot_reply
                }
            )

            self.save_history()

            return robot_reply

        except AuthenticationError:
            self.messages.pop()
            return "API Key 无效，请检查 .env 文件中的 OPENAI_API_KEY。"

        except APIConnectionError:
            self.messages.pop()
            return "无法连接到 AI 服务，请检查网络后重试。"

        except RateLimitError:
            self.messages.pop()
            return "请求过于频繁或当前 API 额度受限，请稍后再试。"

        except APIStatusError as error:
            self.messages.pop()
            return f"AI 服务返回错误，状态码：{error.status_code}"

        except Exception as error:
            self.messages.pop()
            return f"发生了未知错误：{error}"