import logging, time, ipaddress
from geoip import geolite2


def log_coordinates(filename, north_limit, south_limit, east_limit, west_limit):
    log = logging.getLogger(__name__)
    log.info('Starting log coordinates filter...')
    file = open(filename, 'r')

    while(True):
        line = file.readline()
        ip = line.split()[0]
        if(ip == '127.0.0.1'): continue

        try:
            ipaddress.ip_address(str(ip))
        except ValueError:
            log.error('{} is not a valid IP!'.format(ip))
            continue

        log.info('Looking up {}'.format(ip))
        coordinates = geolite2.lookup(ip).location

        if(coordinates[0] <= north_limit and coordinates[0] >= south_limit and coordinates[1] >= eastlimit and coordinates[1] <= west_limit):
            log.info('IP from coordinate limit: {}'.format(ip))

        time.sleep(1)

    file.close()
