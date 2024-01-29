from importers.nvd_importer import NvdImporter


class CpeImporter(NvdImporter):

    def __init__(self):
        super().__init__('https://services.nvd.nist.gov/rest/json/cpes/2.0?')
    