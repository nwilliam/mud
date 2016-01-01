'''
Created on Nov 8, 2015

@author: nwilliams
'''
import pickle

from models.baseobject import BaseObject
from models.container import Container
from utils import stringutils


class Room(BaseObject,Container):
    '''
    Room is just that, a room.  Room needs to be a container as well (Mixin).
    Should room be a BaseObject?  I don't think it should.  A room doesn't have
    a noun or adjectives.  
    
    Room needs to hold Exits, room needs to hold Beings, room needs to hold
    Objects.  I think I should have a method to access each of these
    individually, and one to access them together.
    
    Rooms can be created or destroyed.
    
    Rooms need to have views.
    
    Properties of a room: Size, Weather (store this here or on player?),
        Element(s)?, Temperature, Biome, ... I need a word for 'situation'..
        indoors, outdoors, 'exposed'? like a porch?
    '''
    #These are in "largest distance point-to-point", ie:
    #    x----------------------------|
    #    |                            |
    #    |                            |
    #    |                            |
    #    |                            |
    #    |----------------------------y
    # point X to point Y would be the room size in feet.
    room_sizes = {'tiny':4, 'very small':8, 'small':16, 'medium-small':32,
                  'medium':64, 'medium-large':128, 'large':256, 'very_large':512,
                  'huge':1024,'gigantic':2048,'limitless':4096 }


    def __init__(self,title='The Nebula',desc='The fires of creation around you, writhing gases and colors stretching into infinity.  You float through the awe-inspiring display with nary a way to escape or exit.',
                 contents=None,size=room_sizes['medium'],weather=None,element=None,
                 temperature=72,biome='deciduous forest',isIndoors=False,isCovered=False,
                 address='staff/default/000000',**kwargs):
        super(Room,self).__init__(**kwargs)
        self.title=title.title() #lol
        self.desc=desc
        self.size = size
        self.weather = weather
        self.element = element
        self.temperature = temperature
        self.biome = biome
        self.isIndoors = isIndoors
        self.isCovered = isCovered
        self.address = address

    def Title(self):
        return self.title

    def GetView(self,bodyRequesting=None):
        '''
        Still not 100% sure I like this.  It's.. pretty hardcoded.
        Eventually I would like to do things like,
        "[Room]
        This is a room.  There is stuff in it.  It has things, and
        maybe other things.  I don't know what else to say here
        but I need a few lines.  Bob leans against the bar, Fred
        is sitting on a barstool.  Frank and Steve are also here.
        You also see a goddamned monkey hiding behind the couch 
        and a wooden spork on the floor.
        Obvious Exits: North, South, and East
        "
        '''
        roomView = '[%s]\n' % self.Title()
        roomView += '%s ' % self.Desc()
        if bodyRequesting:
            items = [it.AShort() for it in self.ItemContents() if not it.isa('CardinalExit') and it.isVisible]
            items += [be.AShort() for be in self.BeingContents() if be.isVisible and not be.name]
            cards = [item.Short() for item in self.ItemContents() if item.isa('CardinalExit')]
            people = [be.FullName() for be in self.BeingContents() if be.isVisible and be.name and be != bodyRequesting]
            
            if len(people) > 1:
                verb = 'are'
            else:
                verb = 'is'
            roomView += ('%s %s also here.\n' % (stringutils.BuildCommaSeperatedList(people),verb) if people else '')
            roomView += ('You also see %s.\n' % stringutils.BuildCommaSeperatedList(items) if items else '')
            roomView += ('Obvious Exits: %s\n' % stringutils.BuildCommaSeperatedList(cards) if cards else '')
        return roomView

    def BeingContents(self):
        return filter(lambda x: x.isa('Being'),self.GetContents())
    
    def ItemContents(self):
        return filter(lambda x: not x.isa('Being'),self.GetContents())
 
    def Persist(self):
        filename = open('./persist/world/rooms/' + self.address + '.room','w')
        pickle.dump(self,filename)
        
    def Destroy(self):
        pass
    
    def Tell(self,msg):
        for being in self.BeingContents():
            if being.client:
                being.Tell(msg)