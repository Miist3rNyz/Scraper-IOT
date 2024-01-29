import logging
import time
from typing import TypeVar

from db.cpe_collection import CpeCollection
from db.cve_collection import CveCollection
from db.nvd_collection import NvdCollection
from importers.cpe_importer import CpeImporter
from importers.cve_importer import CveImporter
from importers.nvd_importer import NvdImporter

LOGGER = logging.getLogger(__name__)
T = TypeVar('T', bound=NvdImporter)
U = TypeVar('U', bound=NvdCollection)


class ImportController(object):

    TIME_BETWEEN_REQUESTS = 6
    RESULT_PER_PAGE = 2000

    def import_cpes(self) -> None:
        self.__import_many_and_save(CpeImporter(), CpeCollection())

    def import_cves(self) -> None:
        self.__import_many_and_save(CveImporter(), CveCollection())

    def __import_many_and_save(self, importer: T, collection: U) -> None:
        LOGGER.info("🚀 Starting import")

        start_index = 0
        remaining_results = 1

        while start_index < remaining_results:
            LOGGER.info(f"⏳ State of import: {start_index * 100} / {remaining_results}")

            data = importer.run_import(start_index)
            collection.insert(data)

            start_index += ImportController.RESULT_PER_PAGE
            remaining_results = data['totalResults'] - start_index + 1  # 1 because start_index is 0-based

            LOGGER.debug(f"Waiting {self.TIME_BETWEEN_REQUESTS} seconds before next request")
            time.sleep(self.TIME_BETWEEN_REQUESTS)  # NVD API rate limit is 10 requests per minute

        LOGGER.info("🏁 Finished import")
