"""
Created on Dec 31, 2015

@author: nwilliams
"""
import unittest
from models.baseobject import BaseObject
from models.body import Body
from models.room import Room

class TestRooms(unittest.TestCase):
    def testRoomAddToContentsObject(self):
        obj = BaseObject()
        room = Room()
        room.AddToContents(obj)
        self.assertIn(obj,room.contents)
        
    def testRoomAddToContentsBody(self):
        body = Body()
        room = Room()
        room.AddToContents(body)
        self.assertIn(body,room.contents)
        
    def testRoomGetObjectsViewWithOneObject(self):
        room = Room()
        room.AddToContents(BaseObject())
        self.assertEqual(room.GetObjectsView(),'You also see a rock.')

    def testRoomGetObjectsViewWithTwoObjects(self):
        room = Room()
        room.AddToContents(BaseObject())
        room.AddToContents(BaseObject('tiny rock'))
        self.assertEqual(room.GetObjectsView(),'You also see a rock and a tiny rock.')
        
    def testRoomGetObjectsViewWithThreeObjects(self):
        room = Room()
        room.AddToContents(BaseObject())
        room.AddToContents(BaseObject('tiny rock'))
        room.AddToContents(BaseObject('goddamned monkey'))
        self.assertEqual(room.GetObjectsView(),'You also see a rock, a tiny rock and a goddamned monkey.') 
    
    def testRoomGetBodiesViewWithOneBody(self):
        room = Room()
        me = Body(name='Me')
        room.AddToContents(me)
        self.assertEqual(room.GetBodiesView(me),'')              
     
    def testRoomGetBodiesViewWithTwoBodies(self):
        room = Room()
        me = Body(name='Me')
        room.AddToContents(me)
        room.AddToContents(Body(name='Steve'))
        self.assertEqual(room.GetBodiesView(me),'\nAlso here: Steve.')   

    def testRoomGetBodiesViewWithThreeBodies(self):
        room = Room()
        me = Body(name='Me')
        room.AddToContents(me)
        room.AddToContents(Body(name='Steve'))
        room.AddToContents(Body(name='Frank'))
        self.assertEqual(room.GetBodiesView(me),'\nAlso here: Steve and Frank.')

    def testRoomGetBodiesViewWithFourBodies(self):
        room = Room()
        me = Body(name='Me')
        room.AddToContents(me)
        room.AddToContents(Body(name='Steve'))
        room.AddToContents(Body(name='Frank'))
        room.AddToContents(Body(name='Bob'))        
        self.assertEqual(room.GetBodiesView(me),'\nAlso here: Steve, Frank and Bob.')
        
    def testRoomisaRoom(self):
        room = Room()
        self.assertEqual(room.isa('room'), True)
        
    def testRoomisaBody(self):
        room = Room()
        self.assertEqual(room.isa('body'),False)   
                    

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()