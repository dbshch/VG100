import socket
import re
from multiprocessing import Process, Manager, Queue


def send(msg, data):
    i = 0
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
            d=[addr[0]]
            if data:
                s.close()
                d.append(data)
                return d


def netService(a, cmd):
    while True:
        data = listen()
        print(data[1].decode("utf-8")[0])
        if data[1].decode("utf-8")[0] == 'd':
            dry = ['Not dry', 'Dry', 'Too dry']
            send('{"Temperature":%d,"Humidity":%d,"Dry Status":"%s","Light":%d}' % (a[0], a[1], dry[a[2]], a[3]), data)
        else:
            send("a", data)


def add(l, cmd):
    for i in range(4):
        l.append(i)



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

