import multiprocessing as mp
import communicationModule as cm


def main():
    print("Type name of the device in /dev/ divtionary")
    devName = input()
    p_conn, c_conn = mp.Pipe()
    p = mp.Process(target=cm.main, args=(c_conn,))
    p.start()
    p_conn.send('register_device:serial:' + devName)
    '''    
    print("SelfCheck!")
    print("Getting the name of the Arduino module!")
    p_conn.send("getname")
    if p_conn.poll(10):
        print(p_conn.recv())
    else:
        print("Arduino timed out.")
        print("Counting to 9")
    for i in range(10):
        p_conn.send(i)
        print(p_conn.recv())

    print("Check out the echo!")
    print("Write your word, and then the number of repetitions.")
    print("Write \"close\" to exit.")
    '''
    while True:
        s = input()
        if s == "close":
            print("Wychodze")
            break
        if s == 'services':
            p_conn.send(s + ':' + devName)
        else:
            p_conn.send('send2dev:' + devName + ':' + s)
        if p_conn.poll(10):
            print(p_conn.recv())
        else:
            print("timed out")

    p.kill()
    exit()


if __name__ == '__main__':
    main()
