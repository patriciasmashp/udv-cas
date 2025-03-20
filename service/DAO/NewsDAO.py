from typing import Dict, List
from service.DAO.CommentsDAO import CommentsDAO
from service.classes.FileReader import FileReader
from service.schema.news import NewsModel
from config import config


class NewsDAO:

    def __init__(self, path: str, reader: FileReader = FileReader):
        self.path = path
        self.reader: FileReader = reader(path)

    async def get_actual_news(self) -> List[NewsModel]:
        """Получить актуальные новости

        Returns:
            dict: json с данными новостей 
        """
        news_data = await self.reader.get_data()
        return [
            NewsModel(**news) for news in news_data["news"]
            if not news["deleted"]
        ]

    async def get_news(self) -> Dict:
        """Получить все актуальные новости и их кол-во

        Returns:
            dict: json с данными новостей 
        """
        news_data = await self.get_actual_news()
        comments_dao = CommentsDAO(config.comments_path)

        actual_news = [news for news in news_data if not news.deleted]
        # ? Не понятно нужно ли в кол-ве новостей учитывать удаленные новости
        for news in actual_news:
            news.comments_count = len(await
                                      comments_dao.get_comments_by_news(news.id
                                                                        ))

        return {"news": actual_news, "news_count": len(actual_news)}

    async def get_news_by_id(self, news_id: int) -> Dict:
        """Получить новость по id

        Args:
            news_id (int): id новости

        Returns:
            dict: json с данными новости 
        """
        news_data = await self.get_actual_news()
        comments_dao = CommentsDAO(config.comments_path)
        # TODO По хорошему наверное стоило при запуске приложения
        # выгружать данные в память и переформировывать список
        # в словарь с ключем равным id, аля индексы таблицы

        news = [news for news in news_data if news.id == news_id]
        if not news:
            return None
        news[0].comments = await comments_dao.get_comments_by_news(news_id)
        return {"news": news[0], "comments_count": len(news[0].comments)}
