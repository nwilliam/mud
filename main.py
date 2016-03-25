"""
Created on Nov 4, 2015

@author: nwilliams

"""
import sys
import os

from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS
from twisted.internet import reactor

from server import Server


class MudClient(WebSocketServerProtocol):
    def __init__(self):
        self.isAdmin = False
        self.LoginDone = False
        self.body = None
        super(MudClient, self).__init__()

    def onOpen(self):
        Server.onOpen(self)

    def onLogin(self):
        pass

    def onMessage(self, msg, isBinary):
        Server.onMessage(self, msg)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        Server.onClose(self, reason)

    def Tell(self, msg, pre=False):
        # Le Hack.
        msg = msg.replace('\n', '<br />')
        if pre:
            msg = '<span class=\'pre\'>' + msg + '</span>'
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
