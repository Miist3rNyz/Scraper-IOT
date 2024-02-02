import json
from datetime import datetime

from importers.nvd_importer import NvdImporter


class CveImporter(NvdImporter):

    last_update: datetime

    def __init__(self, start_index: int = 0, api_options: dict = None):
        super().__init__(api_url='https://services.nvd.nist.gov/rest/json/cves/2.0?',
                         start_index=start_index,
                         api_options=api_options)

    @staticmethod
    def load_last_update() -> datetime:
        with open(".metadata.json", "r") as file:
            content = json.load(file)
        return datetime.fromisoformat(content['cve_last_update'])

    @staticmethod
    def write_last_update(date: datetime) -> None:
        with open(".metadata.json", "r") as file:
            content = json.load(file)
        content['cve_last_update'] = date.isoformat()
        with open(".metadata.json", "w") as file:
            json.dump(content, file, indent=4)

