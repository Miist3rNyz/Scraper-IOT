import logging
from typing import NoReturn

from db.nvd_collection import NvdCollection
from db.scraper_database import ScraperDatabase

LOGGER = logging.getLogger("scraper-iot")


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
        cpes_ids = self.get_cpe_ids(data)
        filter_outdated_cpes = {"_id": {"$in": cpes_ids}}
        LOGGER.debug(f"Deleting outdated {len(cpes_ids)} CPEs and replace them: {cpes_ids}")
        self.delete_many(filter=filter_outdated_cpes)  # First delete all outdated CVEs we need to replace
        self.insert(data)  # Then insert the updated ones

    def get_cpe_ids(self, data: dict) -> list:
        return [cpe["matchString"]["matchCriteriaId"] for cpe in data['matchStrings']]
