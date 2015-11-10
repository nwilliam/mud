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
        self.world = WorldManager()
        
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
        if len(msg) > 16 or len(msg) < 3 or ' ' in msg.strip():
            client.Tell('That name is not acceptable, please try again.')
            return
        
        if msg.title() in [c.Name() for c in self.clients]:
            client.Tell('Name is use, please try another.')
            return
        
        #Try to Unpickle it.
        with open('persist/players/%s.name' % msg.title()) as f:
            body = pickle.load(f)
            
        if body:
            client.body = body
        else:    
            client.body = Body(client,name=msg,location=self.default_room.address)
        
        client.body.Move(self.default_room.address)
        client.body.GetRoom().AddToContents(client.body)
        client.Tell('Welcome, %s.' % client.body.Name())
        client.body.GetRoom().Tell('%s just arrived.' % client.body.Name())
        client.Tell(client.body.GetView())
        client.LoginDone = True
            
            
    def onClose(self,client, reason):
        if client in self.clients:
            client.GetRoom().Tell('%s just left.' % client.body.Name())
            client.GetRoom().RemoveFromContents(client.body)
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