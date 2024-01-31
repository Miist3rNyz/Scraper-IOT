from importers.nvd_importer import NvdImporter


class CveImporter(NvdImporter):

    def __init__(self, api_options: dict = None):
        super().__init__('https://services.nvd.nist.gov/rest/json/cves/2.0?', api_options=api_options)
