from typing import NoReturn

from db.nvd_collection import NvdCollection
from db.scraper_database import ScraperDatabase


class CveCollection(NvdCollection):

    def __init__(self):
        super().__init__(ScraperDatabase(), 'cves')

    def __bool__(self) -> NoReturn:
        super().__bool__()

    def insert(self, data: dict) -> None:
        self.insert_many(data['vulnerabilities'])

    def replace(self, data: dict) -> None:
        filter = {"cve.id": {"$in": self.get_cve_ids(data)}}
        self.delete_many(filter=filter)  # First delete all outdated CVEs we need to replace
        self.insert(data)  # Then insert the updated ones

    def get_cve_ids(self, data: dict) -> list:
        return [cve["cve"]["id"] for cve in data['vulnerabilities']]
