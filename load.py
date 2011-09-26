import utils
import os

class Linux:
    def __init__(self):
        self.memory = '/proc/meminfo'
        self.swap = '/proc/swaps'
        self.loadavg = '/proc/loadavg'
        self.pagesize = os.sysconf('SC_PAGE_SIZE')

    def get_uptime(self):
        '''
        Get machine uptime in seconds as provided by /proc/uptime.
        Also see parse_uptime().
        '''
        f = open('/proc/uptime', 'r', 0)
        seconds = float(f.read().split()[0])
        f.close()
        return seconds

    def get_memory(self):
        '''
        Get memory information from /proc/meminfo.
        Also see parse_memory().
        '''
        f = open(self.memory, 'r', 0)
        data = f.read()
        f.close()
        return data

    def get_swap(self):
        '''
        Get swap information from /proc/swaps.
        Also see parse_swap().
        '''
        f = open(self.swap, 'r', 0)
        data = f.read()
        f.close()
        return data

    def get_loadavg(self):
        '''Get load information from /proc/loadavg.'''
        f = open(self.loadavg, 'r', 0)
        data = f.read()
        f.close()
        return data

    def parse_uptime(self):
        '''
        Parse output from get_uptime().
        Returned structure is a tuple:
        (days, hours, minutes, seconds, seconds since boot)
        '''
        return utils.parser_uptime(self.get_uptime())

    def parse_memory(self, mem_fields=('MemTotal', 'MemFree')):
        '''
        Parse memory info from output of get_memory().
        Returned key, value pairs depend on keywords defined in mem_fields,
        which MUST be a tuple:
        self.parse_memory(('MemTotal',))
        Search is case sensitive.

        Returned structure is a dictionary:
        {key: value, ...}
        '''
        return utils.parser_memory(self.get_memory(), mem_fields)

    def parse_swap(self):
        '''
        Parse output of get_swap().
        Returned structure is a dictionary of dictionaries:
        {device:
            {'type': value,
            'size': value,
            'used', value,
            'priority', value}
        }
        '''
        fields = ('type', 'size', 'used', 'priority')
        return utils.parser_swap(self.get_swap(), fields)

    def parse_loadavg(self):
        '''
        Parse output of get_loadavg().
        Returned structure is a tuple:
        (1min, 5min, 15min)
        '''
        return utils.parser_loadavg(self.get_loadavg())

class FreeBSD:
    def __init__(self, libc='/lib/libc.so.7'):
        self.memory = 'sysctl vm.stats.vm'
        self.swap = 'pstat -s'
        self.loadavg = 'sysctl -n vm.loadavg'
        self.libc = libc
        self.pagesize = os.sysconf('SC_PAGE_SIZE')

    def get_uptime(self):
        '''
        Get machine uptime in seconds as provided by clock_gettime(2).
        clock_gettime's first argument is CLOCK_UPTIME_PRECISE, which
        is defined in time.h:
        #define CLOCK_UPTIME    5               /* FreeBSD-specific. */
        #define CLOCK_UPTIME_PRECISE    7       /* FreeBSD-specific. */
        #define CLOCK_UPTIME_FAST       8       /* FreeBSD-specific. */
        '''
        from ctypes import Structure, cdll, byref, c_long
        lib = cdll.LoadLibrary(self.libc)
        class Data(Structure):
            _fields_ = [('sec', c_long), ('nsec', c_long)]
        struct = Data()
        lib.clock_gettime(7, byref(struct))
        return struct.sec

    def get_memory(self):
        '''Get memory information.'''
        return utils.run(self.memory)

    def get_swap(self):
        '''Get swap information.'''
        return utils.run(self.swap)

    def get_loadavg(self):
        '''Get load average.'''
        return utils.run(self.loadavg)

    def parse_uptime(self):
        '''
        Parse output from get_uptime().
        Returned structure is tuple:
        (days, hours, minutes, seconds, seconds since boot)
        '''
        return utils.parser_uptime(self.get_uptime())

    def parse_memory(self, mem_fields=('vm.stats.vm.v_page_count', 'vm.stats.vm.v_free_count', 'vm.stats.vm.v_inactive_count', 'vm.stats.vm.v_cache_count')):
        '''
        Parse output from get_memory().
        Returned key, value pairs depend on keywords defined in mem_fields,
        which MUST be a tuple:
        self.parse_memory(('vm.stats.vm.v_page_count',))
        Search is case sensitive.

        By default, returned values are pages of memory.

        Returned structure is a dictionary.
        {key: value, ...}

        free = v_free_count + v_inactive_count + v_cache_count
        '''
        return utils.parser_memory(self.get_memory(), mem_fields)

    def parse_swap(self):
        '''
        Parse output from get_swap().
        Returned structure is a dictionary of dictionaries:
        {'device':
            {'blocks': value,
            'used: value,
            'free', value,
            'percent', value}
        }
        '''
        fields = ('blocks', 'used', 'free', 'percent')
        return utils.parser_swap(self.get_swap(), fields)

    def parse_loadavg(self):
        '''
        Parse output of get_loadavg().
        Returned structure is a tuple:
        (1min, 5min, 15min)
        '''
        return utils.parser_loadavg(self.get_loadavg())

