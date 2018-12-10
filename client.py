import sys
import socket


ADDR = sys.argv[1]
OPT = sys.argv[2]
PARSED_ADDR = ADDR.split(':')
CONN_ADDR = (PARSED_ADDR[0], int(PARSED_ADDR[1]))


c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect(CONN_ADDR)


def get(path):
    response = ''
    headers = "GET {0} HTTP/1.0\r\nHost: {1}\r\n\r\n".format(path, ADDR)

    c.send(headers)
    while True:
        recv = c.recv(1024)
        if not recv:
            break
        response += recv

    return response


a = get("/api/netname/14")
print(a)


c.close()
