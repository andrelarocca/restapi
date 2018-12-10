import sys
import socket
import json


ADDR = sys.argv[1]
OPT = int(sys.argv[2])
PARSED_ADDR = ADDR.split(':')
CONN_ADDR = (PARSED_ADDR[0], int(PARSED_ADDR[1]))


def get(path):
    response = ''
    headers = "GET {0} HTTP/1.0\r\nHost: {1}\r\nContent-Type: application/json\r\n\r\n".format(path, ADDR)

    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect(CONN_ADDR)
    c.send(headers)
    while True:
        recv = c.recv(1024)
        if not recv:
            break
        response += recv
    c.close()

    body = None
    s = response.split("\r\n\r\n")
    if len(s) > 1:
        payload = s[1]
        body = json.loads(payload)

    if body is not None:
        return body["data"]
    else:
        return body


def netsByIxp():
    output = ""
    for ix, data in ix_nets.iteritems():
        nets_size = str(len(data["nets"]))
        output += u' '.join((str(ix), "\t", data["name"], "\t", nets_size, "\r\n")).encode('utf-8').strip()
    print(output)


def ixpsByNet():
    nets_ix = {}
    for ix, data in ix_nets.iteritems():
        for net in data["nets"]:
            if hasattr(nets_ix, net):
                nets_ix[net]["count"] += 1
            else:
                net_uri = "/api/netname/{0}".format(net)
                nets_ix[net] = {
                    "name": get(net_uri),
                    "count": 1,
                }
    output = ""
    for net, data in nets_ix.iteritems():
        ix_size = str(data["count"])
        output += u' '.join((net, "\t", data["name"], "\t", ix_size, "\r\n")).encode('utf-8').strip()
    print(output)


ix_nets = {}
ix = get("/api/ix")
for i in ix:
    ix_id = str(i["id"])
    uri = "/api/ixnets/{0}".format(ix_id)
    nets = get(uri)

    if nets is None:
        nets = []

    ix_nets[ix_id] = {
        "name": i["name"],
        "nets": map(str, nets),
    }


if OPT == 0:
    ixpsByNet()
elif OPT == 1:
    netsByIxp()
