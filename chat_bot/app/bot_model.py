from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class UserMsg(BaseModel):
    user_msg: str
    bot_memory: list[Message]


class BotMemory(BaseModel):
    bot_memory: list


class BotMsg(BaseModel):
    bot_msg: str
    bot_memory: list[Message]
