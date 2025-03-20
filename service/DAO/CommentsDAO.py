from typing import List
from service.classes.FileReader import FileReader
from service.schema.comments import CommentModel


class CommentsDAO:

    def __init__(self, path: str, reader: FileReader = FileReader):
        self.path = path
        self.reader: FileReader = reader(path)

    async def get_comments_by_news(self, news_id: int) -> List[CommentModel]:
        """Получить комментарии к новости

        Args:
            news_id (int): id новости

        Returns:
            list: список комментариев
        """
        comments_data = await self.reader.get_data()
        return [
            CommentModel(**comment) for comment in comments_data["comments"]
            if comment["news_id"] == news_id
        ]
