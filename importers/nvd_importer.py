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

    def _get_data(self, url: str) -> dict:
        headers = {"apiKey": API_KEY}
        try:
            response = requests.get(url, headers=headers)
        except requests.exceptions.RequestException as e:
            LOGGER.error(f"Error while requesting {url}: {e}")
            return {}
        
        if response.headers['apiKey'] == "No":
            LOGGER.error(f"Error while requesting {url}: Request without API Key")

        LOGGER.debug(f"Successfully requested {url}")
        return response.json()

    def __build_url(self, start_index: int, other_options: dict = None) -> str:
        start_index = {'startIndex': start_index}
        options = {**start_index, **other_options}
        return self.api_url + parse.urlencode(options)

    def run_import(self, start_index: int = 0, other_options: dict = None) -> dict:
        if other_options is None:
            other_options = {}
        url = self.__build_url(start_index, other_options)
        data = self._get_data(url)
        return data
