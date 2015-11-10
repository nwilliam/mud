'''
Created on Nov 4, 2015

@author: nwilliams
'''
import pickle

from models.baseobject import BaseObject
from models.body import Body
from models.exit import CardinalExit, Exit
from models.room import Room
from world.world import WorldManager


class ServerClass(object):
    '''
    Only one instance of this class needed.  Keeps track of everyone/everything
    that is connected.  Also handles Broadcasts.
    '''

    def __init__(self):
        self.clients = []
        self.world = WorldManager(self)
        
        with open('persist/world/rooms/staff/default/000000.room') as f:
            self.default_room=pickle.load(f)
        
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