import utils

class Linux:
    '''
    Linux related storage information.
    '''
    def __init__(self, path=''):
        self.path = path
        self.inodes = 'df -i -P %s' % self.path
        self.usage = 'df -k -P %s' % self.path
        self.iostat = 'iostat -d -N'
        self.fields = None

    def get_inodes(self):
        '''Inodes info.'''
        return utils.run(self.inodes)

    def get_usage(self):
        '''Usage info in Kb.'''
        return utils.run(self.usage)

    def get_iostat(self):
        '''IOstat info.'''
        return utils.run(self.iostat)

    def parse_inodes(self):
        self.fields = ('inodes', 'used', 'free', 'percent', 'mount')
        return utils.parse_storage(self.get_inodes(), self.fields)

    def parse_usage(self):
        self.fields = ('size', 'used', 'free', 'percent', 'mount')
        return utils.parse_storage(self.get_usage(), self.fields)



class FreeBSD:
    '''
    FreeBSD related storage information.
    On FreeBSD inode information is appended to FS usage info,
    that is whiy get_usage, get_inode and parse_usage, parse_inode
    are the same.
    '''
    def __init__(self, path=''):
        self.path = path
        self.usage = 'df -k -i %s' % self.path
        self.iostat = 'iostat -d %s' % self.path
        self.fields = None

    def parse_usage(self):
        self.fields('blocks', 'used', 'avail', 'percent', 'mount')
        return utils.parse_storage(self.get_inodes(), self.fields)

    def get_inodes(self):
        return utils.run(self.usage)

    def get_usage(self):
        return self.get_inodes()

    def get_iostat(self):
        return utils.run(self.iostat)

    def parse_inodes(self):
        self.fields('blocks', 'used', 'free', 'percent', 'iused', 'ifree', 'ipercent', 'mount')
        return utils.parse_storage(self.get_inodes(), self.fields)

    def parse_usage(self):
        return self.parse_inodes()

if __name__ == '__main__':
    print "not yet"
