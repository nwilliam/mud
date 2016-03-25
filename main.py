"""
Created on Nov 4, 2015

@author: nwilliams

"""
import sys

from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS
from twisted.internet import reactor

from channels.channel import UtilityChannel
from server import Server


class MudClient(WebSocketServerProtocol):
    def __init__(self):
        self.isAdmin = False
        self.server = Server
        self.LoginDone = False
        self.body = None
        super(MudClient, self).__init__()

    def onOpen(self):
        self.server.onOpen(self)

    def onLogin(self):
        pass

    def onMessage(self, msg, isBinary):
        self.server.onMessage(self, msg)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.server.onClose(self, reason)

    def Tell(self, msg):
        # Le Hack.
        msg = msg.replace('\n', '<br />')
        self.sendMessage(msg)


class MudServerFactory(WebSocketServerFactory):
    protocol = MudClient

    def __init__(self, url):
        WebSocketServerFactory.__init__(self, url)


if __name__ == '__main__':
    try:
        address = 'ws://0.0.0.0:%s' % os.environ['PORT']
    except:
        try:
            address = sys.argv[1]
        except:
            address = 'ws://0.0.0.0:9000'
    print "Server Factory Running on {}".format(address)
    factory = MudServerFactory(address)
    listenWS(factory)
    reactor.run()
