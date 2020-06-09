import multiprocessing as mp
import datetime
import time
from system import scheduleChecker
from system import communicationModule as cm
from system import schedueService as ss
from webapp import httpserver
from system.interprocess_communication import Webapp2CoreKeys, Webapp2CoreMessages, Core2WebappMessages, Core2WebappKeys
from system.interprocess_communication import Core2CommunicationModuleKeys, Core2CommunicationModuleValues


def main():
    p_conn, c_conn = mp.Pipe()
    p = mp.Process(target=cm.main, args=(c_conn,))
    p.start()
    p_conn.recv()
    scheduler = ss.ScheduleService(p_conn)
    schedule_checker = scheduleChecker.ScheduleChecker()
    last_minute = datetime.datetime.now().minute

    web_p_conn, web_c_conn = mp.Pipe()
    web_p = mp.Process(target=httpserver.main, args=(web_c_conn, ))
    web_p.start()

    first_loop = True
    while True:
        if first_loop or web_p_conn.poll():
            first_loop = False
            web_received = web_p_conn.recv()
            if web_received[Webapp2CoreKeys.COMMAND] == Webapp2CoreMessages.GET_DEVICES:
                p_conn.send({Core2CommunicationModuleKeys.COMMAND: Core2CommunicationModuleValues.DEVS})
                devices = p_conn.recv()
                web_p_conn.send({Core2WebappKeys.TYPE: Core2WebappMessages.DEVICES,
                                 Core2WebappKeys.DEVICES_LIST: devices})

            elif web_received[Webapp2CoreKeys.COMMAND] == Webapp2CoreMessages.DEV_SERVICES:
                p_conn.send({Core2CommunicationModuleKeys.COMMAND: Core2CommunicationModuleValues.SERVICES,
                             Core2CommunicationModuleKeys.DEV_NAME: web_received[Webapp2CoreKeys.DEV_NAME]})

                web_p_conn.send({Core2WebappKeys.TYPE: Core2WebappMessages.DEV_SERVICES,
                                 Core2WebappKeys.SERVICES_LIST: p_conn.recv()})
            elif web_received[Webapp2CoreKeys.COMMAND] == Webapp2CoreMessages.RUN_SERVICE:
                p_conn.send({Core2CommunicationModuleKeys.COMMAND: Core2CommunicationModuleValues.SEND2DEV,
                             Core2CommunicationModuleKeys.DEV_NAME: web_received[Webapp2CoreKeys.DEV_NAME],
                             Core2CommunicationModuleKeys.MESSAGE: web_received[Webapp2CoreKeys.SERVICE]})

                web_p_conn.send({Core2WebappKeys.TYPE: Core2WebappMessages.DEV_RESPONSE,
                                 Core2WebappMessages.RESPONSE: p_conn.recv()})

            elif web_received[Webapp2CoreKeys.COMMAND] == Webapp2CoreMessages.REGISTER_DEVICE:
                p_conn.send({Core2CommunicationModuleKeys.COMMAND: Core2CommunicationModuleValues.REGISTER_DEVICE,
                            Core2CommunicationModuleKeys.DEV_TYPE: Core2CommunicationModuleValues.SERIAL,
                             Core2CommunicationModuleKeys.DEV_PORT: web_received[Webapp2CoreKeys.DEV_NAME]})
                web_p_conn.send({Core2WebappKeys.TYPE: Core2WebappMessages.DEV_RESPONSE,
                                 Core2WebappMessages.RESPONSE: p_conn.recv()})

            elif web_received[Webapp2CoreKeys.COMMAND] == Webapp2CoreMessages.REGISTER_SCHEDULE:
                str = scheduler.quick_register(web_received[Webapp2CoreKeys.TASK])
                web_p_conn.send({Core2WebappKeys.TYPE: Core2WebappMessages.RESPONSE,
                                 Core2WebappKeys.RESPONSE: str})

        if datetime.datetime.now().minute != last_minute:
            jobs = schedule_checker.checkJobs()
            for job in jobs:
                p_conn.send({Core2CommunicationModuleKeys.COMMAND: Core2CommunicationModuleValues.SEND2DEV,
                             Core2CommunicationModuleKeys.DEV_NAME: job['dev'],
                             Core2CommunicationModuleKeys.MESSAGE: job['com']})
                p_conn.recv()

            scheduleChecker.set_timestamp()
            last_minute = datetime.datetime.now().minute

    p.kill()
    exit()


if __name__ == '__main__':
    main()
