import argparse

parser = argparse.ArgumentParser(description="FASS Storage Server")
parser.add_argument("port", type=int, help="FASS Storage Server Port")
parser.add_argument("certfile", type=str, help="Certificate file")
parser.add_argument("certkey", type=str, help="Certificate Key file")
parser.add_argument("serveraddr", type=str, help="FASS Data Server Address")
parser.add_argument("serverport", type=int, help="FASS Data Server Port")
parser.add_argument("servertoken", type=str, help="FASS Data Server Token")
parser.add_argument("name", type=str, help="FASS Storage Server Name")
parser.add_argument("path", type=str, help="FASS Storage Server Path")

args = parser.parse_args()
