"""
Created on Dec 31, 2015

@author: nwilliams
"""
from models.body import Body


class Being(Body):
    """
    Body is anything - a spider, a monkey, a human, an elf.  Anything living.
    Being is a humanoid (NPC/Player).  It has a name, a title, lots of fun crap.
    
    """

    def __init__(self, name='unnamed', pretitle='', posttitle='', **kwargs):
        super(Being, self).__init__(noun=name.title(), adjs='', **kwargs)
        self.name = name.title()
        self.pretitle = pretitle.title()
        self.posttitle = posttitle.title()

    def Name(self):
        """
        Name if you have it, else Noun if you have it, if not then just Unnamed.
        """
        if self.name:
            return self.name
        else:
            if self.noun:
                return self.noun
            else:
                return 'Unnamed'

    def Noun(self):
        return self.Name()

    def Article(self):
        # Beings don't get articles.
        return ''

    def FullName(self):
        if self.posttitle.startswith(','):
            return '%s %s%s' % (self.pretitle, self.Name(), self.posttitle)
        else:
            return '%s %s %s' % (self.pretitle, self.Name(), self.posttitle)
