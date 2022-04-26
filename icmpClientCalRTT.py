from socket import *
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8


def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0
    while count < countTo:
        thisVal = (string[count + 1]) * 256 + (string[count])
        csum += thisVal
        csum &= 0xffffffff
        count += 2
    if countTo < len(string):
        csum += (string[len(string) - 1])
        csum &= 0xffffffff
    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer


def receiveOnePing(mySocket, ID, timeout, destAddr):
    global rtt_min, rtt_max, rtt_sum, rtt_cnt
    timeLeft = timeout
    while 1:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        if whatReady[0] == []:  # Timeout
            return (None, None)
        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)
        # Fill in start
        # Fetch the ICMP header from the IP packet
        icmpHeader = recPacket[20:28]
        # check size
        pktFormat = 'bbHHhd'
        pktSizeWithData = struct.calcsize(pktFormat)

        pktFormat = 'bbHHh'
        pktSizeHeader = struct.calcsize(pktFormat)
        # print("pktSize", pktSize)
        icmpType, code, mychecksum, packetID, sequence = struct.unpack("bbHHh", icmpHeader)
        data = struct.unpack("d", recPacket[28: 28 + pktSizeWithData - pktSizeHeader])

        # Precisely, the type of the list should be
        # [(float, (integer, integer, integer, integer, integer, double))].
        # The first element of the tuple should be a float,
        # and should be the delay of the ping in milliseconds. The second element of the
        # tuple should be a 6-tuple, in which each element corresponds to an ICMP field from the pong
        # packet (response) from the server.
        # In order, they should be (type, code, checksum, ID, sequence, number, data).
        if icmpType == 0 and packetID == ID:
            bytesInDouble = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
            rtt = (timeReceived - timeSent) * 1000

            rtt_cnt += 1
            rtt_sum += rtt
            rtt_min = min(rtt_min, rtt)
            rtt_max = max(rtt_max, rtt)

            return rtt, (icmpType, code, mychecksum, ID, sequence, data[0])

        # Fill in end
        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            print("request timed out")
            return None, None


def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    myChecksum = 0
    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)
    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        # Convert 16-bit integers from host to network byte order
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data
    mySocket.sendto(packet, (destAddr, 1))  # AF_INET address must be tuple, not str

    # Both LISTS and TUPLES consist of a number of objects
    # which can be referenced by their position number within the object.


def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")
    # SOCK_RAW is a powerful socket type. For more details: http://sockraw.org/papers/sock_raw
    mySocket = socket(AF_INET, SOCK_RAW, icmp)
    myID = os.getpid() & 0xFFFF  # Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    result = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()
    return result


def ping(host, timeout=1):
    global rtt_min, rtt_max, rtt_sum, rtt_cnt
    rtt_min = float('+inf')
    rtt_max = float('-inf')
    rtt_sum = 0
    rtt_cnt = 0
    cnt = 0  # as range(0, 5) below
    raceNum = 0
    # timeout=1 means: If one second goes by without a reply from the server,
    # the client assumes that either the client's ping or the server's pong is lost
    dest = gethostbyname(host)
    resps = []
    print("Pinging " + dest + " using Python:")
    print("")
    # Calculate vars values and return them
    # Send ping requests to a server separated by approximately one second
    for i in range(0, 5):
        cnt += 1
        result = doOnePing(dest, timeout)
        resps.append(result)
        print(result)
        time.sleep(1)  # one second

    print( "Ping lost rate calculation:")
    print("\tpackage: sent = 10, receive =", str(rtt_cnt), "lost =", str(10 - rtt_cnt),
          "(", str(int((10 - rtt_cnt) * 100 / 10)), "% lost rate)")

    if cnt != 0:
        print('--- {} ping statistics ---'.format(host))
        print('{} packets transmitted, {} packets received, {:.1f}% packet loss'.format(cnt, rtt_cnt, 100.0 - rtt_cnt
                                                                                        * 100.0 / cnt))
    if rtt_cnt != 0:
        print('round-trip min/avg/max {:.3f}/{:.3f}/{:.3f} ms'.format(rtt_min, rtt_sum / rtt_cnt, rtt_max))

    return resps


if __name__ == '__main__':
    # ping("127.0.0.1")
    ping('google.co.il')
