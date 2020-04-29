import datetime
import mongoCollection


class Logger:
    def __init__(self):
        self.__logs = mongoCollection.MongoCollection("logs")

    def addlog(self, device, service, message):
        log = { "device": device.get_name(),
                "service": service,
                "date": datetime.datetime.now(),
                "message": message}
        self.__logs.send(log)
