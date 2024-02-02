from datetime import datetime

from importers.nvd_importer import NvdImporter


class CpeImporter(NvdImporter):

    def __init__(self):
        super().__init__('https://services.nvd.nist.gov/rest/json/cpes/2.0?')

    @staticmethod
    def load_last_update() -> datetime:
        pass

    @staticmethod
    def write_last_update(date: datetime) -> None:
        pass
    