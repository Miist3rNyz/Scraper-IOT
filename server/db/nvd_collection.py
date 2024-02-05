from abc import abstractmethod

from pymongo.collection import Collection


class NvdCollection(Collection):

    @abstractmethod
    def insert(self, data: dict) -> None:
        raise NotImplementedError("This method should be implemented in a child class")

    @abstractmethod
    def replace(self, data: dict) -> None:
        raise NotImplementedError("This method should be implemented in a child class")