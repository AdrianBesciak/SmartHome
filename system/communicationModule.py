import serialdevice
import datetime
import mongoCollection as mongo
from scheduleChecker import ScheduleChecker


def main(pipe):
    devices_db = mongo.MongoCollection('devices')
    devices_dict = {}
    schedule = ScheduleChecker()
    lastMinute = datetime.datetime.now().minute
    while True:
        if pipe.poll(1):
            rec = pipe.recv()
            if rec['command'] == 'register_device':
                if rec['dev_type'] == 'serial':
                    dev = serialdevice.SerialDevice(rec['dev_port'])
                    devices_dict[dev.get_name()] = dev
                    pipe.send(dev.get_name())
                    print('Registered device: ' + dev.get_name())
                    if devices_db.get('dev_name', dev.get_name()):
                        print("Device: " + dev.get_name() + " already exists in db.")
                    else:
                        post = {'dev_name': dev.get_name(),
                                'dev_type': rec['dev_type'],
                                'services': dev.get_services_list(),
                                'registration_date': datetime.datetime.now()}
                        devices_db.send(post)

            elif rec['command'] == 'send2dev':
                pipe.send(devices_dict[rec['dev_name']].talk(rec['message']))
            elif rec['command'] == 'services':
                pipe.send(devices_dict[rec['dev_name']].get_services_list())
            elif rec['command'] == 'devs':
                devices_names = []
                for dev in devices_dict:
                    devices_names.append(dev)
                pipe.send(devices_names)
            else:
                pipe.send('Unrecognized command')

        if datetime.datetime.now().minute != lastMinute:
            jobs = schedule.checkJobs()
            for job in jobs:
                devices_dict[job['dev']].talk(job['message'])

if __name__ == "__main__":
    main()
