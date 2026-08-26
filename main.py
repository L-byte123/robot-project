from dotenv import load_dotenv

from bot import ChatBot
from config import BOT_NAME


load_dotenv()

bot = ChatBot()

print(f"{BOT_NAME} 启动成功！")
print("输入 /help 查看可用命令。")


while True:
    user_input = input("你：").strip()

    if user_input == "/exit":
        print(f"{BOT_NAME}：再见！")
        break

    if user_input == "/help":
        print("""
可用命令：

/help      查看帮助
/history   查看聊天记录
/clear     清空聊天记录
/exit      退出程序
""")
        continue

    if user_input == "/history":
        history = bot.get_history()

        if not history:
            print(f"{BOT_NAME}：当前没有聊天记录。")
            continue

        print("----- 聊天记录 -----")

        for message in history:
            role = message["role"]
            content = message["content"]

            if role == "user":
                print("你：", content)

            elif role == "assistant":
                print(f"{BOT_NAME}：{content}")

        print("--------------------")
        continue

    if user_input == "/clear":
        bot.clear_history()
        print(f"{BOT_NAME}：聊天记录已清空。")
        continue

    if user_input == "":
        continue

    reply = bot.ask(user_input)

    print(f"{BOT_NAME}：{reply}")