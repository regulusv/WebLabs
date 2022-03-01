# import socket module
from socket import *
import sys  # In order to terminate the program

HOST = "localhost"
PORT = 6789


def webServer(port=6789):
    serverSocket = socket(AF_INET, SOCK_STREAM)
    # Prepare a sever socket
    serverSocket.bind((HOST, PORT))
    serverSocket.listen(1)
    while True:
        print("listening")
        connectionSocket, addr = serverSocket.accept()
        try:
            message = connectionSocket.recv(1024)
            print("msg: ", message)
            filename = message.split()[1]
            print("filename: ", message.split()[1])
            f = open(filename[1:])
            # Send one HTTP header line into socket
            outputs = f.read()
            connectionSocket.send(bytes('HTTP/1.1 200 OK\r\n\r\n', 'UTF-8'))
            print(outputs)
            for i in range(0, len(outputs)):
                connectionSocket.send(outputs[i].encode())
            connectionSocket.send("\r\n".encode())
            connectionSocket.close()
        except IOError:
            connectionSocket.send(bytes("HTTP/1.1 404 Not Found\r\n\r\n", 'UTF-8'))
            connectionSocket.send(bytes("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n", 'UTF-8'))
            # Close the client connection socket
            connectionSocket.close()
        serverSocket.close()
        sys.exit()


if __name__ == "__main__":
    webServer(6789)
