# import socket module
import threading
from _thread import start_new_thread
from socket import *
import sys  # In order to terminate the program
from threading import Thread

HOST = "localhost"
print_lock = threading.Lock()


def request_handler(connection_socket):
    print("client {} has connected".format(connection_socket))

    try:
        message = connection_socket.recv(1024)
        print("msg: ", message)
        filename = message.split()[1]
        print("filename: ", message.split()[1])
        f = open(filename[1:])
        # Send one HTTP header line into socket
        outputs = f.read()
        connection_socket.send(bytes('HTTP/1.1 200 OK\r\n\r\n', 'UTF-8'))
        print(outputs)
        # Send the content of the requested file to the connection socket
        for i in range(0, len(outputs)):
            connection_socket.send(outputs[i].encode())
        connection_socket.send("\r\n".encode())
        connection_socket.close()
    except IOError:
        # Send HTTP response message for file not found
        connection_socket.send(bytes("HTTP/1.1 404 Not Found\r\n\r\n", 'UTF-8'))
        # Close the client connection socket
        connection_socket.close()


def webServer(port=6789):
    server_socket = socket(AF_INET, SOCK_STREAM)
    # Prepare a sever socket
    server_socket.bind((HOST, port))
    server_socket.listen(5)
    while True:
        # Establish the connection
        print('Ready to serve...')
        try:
            connection_socket, addr = server_socket.accept()
            start_new_thread(request_handler, (connection_socket,))
        except IOError:
            print('Exit')
            break
    server_socket.close()
    sys.exit()


if __name__ == "__main__":
    webServer(6789)
