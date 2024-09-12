from fastapi import FastAPI, HTTPException
from chatbot_Xsource import chatbot
from bot_model import *
import uvicorn
from get_key import get_openai_key


chatbot_app = FastAPI(
    title="chatbot Service API",
    description="API for general information chatbot.",
    version="1.2.2",
    openapi_tags=[
        {
            "name": "Chatbot",
            "description": "Operations related to chatbot, including answer user's message and summarize user's answer",
        }
    ],
)


@chatbot_app.post("/reply_msg", response_model=BotMemory, description="Answer the user's input message for major.")
async def reply_msg(bot_memory: BotMemory, level: Level, part: Part):
    bot = chatbot.Chatbot(bot_memory.bot_memory)
    if part.part == PartEnum.ARTICLE:
        if level.level == LevelEnum.MAJOR:
            chatbot_memory_new = bot.generate_response_for_major()
        elif level.level == LevelEnum.FIELD:
            chatbot_memory_new = bot.generate_response_for_field()
        elif level.level == LevelEnum.TOPIC:
            chatbot_memory_new = bot.generate_response_for_topic()
        elif level.level == LevelEnum.TITLE:
            chatbot_memory_new = bot.generate_response_for_title()
        else:
            raise HTTPException(status_code=422, detail="Invalid level name")
    else:
        raise HTTPException(status_code=422, detail="Invalid part name")
    return {'bot_memory': chatbot_memory_new}


@chatbot_app.post("/summarize_info", description="Summarize user's general information")
async def summarize_info(bot_memory: BotMemory, part: Part):
    if part.part == PartEnum.ARTICLE:
        bot = chatbot.Chatbot(bot_memory.bot_memory)
        chatbot_msg = bot.get_summary()
        chatbot_msg_json = eval(chatbot_msg)
    else:
        raise HTTPException(status_code=422, detail="Invalid part name")
    return chatbot_msg_json


if __name__ == "__main__":
    get_openai_key()
    uvicorn.run("main:chatbot_app", host = "0.0.0.0", port=8050, reload=True)

