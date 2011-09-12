import subprocess as sub
import os, re

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
    if os.uname()[0] == 'Linux':
        data = data.split('\n')[3:-2]
    if os.uname()[0] == 'FreeBSD' or os.uname()[0] == 'SunOS':
        data = data.split('\n')[2:-1]
    for item in data:
        item = item.split()
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
    if os.uname()[0] == "Linux":
        data = data.split('\n')[1:-1]
    if os.uname()[0] == 'FreeBSD':
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

if __name__ == '__main__':
    print "not yet!"
