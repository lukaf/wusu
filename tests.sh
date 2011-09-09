#!/bin/sh

echo "Test load module ..."
python <<EOF
from load import `uname`
a = `uname`()
print "get_uptime()"
print a.get_uptime()
print
print "parse_uptime()"
print a.parse_uptime()
print
print "get_memory()"
print a.get_memory()
print
print "parse_memory()"
print a.parse_memory()
print
print "get_swap()"
print a.get_swap()
print
print "parse_swap()"
print a.parse_swap()
print
print "get_loadavg()"
print a.get_loadavg()
print
print "parse_loadavg()"
print a.parse_loadavg()
print
EOF

echo "Test storage module ..."
python <<EOF
from storage import `uname`
a = `uname`()
print "get_inodes()"
print a.get_inodes()
print
print "parse_inodes()"
print a.parse_inodes()
print
print "get_iostat()"
print a.get_iostat()
print
print "parse_iostat()"
print a.parse_iostat()
print
print "parse_fsusage()"
print a.parse_fsusage()
print
print "get_fsusage()"
print a.get_fsusage()
print
EOF

if [ $? = 0 ]; then
    echo "All is fine ..."
fi
