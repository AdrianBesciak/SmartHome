import time
import serial
from system import device
from system.logger import Logger


class SerialDevice(device.Device):
    def __init__(self, port_name):
        self.device = serial.Serial(
            port='/dev/' + port_name,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        if not self.device.isOpen():
            print('Nie udalo sie otworzyc portu szeregowego')
        else:
            time.sleep(2)
        self.services = self.get_services_list()
        self.send('getName')
        device.Device.__init__(self, self.read())

    def send(self, command):
        self.device.write(str.encode(command.__str__() + "\n"))

    def read(self):
        return self.device.read_until('\n').decode("utf-8").split('}')[0]
