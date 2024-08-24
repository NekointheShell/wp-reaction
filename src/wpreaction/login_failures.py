import logging
from .ban_ip import ban_ip


def login_failures(filename):
    log = logging.getLogger(__name__)
    file = open(filename, 'r')

    while(True):
        line = file.readline()
        if(line != '' and line != "\n"):
            toban = line.split(', ')[0].split(': ')[1]
            ban_ip(toban)

    file.close()
