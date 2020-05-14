import mongoCollection
from multiprocessing import Pipe


class ScheduleService:
    def __init__(self, pipe):
        self.__task_base = mongoCollection.MongoCollection("tasks")
        self.__pipe = pipe
        # structure of a job:
        # name, device, command,
        # modifier(at/every), number, minutes/seconds/days/weeks/months

    def welcome(self):
        keep_looping = True
        while keep_looping:
            task = input("What do you want to do? Available options: add, remove, list: ")
            if task == 'add':
                self.add()
            elif task == 'remove':
                self.remove()
            elif task == 'list':
                self.getAll()
            elif task == 'get':
                self.get()
            else:
                print("Sorry, didn't understand that.")
            r = input("Wanna do something else with the schedule? [Y/N]")
            if r == 'N':
                keep_looping = False

    def add(self):
        name = input("What should the job be called?")
        dev = input("Which device does it use?")
        com = input("What command should be executed?")
        mod = input("Should it be executed at a given time or periodically?")
        unit = input("What time unit are we using?")
        num = input("And how many " + unit + "s?")

        self.__pipe.send({'command': 'devs'})
        devices = self.__pipe.recv()
        if dev not in devices:
            print("This device doesn't exist!")
            return

        self.__pipe.send({'command': 'services', 'dev_name': dev})
        services = self.__pipe.recv()
        if com not in services:
            print("This device does not have given service!")
            return

        if mod not in ['at', 'every']:
            print("Please use at or every for this")
            return

        if unit not in ['year', 'month', 'day', 'hour', 'minute']:
            print("Please use a valid unit! Valid units include year, month, day, hour, minute.")
            return

        job = {
            "name": name,
            "device": dev,
            "command": com,
            "modifier": mod,
            "number": num,
            "unit": unit
        }
        self.__task_base.send(job)
        print("Task added!")

    def remove(self):
        name = input("Which job is to be deleted? All jobs are available with getAll")
        job = self.__task_base.get("name", name)
        if job is None:
            print("This job already doesn't exist.")
        else:
            self.__task_base.remove("name", name)
            print("Job removed!")

    def getAll(self):
        jobs = self.__task_base.getAll()
        for job in jobs:
            print("Name: " + job['name'] + ", device: " + job['device'] + ", command: " + job['command'])
            print("Executed" + job['modifier'] + job['number'] + job['unit'] + 's\r\n')

    def get(self):
        name = input("Which job do you want? All jobs are available with getAll")
        job = self.__task_base.getAll("name", name)
        if job is None:
            print("This job doesn't exist.")
        else:
            print("Name: " + job['name'] + ", device: " + job['device'] + ", command: " + job['command'])
            print("Executed" + job['modifier'] + job['number'] + job['unit'] + 's\r\n')
