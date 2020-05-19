# python 3

# A module for monitoring changes in log files

import sys
from pygtail import Pygtail


with open('')

for line in Pygtail("/var/log/syslog"):
    print(line)