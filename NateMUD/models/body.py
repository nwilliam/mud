'''
Created on Nov 7, 2015

@author: nwilliams
'''
from models.baseobject import BaseObject

class Body(BaseObject):
    '''
    Top-level Class inherited by Mob, Being, and Player.
    client=None,name='unnamed',pretitle='',posttitle='',
    desc_string='',location=None,**kwargs
    '''
    '''
    A Body is a Mobile Object (MOB) or a Player.
    
    Should every Body have a client? Yes I think so.  This lets me
    have the ability to possess non-player objects and have them DoStuff.
    There's a lot of things that will be added to a Body, but for
    now we'll just keep the basics and template the rest.
    
    I think I should branch this into subclasses. 
    Body -> Being -> Player
    Body -> Mob
    
    NPC's and Players have names and the ability to have a Client.  They also
    have pretitles and post titles.  How titilating.  Do NPCs and Players have
    anything different?  I think only scripts.  I take that back, I want the
    ability to have environmental scripts on players.
    
    Is there anything different?  Yes, there is.  Persist().  
    
    I think mobs may need to be a subclass for movement and because they don't
    have names.
    
    I'm going to keep self.client in Body.  I want to be able to possess Mobs.
    
    I think I want to treat Bodies like BaseObjects.  That way I can call
    all of the BaseObject methods on it if I need to.  I'll just override
    most of them.
    
    Bodies are also Containers.  I'll do this as a Mixin.
    '''


    def __init__(self, client=None,name='unnamed',pretitle='',posttitle='',
                 desc_string='',location=None,**kwargs):
        super(Body,self).__init__(noun=name.title(),adjs='', length=20, 
                                  width=15, height=72, weight=160, **kwargs)
        self.client = client
        self.name = name.title()
        self.pretitle = pretitle.title()
        self.posttitle = posttitle.title()
        self.desc_string = desc_string
        self.location = location

    def GetView(self):
        return self.location.GetView(self)

    def Possess(self,client):
        self.client = client
    
    def Unpossess(self,client):
        self.client = None
    
    def Name(self):
        if self.name:
            return self.name
        else:
            return 'Unnamed'
    
    def Noun(self):
        if self.name:
            return self.name
        else:
            return 'Unnamed'
        
    def Article(self):
        #Bodies don't get articles.
        return ''
    
    def FullName(self):
        if self.posttitle.startswith(','):
            return '%s %s%s' % (self.pretitle,self.Name(),self.posttitle)
        else:
            return '%s %s %s' % (self.pretitle,self.Name(),self.posttitle)
        
    def Tell(self,msg,**kwargs):
        # I'm abstracting this a bit higher to reduce calls to
        # Body.Client.Tell() - also this can let me do some
        # formatting higher up if I need to.  Also, we can intercept
        # errors here and not try to do a Tell to a mob.
        if self.client:
            self.client.Tell(msg,**kwargs)
            
    

    
        
        