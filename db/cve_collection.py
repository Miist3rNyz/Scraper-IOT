import logging
from typing import NoReturn

from db.nvd_collection import NvdCollection
from db.scraper_database import ScraperDatabase
from controllers.classifier import CVEclassifier

LOGGER = logging.getLogger("scraper-iot")

class CveCollection(NvdCollection):

    def __init__(self):
        super().__init__(ScraperDatabase(), 'cves')

    def __bool__(self) -> NoReturn:
        super().__bool__()

    def insert(self, data: dict) -> None:
        cve_classifier=CVEclassifier()
        cves = [cve["cve"] for cve in data['vulnerabilities']]
        refactor_cves = [{'_id': cve.pop('id'), **cve} for cve in cves]
        refactor_cves_classify=cve_classifier.classify_all_cves(refactor_cves)
        self.insert_many(refactor_cves_classify)

    def replace(self, data: dict) -> None:
        cves_ids = self.get_cve_ids(data)
        filter_outdated_cves = {"_id": {"$in": cves_ids}}
        LOGGER.debug(f"Deleting outdated {len(cves_ids)} CVEs and replace them: {cves_ids}")
        self.delete_many(filter=filter_outdated_cves)  # First delete all outdated CVEs we need to replace
        self.insert(data)  # Then insert the updated ones

    def get_cve_ids(self, data: dict) -> list:
        return [cve["cve"]["id"] for cve in data['vulnerabilities']]
