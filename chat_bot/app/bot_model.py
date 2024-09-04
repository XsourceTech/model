from pydantic import BaseModel
from enum import Enum


class Message(BaseModel):
    role: str
    content: str


class BotMemory(BaseModel):
    bot_memory: list[Message]


class FlagEnum(str, Enum):
    major = 'major'
    field = 'field'
    topic = 'topic'
    title = 'title'


class Flag(BaseModel):
    flag: FlagEnum

