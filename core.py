import multiprocessing as mp
import datetime
from system import scheduleChecker
from system import communicationModule as cm
from system import loginService as ls
from system import schedueService as ss
from webapp import httpserver
from system.interprocess_communication import Webapp2CoreKeys, Webapp2CoreMessages, Core2WebappMessages, Core2WebappKeys
from system.interprocess_communication import Core2CommunicationModuleKeys, Core2CommunicationModuleValues


def main():
    p_conn, c_conn = mp.Pipe()
    p = mp.Process(target=cm.main, args=(c_conn,))
    p.start()
    print(p_conn.recv())
    login = ls.LoginService()
    #login.welcome()
    scheduler = ss.ScheduleService(p_conn)
    schedule_checker = scheduleChecker.ScheduleChecker()
    last_minute = datetime.datetime.now().minute

    print('Tworze serwer webowy')
    web_p_conn, web_c_conn = mp.Pipe()
    web_p = mp.Process(target=httpserver.main, args=(web_c_conn, ))
    web_p.start()
  #  print(web_p_conn.recv())
  #  print(web_p_conn.recv())

    while True:
        '''
        s = input()
        if s == "close":
            print("Wychodze")
            break
        elif s == "login":
            login.welcome()
        elif s == "logout":
            login.logout()
        elif s == "grant":
            if login.check_privilege("admin"):
                usr = input("Which user?")
                priv = input("Which privilege?")
                login.grant_privilege(usr, priv)
        elif s == "revoke":
            if login.check_privilege("admin"):
                usr = input("Which user?")
                priv = input("Which privilege?")
                login.revoke_privilege(usr, priv)
        elif s == "add_device":
            if login.check_privilege("add"):
                dev = input("Device port? ")
                p_conn.send({'command': 'register_device', 'dev_type': 'serial', 'dev_port': dev})
            else:
                print("You do not have access to this. Ask your admin.")
        elif s == 'services':
            if login.check_privilege("list"):
                dev = input("Which device?")
                p_conn.send({'command': 'devs'})
                devices = p_conn.recv()
                if dev in devices:
                    if login.check_privilege("dev_"+dev):
                        p_conn.send({'command': 'services', 'dev_name': dev})
                    else:
                        print("You do not have permission to touch this")
                else:
                    print("The device does not exist.")
                    print("Use <devices_list> to get the list of devices.")
            else:
                print("You do not have access to this. Ask your admin.")
        elif s == 'devices_list':
            if login.check_privilege("list"):
                p_conn.send({'command': 'devs'})
                devices = p_conn.recv()
                for i in devices:
                    print(i)
            else:
                print("You do not have access to this. Ask your admin.")
        elif s == "send":
            if login.check_privilege("send"):
                dev = input("Device? ")
                com = input("Service? ")
                p_conn.send({'command': 'devs'})
                devices = p_conn.recv()
                if dev in devices:
                    if login.check_privilege("dev_" + dev):
                        p_conn.send({'command': 'send2dev', 'dev_name': dev, 'message': com})
                    else:
                        print("You do not have access to this device!")
                else:
                    print("Usage: send <device> <service>")
                    print("Use <devices_list> for the list of available devices.")
                    print("Use <services <device>> for the list of available services")
            else:
                print("You do not have access to this. Ask your admin.")
        elif s == "scheduler":
            scheduler.welcome()
        else:
            print("Available commands: close, login, logout, add_device, devices_list, services, send, scheduler")
            print("Admin commands: grant, revoke")
            """if login.check_privilege("send")
                p_conn.send({'command': 'send2dev', 'dev_name': dev_name, 'message': s})"""
        if p_conn.poll(10):
            print(p_conn.recv())
        else:
            print("timed out")
        '''
        web_received = web_p_conn.recv()
        print('core - cos dostalem')
        if web_received:
            if web_received[Webapp2CoreKeys.COMMAND] == Webapp2CoreMessages.GET_DEVICES:
                print('core - to tak komenda')
                p_conn.send({Core2CommunicationModuleKeys.COMMAND: Core2CommunicationModuleValues.DEVS})
                devices = p_conn.recv()
                print("Zarejestrowano ", len(devices), 'urzadzen')
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
                scheduler.quick_register(web_received[Webapp2CoreKeys.TASK])

        if datetime.datetime.now().minute != last_minute:
            jobs = schedule_checker.checkJobs()
            for job in jobs:
                #devices_dict[job['dev']].talk(job['com'])
                p_conn.send({Core2CommunicationModuleKeys.COMMAND: Core2CommunicationModuleValues.SEND2DEV,
                             Core2CommunicationModuleKeys.DEV_NAME: job['dev'],
                             Core2CommunicationModuleKeys.MESSAGE: job['com']})
            scheduleChecker.set_timestamp()
            last_minute = datetime.datetime.now().minute

    p.kill()
    exit()


if __name__ == '__main__':
    main()
