__author__ = 'dbshch'
# !/usr/bin/python
import socket


class NetServer(object):
    def tcpServer(self, l):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 9527))
        sock.listen(5)

        while True:
            clientSock, (remoteHost, remotePort) = sock.accept()
            print("[%s:%s] connect" % (remoteHost, remotePort))
            recvData = clientSock.recv(1024).decode("utf-8")
            l[7] = int(recvData)
            while l[8] == 0:
                pass
            l[8] = 0
            pic = open("./pics/pic" + recvData + ".jpg", "rb")
            snd = pic.read(960)
            while snd:
                sendDataLen = clientSock.send(snd)
                snd = pic.read(960)
            print("recvData: ", recvData)
            print("sendDataLen: ", sendDataLen)
            pic.close()
            clientSock.close()


if __name__ == "__main__":
    netServer = NetServer()
    netServer.tcpServer()
