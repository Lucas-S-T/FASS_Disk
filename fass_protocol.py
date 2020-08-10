import json
import socket
import ssl
import sys
import threading
import time
import uuid

from args import args

myToken = uuid.uuid4().hex

context = ssl.SSLContext()

connected = False
beat_interval = 0


def identify():

    global connected
    global beat_interval

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((args.serveraddr, args.serverport))

        nc = context.wrap_socket(s, server_side=False)

        j = {"op": 3, "data": {"token": args.servertoken, "id": args.name, "my_token": myToken, "my_port": args.port}}

        strn = json.dumps(j)

        nc.sendall(b"FASS"+bytes(strn, "utf-8"))

        dt = nc.read(4096)

        j = json.loads(str(dt[4:], "utf-8"))

        if j["op"] == 5:

            exit("Server return Unauthorized packet.")

        if j["op"] == 9:

            exit("Server return Error packet: "+j["data"]["error"])

        if j["op"] == 4:

            connected = True
            beat_interval = j["data"]["heartbeat"]
            print("Connected to FASS Data Provider, heartbeat interval:", j["data"]["heartbeat"], "ms")
            threading.Thread(target=process_beat).start()

        nc.close()


def process_beat():

    beat_un = False

    global connected
    global beat_interval

    while connected:

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            try:
                s.connect((args.serveraddr, args.serverport))
            except all as e:
                print("Cannot beat... Waiting 30s...")
                time.sleep(30)
                print("Reconnecting...")
                beat_un = True
                break

            nc = context.wrap_socket(s, server_side=False)

            j = {"op": 1}

            nc.sendall(b"FASS"+bytes(json.dumps(j), "utf-8"))
            dt = nc.read(4096)
            j = json.loads(str(dt[4:], "utf-8"))

            if j["op"] == 5:
                connected = False
                beat_un = True
                print("Unauthorized heartbeat, reconnecting...")
                break
            nc.close()
        time.sleep(beat_interval / 1000.0)

    if beat_un:
        identify()
        return


def bye():

    global connected

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.connect((args.serveraddr, args.serverport))
        nc = context.wrap_socket(s, server_side=False)

        j = {"op": 12}

        jstr = json.dumps(j)

        nc.sendall(b"FASS"+bytes(jstr, "utf-8"))

        dt = nc.read(4096)

        j = json.loads(str(dt[4:], "utf-8"))

        if j["op"] == 12:
            connected = False
            exit("Disconnected. Goodbye.")
            sys.exit(0)

        else:
            print("Server not allow disconnect now.")
