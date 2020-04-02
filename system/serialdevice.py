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
        if not self.device.isOpen():
            print('Nie udalo sie otworzyc portu szeregowego')
        else:
            time.sleep(2)
#            self.getserviceslist()

    def send(self, command):
        self.device.write(str.encode(command.__str__() + "\n"))

    def read(self):
        return self.device.read_until('\n').decode("utf-8")

    def talk(self, command):
        self.send(command)
        return self.read()

    def getserviceslist(self):
        self.send('sendservices')
        amount = self.read()
        for i in range(amount):
            print(self.read())
