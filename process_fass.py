import json
import os
import sys
import threading
import time
import fass_protocol
from args import args
from disk import get_size


def process_fass(conn, addr, obj):

    if addr[0] != args.serveraddr:

        j = {"op": 5}
        conn.send(b'FASS'+bytes(json.dumps(j), "utf-8"))
        conn.close()
        return

    if obj["op"] == 10:
        process_file(conn, addr, obj)
        conn.close()
        return

    if obj["op"] == 12:
        process_bye(conn, addr, obj)
        conn.close()
        return

    if obj["op"] == 13:
        process_disk_info(conn, addr, obj)
        conn.close()
        return




def process_bye(conn, addr, obj):

    fass_protocol.connected = False

    print("Server wants disconnect. Goodbye.")

    conn.send(b'FASS'+bytes(json.dumps(obj), "utf-8"))

    sys.exit(0)


def process_disk_info(conn, addr, obj):

    df = get_size(args.path)

    obj = {"op": 14, "data": {"free": df[0], "total": df[1], "used": df[2]}}

    conn.send(b"FASS"+bytes(json.dumps(obj), "utf-8"))


def process_file(conn, addr, obj):

    files = []
    dirs = []

    for f in os.scandir(args.path+"/"+obj["data"]["path"]):
        if f.is_dir():
            dirs.append(f.name)
        else:
            files.append(f.name)

    obj = {"op": 11, "data": {"files": files, "dirs": dirs}}

    conn.send(b"FASS"+bytes(json.dumps(obj), "utf-8"))
    conn.close()

