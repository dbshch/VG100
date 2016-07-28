__author__ = 'dbshch'
# !/usr/bin/python
import socket


class NetServer(object):
    def tcpServer(self, l):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 9527))  # 绑定同一个域名下的所有机器
        sock.listen(5)

        while True:
            clientSock, (remoteHost, remotePort) = sock.accept()
            print("[%s:%s] connect" % (remoteHost, remotePort))  # 接收客户端的ip, port
            recvData = clientSock.recv(1024).decode("utf-8")
            l[7] = int(recvData)
            while l[8] == 0:
                pass

            pic = open("D:/p2/cam/0.jpg", "rb")
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
