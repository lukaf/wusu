import utils

class Linux:
    '''
    Linux related storage information.
    '''
    def __init__(self, path=''):
        self.path = path
        self.inodes = 'df -i -P %s' % self.path
        self.usage = 'df -k -P %s' % self.path
        self.iostat = 'iostat -d -N -k -x %s' % self.path
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

    def parse_iostat(self):
        '''
        tps - transfers per second
        kbrs (kB_read/s) - amount of data read from the device expressed in kilobytes per second
        kbws (kB_wrtn/s) - amount of data written to the device expressed in kilobytes per second
        kbr (kB_read) - total number of kilobytes read
        kbw (kB_read) - total number of kilobytes written
        avgrq-sz - The average size (in sectors) of the requests that were issued to the device.
        avgqu-sz - The average queue length of the requests that were issued to the device.
        await - The average time (in milliseconds) for I/O requests issued to the device to be served. This includes the time  spent  by the requests in queue and the time spent servicing them.
        svctm - The average service time (in milliseconds) for I/O requests that were issued to the device.
        '''
        self.fields = ('tps', 'kbrs', 'kbws', 'kbr', 'kbw', 'avgrq-sz', 'avgqu-sz', 'await', 'svctm')
        return utils.parse_iostat(self.get_iostat(), self.fields)

class FreeBSD:
    '''
    FreeBSD related storage information.
    On FreeBSD inode information is appended to FS usage info,
    that is why get_usage, get_inode and parse_usage, parse_inode
    are the same.
    '''
    def __init__(self, path=''):
        self.path = path
        self.usage = 'df -k -i %s' % self.path
        self.iostat = 'iostat -d -x -K %s' % self.path
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

    def parse_iostat(self):
        '''
        rs (r/s) - read operations per second
        ws (w/s) - write operations per second
        krs (kr/s) - kilobytes read per second
        kws (kw/s) - kilobytes write per second
        wait - transactions queue length
        svc_t - average duration of transactions, in milliseconds
        b (%b) - % of time the device had one or more outstanding transactions
        '''
        self.fields('rs', 'ws', 'krs', 'kws', 'wait', 'svc_t', 'b')
        return utils.parse_iostat(self.get_iostat(), self.fields)

if __name__ == '__main__':
    print "not yet"
