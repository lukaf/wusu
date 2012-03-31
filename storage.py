import utils

class Linux(object):
    '''
    Linux related storage information.
    '''
    def __init__(self, path=''):
        self.path = path
        self.inodes = 'df -i -P %s' % self.path
        self.fsusage = 'df -k -P %s' % self.path
        self.iostat = 'iostat -d -N -k -x %s' % self.path

    def get_inodes(self):
        '''Inodes info.'''
        return utils.run(self.inodes)

    def get_fsusage(self):
        '''Usage info in Kb.'''
        return utils.run(self.fsusage)

    def get_iostat(self):
        '''IOstat info.'''
        return utils.run(self.iostat)

    def parse_inodes(self):
        '''
        Parse output of get_inodes()
        Returned structure is a dictionary of dictionaries:
        {device:
            {'mount': value,
            'used': value,
            'percent': value,
            'free': value,
            'inodes': value}
        }

        mount - mount point
        used - amount of used inodes
        percent - amount of used inodes in percent
        free - amount of free inodes
        inodes - amount of all inodes
        '''
        fields = ('inodes', 'used', 'free', 'percent', 'mount')
        return utils.parser_storage(self.get_inodes(), fields)

    def parse_fsusage(self):
        '''
        Parse output of get_fsusage().
        Returned structure is a dictionary of dictionaries:
        {device:
            {'mount': value,
            'used: value,
            'percent': value,
            'free': value,
            'size': value}
        }

        mount - mount point
        used - amount of used disk space in Kb
        percent - amount of used disk space in percent
        free - amount of free disk space in Kb
        size - amount of all disk space in kB
        '''
        fields = ('size', 'used', 'free', 'percent', 'mount')
        return utils.parser_storage(self.get_fsusage(), fields)

    def parse_iostat(self):
        '''
        Parse output of get_iostat().
        Returned structure is a dictionary of dictionaries:
        {device: 
            {'tps': value,
            'kbrs': value,
            'kbws': value,
            'kbr': value,
            'kbw': value,
            'avgrq-sz': value,
            'avgqu-sz': value,
            'await': value,
            'svctm': value}
        }

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
        fields = ('tps', 'kbrs', 'kbws', 'kbr', 'kbw', 'avgrq-sz', 'avgqu-sz', 'await', 'svctm')
        return utils.parser_iostat(self.get_iostat(), fields)

class FreeBSD(object):
    '''
    FreeBSD related storage information.
    On FreeBSD inode information is appended to FS usage info,
    that is why get_fsusage, get_inode and parse_fsusage, parse_inode
    are the same.
    '''
    def __init__(self, path=''):
        self.path = path
        self.fsusage = 'df -k -i %s' % self.path
        self.iostat = 'iostat -d -x -K -I %s' % self.path

    def get_inodes(self):
        '''FS usage and inodes info.'''
        return utils.run(self.fsusage)

    def get_fsusage(self):
        '''See get_inodes().'''
        return self.get_inodes()

    def get_iostat(self):
        '''IOstat info.'''
        return utils.run(self.iostat)

    def parse_inodes(self):
        '''
        Parse output of get_inodes().
        Returned structure is a dictionary of dictionaries:
        {device:
            {'blocks': value,
            'used': value,
            'free': value,
            'percent': value,
            'iused': value,
            'ifree': value,
            'ipercent': value,
            'mount': value}
        }

        blocks - amount of all 1k blocks
        used - amount of used disk space in Kb
        free - amount of free disk space in Kb
        percent - amount of used disk space in percent
        iused - amount of used inodes
        ifree - amount of free inodes
        ipercent - amount of used inodes in percent
        mount - mount point
        '''
        fields = ('blocks', 'used', 'free', 'percent', 'iused', 'ifree', 'ipercent', 'mount')
        return utils.parser_storage(self.get_inodes(), fields)

    def parse_fsusage(self):
        '''See parse_inodes().'''
        return self.parse_inodes()

    def parse_iostat(self):
        '''
        Parse output of get_iostat().
        Returned structure is a dictionary of dictionaries.
        {device:
            {'rs': value,
            'ws': value,
            'krs': value,
            'kws': value,
            'wait': value,
            'svc_t': value,
            'b': value}
        }

        rs (r/s) - read operations per second
        ws (w/s) - write operations per second
        krs (kr/s) - kilobytes read per second
        kws (kw/s) - kilobytes write per second
        wait - transactions queue length
        svc_t - average duration of transactions, in milliseconds
        b (%b) - % of time the device had one or more outstanding transactions
        '''
        fields = ('rs', 'ws', 'krs', 'kws', 'wait', 'svc_t', 'b')
        return utils.parser_iostat(self.get_iostat(), fields)

class SunOS(object):
    def __init__(self, path = ''):
        self.path = path
        self.inodes = 'df -o i %s' % self.path
        self.fsusage = 'df -k %s' % self.path
        self.iostat = 'iostat -n -x -I %s' % self.path

    def get_inodes(self):
        '''Inodes info.'''
        return utils.run(self.inodes)

    def get_fsusage(self):
        '''FS usage info.'''
        return utils.run(self.fsusage)

    def get_iostat(self):
        '''IOstat info.'''
        return utils.run(self.iostat)

    def parse_inodes(self):
        '''
        Parse ouput of get_inodes().
        Returned structure is a dictionary of dictionaries:
        {device:
            {'mount': value,
            'used': value,
            'free': value,
            'percent': value}

        mount - mount point
        used - amount of used inodes
        free - amount of free inodes
        percent - amount of used inodes in percent
        '''
        fields = ('used', 'free', 'percent', 'mount')
        return utils.parser_storage(self.get_inodes(), fields)

    def parse_fsusage(self):
        '''
        Parse output of get_fsusage().
        Returned structure is a dictionary of dictionaries:
        {device:
            {'kbytes': value,
            'used': value,
            'free': value,
            'percent': value,
            'mount': value}
        }

        kbytes - amount of all disk space in Kb
        used - amount of used disk space in Kb
        free - amount of free disk space in Kb
        percent - amount of used disk space in percent
        mount - mount point
        '''
        fields = ('kbytes', 'used', 'free', 'percent', 'mount')
        return utils.parser_storage(self.get_fsusage(), fields)

    def parse_iostat(self):
        '''
        Parse output of get_iostat().
        Returned structure is a dictionary of dictionaries:
        {device:
            {'rs': value,
            'ws': value,
            'krs': value,
            'kws': value,
            'wait': value,
            'actv': value,
            'svc_t': value,
            'w': value,
            'b': value}
        }

        rs (r/s) - reads per second
        ws (w/s) - writes per second
        krs (kr/s) - kilobytes read per second
        kws (kw/s) - kilobytes write per second
        wait - average number of transactions waiting for service (queue length)
        actv - average number of transactions actively being serviced  (removed
            from  the  queue but not yet completed)
        svc_t - average response time  of  transactions,  in  milliseconds
        w - percent of time there are transactions waiting for service (queue not-empty)
        b - percent of time the disk is busy (transactions in progress)
        '''
        fields = ('rs', 'ws', 'krs', 'kws', 'wait', 'actv', 'svc_t', 'w', 'b')
        return utils.parser_iostat(self.get_iostat(), fields)

if __name__ == '__main__':
    print "not yet"
