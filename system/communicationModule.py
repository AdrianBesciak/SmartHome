import serialdevice


def main(pipe):
    devices_dict = {}
    while True:
        if pipe.poll(1):
            rec = pipe.recv()
            if rec['command'] == 'register_device':
                if rec['dev_type'] == 'serial':
                    devices_dict[rec['dev_name']] = serialdevice.SerialDevice(rec['dev_name'])
                print('Registered device: ' + rec['dev_name'])
            elif rec['command'] == 'send2dev':
                pipe.send(devices_dict[rec['dev_name']].talk(rec['message']))
            elif rec['command'] == 'services':
                pipe.send(devices_dict[rec['dev_name']].getserviceslist())
            elif rec['command'] == 'devs':
                pipe.send(devices_dict)
            else:
                pipe.send('Unrecognized command')


if __name__ == "__main__":
    main()
