"""
Created on Nov 4, 2015

@author: nwilliams
"""
import pickle

from models.being import Being
from world.world import WorldManager


class ServerClass(object):
    """
    Only one instance of this class needed.  Keeps track of everyone/everything
    that is connected.  Also handles Broadcasts.
    """

    def __init__(self):
        self.clients = []
        self.default_room = WorldManager.GetRoom('staff/default/000000')

    def onOpen(self, client):
        if client not in self.clients:
            self.WallAdmin('Registered Client: %s' % client.peer)
            self.clients.append(client)
            print 'Registered Client: %s' % client.peer

        if not client.LoginDone:
            client.Tell('Enter a name:')

    def onLogin(self, client, msg):
        if len(msg) > 16 or len(msg) < 3 or ' ' in msg.strip():
            client.Tell('That name is not acceptable, please try again.')
            return

        if msg.title() in [c.body.Name() for c in self.clients if not client]:
            client.Tell('Name is use, please try another.')
            return

        body = None

        # Try to Unpickle it.
        try:
            with open('persist/players/%s.name' % msg.title()) as f:
                body = pickle.load(f)
        except:
            pass

        if body:
            client.body = body
        else:
            client.body = Being(client=client, name=msg, location=self.default_room.address)

        print "%s is %s" % (client.peer, client.body.Name())
        client.body.Move(self.default_room.address)
        client.body.GetRoom().AddToContents(client.body)
        client.body.GetRoom().Tell('%s just arrived.' % client.body.Name())
        client.Tell(client.body.GetView())
        client.LoginDone = True

    def onClose(self, client, reason):
        if client.body:
            client.body.GetRoom().Tell('%s just left.' % client.body.Name())
            client.body.GetRoom().RemoveFromContents(client.body)

        if client in self.clients:
            self.clients.remove(client)
            try:
                self.WallAdmin('Unregistered Client: %s (%s), %s' % (client.body.Name(), client.peer, reason.value))
                print 'Unregistered Client: %s (%s), %s' % (client.body.Name(), client.peer, reason.value)
            except:
                pass

    def WallAdmin(self, message):
        for c in self.clients:
            if c.isAdmin:
                c.Tell(message)

    def Wall(self, message):
        for c in self.clients:
            c.Tell(message)

    def ReportError(self, err):
        self.WallAdmin(err)


Server = ServerClass()
