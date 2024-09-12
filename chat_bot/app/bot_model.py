from pydantic import BaseModel
from enum import Enum


class Message(BaseModel):
    role: str
    content: str


class BotMemory(BaseModel):
    bot_memory: list[Message]


class LevelEnum(str, Enum):
    MAJOR = 'major'
    FIELD = 'field'
    TOPIC = 'topic'
    TITLE = 'title'


class Level(BaseModel):
    level: LevelEnum


class PartEnum(str, Enum):
    ARTICLE = 'article'
    ABSTRACT = 'abstract'
    INTRODUCTION = 'introduction'
    LITERATURE_REVIEW = 'literature_review'
    METHODOLOGY = 'methodology'
    RESULTS = 'results'
    CONCLUSION = 'conclusion'
    REFERENCES = 'references'


class Part(BaseModel):
    part: PartEnum

