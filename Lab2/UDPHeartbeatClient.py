# UDPPingerClient.py
from socket import *
import time


def ping(host, port):
    serverName = host
    serverPort = port
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    while True:
        time1 = time.time()
        outputs = 'Heartbeat ' + str(time1)
        clientSocket.sendto(outputs.encode(), (serverName, serverPort))
        time.sleep(10)


if __name__ == '__main__':
    ping('127.0.0.1', 12000)
