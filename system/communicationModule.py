import serialdevice


def main(pipe):
    devices_dict = {}
    while True:
        if pipe.poll(1):
            rec = pipe.recv().split(':')
            for i in rec:
                print('\t' + i)
            for i in devices_dict:
                print('\t\t' + i)
            if rec[0] == 'register_device':
                print('Register dev' + rec[1])
                if rec[1] == 'serial':
                    devices_dict[rec[2]] = serialdevice.SerialDevice(rec[2])
            elif rec[0] == 'send2dev':
                pipe.send(devices_dict[rec[1]].talk(rec[2]))
            elif rec[0] == 'services':
                pipe.send(devices_dict[rec[1]].getserviceslist())
            else:
                pipe.send('Unrecognized command')


if __name__ == "__main__":
    main()
