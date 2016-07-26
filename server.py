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

if __name__ == "__main__":
    print(requestDetail('127.0.0.1', 1))