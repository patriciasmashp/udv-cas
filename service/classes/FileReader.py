from typing import Dict
import aiofiles as aiof
import json


class FileReader:
    """
    Класс для чтения файлов с данными
    """

    def __init__(self, path):
        self.path = path

    async def get_data(self) -> Dict:
        """Получить все новости из файла

        Returns:
            dict: json с данными новостей 
        """
        async with aiof.open(self.path, "r", encoding="utf8") as f:
            return json.loads(await f.read())
