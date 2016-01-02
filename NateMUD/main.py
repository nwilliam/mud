'''
Created on Nov 4, 2015

@author: nwilliams


I need to do a lot of things to get this thing working.
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
        self.server.onOpen(self)
    
    def onLogin(self):
        pass
    
    def onMessage(self,msg,isBinary):
        if not self.LoginDone:
            self.server.onLogin(self,msg)
        elif msg.startswith("'"): #say 
            self.server.Wall('%s says, "%s"' % (self.body.Name(),msg.strip("'")))
        
        elif msg.startswith('l'): #look
            if len(msg.split(' ')) > 1:
                for obj in self.body.GetRoom().GetContents():
                    if obj.Noun().lower() == msg.split(' ')[1].lower():
                        print 'Found: %s' % obj.Noun()
                        self.Tell(obj.Desc())
                        break
                else:
                    self.Tell('I don\'t see %s here.' % msg.split(' ')[1])
            else:
                self.Tell(self.body.GetRoom().GetView(self.body))
                
        elif msg.startswith('go'): #go
            splitMsg = msg.split(' ')
            if len(splitMsg) > 1:
                for obj in self.body.GetRoom().ItemContents():
                    if splitMsg[1].lower() == obj.Noun().lower():
                        obj.DoExit(self.body)
                        break
            else:
                self.Tell('Go where?')
                
        else:
            self.Tell('What?  I don\'t understand what "%s" means.' % msg)
                
    
    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.server.onClose(self,reason)
    
    def Tell(self,msg):
        #Le Hack.
        msg = msg.replace('\n','<br />')
        self.sendMessage(msg)

class MudServerFactory(WebSocketServerFactory):
    protocol = MudClient
    
    def __init__(self,url):
        WebSocketServerFactory.__init__(self,url)

if __name__ == '__main__':
    
    factory = MudServerFactory('ws://localhost:9000')
    listenWS(factory)
    reactor.run() #@UndefinedVariable
