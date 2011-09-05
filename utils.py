#!/usr/bin/python

import subprocess as sub
import os

def run(cmd):
    cmd = cmd.split()
    p = sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.STDOUT, universal_newlines=True)
    p.wait()
    if p.returncode == 0:
        return p.communicate()[0]
    return p.communicate()[1]

def parser_storage(data, fields):
    '''Parse storage data.'''
    parsed = {}
    # Transform data to array and remove header and an empty line at the end.
    data = data.split('\n')[1:-1]
    for item in data:
        item = item.split()
        parsed[item[0]] = {}
        for i in range(1, len(fields)+1):
            parsed[item[0]][fields[i-1]] = item[i]
    return parsed

def parser_iostat(data, fields):
    '''Parse iostat output on Linux.'''
    parsed = {}
    # Transform data to array and remove header (3 lines in Linux, 2 in FreeBSD) and an empty line at the end.
    if os.uname()[0] == 'Linux':
        data = data.split('\n')[3:-2]
    if os.uname()[0] == 'FreeBSD':
        data = data.split('\n')[2:-1]
    print data
    for item in data:
        item = item.split()
        parsed[item[0]] = {}
        for i in range(1, len(fields)+1):
            parsed[item[0]][fields[i-1]] = item[i]
    return parsed

if __name__ == '__main__':
    print "not yet!"
