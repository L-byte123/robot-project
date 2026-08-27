from dataclasses import dataclass

from bot import ChatBot
from config import BOT_NAME


@dataclass
class CommandResult:
    handled: bool
    should_exit: bool = False


class CommandRouter:
    def __init__(self, session_manager, bot_factory=ChatBot, output=print):
        self.session_manager = session_manager
        self.bot_factory = bot_factory
        self.output = output
        self.bot = bot_factory(session_manager.current_session)

    def dispatch(self, user_input):
        if not user_input.startswith("/"):
            return CommandResult(False)
        command, _, argument = user_input.partition(" ")
        handler = {
            "/help": self._help, "/about": self._about, "/history": self._history,
            "/clear": self._clear, "/session": self._session, "/sessions": self._sessions,
            "/new": self._new, "/switch": self._switch,
            "/delete-session": self._delete_session, "/exit": self._exit,
        }.get(command)
        if handler is None:
            self.output(f"未知命令：{command}。输入 /help 查看可用命令。")
            return CommandResult(True)
        return handler(argument.strip())

    def _help(self, _):
        self.output("可用命令：\n/help  查看帮助\n/about  关于本程序\n/history  查看聊天记录\n/clear  清空聊天记录\n/session  查看当前会话\n/sessions  查看所有会话\n/new 会话名  新建并切换会话\n/switch 会话名  切换会话\n/delete-session 会话名  删除会话\n/exit  退出程序")
        return CommandResult(True)

    def _about(self, _):
        self.output(f"{BOT_NAME}\n这是一个使用 Python、OpenAI API 和 SQLite 开发的多会话命令行聊天机器人。")
        return CommandResult(True)

    def _history(self, _):
        history = self.bot.get_history()
        if not history:
            self.output(f"{BOT_NAME}：当前没有聊天记录。")
        else:
            self.output("----- 聊天记录 -----")
            for message in history:
                speaker = "你" if message["role"] == "user" else BOT_NAME
                self.output(f'{speaker}：{message["content"]}')
            self.output("--------------------")
        return CommandResult(True)

    def _clear(self, _):
        self.bot.clear_history()
        self.output(f"{BOT_NAME}：聊天记录已清空。")
        return CommandResult(True)

    def _session(self, _):
        self.output(f"当前会话：{self.session_manager.current_session}")
        return CommandResult(True)

    def _sessions(self, _):
        self.output("所有会话：")
        for session in self.session_manager.list_sessions():
            marker = "*" if session["name"] == self.session_manager.current_session else " "
            self.output(f'{marker} {session["name"]}（{session["message_count"]} 条消息）')
        return CommandResult(True)

    def _new(self, name):
        return self._change_session(name, True)

    def _switch(self, name):
        return self._change_session(name, False)

    def _change_session(self, name, create):
        try:
            if create:
                self.session_manager.create(name)
                action = "已创建并切换到"
            else:
                self.session_manager.switch(name)
                action = "已切换到"
            self.bot = self.bot_factory(self.session_manager.current_session)
            self.output(f"{action}会话：{self.session_manager.current_session}")
        except ValueError as error:
            self.output(str(error))
        return CommandResult(True)

    def _delete_session(self, name):
        try:
            self.session_manager.delete(name)
            self.output(f"已删除会话：{name}")
        except ValueError as error:
            self.output(str(error))
        return CommandResult(True)

    def _exit(self, _):
        self.output(f"{BOT_NAME}：再见！")
        return CommandResult(True, True)
