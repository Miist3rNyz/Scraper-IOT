from pymongo import MongoClient


class Database(object):

    URI = "mongodb+srv://scraper-iot.gqwzipg.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority"
    CLIENT = None
    DATABASE = None

    def __init__(self):
        self.CLIENT = MongoClient(self.URI, tls=True, tlsCertificateKeyFile='/Users/jpetry/jpetry_x509_scraper_iot.pem')
        self.DATABASE = self.CLIENT['scraper-iot']


