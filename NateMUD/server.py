'''
Created on Nov 4, 2015

@author: nwilliams
'''
import pickle

from models.body import Body
from models.baseobject import BaseObject
from models.room import Room

class ServerClass(object):
    '''
    Only one instance of this class needed.  Keeps track of everyone/everything
    that is connected.  Also handles Broadcasts.
    '''

    def __init__(self):
        self.clients = []
        self.default_room = Room(title='Welcome Room', desc='A small desk with a welcome sign sits in the middle of a lushly carpeted, dark-wood paneled room. A raging fire burns in the hearth.')
        self.default_room.AddToContents(BaseObject('goddamned monkey',desc='This goddamned monkey keeps running the fuck around.  Someone seriously need to shoot this little asshole.'))
        self.default_room.AddToContents(BaseObject('raging fire',desc='A warm fire crackles away in the hearth, lending light and warmth to the already cozy room.',isVisible=False))
        self.default_room.AddToContents(BaseObject('hearth',desc='A warm fire crackles away in the hearth, lending light and warmth to the already cozy room.',isVisible=False))
        self.default_room.AddToContents(Body(name='Arthur', pretitle='Sir',posttitle=', Vogon Poet-Lauriete'))
        self.default_room.Persist()
        
    def onOpen(self,client):
        if not client in self.clients:
            self.WallAdmin('Registered Client: %s' % client.peer)
            self.clients.append(client)
            print 'Registered Client: %s' % client.peer
        
        if not client.LoginDone:
            client.Tell('Enter a name:')
    
    def onLogin(self,client,msg):
        for c in self.clients:
            if not c.body:
                continue
            
            if c.body.Name == msg.title() or len(msg)>16 or len(msg) < 3:
                client.Tell('That name is not acceptable, please try again.')
                return

            
        client.Tell('Welcome, %s.' % msg)
        client.body = Body(client,name=msg,location=self.default_room)
        client.body.location.AddToContents(client.body)
        client.Tell(client.body.GetView())
        client.LoginDone = True
            
            
    def onClose(self,client, reason):
        if client in self.clients:
            self.clients.remove(client)
            self.WallAdmin('Deregistered Client: %s, %s' % (client.peer, reason))
            print 'Deregistered Client: %s, %s' % (client.peer, reason)
        
    def WallAdmin(self,message):
        for c in self.clients:
            if c.isAdmin:
                c.Tell(message)
                
    def Wall(self,message):
        for c in self.clients:
            c.Tell(message)
    
    def ReportError(self,err):
        self.WallAdmin(err)          

Server = ServerClass()    