from importers.nvd_importer import NvdImporter


class CveImporter(NvdImporter):

    RESULT_PER_PAGE = 2000  # NVD API max value

    def __init__(self, start_index: int = 0, api_options: dict = None, last_update_key='cve_last_update'):
        super().__init__(api_url='https://services.nvd.nist.gov/rest/json/cves/2.0?',
                         start_index=start_index,
                         api_options=api_options,
                         last_update_key=last_update_key)


