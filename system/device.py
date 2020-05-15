from abc import ABC, abstractmethod
from system.logger import Logger


class Device(ABC):
    @abstractmethod
    def __init__(self, name):
        self.name = name
        self.services = self.get_services_list()
        self.__logger = Logger()
        self.__logger.addlog(self, 'device registration', 'Registered device: ' + self.name)

    @abstractmethod
    def send(self, command):
        raise NotImplementedError("Implement send subclass!")

    @abstractmethod
    def read(self):
        raise NotImplementedError("Implement send subclass!")

    def get_name(self):
        return self.name

    def talk(self, command):
        self.send(command)
        result = self.read()
        self.__logger.addlog(self, command, result)
        return result

    def get_services_list(self):
        self.send('sendservices')
        services = self.read()
        return services.split(';')
