'''
Created on Nov 7, 2015

@author: nwilliams
'''
import unittest

from models.baseobject import BaseObject

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
      
         
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()