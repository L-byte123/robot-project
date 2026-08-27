from dotenv import load_dotenv

from bot import ChatBot
from config import BOT_NAME


load_dotenv()

current_session = "default"
bot = ChatBot(current_session)

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

/help              查看帮助
/about             关于本程序
/history           查看聊天记录
/clear             清空聊天记录
/exit              退出程序
/session           查看当前会话
/new 会话名         新建并切换会话
/switch 会话名      切换会话
""")
        continue

    if user_input == "/about":
        print(f"""
{BOT_NAME}

这是一个使用 Python 和 OpenAI API 开发的聊天机器人。
支持连续对话、聊天记录、日志、配置系统、命令系统和多会话。
""")
        continue

    if user_input == "/session":
        print(f"当前会话：{current_session}")
        continue

    if user_input.startswith("/new "):
        session_name = user_input[5:].strip()

        if session_name == "":
            print("请输入会话名称。")
            continue

        current_session = session_name
        bot = ChatBot(current_session)

        print(f"已创建并切换到会话：{current_session}")
        continue

    if user_input.startswith("/switch "):
        session_name = user_input[8:].strip()

        if session_name == "":
            print("请输入会话名称。")
            continue

        current_session = session_name
        bot = ChatBot(current_session)

        print(f"已切换到会话：{current_session}")
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