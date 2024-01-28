from typing import NoReturn

from pymongo.collection import Collection

from db.scraper_database import ScraperDatabase


class CveCollection(Collection):

    def __init__(self):
        super().__init__(ScraperDatabase(), 'cves')

    def __bool__(self) -> NoReturn:
        super().__bool__()