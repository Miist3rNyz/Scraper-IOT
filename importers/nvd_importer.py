import logging
import requests
import os
from abc import ABC
from urllib import parse
from dotenv import load_dotenv

load_dotenv()

LOGGER = logging.getLogger("scraper-iot")
API_KEY = os.getenv("NVD_API_KEY")


class NvdImporter(ABC):

    api_url: str

    def __init__(self, api_url: str):
        self.api_url = api_url

    def _get_data(self, start_index=0) -> dict:
        url: str = self.__build_url(start_index)
        headers = {"apiKey": API_KEY}
        try:
            response = requests.get(url, headers=headers).json()
        except requests.exceptions.RequestException as e:
            LOGGER.error(f"Error while requesting {url}: {e}")
            return {}

        LOGGER.debug(f"Successfully requested {url}")
        return response

    def __build_url(self, start_index: int) -> str:
        return self.api_url + parse.urlencode({
            'startIndex': start_index,
        })

    def run_import(self, start_index: int = 0) -> dict:
        data = self._get_data(start_index)
        return data
