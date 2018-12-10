import sys
import json
from flask import Flask


app = Flask(__name__)
PORT = sys.argv[1]
NET_FILE = sys.argv[2]
IX_FILE = sys.argv[3]
NETIXLAN_FILE = sys.argv[4]


with open(NET_FILE) as net_file:
    net = json.load(net_file)

with open(IX_FILE) as ix_file:
    ix = json.load(ix_file)

with open(NETIXLAN_FILE) as netixlan_file:
    netixlan = json.load(netixlan_file)


@app.route('/api/ix')
def api_ix():
    response = {
        "data": ix["data"]
    }
    return json.dumps(response)


@app.route('/api/ixnets/<ix_id>')
def api_ixnets(ix_id):
    net_ids = []
    for ni in netixlan["data"]:
        if ni["ix_id"] == int(ix_id):
            net_ids.append(ni["net_id"])
    response = {
        "data": net_ids
    }
    return json.dumps(response)


if __name__ == '__main__':
    app.run()
