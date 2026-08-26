from dotenv import load_dotenv
from bot import ChatBot

load_dotenv()

bot = ChatBot()

print("AI 机器人启动成功！")

while True:
    user_input = input("你：")

    if user_input == "退出":
        print("机器人：再见！")
        break
    if user_input == "/clear":
       bot.clear_history()
       print("机器人：聊天记录已清空。")
       continue
    reply = bot.ask(user_input)

    print("机器人：", reply)