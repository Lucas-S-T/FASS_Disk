import asyncio
import signal
import sys
import threading

from fass_protocol import identify, bye, connected
from socket_host import start_socket
import args


async def main():

    threading.Thread(target=start_socket).start()
    identify()


def disconnect(sig, frame):

    if connected:
        bye()
    sys.exit(0)


signal.signal(signal.SIGINT, disconnect)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())



