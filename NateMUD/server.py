'''
Created on Nov 4, 2015

@author: nwilliams
'''

class ServerClass(object):
    '''
    Only one instance of this class needed.  Keeps track of everyone/everything
    that is connected.  Also handles Broadcasts.
    '''

    def __init__(self):
        self.clients = []
        
    def onOpen(self,client):
        if not client in self.clients:
            self.WallAdmin('Registered Client: %s' % client.peer)
            self.clients.append(client)
            print 'Registered Client: %s' % client.peer
        
        if not client.name:
            client.Tell('Enter a name:')
    
    def onLogin(self,client,msg):
        for c in self.clients:
            if c.name == msg or len(msg)>16 or len(msg) < 3:
                client.Tell('That name is not acceptable, please try again.')
                return
        client.Tell('Welcome, %s.' % msg)
        client.name = msg
        client.LoginDone = True
            
            
    def onClose(self,client, reason):
        if client in self.clients:
            self.clients.remove(client)
            self.WallAdmin('Deregistered Client: %s, %s' % (client.peer, reason))
            print 'Deregistered Client: %s, %s' % (client.peer, reason)
        
    def WallAdmin(self,message):
        for c in self.clients:
            if c.isAdmin:
                c.Tell(message)
                
    def Wall(self,message):
        for c in self.clients:
            c.Tell(message)
    
    def ReportError(self,err):
        self.WallAdmin(err)          

Server = ServerClass()    