from system import mongoCollection
from datetime import datetime
from operator import mod, eq


class ScheduleChecker:
    def __init__(self):
        self.__task_base = mongoCollection.MongoCollection("tasks")
        self.__lastCompleted = {}

    def checkJobs(self):
        toRet = []
        now = datetime.now()
        jobs = self.__task_base.getAll()
        for job in jobs:
            op = None
            if job['modifier'] == 'at':
                op = eq
            elif job['modifier'] == 'every':
                op = mod

            now_reduced = None
            if job['unit'] == 'minute':
                now_reduced = {'hour': now.hour, 'minute': now.minute}
            elif job['unit'] == 'hour':
                now_reduced = {'day': now.day, 'hour': now.hour}
            elif job['unit'] == 'day':
                now_reduced = {'month': now.month, 'day': now.day}
            elif job['unit'] == 'month':
                now_reduced = {'year': now.year, 'month': now.month}
            elif job['unit'] == 'year':
                now_reduced = {'year': now.year}
            else:
                print("Something went wrong while reading an entry.")
                continue

            if op(getattr(now, job['unit']), int(job['number'])) and \
                    (job['name'] not in self.__lastCompleted or self.__lastCompleted[job['name']] is not now_reduced):
                toRet.append({'dev': job['device'], 'com': job['command']})
                self.__lastCompleted[job['name']] = now_reduced

        return toRet
