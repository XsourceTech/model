from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class BotMemory(BaseModel):
    bot_memory: list[Message]


