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
        if s == "login":
            s = input("Username? ")
            login.login(s)
        if s == "logout"
            login.logout()
        if 
        if s == 'services':
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
        else:
            if login.check_privilege("send")
                p_conn.send({'command': 'send2dev', 'dev_name': dev_name, 'message': s})
            else:
                print("You do not have access to this. Ask your admin.")
        if p_conn.poll(10):
            print(p_conn.recv())
        else:
            print("timed out")

    p.kill()
    exit()


if __name__ == '__main__':
    main()