class SunOS:
    def __init__(self):
        self.uptime = 'kstat -p unix:0:system_misc:boot_time'
        self.loadavg = 'kstat -p unix:0:system_misc:avenrun*'
        self.memory = 'kstat -p unix:0:system_pages'
        self.swap = 'swap -l'
        self.pagesize = os.sysconf('SC_PAGE_SIZE')

    def get_uptime(self):
        '''Get machine uptime.'''
        return utils.run(self.uptime)

    def get_memory(self):
        '''Get memory info.'''
        return utils.run(self.memory)

    def get_swap(self):
        '''Get swap info.'''
        return utils.run(self.swap)

    def get_loadavg(self):
        '''Get load average.'''
        return utils.run(self.loadavg)

    def parse_uptime(self):
        '''Parse output of get_uptime().'''
        from time import time
        return utils.parser_uptime(int(time()) - int(self.get_uptime().split()[-1]))

    def parse_memory(self, mem_fields = ('unix:0:system_pages:physmem', 'unix:0:system_pages:freemem')):
        '''
        Parse output from get_memory().
        Returned key, value pairs depend on keywords defined in mem_fields,
        whish MUST be a tuple:
        self.parse_memory(('unix:0:system_pages:physmem',))
        Search is case sensitive.

        By default, returned values are pages of memory.

        Returned structure is a dictionary:
        {key: value, ...}
        '''
        return utils.parser_memory(self.get_memory(), mem_fields)

    def parse_swap(self):
        '''
        Parse output of get_swap().
        Returned structure is a dictionary of dictionaries:
        {path:
            {'dev': value,
            'swaplo': value,
            'blocks': value,
            'free': value}
        }

        path - The path name for the swap area.
        dev - The major/minor device number in decimal if it is a block special device; zeroes otherwise.
        swaplo - The swaplow value for the area in 512-byte blocks.
        blocks - The swaplen value for the area in 512-byte blocks.
        free - The number of 512-byte blocks in this area that are not currently allocated.
        '''
        fields = ('dev', 'swaplo', 'blocks', 'free')
        return utils.parser_storage(self.get_swap(), fields)


    def parse_loadavg(self):
        '''
        Parse output of get_loadavg().
        Returned structure is a tuple:
        (1min, 5min, 15min)

        Values returned by get_loadavg() must be divided by the scale factor.
        Scale factor is defined in /usr/include/sys/param.h:
        /*
        * Scale factor for scaled integers used to count
        * %cpu time and load averages.
        */
        #define FSHIFT  8               /* bits to right of fixed binary point */
        #define FSCALE  (1<<FSHIFT)
        '''
        data = self.get_loadavg()
        data = data.split('\n')[:-1]
        rvalue = []
        for item in data:
            rvalue.append('%.2f' % float(item.split()[-1]) / 256.00)
        return tuple(rvalue)

if __name__ == '__main__':
    print "not yet"
