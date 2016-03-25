"""
Created on Nov 4, 2015

@author: nwilliams
"""
import pickle

from models.being import Being
from world.world import WorldManager
from channels.channel import ConnectionChannel, UtilityChannel, AdminChannel


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
            ConnectionChannel.Tell('Registered Client: %s' % client.peer)

        if not client.LoginDone:
            client.Tell('Enter a name:')

    def onLogin(self, client, msg):
        if len(msg) > 16 or len(msg) < 3 or ' ' in msg.strip():
            client.Tell('That name is not acceptable, please try again.')
            return

        if msg.title() in [c.body.Name() for c in self.clients if c.body]:
            client.Tell('Name is use, please try another.')
            return

        if msg.title() in self.adminList:
            client.isAdmin = True

        body = None

        # Try to Unpickle it.
        try:
            with open('persist/players/%s.name' % msg.title()) as f:
                body = pickle.load(f)
        except:
            ConnectionChannel.Tell('Unable to unpickle {}, creating new body.'.format(msg.title()), 20)
            pass

        if body:
            client.body = body
        else:
            client.body = Being(client=client, name=msg, location=self.default_room.address)

        ConnectionChannel.Tell("%s is %s" % (client.peer, client.body.Name()))
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
        """
        All of this needs ripped out and stuffed into a parser.  For now its there to
        test various functionality that I'm adding.  Think of it as a hacky-parser?
        """
        if not client.LoginDone:
            self.onLogin(client, msg)

        elif msg.startswith("'") or msg.startswith('say'):  # say
            client.body.GetRoom().Tell('%s says, "%s"' % (client.body.Name(), msg.strip("'")), client.body)
            client.Tell('You say, "%s"' % (msg.strip("'")))

        elif msg.startswith('l'):  # look
            if len(msg.split(' ')) > 1:
                for obj in client.body.GetRoom().GetContents():
                    if obj.Noun().lower() == msg.split(' ')[1].lower():
                        UtilityChannel.Tell('Found: %s' % obj.Noun(), 90)
                        client.Tell(obj.Desc())
                        break
                else:
                    client.Tell('I don\'t see %s here.' % msg.split(' ')[1])
            else:
                client.Tell(client.body.GetRoom().GetView(client.body))

        elif msg.startswith('go'):  # go
            splitMsg = msg.split(' ')
            if len(splitMsg) > 1:
                for obj in client.body.GetRoom().ItemContents():
                    if splitMsg[1].lower() == obj.Noun().lower():
                        obj.DoExit(client.body)
                        break
                else:
                    client.Tell('You can\'t go %s!' % splitMsg[1])
            else:
                client.Tell('Go where?')

        elif msg.startswith('chan'): #change listening channels
            splitMsg = msg.split(' ')
            if len(splitMsg) == 2:
                if splitMsg[1].lower() in 'show':
                    msg = 'Channel\t|\tVerbosity'
                    for k, v in client.body.listeningTo.items():
                        msg += '\n{}\t|\t{}'.format(k,v)
                    client.Tell(msg)
                    return
                if splitMsg[1].title() in client.body.listeningTo.keys():
                    del client.body.listeningTo[splitMsg[1].title()]
                    client.Tell('Stopped listening to {} channel.'.format(splitMsg[1]))
                else:
                    client.body.listeningTo[splitMsg[1].title()] = 100
                    client.Tell('Started listening to {} channel at verbosity 100.'.format(splitMsg[1]))
            elif len(splitMsg) > 2:
                try:
                    verbosity = int(splitMsg[2])
                except:
                    client.Tell('Verbosity Level must be an integer.')
                    return
                if splitMsg[1].title() not in client.body.listeningTo.keys():
                    client.Tell('Started listening to {} channel.'.format(splitMsg[1].title()))
                client.body.listeningTo[splitMsg[1].title()] = verbosity
                client.Tell('Set {} verbosity to {}'.format(splitMsg[1].title(), verbosity))

        elif msg.startswith('admin'):
            if not client.isAdmin:
                return
            try:
                newAdmin = msg.split(' ')[1].title()
            except IndexError:
                client.Tell('You need to specify a name.')
                return
            self.adminList.append(newAdmin)
            for c in self.clients:
                if c.body and c.body.Name() == newAdmin:
                    AdminChannel.Tell('{} has made {} an admin.'.format(client.body.Name(), newAdmin), 0)
                    c.isAdmin = True
                    c.Tell('{} has made you an administrator.'.format(client.body.Name()))
                    client.Tell('{} is now an admin.'.format(newAdmin))
                    break
            else:
                client.Tell('Could not find {}.'.format(newAdmin))

        else:
            client.Tell('What?  I don\'t understand what "%s" means.' % msg)

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