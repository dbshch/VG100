import socket
import re


def sendDetail():
    i=0
    while True:
        address = ('0.0.0.0', 19000)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(address)
        print(i)
        i+=1
        flg=1
        while flg:
            data, addr = s.recvfrom(2048)
            print(addr[1])
            if data.decode('utf-8')[:6]=='detail':
                flg=0

        s.close()
        addr = ('192.168.1.14', 18000+int(re.findall(r'[0-9]+', data.decode('utf-8'))[0]))
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        msg = '{"a": 1, "b": 2}'
        s.sendto(msg.encode(), addr)
        s.close()

if __name__ == "__main__":
    sendDetail()