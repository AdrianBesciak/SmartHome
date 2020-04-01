import time
import serial


class SerialDevice:
    def __init__(self, name):
        self.name = name
        self.device = serial.Serial(
            port='/dev/' + self.name,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        if self.device.isOpen():
            print('Pomyślnie otwarto port szeregowy')
            time.sleep(2)

    def send(self, command):
        self.device.write(str.encode(command + '\n'))

    def read(self):
        return self.device.read_until('\n').decode("utf-8")
