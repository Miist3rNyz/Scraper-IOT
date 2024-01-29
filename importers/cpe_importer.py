from typing import override

from importers.nvd_importer import NvdImporter


class CpeImporter(NvdImporter):

    @property
    @override
    def api_url(self) -> str:
        return 'https://services.nvd.nist.gov/rest/json/cpes/2.0?'
    