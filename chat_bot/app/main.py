from fastapi import FastAPI, HTTPException
from chatbot_Xsource import chatbot
from bot_model import *
import uvicorn
from get_key import get_openai_key


chatbot_app = FastAPI(
    title="chatbot Service API",
    description="API for general information chatbot.",
    version="1.2.1",
    openapi_tags=[
        {
            "name": "Chatbot",
            "description": "Operations related to chatbot, including answer user's message and summarize user's general information",
        }
    ],
)


@chatbot_app.post("/reply_msg", response_model=BotMemory, description="Answer the user's input message for major.")
async def reply_msg(memory: BotMemory, flag: Flag):
    bot = chatbot.Chatbot(memory.bot_memory)
    flag = flag.flag
    if flag == FlagEnum.major:
        chatbot_memory_new = bot.generate_response_for_major()
    elif flag == FlagEnum.field:
        chatbot_memory_new = bot.generate_response_for_field()
    elif flag == FlagEnum.topic:
        chatbot_memory_new = bot.generate_response_for_topic()
    elif flag == FlagEnum.title:
        chatbot_memory_new = bot.generate_response_for_title()
    else:
        raise HTTPException(status_code=422, detail="Invalid flag")
    return {'bot_memory': chatbot_memory_new}


@chatbot_app.post("/summarize_info", description="Summarize user's general information")
async def summarize_info(memory: BotMemory):
    bot = chatbot.Chatbot(memory.bot_memory)
    chatbot_msg = bot.get_summary()
    chatbot_msg_json = eval(chatbot_msg)
    return chatbot_msg_json

@chatbot_app.get("/api/v1/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    get_openai_key()
    uvicorn.run("main:chatbot_app", host="0.0.0.0", port=8050, reload=True)

