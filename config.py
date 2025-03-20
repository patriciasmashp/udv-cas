from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    news_path: str = 'database/news.json'
    comments_path: str = 'database/comments.json'


config = Settings()
