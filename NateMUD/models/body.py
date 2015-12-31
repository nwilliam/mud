'''
Created on Nov 7, 2015

@author: nwilliams
    
    A Body is a Mobile Object (MOB) or a Player.
    
    Should every Body have a client? Yes I think so.  This lets me
    have the ability to possess non-player objects and have them DoStuff.
    There's a lot of things that will be added to a Body, but for
    now we'll just keep the basics and template the rest.
    
    I think I should branch this into subclasses. 
    Body -> Being -> Player
    Body -> Mob
    
    Everything has the ability to have a Client.  Beings will 
    have pretitles and post titles.  How titilating.  Do NPCs and Players have
    anything different?  I think only scripts.  I take that back, I want the
    ability to have environmental scripts on players.
    
    Is there anything different?  Yes, there is.  Persist().  
    
    I think mobs may need to be a subclass for movement and because they don't
    have names.
    
    I'm going to keep self.client in Body.  I want to be able to possess mobs.
    
    I think I want to treat Bodies like BaseObjects.  That way I can call
    all of the BaseObject methods on it if I need to.  I'll just override
    most of them as needed.
    
    All Bodies are Containers.  I'll do this as a Mixin.
    
'''
from models.baseobject import BaseObject
from models.container import Container
from world.world import WorldManager


class Body(BaseObject, Container):
    '''
    Top-level Class inherited by Mob, Being, and Player.
    client=None,name='unnamed',pretitle='',posttitle='',
    desc_string='',location=None,**kwargs
    '''

    def __init__(self, client=None,desc_string='',
                 location='staff/default/000000',**kwargs):
        super(Body,self).__init__(length=20,width=15, height=72, weight=160, **kwargs)
        self.client = client
        self.desc_string = desc_string
        self.location = location #Location needs to be stored as an address. :\
        self.room = None

    def Move(self,destination):
        try:
            newRoom = WorldManager.GetRoom(destination)
        except ValueError:
            print '{} could not move from {} to {}.'.format(
                        self.Noun(),self.location,destination)
            return
        
        self.location = destination
        self.room = newRoom

    def GetRoom(self):
        if self.room:
            if self.room.address == self.location:
                return self.room
        try:
            self.room = WorldManager.GetRoom(self.location)
        except ValueError:
            print '{} failed GetRoom() with location: {}'.format(
                        self.Noun(),self.location)
            self.Move(WorldManager.defaultAddress)
        return self.room
                
    def GetView(self):
        return self.GetRoom().GetView(self)

    def Possess(self,client):
        self.client = client
    
    def Unpossess(self,client):
        self.client = None
        
    def Tell(self,msg,**kwargs):
        # I'm abstracting this a bit higher to reduce calls to
        # Body.Client.Tell() - also this can let me do some
        # formatting higher up if I need to.  Also, we can intercept
        # errors here and not try to do a Tell to a mob.
        if self.client:
            self.client.Tell(msg,**kwargs)
            
    def Persist(self):
        pass
        #BE SURE TO DUMP SELF.ROOM OR YOU RISK SAVING THE WHOLE GODDAMN SHEBANG

    
        
        