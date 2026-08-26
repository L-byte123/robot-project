from openai import (
    OpenAI,
    APIConnectionError,
    AuthenticationError,
    RateLimitError,
    APIStatusError,
)

from config import MODEL_NAME, SYSTEM_PROMPT
from logger import get_logger
from storage import ChatStorage


logger = get_logger()


class ChatBot:
    def __init__(self):
        self.client = OpenAI()
        self.storage = ChatStorage()
        self.messages = self.storage.load()
        self.system_prompt = SYSTEM_PROMPT

    def ask(self, user_input):
        self.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        try:
            response = self.client.responses.create(
                model=MODEL_NAME,
                instructions=self.system_prompt,
                input=self.messages
            )

            logger.info("OpenAI API 请求成功")

            robot_reply = response.output_text

            self.messages.append(
                {
                    "role": "assistant",
                    "content": robot_reply
                }
            )

            self.storage.save(self.messages)

            return robot_reply

        except AuthenticationError:
            self.messages.pop()
            logger.error("OpenAI API 认证失败")
            return "API Key 无效，请检查 .env 文件。"

        except APIConnectionError:
            self.messages.pop()
            logger.error("OpenAI API 连接失败")
            return "无法连接到 AI 服务，请检查网络后重试。"

        except RateLimitError:
            self.messages.pop()
            logger.warning("OpenAI API 触发速率限制")
            return "请求过于频繁或当前 API 额度受限，请稍后再试。"

        except APIStatusError as error:
            self.messages.pop()

            logger.error(
                f"OpenAI API 状态错误：{error.status_code}"
            )

            return (
                f"AI 服务返回错误，"
                f"状态码：{error.status_code}"
            )

        except Exception:
            self.messages.pop()

            logger.exception("发生未知异常")

            return "程序发生未知错误，请稍后再试。"

    def get_history(self):
        return self.messages

    def clear_history(self):
        self.messages = []
        self.storage.clear()

        logger.info("聊天记录已清空")