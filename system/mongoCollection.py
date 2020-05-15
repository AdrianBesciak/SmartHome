from pymongo import MongoClient


class MongoCollection:
    def __init__(self, collection_name):
        self.__client = MongoClient()
        self.__db = self.__client.SmartHomeServer
        self.__collection = self.__db[collection_name]

    def send(self, message):
        self.__collection.insert_one(message)

    def get(self, field, value):
        return self.__collection.find_one({field: value})

    def remove(self, field, value):
        return self.__collection.delete_one({field: value})

    def getAll(self):
        return self.__collection.find({})