from channels.channel import UtilityChannel, AdminChannel


class ParserClass(object):
    """
    This whole parser is a goddamn hideous hack.  Right now it's there just to get
    the framework in place and have a few pieces of functionality in the game for
    testing.  It will be expanded and made dynamic.
    """
    def __init__(self):
        self.verbList = []
        self.prepList = []
        self.adjList = []

    def CompileVerbs(self):
        pass

    def Parse(self, client, clients, msg):
        if msg in self.verbList:
            pass

        if msg.startswith("'") or msg.startswith('say'):  # say
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
                        if obj.isa('Exit'):
                            obj.DoExit(client.body)
                            break
                else:
                    client.Tell('You can\'t go %s!' % splitMsg[1])
            else:
                client.Tell('Go where?')

        elif msg.startswith('chan'):  # change listening channels
            splitMsg = msg.split(' ')
            if len(splitMsg) == 1:
                msg = ('Channel | Verbosity\n'
                       '-------------------')
                for k in sorted(client.body.listeningTo):
                    msg += '\n{}{}|{}{}'.format(k,
                                                ('&nbsp;' * (8 - len(k))),
                                                ('&nbsp;' * (10 - len(str(client.body.listeningTo[k])))),
                                                client.body.listeningTo[k])
                client.Tell(msg, pre=True)
            elif len(splitMsg) == 2:
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
                else:
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
            else:
                for c in clients:
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

Parser = ParserClass()
