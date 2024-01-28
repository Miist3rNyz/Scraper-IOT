from db.cve_collection import CveCollection
from db.scraper_database import ScraperDatabase


class CveController:

    @staticmethod
    def save_cves(self, cves: list) -> None:
        CveCollection(ScraperDatabase()).insert(cves)
