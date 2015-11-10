'''
Created on Nov 8, 2015

@author: nwilliams
'''
import pickle

from models.body import Body
from models.container import Container
from models.exit import Exit, CardinalExit


class Room(Container):
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
                 address='staff/default/000000.room',**kwargs):
        super(Room,self).__init__(**kwargs)
        self.title=title.title() #lol
        self.desc=desc
        self.contents = list()
        self.size = size
        self.weather = weather
        self.element = element
        self.temperature = temperature
        self.biome = biome
        self.isIndoors = isIndoors
        self.isCovered = isCovered
        self.address = address

    def GetView(self,bodyRequesting=None):
        roomView = '[%s]\n' % self.title
        roomView += '%s ' % self.desc
        if bodyRequesting:
            roomView += self.GetObjectsView()
            roomView += self.GetBodiesView(bodyRequesting)
            roomView += self.GetExitsView()
        return roomView
    
    def GetObjects(self):
        return [obj for obj in self.GetContents() if not isinstance(obj,Body)]
    
    def GetObjectsView(self):
        objShorts = [obj.AShort() for obj in self.GetObjects() if obj.isVisible and not isinstance(obj,CardinalExit)]
        return ('You also see %s.' % self.BuildCommaSeperatedList(objShorts)) if objShorts else ''
    
    def GetBodies(self):
        return [body for body in self.GetContents() if isinstance(body,Body)]
    
    def GetBodiesView(self,bodyRequesting):
        names = [body.FullName() for body in self.GetBodies() if body != bodyRequesting and body.isVisible]
        return ('\nAlso here: %s.' % self.BuildCommaSeperatedList(names)) if names else ''
    
    def GetExits(self):
        return [exitobj for exitobj in self.GetContents() if isinstance(exitobj,(Exit,CardinalExit))]
    
    def GetExitsView(self):
        exits = [ex.Short() for ex in self.GetExits() if isinstance(ex,CardinalExit)]
        return ('\nObvious exits: %s' % self.BuildCommaSeperatedList(exits)) if exits else ''
    
    #def GetCardinalExits(self):
        #return [exitobj for exitobj in self.GetExits() if isinstance(obj,CardinalExit)]

    def BuildCommaSeperatedList(self,listOfStrings):
        listOfStrings = [stri.strip() for stri in listOfStrings]
        if len(listOfStrings) > 1:
            last = listOfStrings.pop()
            returnString = ', '.join(listOfStrings).strip(', ')
            returnString += ' and %s' % last
        else:
            returnString = listOfStrings.pop()
        return returnString
    
    def Persist(self):
        filename = open(self.address,'w')
        pickle.dump(self,filename)
        
    def Destroy(self):
        pass
    
    def Tell(self,msg):
        for being in self.GetBodies():
            if being.client:
                being.Tell(msg)