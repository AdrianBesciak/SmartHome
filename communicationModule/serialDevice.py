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

    def send(self, command):
        self.device.write(str.encode(command))
