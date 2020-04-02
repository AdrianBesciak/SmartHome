import serialdevice


def main():
    dev = serialdevice.SerialDevice('ttyACM0')

    dev.send('Pierwsza komenda')
    print('Odebrano: ' + dev.read())
    dev.send('Druga komenda')
    print('Odebrano: ' + dev.read())


if __name__ == "__main__":
    main()