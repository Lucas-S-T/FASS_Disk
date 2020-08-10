import json
import ssl
from file_request import file_request
from http import HttpPacket
from args import args
from process_fass import process_fass

context = ssl.SSLContext()
context.load_cert_chain(certfile=args.certfile, keyfile=args.certkey)


def handler_connection(conn, addr):

    req = context.wrap_socket(conn, server_side=True)

    v = req.read(len=4096)
    if len(v) > 0:
        if v.startswith(b"FASS"):
            obj = json.loads(str(v, "utf-8")[4:])
            process_fass(req, addr, obj)

        else:

            pack = HttpPacket().parseRequest(v.decode("utf-8"))
            file_request(req, pack)

    conn.close()
