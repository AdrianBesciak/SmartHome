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
        elif s == 'services':
            if login.check_privilege("list"):
                p_conn.send({'command': 'services', 'dev_name': dev_name})
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
        elif s.startswith('send'):
            if login.check_privilege("send"):
                tokens = s.split()
                if len(tokens) >= 3:
                    if login.check_privilege("dev_" + tokens[1]):
                        p_conn.send({'command': 'send2dev', 'dev_name': tokens[1], 'message': tokens[2]})
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
