from pymongo import MongoClient
import datetime


class Logger:
    def __init__(self):
        self.__client = MongoClient()
        self.__db = self.__client.SmartHomeServer
        self.__logs = self.__db.logs

    def addlog(self, device, service, message):
        log = { "device": device.getname(),
                "service": service,
                "date": datetime.datetime.utcnow(),
                "message": message}
        self.__logs.insert_one(log)
