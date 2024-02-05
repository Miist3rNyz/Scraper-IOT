import logging
from datetime import datetime
from typing import Dict

import requests
import os
from abc import ABC, abstractmethod
from urllib import parse
from dotenv import load_dotenv

load_dotenv()

LOGGER = logging.getLogger("scraper-iot")
API_KEY = os.getenv("NVD_API_KEY")


class NvdImporter(ABC):

    TIME_BETWEEN_REQUESTS = 6
    RESULT_PER_PAGE = 2000

    api_url: str
    api_options: Dict[str, str]
    start_index: int

    def __init__(self, api_url: str, start_index=0, api_options: dict = None):
        if api_options is None:
            api_options = {}
        self.api_options = api_options
        self.api_url = api_url
        self.start_index = start_index

    @staticmethod
    @abstractmethod
    def load_last_update() -> datetime:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def write_last_update(date: datetime) -> None:
        raise NotImplementedError

    def _get_data(self, url: str) -> dict:
        headers = {"apiKey": API_KEY}
        try:
            response = requests.get(url, headers=headers)
        except requests.exceptions.RequestException as e:
            LOGGER.error(f"Error while requesting {url}: {e}")
            return {}

        try:
            if response.headers['apikey'] == "No":
                LOGGER.warning(f"Error while requesting {url}: Request without API Key")
        except KeyError as e:
            LOGGER.warning(f"WTF {response.headers}, {e}")

        LOGGER.debug(f"Successfully requested {url}")
        return response.json()

    def __build_url(self) -> str:
        start_index = {'startIndex': self.start_index}
        options = {**start_index, **self.api_options}
        url = self.api_url + parse.urlencode(options, safe=':*')  # safe param avoid : and * to be encoded
        LOGGER.debug(f"Built URL: {url}")
        return url

    def run_import(self) -> dict:
        url = self.__build_url()
        data = self._get_data(url)
        return data


