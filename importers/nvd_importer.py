import json
import logging
from datetime import datetime
from typing import Dict

import requests
import os
from abc import ABC, abstractmethod
from urllib import parse
from dotenv import load_dotenv

from models.nvd_datetime import NvdDatetime

load_dotenv()

LOGGER = logging.getLogger("scraper-iot")
API_KEY = os.getenv("NVD_API_KEY")


class NvdImporter(ABC):

    TIME_BETWEEN_REQUESTS = 6  # NVD API preconizes 10 requests per minute max

    api_url: str
    api_options: Dict[str, str]
    start_index: int
    last_update: datetime
    last_update_key: str

    def __init__(self, api_url: str, last_update_key: str, start_index=0, api_options: dict = None):
        if api_options is None:
            api_options = {}
        self.api_options = api_options
        self.api_url = api_url
        self.start_index = start_index
        self.last_update_key = last_update_key

    def load_last_update(self) -> NvdDatetime:
        with open(".metadata.json", "r") as file:
            content = json.load(file)
        return NvdDatetime(datetime.fromisoformat(content[self.last_update_key]))

    def write_last_update(self, date: datetime) -> None:
        with open(".metadata.json", "r") as file:
            content = json.load(file)
        content[self.last_update_key] = date.isoformat()
        with open(".metadata.json", "w") as file:
            json.dump(content, file, indent=4)

    def _get_data(self, url: str) -> dict:
        headers = {"apiKey": API_KEY}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        if response.status_code == 204:
            LOGGER.warning(f"Error while requesting {url}: No Content")
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

    @abstractmethod
    def set_next_start_index(self, data: dict) -> None:
        raise NotImplementedError



