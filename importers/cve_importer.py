import logging
from typing import override

from importers.nvd_importer import NvdImporter


class CveImporter(NvdImporter):

    @property
    @override
    def api_url(self) -> str:
        return 'https://services.nvd.nist.gov/rest/json/cves/2.0?'
