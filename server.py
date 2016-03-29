"""
Created on Nov 4, 2015

@author: nwilliams
"""
import pickle

from models.being import Being
from world.world import WorldManager
from channels.channel import ConnectionChannel, AdminChannel
from parsing.parser import Parser


class ServerClass(object):
    """
    Only one instance of this class needed.  Keeps track of everyone/everything
    that is connected.  Also handles Broadcasts.
    """

    def __init__(self):
        self.clients = []
        self.adminList = ['Nate']
        self.default_room = WorldManager.GetRoom('staff/default/000000')

    def onOpen(self, client):
        if client not in self.clients:
            self.clients.append(client)
            ConnectionChannel.Tell('Registered Client: %s' % client.peer, 20)

        if not client.LoginDone:
            client.Tell('Enter a name:')

    def onLogin(self, client, msg):
        if len(msg) > 16 or len(msg) < 3 or ' ' in msg.strip():
            client.Tell('That name is not acceptable, please try again.')
            return

        if msg.title() in [c.body.Name() for c in self.clients if c.body]:
            client.Tell('Name is use, please try another.')
            return

        # if msg.title() in self.adminList:
        client.isAdmin = True
        AdminChannel.Tell('Admin %s is now online.' % msg.title())

        body = None

        # Try to Unpickle it.
        try:
            with open('persist/players/%s.name' % msg.title()) as f:
                body = pickle.load(f)
        except IOError:
            ConnectionChannel.Tell('Unable to unpickle {}, creating new body.'.format(msg.title()), 20)
            pass

        if body:
            client.body = body
        else:
            client.body = Being(client=client, name=msg, location=self.default_room.address)

        ConnectionChannel.Tell("%s is %s" % (client.peer, client.body.Name()))
        client.Tell('Welcome, {}{}'.format(('Admin ' if client.isAdmin else ''), client.body.Name()))
        client.body.Move(self.default_room.address)
        client.body.GetRoom().Tell('%s just arrived.' % client.body.Name())
        client.body.GetRoom().AddToContents(client.body)
        client.Tell(client.body.GetView())
        client.LoginDone = True

    def onClose(self, client, reason):
        if client.body:
            client.body.GetRoom().Tell('%s just left.' % client.body.Name())
            client.body.GetRoom().RemoveFromContents(client.body)

        if client in self.clients:
            self.clients.remove(client)
            try:
                ConnectionChannel.Tell('Unregistered Client: %s (%s), %s' %
                                       (client.body.Name(), client.peer, reason.value))
            except:
                ConnectionChannel.Tell('Unregistered Client (%s), %s' %
                                       (client.peer, reason.value))

    def onMessage(self, client, msg):
        if not client.LoginDone:
            self.onLogin(client, msg)
        else:
            Parser.Parse(client, self.clients, msg)

    def WallAdmin(self, message):
        for c in self.clients:
            if c.isAdmin:
                c.Tell(message)

    def Wall(self, message):
        for c in self.clients:
            c.Tell(message)

    def ChannelBroadcast(self, message, channel=None, verbosity=0):
        for c in self.clients:
            if c.body:
                if channel.adminChannel:
                    if c.isAdmin:
                        if channel.name in c.body.listeningTo and verbosity <= c.body.listeningTo[channel.name]:
                            c.Tell(message)
                else:
                    # Non-admin channels do not have a verbosity level.
                    c.Tell(message)


Server = ServerClass()
