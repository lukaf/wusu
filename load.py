#!/usr/bin/python

import utils

class Linux:
    def __init__(self):
        self.memdata = '/proc/meminfo'

    def get_uptime(self):
        '''
        Get machine uptime in seconds as provided by /proc/uptime.
        Also see parse_uptime().
        '''
        f = open('/proc/uptime', 'r', 0)
        seconds = float(f.read().split()[0])
        f.close()
        return self.seconds

    def get_meminfo(self):
        '''
        Get memory information from /proc/meminfo.
        Also see parse_meminfo().
        '''
        f = open(self.memdata, 'r', 0)
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
        Parse memory info from output of get_meminfo().
        Returned key, value pairs depend on keywords defined in mem_fields,
        which MUST be a tuple:
        self.parse_memory(('MemTotal',))
        Search is case sensitive.

        Returned structure is a dictionary:
        {key: value, ...}
        '''
        return utils.parser_meminfo(self.get_meminfo(), mem_fields)

    def parse_swap(self, mem_fields=('SwapTotal', 'SwapFree')):
        '''
        Parse swap info from output of get_meminfo().
        Returned key, value pairs depend on keywords defined in mem_fields,
        which MUST be a tuple:
        self.parse_swap(('SwapTotal',))
        Search is case sensitive.

        Returned structure is a dictionary.
        {key: value, ...}
        '''
        return utils.parser_meminfo(self.get_meminfo(), mem_fields)

class FreeBSD:
    def __init__(self, libc='/lib/libc.so.7'):
        self.memdata = 'sysctl vm'
        self.libc = libc

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
        return struct

    def get_meminfo(self):
        '''
        Get memory information.
        '''
        return utils.run(self.memdata)

    def parse_uptime(self):
        '''
        Parse output from get_uptime().
        Returned structure is tuple:
        (days, hours, minutes, seconds, seconds since boot)
        '''
        return utils.parser_uptime(self.get_uptime())

    def parse_memory(self, mem_fields=('vm.stats.vm.v_page_count', 'vm.stats.vm.v_free_count', 'vm.stats.vm.v_inactive_count', 'vm.stats.vm.v_cache_count')):
        '''
        Parse output from get_meminfo().
        Returned key, value pairs depend on keywords defined in mem_fields,
        which MUST be a tuple:
        self.parse_memory(('vm.stats.vm.v_page_count',))
        Search is case sensitive.

        Returned structure is a dictionary.
        {key: value, ...}
        '''
        return utils.parser_meminof(self.get_meminfo(), mem_fields)

if __name__ == '__main__':
    print "not yet"
