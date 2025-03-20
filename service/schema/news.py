from pydantic import BaseModel


class NewsModel(BaseModel, extra='allow'):
    id: int
    title: str
    date: str
    body: str
    deleted: bool
