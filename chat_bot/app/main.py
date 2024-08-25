from fastapi import FastAPI, Body
from chatbot_Xsource import chatbot
import uvicorn
from dotenv import load_dotenv
load_dotenv()


chatbot_app = FastAPI(
    title="chatbot Service API",
    description="API for managing users, including registration, login, and profile management.",
    version="1.1.0",
    openapi_tags=[
        {
            "name": "Chatbot",
            "description": "Operations related to chatbot, including get user message and return model message",
        }
    ],
)

chatbot = chatbot.Chatbot()

@chatbot_app.post("/receive_msg", description="Answer the user's input message.")
async def receive_message(usr_msg: str = Body(...)):
    """
    Answer the user's message with chatbot.

    Returns the answer message.
    """
    chatbot_msg = chatbot.generate_response_for_general_information(usr_msg)
    return chatbot_msg


@chatbot_app.post("/summarize_msg", description="Return the first message.")
async def summarize_message():
    """
    Answer the user's message with chatbot.

    Returns the answer message.
    """
    chatbot_msg = chatbot.summarize_general_information()
    return chatbot_msg


@chatbot_app.get("/")
async def root():
    return {"message": "Welcome to Xsource paper-writing chatbot!"}


if __name__ == "__main__":
    uvicorn.run("main:chatbot_app", port=8080, reload=True)


