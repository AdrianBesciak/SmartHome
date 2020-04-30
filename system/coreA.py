import multiprocessing as mp
import communicationModule as cm
import loginService as ls


def main():
    print("Type port of the device in /dev/ dictionary")
    dev_port = input()
    p_conn, c_conn = mp.Pipe()
    p = mp.Process(target=cm.main, args=(c_conn,))
    p.start()
    p_conn.send({'command': 'register_device', 'dev_type': 'serial', 'dev_port': dev_port})
    dev_name = p_conn.recv()
    login = ls.LoginService()
    login.welcome()

    while True:
        s = input()
        if s == "close":
            print("Wychodze")
            break
        elif s == "login":
            s = input("Username? ")
            login.login(s)
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
                if dev in devices and login.check_privilege("dev_"+dev):
                    p_conn.send({'command': 'services', 'dev_name': dev})
                else:
                    print("The device does not exist or you do not have permission to touch it")
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
        else:
            print("Available commands: close, login, logout, devices_list, services, send")
            print("Admin commands: grant, revoke")
            """if login.check_privilege("send")
                p_conn.send({'command': 'send2dev', 'dev_name': dev_name, 'message': s})"""
        if p_conn.poll(10):
            print(p_conn.recv())
        else:
            print("timed out")

    p.kill()
    exit()


if __name__ == '__main__':
    main()
