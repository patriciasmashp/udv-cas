from pydantic import BaseModel


class CommentModel(BaseModel):
    id: int
    news_id: int
    title: str
    date: str
    comment: str
