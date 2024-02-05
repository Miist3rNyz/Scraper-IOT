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
        cve_importer = CveImporter()
        api_options = {
            "lastModStartDate": cve_importer.load_last_update().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "lastModEndDate": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        }
        cve_importer.api_options= api_options
        self.__import_many_and_replace(cve_importer, CveCollection())
        cve_importer.write_last_update(date_now)

    def import_cves(self, start_index=0) -> None:
        # The new last_mod_date is taken before update in case of long-running time to update
        date_now = datetime.now()
        cve_importer = CveImporter(start_index=start_index)
        self.__import_many_and_save(cve_importer, CveCollection())
        cve_importer.write_last_update(date_now)

    def update_cpes(self) -> None:
        # The new last_mod_date is taken before update in case of long-running time to update
        date_now = datetime.now()
        cpe_importer = CpeImporter()
        api_options = {
            "lastModStartDate": cpe_importer.load_last_update(),
            "lastModEndDate": datetime.now().isoformat()
        }
        cpe_importer.api_options = api_options
        self.__import_many_and_replace(cpe_importer, CpeCollection())
        cpe_importer.write_last_update(date_now)

    def import_cpes(self) -> None:
        # The new last_mod_date is taken before update in case of long-running time to update
        date_now = datetime.now()
        api_options = {
            "matchStringSearch": "cpe:2.3:h:*",
        }
        cpe_importer = CpeImporter(api_options=api_options)
        self.__import_many_and_save(cpe_importer, CpeCollection())
        cpe_importer.write_last_update(date_now)

    def __import_many_and_save(self, importer: T, collection: U) -> None:
        LOGGER.info("🚀 Starting import")

        total_results: int = importer.start_index + 1

        while importer.start_index < total_results:
            state: float = (importer.start_index * 100) / total_results
            LOGGER.info(f"⏳ State of import: {state:.1f} %")

            data = importer.run_import()
            collection.insert(data)

            importer.start_index += importer.RESULT_PER_PAGE
            total_results = data['totalResults']

            LOGGER.debug(f"Waiting {importer.TIME_BETWEEN_REQUESTS} seconds before next request")
            time.sleep(importer.TIME_BETWEEN_REQUESTS)  # NVD API rate limit is 10 requests per minute

        LOGGER.info("🏁 Finished import")

    def __import_many_and_replace(self, importer: T, collection: U) -> None:
        LOGGER.info("🚀 Starting import")

        total_results: int = importer.start_index + 1

        while importer.start_index < total_results:
            state: float = (importer.start_index * 100) / total_results
            LOGGER.info(f"⏳ State of import: {state:.1f} %")

            data = importer.run_import()
            collection.replace(data)

            importer.start_index += importer.RESULT_PER_PAGE
            total_results = data['totalResults']

            LOGGER.debug(f"Waiting {importer.TIME_BETWEEN_REQUESTS} seconds before next request")
            time.sleep(importer.TIME_BETWEEN_REQUESTS)  # NVD API rate limit is 10 requests per minute

        LOGGER.info("🏁 Finished import")