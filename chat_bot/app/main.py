from fastapi import FastAPI
from chatbot_Xsource import chatbot
import bot_model
import uvicorn
from get_key import get_openai_key


chatbot_app = FastAPI(
    title="chatbot Service API",
    description="API for general information chatbot.",
    version="1.2.0",
    openapi_tags=[
        {
            "name": "Chatbot",
            "description": "Operations related to chatbot, including answer user's message and summarize user's general information",
        }
    ],
)


@chatbot_app.post("/reply_msg_major", response_model=bot_model.BotMemory, description="Answer the user's input message for major.")
async def reply_msg_major(msg: bot_model.BotMemory):
    bot = chatbot.Chatbot(msg.bot_memory)
    chatbot_memory_new = bot.generate_response_for_major()
    return {'bot_memory': chatbot_memory_new}


@chatbot_app.post("/reply_msg_field", response_model=bot_model.BotMemory, description="Answer the user's input message for field.")
async def reply_msg_field(msg: bot_model.BotMemory):
    bot = chatbot.Chatbot(msg.bot_memory)
    chatbot_memory_new = bot.generate_response_for_field()
    return {'bot_memory': chatbot_memory_new}


@chatbot_app.post("/reply_msg_topic", response_model=bot_model.BotMemory, description="Answer the user's input message for topic.")
async def reply_msg_topic(msg: bot_model.BotMemory):
    bot = chatbot.Chatbot(msg.bot_memory)
    chatbot_memory_new = bot.generate_response_for_topic()
    return {'bot_memory': chatbot_memory_new}


@chatbot_app.post("/reply_msg_title", response_model=bot_model.BotMemory, description="Answer the user's input message for title.")
async def reply_msg_title(msg: bot_model.BotMemory):
    bot = chatbot.Chatbot(msg.bot_memory)
    chatbot_memory_new = bot.generate_response_for_title()
    return {'bot_memory': chatbot_memory_new}


@chatbot_app.post("/summarize_info", description="Summarize user's general information")
async def summarize_info(memory: bot_model.BotMemory):
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

