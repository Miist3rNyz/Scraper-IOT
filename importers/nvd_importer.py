import logging
import requests
from abc import ABC, abstractmethod
from urllib import parse

LOGGER = logging.getLogger(__name__)


class NvdImporter(ABC):

    @property
    @abstractmethod
    def api_url(self) -> str:
        raise NotImplementedError("This method should be implemented in a child class")

    def _get_data(self, start_index=0) -> dict:
        url: str = self.__build_url(start_index)
        try:
            response = requests.get(url).json()
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
