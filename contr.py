import socket
import re
from multiprocessing import Process, Manager, Queue
from homecontr8 import *
from tcpserver import *


def send(msg, data):
    addr = (data[0], 18000 + int(re.findall(r'[0-9]+', data[1].decode('utf-8'))[0]))
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
            d = [addr[0]]
            if data:
                s.close()
                d.append(data)
                return d


def netService(a):
    while True:
        data = listen()
        flg = data[1].decode("utf-8")[0]
        print(flg)
        if flg == 'd':
            dry = ['Not dry', 'Dry', 'Too dry']
            post = '{"Temperature":%d,"Humidity":%d,"Dry Status":"%s","Light":%d}' % (a[0], a[1], dry[a[2]], a[3])
            send(post, data)
        elif flg == 'w':
            a[5] = 1
        elif flg == 'a':
            a[6] = 1
        elif flg == 'l':
            a[4] = 1
        else:
            send("a", data)


if __name__ == "__main__":
    m = Manager()
    l = m.list([0, 0, 0, 0, 0, 0, 0, 0, 0])
    p = Process(target=netService, args=(l,))
    q = Process(target=prog, args=(l,))
    pp = Process(target=NetServer().tcpServer, args=(l,))
    p.start()
    q.start()
    pp.start()
    p.join()
    q.join()
    pp.join()
