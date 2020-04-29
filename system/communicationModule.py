import serialdevice
import mongoCollection as mongo


def main(pipe):
    devices_db = mongo.MongoCollection('Devices')
    devices_dict = {}
    while True:
        if pipe.poll(1):
            rec = pipe.recv()
            if rec['command'] == 'register_device':
                if rec['dev_type'] == 'serial':
                    dev = serialdevice.SerialDevice(rec['dev_port'])
                    devices_dict[dev.getname()] = dev
                    pipe.send(dev.getname())
                    print('Registered device: ' + dev.getname())
                    if devices_db.get('dev_name', dev.getname()):
                        print("Device: " + dev.getname() + " already exists in db.")
                    else:
                        post = {'dev_name': dev.getname(),
                                'dev_type': rec['dev_type'],
                                'services': dev.getserviceslist()}
                        devices_db.send(post)

            elif rec['command'] == 'send2dev':
                pipe.send(devices_dict[rec['dev_name']].talk(rec['message']))
            elif rec['command'] == 'services':
                pipe.send(devices_dict[rec['dev_name']].getserviceslist())
            elif rec['command'] == 'devs':
                devices_names = []
                for dev in devices_dict:
                    devices_names.append(dev)
                pipe.send(devices_names)
            else:
                pipe.send('Unrecognized command')


if __name__ == "__main__":
    main()
