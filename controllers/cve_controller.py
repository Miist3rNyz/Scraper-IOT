from db.cve_collection import CveCollection
from db.database import Database


class CveController:

    @staticmethod
    def save(self, cves: list) -> None:
        CveCollection(Database()).insert(cves)
