import pymongo.errors
import os
from typing import NoReturn
from pymongo import MongoClient
from pymongo.database import Database


class ScraperDatabase(Database):

    URI = os.environ.get('MONGODB_URI')

    def __init__(self):
        super().__init__(MongoClient(self.URI, 27017), name="scraper-iot")

    def __bool__(self) -> NoReturn:
        super().__bool__()

    def test_connection(self) -> bool:
        try:
            self.client.list_database_names()
        except pymongo.errors.ConnectionFailure as e:
            print(e)
            return False
        return True
