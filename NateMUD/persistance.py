'''
Created on Nov 22, 2015

@author: nwilliams
'''

import pickle

class Persister(object):
    '''
    Saves things to binary, but only the things I want to save.
    
    Oh jesus this is going to burn.
    
    So each class is going to get statekeys, a list of crap that I want to save.
    This should hopefully allow me to say, "only persist this stuff" and also
    have specific overrides to say, only save NPC's in the room, not players.
    
    I also need to handle saving players in that I want to save all their contents,
    but not all of their room.  I need to save DOWN, not up.
    
    I need to be careful of recursion.  ie, a player has a sword.  The sword has
    a location object, which is the player.  Etc, etc, etc.
    
    Lets work through this in my head.  So we're going to make a new object, that
    new object will ONLY have the properties we want to save.  Can we do that?
    I'm not sure we can.
    
    Can I load everything that I want to save into a dict?  What if I'm loading 
    objects into a dict?  I think that's cool.  Let's do that.
    '''
    
    statekeys=[]
    
    def __init__(self, *args, **kwargs):
        pass
        
    def Save(self):
        
        #this is just not going to work.
        
        filename = 'persist/'
        filename += self.__class__.__name__ + '/'
        if self.address:
            filename += self.address + '/'
        filename+=self.noun + '/'
        filename += '.' + self.__class__.__name__
        
        savefile = open(filename,'w')
        
        savedict = {'type':self.__class__.__name__}
        
        for key in self.statekeys:
            savedict[key] = self.__getattribute__(key)
            
        #it can't be that simple, can it?
        
        pickle.dump(savedict,savefile)    
            
            
            
            
            
            