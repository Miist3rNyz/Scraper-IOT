import logging
import time
from datetime import datetime
from typing import TypeVar

from db.cpe_collection import CpeCollection
from db.cve_collection import CveCollection
from db.nvd_collection import NvdCollection
from importers.cpe_importer import CpeImporter
from importers.cve_importer import CveImporter
from importers.nvd_importer import NvdImporter

LOGGER = logging.getLogger("scraper-iot")
T = TypeVar('T', bound=NvdImporter)
U = TypeVar('U', bound=NvdCollection)


class ImportController(object):

    def update_cves(self) -> None:
        api_options = {
            "lastModStartDate": datetime.now().isoformat(),
            "lastModEndDate": datetime.now().isoformat()
        }
        self.__import_many_and_save(CveImporter(api_options), CveCollection())

    def import_cpes(self) -> None:
        self.__import_many_and_save(CpeImporter(), CpeCollection())

    def import_cves(self) -> None:
        self.__import_many_and_save(CveImporter(), CveCollection())

    def __import_many_and_save(self, importer: T, collection: U) -> None:
        LOGGER.info("🚀 Starting import")

        remaining_results = 1

        while importer.start_index < remaining_results:
            LOGGER.info(f"⏳ State of import: {importer.start_index * 100} / {remaining_results}")

            data = importer.run_import()
            collection.insert(data)

            importer.start_index += importer.RESULT_PER_PAGE
            remaining_results = data['totalResults'] - importer.start_index + 1  # 1 because start_index is 0-based

            LOGGER.debug(f"Waiting {importer.TIME_BETWEEN_REQUESTS} seconds before next request")
            time.sleep(importer.TIME_BETWEEN_REQUESTS)  # NVD API rate limit is 10 requests per minute

        LOGGER.info("🏁 Finished import")

    def __import_many_and_replace(self, importer: T, collection: U) -> None:
        LOGGER.info("🚀 Starting import")

        remaining_results = 1

        while importer.start_index < remaining_results:
            LOGGER.info(f"⏳ State of import: {importer.start_index * 100} / {remaining_results}")

            data = importer.run_import()
            collection.insert(data)

            importer.start_index += importer.RESULT_PER_PAGE
            remaining_results = data['totalResults'] - importer.start_index + 1  # 1 because start_index is 0-based

            LOGGER.debug(f"Waiting {importer.TIME_BETWEEN_REQUESTS} seconds before next request")
            time.sleep(importer.TIME_BETWEEN_REQUESTS)  # NVD API rate limit is 10 requests per minute

        LOGGER.info("🏁 Finished import")