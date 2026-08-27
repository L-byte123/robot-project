from dotenv import load_dotenv

from commands import CommandRouter
from config import BOT_NAME
from session_manager import SessionManager


def run():
    load_dotenv()
    router = CommandRouter(SessionManager())
    print(f"{BOT_NAME} 启动成功！")
    print("输入 /help 查看可用命令。")

    while True:
        user_input = input("你：").strip()
        if not user_input:
            continue
        result = router.dispatch(user_input)
        if result.should_exit:
            break
        if result.handled:
            continue
        print(f"{BOT_NAME}：{router.bot.ask(user_input)}")


if __name__ == "__main__":
    run()
