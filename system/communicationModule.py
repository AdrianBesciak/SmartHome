import serialdevice


def main(com):
    dev = serialdevice.SerialDevice('ttyACM0')
    while True:
        if com.poll(1):
            com.send(dev.talk(com.recv()))


if __name__ == "__main__":
    main()
