#!/usr/bin/python

import subprocess as sub

def run(cmd):
    cmd = cmd.split()
    p = sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.STDOUT, universal_newlines=True)
    p.wait()
    if p.returncode == 0:
        return p.communicate()[0]
    return p.communicate()[1]

def parse_storage(data, fields):
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

if __name__ == '__main__':
    print "not yet!"
