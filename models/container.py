'''
Created on Nov 10, 2015

@author: nwilliams
'''

class Container(object):
    '''
    Mixin class that contains methods/properties to hold other objects.
    '''
    def __init__(self,**kwargs):
        super(Container,self).__init__(**kwargs)
        self.contents = None
        
    def AddToContents(self,obj):
        if not self.contents:
            self.contents = []
        if obj:
            self.contents.append(obj)   
    
    def RemoveFromContents(self,obj):
        if obj:
            if obj in self.GetContents():
                self.contents.remove(obj)
        

    def GetContents(self):
        if self.contents:
            return self.contents
        else:
            return []