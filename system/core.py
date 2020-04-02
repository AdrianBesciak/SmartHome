import multiprocessing as mp
import communicationModule as cm


def main():
    p_conn, c_conn = mp.Pipe()
    p = mp.Process(target=cm.main, args=(c_conn,))
    p.start()
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
    while True:
        t = input()
        s = t.split()
        if s[0] == "close":
            print("Wychodze")
            break
        for i in range(int(s[1])):
            p_conn.send(s[0])
            if p_conn.poll(10):
                print(p_conn.recv())
            else:
                print("timed out")

    p.kill()
    exit()


if __name__ == '__main__':
    main()
