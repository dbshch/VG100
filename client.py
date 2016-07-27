import socket
import re
from multiprocessing import Process, Manager, Queue


def send(msg, data):
    i = 0
    addr = ('192.168.1.8', 18000 + int(re.findall(r'[0-9]+', data.decode('utf-8'))[0]))
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(msg.encode(), addr)
    s.close()


def listen():
    i = 0
    while True:
        address = ('0.0.0.0', 19000)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(address)
        print(i)
        i += 1
        flg = 1
        while flg:
            data, addr = s.recvfrom(2048)
            print(addr)
            if data:
                s.close()
                return data


def netService(a, cmd):
    while True:
        data = listen()
        print(data.decode("utf-8")[0])
        if data.decode("utf-8")[0] == 'd':
            send('{"a": ' + a[0] + ', "b": 2}', data)
        else:
            send("a", data)


def add(l, cmd):
    l.append('a')
    while True:
        l[0]='5'



if __name__ == "__main__":
    q = Queue()
    m = Manager()
    cmd='1'
    l = m.list()
    p = Process(target=netService, args=(l, cmd))
    q = Process(target=add, args=(l, cmd))
    p.start()
    q.start()
    p.join()
    q.join()

