from system import mongoCollection
from datetime import datetime
from operator import mod, eq


def check_timestamp():
    stamp = open('timestamp.txt', 'r')
    str = stamp.read()
    stamp.close()
    if str == datetime.now().strftime("%Y/%m/%d, %H:%M"):
        return False
    return True


def set_timestamp():
    stamp = open('timestamp.txt', 'w')
    stamp.write(datetime.now().strftime("%Y/%m/%d, %H:%M"))
    stamp.close()


def check_timestamp_delayed():
    now = datetime.now()
    stamp = open('timestamp.txt', 'r')
    then_str = stamp.read()
    stamp.close()
    then = datetime.strptime(then_str, "%Y/%m/%d, %H:%M")
    diff = now - then
    if floor(diff.total_seconds() / 60) > 5:
        return False
    return True


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
                op = lambda a, b: (a % b) == 0

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
                    (job['name'] not in self.__lastCompleted or self.__lastCompleted[job['name']] != now_reduced):
                toRet.append({'dev': job['device'], 'com': job['command']})
                self.__lastCompleted[job['name']] = now_reduced

        return toRet
