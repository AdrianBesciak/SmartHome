import serialDevice


dev = serialDevice.SerialDevice('ttyACM0')

dev.send('Pierwsza komenda')
print('Odebrano: ' + dev.read())
dev.send('Druga komenda')
print('Odebrano: ' + dev.read())
