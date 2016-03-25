from time import localtime, strftime


class Channel(object):
    def __init__(self, name='Default', adminChannel=True):
        self.name = name
        self.adminChannel = adminChannel

    def tell(self, msg, verbosity=10):
        from server import Server
        Server.ChannelBroadcast('<span id=\'chanid_{0}\'>[{0}]</span> <span id=\'chanmsg_{0}\'>{1}</span>'.format(
            self.name, msg),self, verbosity=verbosity)
        print '{} | [{}] {}'.format(strftime('%Y-%m-%d %H:%M:%S', localtime()), self.name, msg)

ErrorChannel = Channel('Errs')
ConnectionChannel = Channel('Conn')
UtilityChannel = Channel('Util')
