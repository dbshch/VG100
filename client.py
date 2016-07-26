import socket
import re


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
            if data:
                s.close()
                return data


if __name__ == "__main__":
    while True:
        data = listen()
        print(data.decode("utf-8")[0])
        if data.decode("utf-8")[0] == 'd':
            send('{"a": 1, "b": 2}', data)
        else:
            send("a", data)
