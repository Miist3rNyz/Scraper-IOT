from typing import NoReturn

from db.nvd_collection import NvdCollection
from db.scraper_database import ScraperDatabase


class CpeCollection(NvdCollection):

    def __init__(self):
        super().__init__(ScraperDatabase(), name='cpes')

    def __bool__(self) -> NoReturn:
        super().__bool__()

    def insert(self, data: dict) -> None:
        cpes = [cpe["matchString"] for cpe in data['matchStrings']]
        refactor_cpes = [{'_id': cpe.pop('matchCriteriaId'), **cpe} for cpe in cpes]
        self.insert_many(refactor_cpes)

    def replace(self, data: dict) -> None:
        raise NotImplementedError
