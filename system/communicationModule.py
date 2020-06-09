from system import serialdevice
import datetime

from system import mongoCollection as mongo
from system.interprocess_communication import Core2CommunicationModuleKeys, Core2CommunicationModuleValues


def load_devices_from_db(db, dev_dict):
    devices_collection = db.getAll()
    for dev in devices_collection:
        if dev['dev_type'] == 'serial':
            try:
                serial_device = serialdevice.SerialDevice(dev['serial_port'])
                dev_dict[serial_device.get_name()] = serial_device
                print('Loaded device ', serial_device.get_name())
            except:
                print('Device ', dev['dev_name'], ' not found on port ', dev['serial_port'], ' - you can try add this device manually')


def main(pipe):
    devices_db = mongo.MongoCollection('devices')
    devices_dict = {}

    load_devices_from_db(devices_db, devices_dict)
    pipe.send('Loaded devices from database')

    while True:
        if pipe.poll(1):
            rec = pipe.recv()
            if rec[Core2CommunicationModuleKeys.COMMAND] == Core2CommunicationModuleValues.REGISTER_DEVICE:
                if rec[Core2CommunicationModuleKeys.DEV_TYPE] == Core2CommunicationModuleValues.SERIAL:
                    dev = serialdevice.SerialDevice(rec[Core2CommunicationModuleKeys.DEV_PORT])
                    devices_dict[dev.get_name()] = dev
                    pipe.send(dev.get_name())
                    print('Registered device: ' + dev.get_name())
                    if devices_db.get('dev_name', dev.get_name()):
                        print("Device: " + dev.get_name() + " already exists in db.")
                    else:
                        post = {'dev_name': dev.get_name(),
                                'dev_type': rec[Core2CommunicationModuleKeys.DEV_TYPE],
                                'serial_port': rec[Core2CommunicationModuleKeys.DEV_PORT],
                                'services': dev.get_services_list(),
                                'registration_date': datetime.datetime.now()}
                        if post['dev_type'] == Core2CommunicationModuleValues.SERIAL:
                            post['dev_type'] = 'serial'
                        devices_db.send(post)
                    print('\t\tZarejestrowano ', dev.get_name())

            elif rec[Core2CommunicationModuleKeys.COMMAND] == Core2CommunicationModuleValues.SEND2DEV:
                pipe.send(devices_dict[rec[Core2CommunicationModuleKeys.DEV_NAME]].talk(rec[Core2CommunicationModuleKeys.MESSAGE]))
            elif rec[Core2CommunicationModuleKeys.COMMAND] == Core2CommunicationModuleValues.SERVICES:
                pipe.send(devices_dict[rec[Core2CommunicationModuleKeys.DEV_NAME]].get_services_list())
            elif rec[Core2CommunicationModuleKeys.COMMAND] == Core2CommunicationModuleValues.DEVS:
                devices_names = []
                for dev in devices_dict:
                    devices_names.append(dev)
                print('communicationModule: ', len(devices_names))
                pipe.send(devices_names)
            else:
                pipe.send('Unrecognized command')



if __name__ == "__main__":
    main()
