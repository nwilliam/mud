'''
Created on Nov 7, 2015

@author: nwilliams
'''
import unittest

from models.baseobject import BaseObject
from models.body import Body

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
    
    def testBaseObjectisaBaseObject(self):
        obj = BaseObject('stone')
        self.assertEqual(obj.isa('baseobject'),True)
        
    def testBaseObjectisaBaseObjectWithObject(self):
        obj = BaseObject('stone')
        self.assertTrue(obj.isa(BaseObject))
        
    def testBaseObjectisaBody(self):
        obj = BaseObject('stone')
        self.assertEqual(obj.isa('body'), False)
    
    def testBaseObjectisaBodyWithObject(self):
        obj = BaseObject('stone')
        self.assertFalse(obj.isa(Body))
        
    def testBodyisaBaseObject(self):
        body = Body()
        self.assertTrue(body.isa('baseobject'))
        
    def testBodyisaBaseObjectwithObject(self):
        body = Body()
        self.assertTrue(body.isa(BaseObject))  

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()