from datetime import datetime

from importers.nvd_importer import NvdImporter


class CpeImporter(NvdImporter):

    RESULT_PER_PAGE = 5000  # NVD API max value

    def __init__(self, api_options: dict = None, last_update_key='cpe_last_update'):
        super().__init__(api_url='https://services.nvd.nist.gov/rest/json/cpematch/2.0?',
                         api_options=api_options,
                         last_update_key=last_update_key)

    def set_next_start_index(self, data: dict) -> None:
        self.start_index += len(data['matchStrings'])
