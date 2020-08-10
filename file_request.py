import os

import magic

from fass_protocol import myToken
from args import args


def file_request(req, packet):
    if not "Token" in packet.headers:
        req.write(b"HTTP/1.1 500 Token Not Provided\r\nServer: FASS\r\n\r\n")
        return

    if not packet.headers["Token"] == myToken:
        req.write(b"HTTP/1.1 500 Invalid Token\r\nServer: FASS\r\n\r\n")
        return

    if ".." in packet.path:
        req.write(b"HTTP/1.1 400 Invalid Path\r\nServer: FASS\r\n\r\n")
        return

    if not os.path.isfile(args.path + packet.path):
        req.write(b"HTTP/1.1 404 File Not Exist\r\nServer: FASS\r\n\r\n")
        return

    f = open(args.path + packet.path, "rb")

    f.seek(0, 2)
    leng = f.tell()
    f.seek(0)

    mime = magic.Magic(mime=True)
    type = mime.from_file(args.path + packet.path)

    if "Range" in packet.headers:

        rangestr = packet.headers["Range"]
        range = rangestr.split("=")[1].split("-")

        startr = int(range[0])
        if range[1] != "":
            end = int(range[1])
        else:
            end = leng
        amount = end - startr + 1

        res = "HTTP/1.1 206 Partial Content\r\nServer: FASS\r\nAccept-Ranges: bytes\r\nContent-Range: bytes " + str(startr) + "-" + str(
            end) + "/" + str(leng) + "\r\nContent-Type: " + type + "\r\nContent-Length: " + str(
            amount) + "\r\n\r\n"
        req.write(bytes(res, "utf-8"))

        f.seek(startr)

        while amount > 0:

            if amount > 4096:
                data = f.read(4096)
                amount -= 4096
            else:
                data = f.read(amount)
                amount = 0

            req.write(data)

    else:

        res = "HTTP/1.1 200 OK\r\nServer: FASS\r\nAccept-Ranges: bytes\r\nContent-Type: " + type + "\r\nContent-Length: " + str(
            leng) + "\r\n\r\n"

        req.write(bytes(res, "utf-8"))

        while True:

            a = f.read(4096)
            if len(a) == 0:
                req.close()
                break
            req.write(a)
