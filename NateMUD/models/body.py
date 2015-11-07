'''
Created on Nov 7, 2015

@author: nwilliams
'''
from models.baseobject import BaseObject

class Body(BaseObject):
    '''
    A Body is a Mobile Object (MOB) or a Player.
    Should every Body have a client? Yes I think so.  This lets me
    have the ability to possess non-player objects and have them DoStuff.
    There's a lot of things that will be added to a Body, but for
    now we'll just keep the basics and template the rest.
    
    I think I want to treat Bodies like BaseObjects.  That way I can call
    all of the BaseObject methods on it if I need to.  I'll just override
    most of them.
    
    Bodies are also Containers.  I'll do this as a Mixin.
    '''


    def __init__(self, client=None,name='unnamed',pretitle='',posttitle='',
                 desc_string='',location=None,**kwargs):
        super(Body,self).__init__(noun=name.Title(),adjs='',**kwargs)
        self.client = client
        self.name = name.Title()
        self.pretitle = pretitle.Title()
        self.posttitle = posttitle.Title()
        self.desc_string = desc_string
        self.location = location

    def Name(self):
        if self.name:
            return self.name
        else:
            return 'Unnamed'
        
    def Article(self):
        #Bodies don't get articles.
        return ''
    
    def FullName(self):
        return '%s %s %s' % (self.pretitle,self.Name(),self.posttitle)
        
    def Tell(self,msg,**kwargs):
        # I'm abstracting this a bit higher to reduce calls to
        # Body.Client.Tell() - also this can let me do some
        # formatting higher up if I need to.  Also, we can intercept
        # errors here and not try to do a Tell to a mob. This doesn't even
        if self.client:
            self.client.Tell(msg,**kwargs)
            
    

    
        
        