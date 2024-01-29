from typing import NoReturn

from db.nvd_collection import NvdCollection
from db.scraper_database import ScraperDatabase


class CpeCollection(NvdCollection):

    def __init__(self):
        super().__init__(ScraperDatabase(), 'cpes')

    def __bool__(self) -> NoReturn:
        super().__bool__()

    def insert(self, data: dict) -> None:
        self.insert_many(data['products'])
