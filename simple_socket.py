import time
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
class SimpleEcho(WebSocket):

    def handleMessage(self):
        # echo message back to client
        f = open("status.txt", "r")
        msg=f.read()
        f.close()
        self.sendMessage(msg)

    def handleConnected(self):
        print(self.address, 'connected')

    def handleClose(self):
        print(self.address, 'closed')

# server = SimpleWebSocketServer('', 8000, SimpleEcho)
# server.serveforever()

# def connect():
#     print('in connect')
#     server = SimpleWebSocketServer('', 8000, SimpleEcho)
#     server.serveforever()
#
# def sendFeed(server,feed):
#     server.handleMessage(feed)