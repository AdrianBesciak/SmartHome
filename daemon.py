from system import scheduleChecker
from system.interprocess_communication import Core2CommunicationModuleKeys, Core2CommunicationModuleValues

if __name__ == "__main__":
    main()


def executeJobs(jobs):
    from system import communicationModule as cm
    import multiprocessing as mp

    p_conn, c_conn = mp.Pipe()
    p = mp.Process(target=cm.main, args=(c_conn,))
    p.start()
    p_conn.recv()
    for job in jobs:
        p_conn.send({Core2CommunicationModuleKeys.COMMAND: Core2CommunicationModuleValues.SEND2DEV,
                     Core2CommunicationModuleKeys.DEV_NAME: job['dev'],
                     Core2CommunicationModuleKeys.MESSAGE: job['com']})
        p_conn.recv()
    p.kill()


def main():
    if scheduleChecker.check_timestamp_delayed():
        scheduleChecker.set_timestamp()
        ss = scheduleChecker.ScheduleChecker()
        jobs = ss.checkJobs()
        if jobs:
            executeJobs(jobs)
