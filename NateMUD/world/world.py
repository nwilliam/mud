'''
Created on Nov 8, 2015

@author: nwilliams
'''
import pickle

#from server import Server

class RoomManager(object):
    '''
    This thing is scary.
    
    There's only one WorldManager instance.
    '''
    def __init__(self):
        self.rooms = dict()
    
    def GetRoom(self,address):
        
        room = self.rooms.get(address,None)
        
        if not room:
            #Try to unpickle it.
            loc = './persist/world/' + address + '.room'
            try:
                f = open(loc,'r')
                room = pickle.load(f)
            except:
                pass
            
        if not room:
            print "Unable to unpickle: %s" % loc
            #Still no?  That sucks.
            #Server.WallAdmin('Unable to unpickle: %s' % address)
        else:
            self.Register(address, room)
            
        return room    
        
    def Register(self,address,room):
        self.rooms[address] = room
        
WorldManager = RoomManager()        