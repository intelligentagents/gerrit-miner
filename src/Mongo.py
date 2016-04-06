from pymongo import MongoClient


class Insert:
    def __init__(self, json, database):
        self.insert(json, database)

    @staticmethod
    def insert(json, database):
        connection = MongoClient('mongodb://localhost:27017/')
        db = connection[database]
        reviews = db.reviews
        reviews.insert_one(json)
