import socket
import threading

from args import args
from sock_connection import handler_connection


def start_socket():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", args.port))
        s.listen(5)

        while True:

            conn, addr = s.accept()

            threading.Thread(target=handler_connection, args=(conn, addr)).start()
            pass
