import logging, ipaddress, subprocess


log = logging.getLogger(__name__)


def ban_ip(ip):
    log = logging.getLogger(__name__)

    try:
        ipaddress.ip_address(str(ip))

    except ValueError:
        log.error('{} is not a valid IP! This could be a command injection attempt!')
        return False

    log.info('Banning {}'.format(ip))
    iptables = subprocess.run('iptables -A INPUT -p tcp --dports 80,443 -s {} -j DROP'.format(ip).split())

    if(iptables.returncode != 0):
        log.error('Unable to ban {}!'.format(ip)
        return False
