from time import localtime, strftime

class Channel(object):
    def __init__(self, name='Default', adminChannel=True):
        self.name = name
        self.adminChannel = adminChannel


    def Tell(self, msg, verbosity=10):
        from server import Server
        Server.ChannelBroadcast('<span class=\'chanid\' id=\'chanid_{0}\'>[{0}]</span>'
                                     ' <span class=\'chanmsg\' id=\'chanmsg_{0}\'>{1}</span></span>'.format(
                                      self.name, msg),
            self, verbosity=verbosity)
        print '{},[{}],[{:03d}],{}'.format(strftime('%Y-%m-%d %H:%M:%S', localtime()), self.name, verbosity, msg)

UtilityChannel = Channel('Util')
ErrorChannel = Channel('Error')
AdminChannel = Channel('Admin')
ConnectionChannel = Channel('Conn')