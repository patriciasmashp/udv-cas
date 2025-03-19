import json
from typing import Dict, List
from fastapi import FastAPI, HTTPException
import aiofiles as aiof

app = FastAPI()


class FileReader:
    """
    Класс для чтения файлов с данными
    """

    @classmethod
    async def _get_all_news(cls) -> Dict:
        """Получить все новости из файла

        Returns:
            dict: json с данными новостей 
        """
        async with aiof.open("database/news.json", "r", encoding="utf8") as f:
            return json.loads(await f.read())

    @classmethod
    async def _get_all_comments(cls) -> Dict:
        """Получить все комментарии из файла

        Returns:
            dict: json с данными комментариев 
        """
        async with aiof.open("database/comments.json", "r",
                             encoding="utf8") as f:
            return json.loads(await f.read())


class NewsDAO:

    @classmethod
    async def _get_actual_news(cls) -> List[Dict]:
        """Получить актуальные новости

        Returns:
            dict: json с данными новостей 
        """
        news_data = await FileReader._get_all_news()
        return [news for news in news_data["news"] if not news["deleted"]]

    @classmethod
    async def get_news(cls) -> Dict:
        """Получить все актуальные новости и их кол-во

        Returns:
            dict: json с данными новостей 
        """
        news_data = await cls._get_actual_news()
        actual_news = [
            news for news in news_data if not news["deleted"]
        ]
        # ? Не понятно нужно ли в кол-ве новостей учитывать удаленные новости
        for news in actual_news:
            news["comments_count"] = len(
                await cls._get_comments_by_news(news["id"]))

        return {"news": actual_news, "news_count": len(actual_news)}

    @classmethod
    async def _get_comments_by_news(cls, news_id: int) -> List[Dict]:
        """Получить комментарии к новости

        Args:
            news_id (int): id новости

        Returns:
            list: список комментариев
        """
        comments_data = await FileReader._get_all_comments()
        return [
            comment for comment in comments_data["comments"]
            if comment["news_id"] == news_id
        ]

    @classmethod
    async def get_news_by_id(cls, news_id: int) -> Dict:
        """Получить новость по id

        Args:
            news_id (int): id новости

        Returns:
            dict: json с данными новости 
        """
        news_data = await cls._get_actual_news()
        # TODO По хорошему наверное стоило при запуске приложения
        # выгружать данные в память и переформировывать список
        # в словарь с ключем равным id, аля индексы таблицы

        news = [news for news in news_data if news["id"] == news_id]
        if not news:
            return None
        news[0]["comments"] = await cls._get_comments_by_news(news_id)
        return {"news": news[0], "comments_count": len(news[0]["comments"])}


@app.get("/")
async def read_root():
    news = await NewsDAO.get_news()
    return news


@app.get("/news/{news_id}")
async def read_news(news_id: int):
    news = await NewsDAO.get_news_by_id(news_id=news_id)
    if news is None:
        raise HTTPException(404, detail="News not found")
    return news
