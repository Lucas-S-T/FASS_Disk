class HttpPacket:

    def __init__(self):
        self.headerStr = ""
        self.method = ""
        self.remainBytes = ""
        self.path = ""
        self.version = ""
        self.headers = {}

    def parseRequest(self, reqstr):

        rd = reqstr.split("\r\n\r\n")

        self.headerStr = rd[0]
        self.remainBytes = rd[1]

        hr = rd[0].split("\r\n")

        fl = hr[0].split(" ")

        self.method = fl[0]
        self.path = fl[1]
        self.version = fl[2]

        for h in hr[1:]:
            kv = h.replace(": ", ":").split(":")
            self.headers[kv[0]] = kv[1]

        return self
