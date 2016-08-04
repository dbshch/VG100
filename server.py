import socket
import json

def requestDetail(ip, key):
    addr = (ip, 19000)#send to the 19000 port in the arduino
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    msg = 'detail' + str(key)
    s.sendto(msg.encode(), addr)
    s.close()

    address = ('0.0.0.0', 18000+key)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(address)

    flg=1
    while flg:
        data, addr = s.recvfrom(2048)
        if data:
            flg=0
  
    s.close()
    data = data.decode('utf-8')
    return json.dumps(eval(data), sort_keys=True)


def sendCmd(ip, key, cmd):
    addr = (ip, 19000)  # send to the 19000 port in the arduino
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    msg = cmd;
    s.sendto(msg.encode(), addr)
    s.close()

    address = ('0.0.0.0', 18000 + key)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(address)

    flg = 1
    while flg:
        data, addr = s.recvfrom(2048)
        if data:
            flg = 0

    s.close()
    data = data.decode('utf-8')
    return data


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
                return addr[0]

if __name__ == "__main__":
    print(requestDetail('192.168.1.12', 1))