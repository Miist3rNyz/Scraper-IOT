import logging
import time

import schedule

from controllers.import_controller import ImportController
from db.cpe_collection import CpeCollection
from db.cve_collection import CveCollection

LOGGER = logging.getLogger("scraper-iot")


class ImportScheduler(object):

    SCHEDULE_INTERVAL = 2

    def schedule_importer(self) -> None:
        if CveCollection().is_empty():
            LOGGER.info("⚠️ The local database of CVEs is empty, starting import")
            ImportController().import_cves()
        else:
            LOGGER.info("🚧 The local database of CVEs is not empty, starting update")
            ImportController().update_cves()

        if CpeCollection().is_empty():
            LOGGER.info("⚠️ The local database of CPEs is empty, starting import")
            ImportController().import_cpes()
        else:
            LOGGER.info("🚧 The local database of CPEs is not empty, starting update")
            ImportController().update_cpes()

        LOGGER.info("✅ Everything is up to date, starting scheduler")
        LOGGER.info(f"🕒 Scheduling CVE updates every {self.SCHEDULE_INTERVAL} hours")
        LOGGER.info(f"🕒 Scheduling CPE updates every {self.SCHEDULE_INTERVAL} hours")
        LOGGER.info("💡 Closing this process will stop the scheduler and the updates")

        while True:
            schedule.run_pending()
            time.sleep(1)

    def schedule_updates(self):
        schedule.every(self.SCHEDULE_INTERVAL).hours.at_time_zone("UTC").do(ImportController().update_cves())
        schedule.every(self.SCHEDULE_INTERVAL).hours.at_time_zone("UTC").do(ImportController().update_cpes())
