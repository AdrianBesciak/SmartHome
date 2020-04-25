from abc import ABC, abstractmethod


class Device(ABC):
    def __init__(self, name):
        self.name = name
        self.services = self.getserviceslist()

#    @abstractmethod
    def send(self, command):
        raise NotImplementedError("Implement send subclass!")

#    @abstractmethod
    def read(self):
        raise NotImplementedError("Implement send subclass!")

    def talk(self, command):
        self.send(command)
        return self.read()

    def getserviceslist(self):
        self.send('sendservices')
        services = self.read()
        return services.split(';')
