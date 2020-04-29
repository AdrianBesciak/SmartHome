from pymongo import MongoClient


class MongoCollection:
    def __init__(self, collectionname):
        self.__client = MongoClient()
        self.__db = self.__client.SmartHomeServer
        self.__collection = self.__db[collectionname]

    def send(self, message):
        self.__collection.insert_one(message)

    def get(self, field, value):
        return self.__collection.find_one({field: value})
