# UDPPingerServer.py
# We will need the following module to generate randomized lost packets
import sys
import time
from socket import *


def serve(port):
    # Create a UDP socket
    # Notice the use of SOCK_DGRAM for UDP packets
    server_socket = socket(AF_INET, SOCK_DGRAM)
    # Assign IP address and port number to socket
    server_socket.bind(('', port))

    while True:
        try:
            message, address = server_socket.recvfrom(1024)
            message = message.decode()
            message = message.split()[1]
            time_diff = time.time() - float(message)
            print("receive RTT:", time_diff)
        except KeyboardInterrupt:
            server_socket.close()
            sys.exit()
        except:
            continue


if __name__ == '__main__':
    serve(12000)
