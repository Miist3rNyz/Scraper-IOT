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
        # The new last_mod_date is taken before update in case of long-running time to update
        date_now = datetime.now()
        api_options = {
            "lastModStartDate": CveImporter.load_last_update(),
            "lastModEndDate": datetime.now().isoformat()
        }
        self.__import_many_and_replace(CveImporter(api_options), CveCollection())
        CveImporter.write_last_update(date_now)

    def update_cpes(self) -> None:
        # The new last_mod_date is taken before update in case of long-running time to update
        date_now = datetime.now()
        api_options = {
            "lastModStartDate": CpeImporter.load_last_update(),
            "lastModEndDate": datetime.now().isoformat()
        }
        self.__import_many_and_replace(CpeImporter(), CpeCollection()) # TODO: Add api_options
        CpeImporter.write_last_update(date_now)

    def import_cpes(self) -> None:
        # The new last_mod_date is taken before update in case of long-running time to update
        date_now = datetime.now()
        self.__import_many_and_save(CpeImporter(), CpeCollection())
        CpeImporter.write_last_update(date_now)

    def import_cves(self, start_index=0) -> None:
        # The new last_mod_date is taken before update in case of long-running time to update
        date_now = datetime.now()
        self.__import_many_and_save(CveImporter(start_index=start_index), CveCollection())
        CveImporter.write_last_update(date_now)

    def __import_many_and_save(self, importer: T, collection: U) -> None:
        LOGGER.info("🚀 Starting import")

        total_results: int = importer.start_index + 1

        while importer.start_index < total_results:
            state: float = (importer.start_index * 100) / total_results
            LOGGER.info(f"⏳ State of import: {state:.1f} %")

            data = importer.run_import()
            collection.insert(data)

            importer.start_index += importer.RESULT_PER_PAGE
            remaining_results = data['totalResults'] - importer.start_index + 1  # 1 because start_index is 0-based
            total_results = int(data['totalResults'])
            LOGGER.debug(f"totalResults: {total_results}, remaining_results: {remaining_results}")

            LOGGER.debug(f"Waiting {importer.TIME_BETWEEN_REQUESTS} seconds before next request")
            time.sleep(importer.TIME_BETWEEN_REQUESTS)  # NVD API rate limit is 10 requests per minute

        LOGGER.info("🏁 Finished import")

    def __import_many_and_replace(self, importer: T, collection: U) -> None:
        LOGGER.info("🚀 Starting import")

        remaining_results = 1

        while importer.start_index < remaining_results:
            state: float = (importer.start_index * 100) / remaining_results
            LOGGER.info(f"⏳ State of import: {state} %")

            data = importer.run_import()
            collection.replace(data)

            importer.start_index += importer.RESULT_PER_PAGE
            remaining_results = data['totalResults'] - importer.start_index + 1  # 1 because start_index is 0-based

            LOGGER.debug(f"Waiting {importer.TIME_BETWEEN_REQUESTS} seconds before next request")
            time.sleep(importer.TIME_BETWEEN_REQUESTS)  # NVD API rate limit is 10 requests per minute

        LOGGER.info("🏁 Finished import")