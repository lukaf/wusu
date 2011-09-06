#!/usr/bin/python

import utils

class Linux:
    def __init__(self):
        self.seconds = 0

    def get_uptime(self):
        f = open('/proc/uptime', 'r', 0)
        self.seconds = float(f.read().split()[0])
        f.close()
        return parser_uptime(self.seconds)

class FreeBSD:
    def __init__(self, libc='/lib/libc.so.7'):
        self.seconds = 0
        self.data = None
        self.libc = libc

    def get_uptime(self):
        from ctypes import Structure, cdll, byref, c_long
        self.libc = cdll.LoadLibrary(self.libc)
        class Data(Structure):
            _fields_ = [('sec', c_long), ('nsec', c_long)]
        self.data = Data()
        self.libc.clock_gettime(7, byref(self.data))
        return utils.parser_uptime(self.data.sec)
