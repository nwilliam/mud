from time import localtime,strftime


class Channel(object):
    def __init__(self, name='Default', verbosity=1):
        self.verbosity = verbosity
        self.name = name

    def tell(self, msg, verbosity=10):
        if verbosity >= self.verbosity:
            print '{} | [{}] {}'.format(strftime('%Y-%m-%d %H:%M:%S', localtime()), self.name, msg)

ErrorChannel = Channel('Errs')
ConnectionChannel = Channel('Conn')
UtilityChannel = Channel('Util')
