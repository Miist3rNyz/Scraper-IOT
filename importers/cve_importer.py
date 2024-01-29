from importers.nvd_importer import NvdImporter


class CveImporter(NvdImporter):

    def __init__(self):
        super().__init__('https://services.nvd.nist.gov/rest/json/cves/2.0?')
