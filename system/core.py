import multiprocessing as mp
import communicationModule as cm


def main():
    print("Type name of the device in /dev/ dictionary")
    dev_name = input()
    p_conn, c_conn = mp.Pipe()
    p = mp.Process(target=cm.main, args=(c_conn,))
    p.start()
    p_conn.send({'command': 'register_device', 'dev_type': 'serial', 'dev_name': dev_name})

    while True:
        s = input()
        if s == "close":
            print("Wychodze")
            break
        if s == 'services':
            p_conn.send({'command': 'services', 'dev_name': dev_name})
        else:
            p_conn.send({'command': 'send2dev', 'dev_name': dev_name, 'message': s})
        if p_conn.poll(10):
            print(p_conn.recv())
        else:
            print("timed out")

    p.kill()
    exit()


if __name__ == '__main__':
    main()
