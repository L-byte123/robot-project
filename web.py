from dotenv import load_dotenv

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from bot import ChatBot


load_dotenv()

app = FastAPI()

bot = ChatBot("web")


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(
    directory="templates"
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/chat")
def chat(request: ChatRequest):
    reply = bot.ask(request.message)

    return {
        "reply": reply
    }