import logging
from .ban_ip import ban_ip


def login_failures(filename):
    log = logging.getLogger(__name__)
    log.info('Starting login_failures filter...')
    file = open(filename, 'r')

    while(True):
        line = file.readline()
        if(line != '' and line != "\n"):
            toban = line.split(', ')[0].split(': ')[1]
            ban_ip('login_failures', toban)

    file.close()
