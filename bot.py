import json
import os

from openai import OpenAI


class ChatBot:
    def __init__(self):
        self.client = OpenAI()
        self.history_file = "chat_history.json"
        self.messages = self.load_history()

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

    def ask(self, user_input):
        self.messages.append(
            {
                "role": "user",
                "content": user_input
            }
        )

        response = self.client.responses.create(
            model="gpt-5.4-mini",
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
    def clear_history(self):
    self.messages = []

    if os.path.exists(self.history_file):
        os.remove(self.history_file)