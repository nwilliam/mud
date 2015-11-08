'''
Created on Nov 7, 2015

@author: nwilliams
'''
import unittest

from models.baseobject import BaseObject
from models.body import Body
from models.room import Room

class TestBaseObject(unittest.TestCase):

    def testBaseObjectShortWithNoAdjs(self):
        obj = BaseObject(noun='stone',adjs='')
        self.assertEqual(obj.Short(), 'stone')
    
    def testBaseObjectShortWithOneAdj(self):
        obj = BaseObject(noun='stone',adjs='small')
        self.assertEqual(obj.Short(),'small stone')
        
    def testBaseObjectShortWithMultipleAdjs(self):
        obj = BaseObject(noun='stone',adjs='small pointy crazy drunken')
        self.assertEqual(obj.Short(),'small pointy crazy drunken stone')
    
    def testBaseObjectAShortWithNoAdjsConsonant(self):
        obj = BaseObject(noun='stone',adjs='')
        self.assertEqual(obj.AShort(),'a stone')    

    def testBaseObjectAShortWithAdjsConsonant(self):
        obj = BaseObject(noun='stone',adjs='small pointy')
        self.assertEqual(obj.AShort(),'a small pointy stone')
        
    def testBaseObjectAShortWithNoAdjsVowel(self):
        obj = BaseObject(noun='apple',adjs='')
        self.assertEqual(obj.AShort(),'an apple')        

    def testBaseObjectAShortWithAdjsVowel(self):
        obj = BaseObject(noun='apple',adjs='small')
        self.assertEqual(obj.AShort(),'a small apple')
    
    def testBaseObjectAShortWithVowelAdjsVowel(self):
        obj = BaseObject(noun='apple',adjs='alluring green')
        self.assertEqual(obj.AShort(),'an alluring green apple')    

    def testBaseObjectAShortWithPlural(self):
        obj = BaseObject(noun='apples',adjs='alluring green',isPlural=True)
        self.assertEqual(obj.AShort(),'some alluring green apples') 
      
    def testBaseObjectFullMultipleAdjs(self):
        obj = BaseObject('tiny wet stone')
        self.assertEqual(obj.AShort(),'a tiny wet stone')

    def testBaseObjectFullOneAdjs(self):
        obj = BaseObject('wet stone')
        self.assertEqual(obj.AShort(),'a wet stone')
        
    def testBaseObjectFullNoAdjs(self):
        obj = BaseObject('stone')
        self.assertEqual(obj.AShort(),'a stone')        

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
        self.assertEqual(room.GetObjectsView(),'You also see a very large rock.')

    def testRoomGetObjectsViewWithTwoObjects(self):
        room = Room()
        room.AddToContents(BaseObject())
        room.AddToContents(BaseObject('tiny rock'))
        self.assertEqual(room.GetObjectsView(),'You also see a very large rock and a tiny rock.')
        
    def testRoomGetObjectsViewWithThreeObjects(self):
        room = Room()
        room.AddToContents(BaseObject())
        room.AddToContents(BaseObject('tiny rock'))
        room.AddToContents(BaseObject('goddamned monkey'))
        self.assertEqual(room.GetObjectsView(),'You also see a very large rock, a tiny rock and a goddamned monkey.') 
    
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
        self.assertEqual(room.GetBodiesView(me),'Also here: Steve.')   

    def testRoomGetBodiesViewWithThreeBodies(self):
        room = Room()
        me = Body(name='Me')
        room.AddToContents(me)
        room.AddToContents(Body(name='Steve'))
        room.AddToContents(Body(name='Frank'))
        self.assertEqual(room.GetBodiesView(me),'Also here: Steve and Frank.')

    def testRoomGetBodiesViewWithFourBodies(self):
        room = Room()
        me = Body(name='Me')
        room.AddToContents(me)
        room.AddToContents(Body(name='Steve'))
        room.AddToContents(Body(name='Frank'))
        room.AddToContents(Body(name='Bob'))        
        self.assertEqual(room.GetBodiesView(me),'Also here: Steve, Frank and Bob.')   
                    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()