'''
Created on Nov 4, 2015

@author: nwilliams


I need to do a lot of things to get this thing working.
@TODO: Create Rooms object.
@TODO: Create a Container Mixin class.
'''
from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS
from twisted.internet import reactor

from server import Server


class MudClient(WebSocketServerProtocol):
    def onOpen(self):
        self.isAdmin = True
        self.server = Server
        self.LoginDone = False
        self.body = None
        Server.onOpen(self)
    
    def onLogin(self):
        pass
    
    def onMessage(self,msg,isBinary):
        if not self.LoginDone:
            self.server.onLogin(self,msg)
        elif msg.startswith("'"):
            self.server.Wall('%s says, "%s"' % (self.body.Name(),msg.strip("'")))
        elif msg in 'lL':
            self.Tell(self.body.location.GetView(self.body))
        
    
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
