#!/usr/bin/python

import utils

class Linux:
    def __init__(self):
        self.seconds = 0
        self.memdata = '/proc/meminfo'
        self.array = []
        self.mem_fields = None

    def get_uptime(self):
        '''
        Get machine uptime in seconds as provided by /proc/uptime.
        '''
        f = open('/proc/uptime', 'r', 0)
        self.seconds = float(f.read().split()[0])
        f.close()
        return self.seconds

    def get_meminfo(self):
        '''
        Get memory information from /proc/meminfo.
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

    def parse_memory(self):
        '''
        Parse memory info from output of get_meminfo().
        Returned key, value pairs depend on keywords defined in self.mem_fields.

        Returned structure is a dictionary:
        {key: value, ...}
        '''
        self.mem_fields = ('MemTotal', 'MemFree')
        return utils.parser_meminfo(self.get_meminfo(), self.mem_fields)

    def parse_swap(self):
        '''
        Parse swap info from output of get_meminfo().
        Returned key, value pairs depend on keywords defined in self.mem_fields.

        Returned structure is a dictionary.
        {key: value, ...}
        '''
        self.mem_fields = ('SwapTotal', 'SwapFree')
        return utils.parser_meminfo(self.get_meminfo(), self.mem_fields)

class FreeBSD:
    def __init__(self, libc='/lib/libc.so.7'):
        self.seconds = 0
        self.memdata = 'sysctl vm'
        self.data = None
        self.libc = libc
        self.lib = None

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
        self.lib = cdll.LoadLibrary(self.libc)
        class Data(Structure):
            _fields_ = [('sec', c_long), ('nsec', c_long)]
        self.data = Data()
        self.lib.clock_gettime(7, byref(self.data))
        return self.data.sec

    def get_meminfo(self):
        '''
        Get memory information. Command defined in self.memdata.'
        '''
        return utils.run(self.memdata)

    def parse_uptime(self):
        '''
        Parse output from get_uptime().
        Returned structure is tuple:
        (days, hours, minutes, seconds, seconds since boot)
        '''
        return utils.parser_uptime(self.get_uptime())

    def parse_memory(self):
        '''
        Parse output from get_meminfo().
        Returned key, value pairs depend on keywords defined inf self.mem_fields.

        Returned structure is a dictionary.
        {key: value, ...}
        '''
        self.mem_fields('vm.stats.vm.v_page_count', 'vm.stats.vm.v_free_count', 'vm.stats.vm.v_ina
        ctive_count', 'vm.stats.vm.v_cache_count')
        return utils.parser_meminof(self.get_meminfo(), self.mem_fields)

if __name__ == '__main__':
    print "not yet"
