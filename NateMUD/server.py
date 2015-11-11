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
        self.world = WorldManager
        
        rooms = Room(title='Welcome Room',desc='A small desk with a welcome sign sits in the middle of a lushly carpeted, dark-wood paneled room. A raging fire burns in the hearth.',address='staff/default/000000')
        rooms.AddToContents(Exit(destination='staff/default/000001',noun='doorway',adjs='stained wooden'))
        rooms.AddToContents(BaseObject(quick='goddamned monkey',desc='This goddamned monkey won\'t stop running around like an asshole.'))
        rooms.AddToContents(Body(name='Arthur',pretitle='Sir',posttitle=', Vogon Poet-Lauriete'))
        rooms.AddToContents(BaseObject(quick='raging fire',desc='This fire burns warmly in its hearth, casting light and comfort into the room.',isVisible=False))
        rooms.AddToContents(BaseObject(quick='wooden desk',desc='A very nice hand-lettered sign that reads "Welcome" sits on the desk.'))
        rooms.Persist()
        
        rooms = Room(title='Hallway',desc='A long woven rug runs the length of the hallway. Oil paintings of people you don\'t care about line the sides.',address='staff/default/000001')
        rooms.AddToContents(Exit(destination='staff/default/000000',noun='doorway',adjs='richly stained'))
        rooms.Persist()
        
        self.default_room = WorldManager.GetRoom('staff/default/000000')
        
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
        
        if msg.title() in [c.body.Name() for c in self.clients if not client]:
            client.Tell('Name is use, please try another.')
            return
        
        body = None
        
        #Try to Unpickle it.
        try:
            with open('persist/players/%s.name' % msg.title()) as f:
                body = pickle.load(f)
        except:
            pass
            
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
            client.body.GetRoom().Tell('%s just left.' % client.body.Name())
            client.body.GetRoom().RemoveFromContents(client.body)
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