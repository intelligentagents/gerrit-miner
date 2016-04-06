from pymongo import MongoClient
con = MongoClient('mongodb://localhost:27017/')

class Insert:
    def __init__(self, json):
        self.insertIntoMongo(json)

    def insertIntoMongo(self, json):
        db = con.miner2
        reviews = db.reviews
        result = reviews.insert_one(json)
        result.inserted_id
