from enum import Enum


class Webapp2CoreMessages(Enum):
    GET_DEVICES = 1,
    DEV_SERVICES = 2,
    RUN_SERVICE = 3,
    LOGIN = 4


class Webapp2CoreKeys(Enum):
    COMMAND = 1,
    DEV_NAME = 2,
    SERVICE = 3


class Core2WebappKeys(Enum):
    TYPE = 1,
    RESPONSE = 2,
    DEVICES_LIST = 3,
    SERVICES_LIST = 4


class Core2WebappMessages(Enum):
    DEV_RESPONSE = 1,
    DEV_SERVICES = 2,
    RESPONSE = 3,
    DEVICES = 4


class Core2CommunicationModuleKeys(Enum):
    COMMAND = 1,
    DEV_NAME = 2,
    MESSAGE = 3,
    DEV_TYPE = 4,
    DEV_PORT = 5


class Core2CommunicationModuleValues(Enum):
    DEVS = 1,
    SERVICES = 2,
    SEND2DEV = 3,
    REGISTER_DEVICE = 4,
    SERIAL = 5