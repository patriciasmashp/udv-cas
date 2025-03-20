from fastapi import FastAPI, HTTPException
from config import config
from service.DAO.NewsDAO import NewsDAO

app = FastAPI()


@app.get("/")
async def read_root():
    news_dao = NewsDAO(path=config.news_path)
    news = await news_dao.get_news()
    return news


@app.get("/news/{news_id}")
async def read_news(news_id: int):
    news_dao = NewsDAO(path=config.news_path)
    news = await news_dao.get_news_by_id(news_id=news_id)
    if news is None:
        raise HTTPException(404, detail="News not found")
    return news
