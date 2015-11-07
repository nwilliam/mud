'''
Created on Nov 4, 2015

@author: nwilliams


I need to do a lot of things to get this thing working.
@TODO: Create Rooms object.
@TODO: Create a Body object to be in the room.
@TODO: Create a Container Mixin class.
'''
from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS
from twisted.internet import reactor

from server import Server


class MudClient(WebSocketServerProtocol):
    def onOpen(self):
        self.isAdmin = True
        self.name = None
        self.server = Server
        self.LoginDone = False
        Server.onOpen(self)
        
    def onLogin(self):
        pass
    
    def onMessage(self,msg,isBinary):
        if not self.LoginDone:
            self.server.onLogin(self,msg)
        else:
            self.server.Wall('%s: %s' % (self.name,msg))
    
    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.server.onClose(self,reason)
    
    def Tell(self,msg):
        self.sendMessage(msg)

class MudServerFactory(WebSocketServerFactory):
    protocol = MudClient
    
    def __init__(self,url):
        WebSocketServerFactory.__init__(self,url)

if __name__ == '__main__':
    factory = MudServerFactory('ws://localhost:9000')
    listenWS(factory)
    reactor.run() #@UndefinedVariable
