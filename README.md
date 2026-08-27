
# Robot Project

一个使用 Python 和 OpenAI API 开发的命令行 AI 聊天机器人。

## 项目介绍

Robot Project 是一个用于学习 Python 和软件工程开发流程的 AI 聊天机器人项目。

项目涵盖：

- Python
- OpenAI API
- Git
- GitHub
- 多会话聊天
- 文件存储
- 配置管理
- 日志系统
- 自动测试
- Git 分支与 Pull Request

## 功能

- AI 对话
- 连续聊天记忆
- 多会话聊天
- 聊天记录持久化
- API 异常处理
- 日志系统
- 配置系统
- 命令系统
- pytest 自动测试

## 项目结构

```text
robot-project/
├── main.py
├── bot.py
├── storage.py
├── config.py
├── logger.py
├── requirements.txt
├── tests/
│   └── test_storage.py
├── .gitignore
└── README.md
```

### 文件说明

- `main.py`：程序入口，负责用户输入和命令处理。
- `bot.py`：负责 AI 对话和 OpenAI API 调用。
- `storage.py`：负责聊天记录的读取、保存和删除。
- `config.py`：保存机器人名称、模型名称和系统提示词。
- `logger.py`：负责日志系统。
- `requirements.txt`：Python 依赖列表。
- `tests/`：自动测试代码。

## 环境要求

- Python 3.10+
- Git
- OpenAI API Key

## 安装

### 1. 克隆项目

```bash
git clone 你的GitHub仓库地址
```

进入项目目录：

```bash
cd robot-project
```

### 2. 创建虚拟环境

```bash
python -m venv .venv
```

Windows CMD：

```bash
.venv\Scripts\activate.bat
```

Windows PowerShell：

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. 安装依赖

```bash
python -m pip install -r requirements.txt
```

### 4. 配置 API Key

在项目根目录创建：

```text
.env
```

内容：

```text
OPENAI_API_KEY=你的_API_Key
```

**不要把 `.env` 上传到 GitHub。**

## 运行

```bash
python main.py
```

正常启动后：

```text
小智 启动成功！
输入 /help 查看可用命令。
```

## 命令

| 命令 | 功能 |
|---|---|
| `/help` | 查看帮助 |
| `/about` | 查看机器人信息 |
| `/history` | 查看聊天记录 |
| `/clear` | 清空聊天记录 |
| `/session` | 查看当前会话 |
| `/new 会话名` | 创建并切换到新会话 |
| `/switch 会话名` | 切换到指定会话 |
| `/exit` | 退出程序 |

## 使用示例

```text
你：/new python
已创建并切换到会话：python

你：什么是 Python 列表？

小智：Python 列表是一种可以保存多个元素的数据结构。

你：/session
当前会话：python
```

## 自动测试

运行：

```bash
python -m pytest
```

详细模式：

```bash
python -m pytest -v
```

## 日志

日志文件默认保存在：

```text
logs/app.log
```

`logs/` 不会提交到 GitHub。

## 本地数据

以下内容默认不会上传 GitHub：

```text
.env
.venv/
logs/
chat_history_*.json
__pycache__/
```

## Git 开发流程

创建功能分支：

```bash
git switch main
git pull
git switch -c feature/功能名
```

开发完成：

```bash
git add .
git commit -m "描述本次修改"
git push -u origin feature/功能名
```

然后在 GitHub 创建 Pull Request，并合并到 `main`。

## 后续计划

- [x] OpenAI API
- [x] 多会话
- [x] 日志系统
- [x] 自动测试
- [ ] SQLite 数据库
- [ ] Web 聊天界面
- [ ] Docker
- [ ] GitHub Actions
- [ ] 在线部署