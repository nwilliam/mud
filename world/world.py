"""
Created on Nov 8, 2015

@author: nwilliams
"""
import pickle
from channels.channel import ErrorChannel


class RoomManager(object):
    """
    This thing is scary.  There are a lot of ways for this to break.
    
    There's only one WorldManager instance.
    """

    def __init__(self):
        from models.room import Room
        self.rooms = dict()
        self.defaultAddress = 'error/default'
        self.defaultRoom = Room(title='An Open Meadow',
                                desc='Lush green grass,'
                                     'green as the greenest emerald, stretches out as far as the eye can see'
                                     '.  Wispy clouds high in the zaffre sky twist slowly in a warm breeze.  '
                                     'Hints of cinnamon and cherries waft through the air as the glinting sun'
                                     ' directs your attention to a sign that simply states, "An error has '
                                     'occurred.  Please use the REPORT functionality."',
                                address='error/default')
        self.Register(self.defaultAddress, self.defaultRoom)

    def GetRoom(self, address):

        room = self.rooms.get(address, None)

        if room:
            return room

        # Not found in the dict, see if we can unpickle it.
        loc = './persist/world/rooms/' + address + '.room'
        try:
            with open(loc, 'r') as f:
                room = pickle.load(f)
        except (IOError, pickle.UnpicklingError):
            pass

        if room:
            self.Register(address, room)
            return room

        # This room doesn't exist!  Raise an error.
        ErrorChannel.tell("Unable to unpickle: %s".format(loc))
        return None

    def Register(self, address, room):
        self.rooms[address] = room


WorldManager = RoomManager()
