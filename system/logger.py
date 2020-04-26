import datetime
import mongoCollection


class Logger:
    def __init__(self):
        self.__logs = mongoCollection.MongoCollection("logs")

    def addlog(self, device, service, message):
        log = { "device": device.getname(),
                "service": service,
                "date": datetime.datetime.utcnow(),
                "message": message}
        self.__logs.send(log)
