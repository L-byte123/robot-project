from openai import OpenAI


class ChatBot:
    def __init__(self):
        self.client = OpenAI()
        self.messages = []

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

        return robot_reply