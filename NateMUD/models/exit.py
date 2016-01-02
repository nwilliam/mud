'''
Created on Nov 8, 2015

@author: nwilliams
'''

from models.baseobject import BaseObject
from world.world import WorldManager

class Exit(BaseObject):
    '''
    Exits needs an address to go to.
    '''
    def __init__(self, destination=None, departureView='', arrivalView='',**kwargs):
        super(Exit,self).__init__(**kwargs)
        self.destination=destination
        self.departureView=departureView
        self.arrivalView=arrivalView
        
    def DoExit(self,actor):
        last = actor.GetRoom()
        dest = WorldManager.GetRoom(self.destination)
        
        if dest:
            #I need 
            last.RemoveFromContents(actor)
            last.Tell('%s just went %s.' % (actor.Name(),self.Noun()))
        
            dest.Tell('%s just arrived.' % actor.Name())
            dest.AddToContents(actor)
            actor.Move(self.destination)
            actor.Tell(actor.GetView())
        else:
            actor.Tell('A mysterious force blocks your exit.')

    def Desc(self):
        dest = WorldManager.GetRoom(self.destination)
        if dest:
            return 'Through the %s you see...\n%s' % (self.Noun(),dest.GetView())
        else:
            return 'A mysterious fog blocks your view.'
    
    
class CardinalExit(Exit):
    def __init__(self,**kwargs):
        super(CardinalExit,self).__init__(**kwargs)
        

class PathfinderExit(Exit):
    pass