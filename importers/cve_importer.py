from urllib import parse
import requests
import time

from controllers.cve_controller import CveController


class CveImporter(object):

    NVD_API_URL = 'https://services.nvd.nist.gov/rest/json/cves/2.0?'
    RESULT_PER_PAGE = 2000

    def run_full_import(self) -> None:
        start_index = 0
        remaining_results = 1

        while start_index < remaining_results:
            url: str = self.build_url(start_index)
            cves: dict = self.import_cves(url)
            CveController.save_cves(cves['vulnerabilities'], )

            start_index += self.RESULT_PER_PAGE
            remaining_results = cves['totalResults'] - start_index + 1 # 1 because start_index is 0-based
            time.sleep(6) # NVD API rate limit is 10 requests per minute

    def build_url(self, start_index: int) -> str:
        return self.NVD_API_URL + parse.urlencode({
            'startIndex': start_index,
            'resultsPerPage': self.RESULT_PER_PAGE
        })

    def __import_cves(self, url: str) -> dict:
        response = requests.get(url).json()
        return response

