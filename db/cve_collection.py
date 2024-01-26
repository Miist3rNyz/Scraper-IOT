

class CveCollection(object):

    COLLECTION_NAME = 'cves'
    COLLECTION = None

    def __init__(self, database):
        self.COLLECTION = database.DATABASE[self.COLLECTION_NAME]

    @staticmethod
    def insert(self, data):
        self.COLLECTION.insert_one(data)

    def find(self, query):
        return self.COLLECTION.find(query)

    def find_one(self, query):
        return self.COLLECTION.find_one(query)

    def update(self, query, data):
        self.COLLECTION.update_one(query, data)

    def delete(self, query):
        self.COLLECTION.delete_one(query)
