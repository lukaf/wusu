import subprocess as sub
import os, re

_sysname = os.uname()[0]

def run(cmd):
    cmd = cmd.split()
    p = sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.STDOUT, universal_newlines=True)
    p.wait()
    if p.returncode == 0:
        return p.communicate()[0]
    return p.communicate()[1]

def parser_storage(data, fields):
    '''Parse storage data.'''
    if data == None:
        return None
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
    '''Parse iostat data.'''
    parsed = {}
    # Transform data to array and remove header (3 lines in Linux, 2 in FreeBSD) and an empty line at the end.
    if _sysname == 'Linux':
        data = data.split('\n')[3:-2]
    if _sysname == 'FreeBSD' or _sysname == 'SunOS':
        data = data.split('\n')[2:-1]
    for item in data:
        item = item.split()
        if _sysname == 'SunOS':
            parsed[item[-1]] = {}
            for i in range(0, len(fields)):
                parsed[item[-1]][fields[i]] = item[i]
        else:
            parsed[item[0]] = {}
            for i in range(1, len(fields)+1):
                parsed[item[0]][fields[i-1]] = item[i]
    return parsed

def parser_uptime(data):
    '''Parse uptime data.'''
    seconds = int(data)
    days = seconds / 86400
    seconds = seconds % 86400
    hours = seconds / 3600
    seconds = seconds % 3600
    minutes = seconds / 60
    seconds = seconds % 60
    return (days, hours, minutes, seconds, int(data))

def parser_memory(data, fields):
    '''Parse memory data.'''
    parsed = {}
    data = data.split('\n')
    for item in data:
        for field in fields:
            if re.match(field, item):
                parsed[item.split()[0][:-1]] = item.split()[1]
    return parsed

def parser_swap(data, fields):
    '''Parse swap data.'''
    parsed = {}
    if _sysname == 'Linux':
        data = data.split('\n')[1:-1]
    if _sysname == 'FreeBSD':
        data = data.split('\n')[1:-2]
    for item in data:
        item = item.split()
        parsed[item[0]] = {}
        for i in range(1, len(fields)+1):
            parsed[item[0]][fields[i-1]] = item[i]
    return parsed

def parser_loadavg(data):
    parsed = []
    data = data.split()
    for num in data:
        # I don't like this not one bit!
        if re.search('\.', num):
            parsed.append(num)
    return tuple(parsed)

def parser_ifstat(data):
    parsed = {}
    if _sysname == 'Linux':
        data = data.split('\n')[:-1]
    if _sysname == 'FreeBSD' or _sysname == 'SunOS':
        data = data.split('\n')[1:-1]
    for item in data:
        item = item.split()
        # Replace '-' (FreeBSD) and 'N/A' (SunOS) with '0'.
        for i in range(0, len(item)):
            if item[i] == '-' or item[i] == 'N/A':
                item[i] = '0'
        if _sysname == 'Linux':
            parsed[item[1].strip(':')] = {
                'in': {
                    'bytes': item[-21],
                    'packets': item[-20],
                    'errors': item[-19],
                    'dropped': item[-18]
                },
                'out': {
                    'bytes:': item[-6],
                    'packets': item[-5],
                    'errors': item[-4],
                    'dropped': item[-3]
                }
            }
        if _sysname == 'FreeBSD':
            if item[0] not in parsed:
                parsed[item[0]] = {}
            # With PPP, tunnel, pflog interfaces, netstat doesn't always display address info.
            # Next field is always a counter - replace the value with NaN if we get a number.
            if item[3].isdigit():
                item[3] = 'NaN'
            parsed[item[0]][item[3]] = {
                'in': {
                    'bytes': item[-6],
                    'packets': item[-9],
                    'errors': item[-8],
                    'dropped': item[-7]
                },
                'out': {
                    'bytes': item[-3],
                    'packets': item[-5],
                    'errors': item[-4],
                    'dropped': item[-1]
                }
            }
        if _sysname == 'SunOS':
            parsed[item[0]] = {
                'in': {
                    'bytes': item[2],
                    'packets': item[1],
                    'errors': item[3],
                },
                'out': {
                    'bytes': item[5],
                    'packets': item[4],
                    'errors': item[6]
                }
            }
    return parsed

if __name__ == '__main__':
    print "not yet!"
