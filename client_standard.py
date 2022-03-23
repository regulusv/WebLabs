from socket import *
import time
import sys


def ping(host, port):
    server_name = host
    server_port = port
    client_socket = socket(AF_INET, SOCK_DGRAM)
    resps = []
    raceNum = 0
    max_diff_time = -1
    min_diff_time = 2
    aver_diff_time = 0
    for seq in range(1, 11):
        # Send ping message to server and wait for response back On timeouts, you can use the following to add to
        # resps
        # resps.append((seq, ‘Request timed out’, 0))
        # On successful responses, you should instead record the
        # server response and the RTT (must compute server_reply and rtt properly)
        # resps.append((seq, server_reply, rtt))
        #   Fill in start
        # print("seq: ", seq)
        time1 = time.time()
        outputs = 'Ping ' + str(seq) + " " + str(time1)
        # set time out
        client_socket.settimeout(1)
        # client send to server with output ping
        client_socket.sendto(outputs.encode(), (server_name, server_port))
        try:
            # receive response from server
            modified_message, server_address = client_socket.recvfrom(2048)
            # calculate timeout
            time_diff = time.time() - time1
            print("from", server_name, "response：bytes=", str(len(outputs)), "RTTs:", str(time_diff))
            raceNum += 1
            aver_diff_time += time_diff
            if time_diff > max_diff_time:
                max_diff_time = time_diff
            if time_diff < min_diff_time:
                min_diff_time = time_diff
        except:
            # print("lost " + str(seq))
            resps.append((seq, 'Request timed out', 0))
        # Fill in end
    print(server_name, "Ping lost rate calculation:")
    print("\tpackage: sent = 10, receive =", str(raceNum), "lost =", str(10 - raceNum),
          "(", str(int((10 - raceNum) * 100 / 10)), "% lost rate)")
    if raceNum != 0:
        print("Recorded RTTs:")
        print("\tminimum RTTs =", min_diff_time, "maximum RTTs =", max_diff_time, "average RTTs =",
              aver_diff_time / raceNum)
    return resps


if __name__ == '__main__':
    resps = ping('127.0.0.1', 12000)
    # print(resps)
