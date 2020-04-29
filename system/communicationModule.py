import serialdevice


def main(pipe):
    devices_dict = {}
    while True:
        if pipe.poll(1):
            rec = pipe.recv()
            for i in rec:
                print('\tkey: ' + i + 'value: ' + rec[i])
            for i in devices_dict:
                print('\t\t' + i)
            if rec['command'] == 'register_device':
                print('Register dev' + rec[1])
                if rec['dev_type'] == 'serial':
                    devices_dict[rec['dev_name']] = serialdevice.SerialDevice(rec['dev_name'])
            elif rec['dev_type'] == 'send2dev':
                pipe.send(devices_dict[rec['dev_name']].talk(rec['message']))
            elif rec['dev_type'] == 'services':
                pipe.send(devices_dict[rec['dev_name']].getserviceslist())
            elif rec['dev_type'] == 'devs':
                pipe.send(devices_dict)
            else:
                pipe.send('Unrecognized command')


if __name__ == "__main__":
    main()
