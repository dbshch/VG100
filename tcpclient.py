__author__ = 'dbshch'
#!/usr/bin/env python
# -*- coding:utf8 -*-

import socket

class getPic():
    def tcpclient(self, ip, key):
        clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSock.connect((ip, 9527))

        sendDataLen = clientSock.send((str(key)).encode())



        file = open("./static/temp/temp_"+str(key)+".jpg",'wb')
        recvData = clientSock.recv(1024)
        while recvData:
            file.write(recvData)
            recvData = clientSock.recv(1024)
        file.close()
        clientSock.close()

if __name__ == "__main__":
    netClient = getPic()
    netClient.tcpclient(1)