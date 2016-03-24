"""
Created on Nov 4, 2015

@author: nwilliams

"""
import sys

from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol, listenWS
from twisted.internet import reactor

from channels.channel import UtilityChannel
from server import Server


class MudClient(WebSocketServerProtocol):
    def __init__(self):
        self.isAdmin = True
        self.server = Server
        self.LoginDone = False
        self.body = None
        super(MudClient, self).__init__()

    def onOpen(self):
        self.server.onOpen(self)

    def onLogin(self):
        pass

    """
    I need to do this in the Server, not here.
    """

    def onMessage(self, msg, isBinary):
        if not self.LoginDone:
            self.server.onLogin(self, msg)
        elif msg.startswith("'"):  # say
            self.server.Wall('%s says, "%s"' % (self.body.Name(), msg.strip("'")))

        elif msg.startswith('l'):  # look
            if len(msg.split(' ')) > 1:
                for obj in self.body.GetRoom().GetContents():
                    if obj.Noun().lower() == msg.split(' ')[1].lower():
                        UtilityChannel.tell('Found: %s' % obj.Noun())
                        self.Tell(obj.Desc())
                        break
                else:
                    self.Tell('I don\'t see %s here.' % msg.split(' ')[1])
            else:
                self.Tell(self.body.GetRoom().GetView(self.body))

        elif msg.startswith('go'):  # go
            splitMsg = msg.split(' ')
            if len(splitMsg) > 1:
                for obj in self.body.GetRoom().ItemContents():
                    if splitMsg[1].lower() == obj.Noun().lower():
                        obj.DoExit(self.body)
                        break
                else:
                    self.Tell('You can\'t go %s!' % splitMsg[1])
            else:
                self.Tell('Go where?')

        else:
            self.Tell('What?  I don\'t understand what "%s" means.' % msg)

    def connectionLost(self, reason):
        WebSocketServerProtocol.connectionLost(self, reason)
        self.server.onClose(self, reason)

    def Tell(self, msg):
        # Le Hack.
        msg = msg.replace('\n', '<br />')
        self.sendMessage(msg)


class MudServerFactory(WebSocketServerFactory):
    protocol = MudClient

    def __init__(self, url):
        WebSocketServerFactory.__init__(self, url)


if __name__ == '__main__':
    try:
        address = sys.argv[1]
    except IndexError:
        print "Run Address required (ws://address:port)"
        sys.exit(1)
    factory = MudServerFactory(address)
    listenWS(factory)
    UtilityChannel.tell('Websocket Server Factory running on {}'.format(address))
    reactor.run()
