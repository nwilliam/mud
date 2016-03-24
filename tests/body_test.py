'''
Created on Dec 31, 2015

@author: nwilliams

As of right now, Body can only be checked with Integrated testing.  Ouch.
I guess we can do these here, but this has a LOT of code coverage in one or
two tests... and is going to be hard to trace WHAT broke when something does.

I would HIGHLY advise running Room tests before running these.

'''
import unittest
from models.body import Body
from models.room import Room
from world.world import WorldManager

class TestBodies(unittest.TestCase):
    def setUp(self):
        self.start_room=Room(title='Starting Room',desc='This is the starting room.',
                        address='test/0')
        self.dest_room=Room(title='Destination Room',desc='This is the destination room.',
                       address='test/1')
        WorldManager.Register(self.start_room.address, self.start_room)
        WorldManager.Register(self.dest_room.address,self.dest_room)
        self.body = Body(location='test/0')
              
    def testBodyMoveRoomToRoomGoodRoom(self):
        self.body.Move('test/1')
        self.assertEqual(self.body.location, 'test/1')
        self.assertEqual(self.body.room,self.dest_room)
    
    def testBodyMoveRoomToRoomBadRoom(self): 
        self.body.Move('test/0')
        self.body.Move('test/2')
        self.assertEqual(self.body.location, 'test/0')
        self.assertEqual(self.body.room,self.start_room)
        
    def testBodyGetRoomWithGoodRoom(self):
        self.assertEqual(self.body.GetRoom(), self.start_room)
   
    def testBodyGetRoomWithBadRoom(self):
        self.body.location='test/2'
        self.assertEqual(self.body.GetRoom(),WorldManager.GetRoom('error/default'))

        
        
      

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()