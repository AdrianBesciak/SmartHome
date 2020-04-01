import serialDevice
import time


dev = serialDevice.SerialDevice('ttyACM0')

dev.send('Pierwsza komenda\n')
time.sleep(2)
dev.send('Druga komenda\n')