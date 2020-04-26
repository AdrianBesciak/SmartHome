from pymongo import MongoClient
import datetime


class Logger:
    def __init__(self):
        __client = MongoClient()
        __db = __client.SmartHomeServer
        __logs = __db.logs

    def addlog(self, device, service, message):
        log = { "device": device.getname(),
                "service": service,
                "date": datetime.datetime.utcnow(),
                "message": message}
        self.__logs.insert_one(log)
