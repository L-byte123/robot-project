from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

print("AI 机器人启动成功！")

messages = []

while True:
    user_input = input("你：")

    if user_input == "退出":
        print("机器人：再见！")
        break

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    response = client.responses.create(
        model="gpt-5.4-mini",
        input=messages
    )

    robot_reply = response.output_text

    print("机器人：", robot_reply)

    messages.append(
        {
            "role": "assistant",
            "content": robot_reply
        }
    )