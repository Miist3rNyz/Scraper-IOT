from typing import NoReturn

from pymongo import MongoClient
from pymongo.database import Database


class ScraperDatabase(Database):

    URI = "mongodb+srv://scraper-iot.gqwzipg.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"

    def __init__(self):
        super().__init__(MongoClient(self.URI,
                                     tls=True,
                                     tlsCertificateKeyFile='/Users/jpetry/jpetry_x509_scraper_iot.pem'),
                         'scraper-iot')

    def __bool__(self) -> NoReturn:
        super().__bool__()
