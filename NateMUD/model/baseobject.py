'''
Created on Nov 7, 2015

@author: nwilliams
'''

class BaseObject(object):
    '''
    Base Handler for all classes.
    '''


    def __init__(self, noun='rock', adjs='very large', 
                 article=None, short=None, desc=None, 
                 isPlural=False, **kwargs):
        self.noun = noun
        self.adjs = adjs.split(' ')
        self.article = article
        self.short = short
        self.desc = desc
        self.isPlural = isPlural
    
    def Adjs(self):
        if self.adjs:
            return self.adjs
        else:
            return ''

    def AShort(self):
        article = self.Article()
        short = self.Short()
        if article:
            return '%s %s' % (article,short)
        else:
            return short
    
    def Article(self):
        if self.article:
            return self.article
        elif self.isPlural:
            return 'some'
        else:
            return 'an' if self.Short()[0] in 'aeiou' else 'a'
       
    def Short(self):
        if self.short:
            return self.short
        else:
            return ' '.join([' '.join(self.adjs),self.noun]).strip()
    
    def Desc(self):
        if self.desc:
            return self.desc
        else:
            return 'This is %s' % (self.AShort())
    

        
        