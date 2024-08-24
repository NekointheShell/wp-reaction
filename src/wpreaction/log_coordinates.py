import logging, ipaddress, time
from geoip import geolite2


def log_coordinates(filename, north_limit, south_limit, east_limit, west_limit):
    log = logging.getLogger(__name__)
    log.info('Starting log coordinates filter...')
    file = open(filename, 'r')

    log.debug('log_coordinates north limit: {}'.format(north_limit))
    log.debug('log_coordinates south limit: {}'.format(south_limit))
    log.debug('log_coordinates east limit: {}'.format(east_limit))
    log.debug('log_coordinates west limit: {}'.format(west_limit))

    while(True):
        line = file.readline()
        if(line != '' and line != "\n"):
            ip = line.split()[0]
            if(ip == '127.0.0.1'): continue

            try:
                ipaddress.ip_address(str(ip))

            except ValueError:
                log.error('{} is not a valid IP!'.format(ip))
                continue

            lookup = geolite2.lookup(ip)
            if(lookup != None):
                coordinates = lookup.location

                if(len(coordinates) == 2):
                    log.debug('{} has coordinates {}'.format(ip, coordinates))
                    if(coordinates[0] <= north_limit and coordinates[0] >= south_limit and coordinates[1] >= east_limit and coordinates[1] <= west_limit):
                        log.info('IP from coordinate limit: {}'.format(ip))

        time.sleep(0.1)

    file.close()
