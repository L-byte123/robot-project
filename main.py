from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

print("AI 机器人启动成功！")

while True:
    user_input = input("你：")

    if user_input == "退出":
        print("机器人：再见！")
        break

    response = client.responses.create(
        model="gpt-5.4-mini",
        input=user_input
    )

    print("机器人：", response.output_text)