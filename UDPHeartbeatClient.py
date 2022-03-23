# UDPPingerClient.py
from socket import *
import time


def ping(host, port):
    serverName = '127.0.0.1'
    serverPort = 12000
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    while True:
        time1 = time.time()
        outputdata = 'Heartbeat ' + str(time1)
        clientSocket.sendto(outputdata.encode(), (serverName, serverPort))
        time.sleep(10)


if __name__ == '__main__':
    resps = ping('127.0.0.1', 12000)
    print(resps)
